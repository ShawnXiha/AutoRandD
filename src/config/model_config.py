"""
模型配置模块
Model Configuration Module

定义系统使用的所有模型配置，包括 Ollama 模型设置
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class OllamaConfig(BaseModel):
    """Ollama 模型配置"""
    model_name: str = "qwen3.5:cloud"
    base_url: str = "http://localhost:11434/v1"
    temperature: float = 0.7
    max_tokens: int = 4000

    class Config:
        extra = "allow"


MODEL_PROFILE_ALIASES: Dict[str, str] = {
    "qwen": "qwen3.5:cloud",
    "qwen3.5": "qwen3.5:cloud",
    "glm": "glm-5:cloud",
    "glm5": "glm-5:cloud",
    "glm-5": "glm-5:cloud",
    "kimi": "kimi-k2:latest",
    "kimi2.5": "kimi-k2:latest",
    "kimi-2.5": "kimi-k2:latest",
}


class ModelConfig(BaseModel):
    """全局模型配置"""
    # 默认使用 Ollama 配置
    ollama: OllamaConfig = OllamaConfig()
    model_profile: str = "default"

    # 可以根据需要添加其他模型配置
    openai: Dict[str, Any] = Field(default_factory=dict)
    anthropic: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "ModelConfig":
        """从环境变量加载配置"""
        config = cls()

        selected_profile = (os.getenv("MODEL_PROFILE") or "default").strip().lower()
        profile_model = cls._resolve_model_profile(selected_profile)
        if profile_model:
            config.model_profile = selected_profile
            config.ollama.model_name = profile_model

        # 从环境变量读取 Ollama 配置
        if os.getenv("OLLAMA_MODEL"):
            config.ollama.model_name = os.getenv("OLLAMA_MODEL")
        if os.getenv("OLLAMA_BASE_URL"):
            config.ollama.base_url = os.getenv("OLLAMA_BASE_URL")
        if os.getenv("OLLAMA_TEMPERATURE"):
            config.ollama.temperature = float(os.getenv("OLLAMA_TEMPERATURE"))
        if os.getenv("OLLAMA_MAX_TOKENS"):
            config.ollama.max_tokens = int(os.getenv("OLLAMA_MAX_TOKENS"))

        return config

    @staticmethod
    def _resolve_model_profile(profile_name: str) -> Optional[str]:
        if profile_name in ("", "default"):
            return None
        return MODEL_PROFILE_ALIASES.get(profile_name, profile_name)

    def apply_runtime_model(
        self,
        model_name: Optional[str] = None,
        model_profile: Optional[str] = None,
    ) -> str:
        profile_name = model_profile.strip().lower() if model_profile else ""
        resolved_model = (
            self._resolve_model_profile(profile_name)
            if profile_name
            else None
        )

        if model_name:
            self.ollama.model_name = model_name.strip()
            if profile_name:
                self.model_profile = profile_name
            return self.ollama.model_name

        if resolved_model:
            self.model_profile = profile_name
            self.ollama.model_name = resolved_model
            return self.ollama.model_name

        return self.ollama.model_name

    def get_llm_config(self, provider: str = "ollama") -> Dict[str, Any]:
        """获取指定提供商的 LLM 配置"""
        if provider == "ollama":
            return {
                "model": self.ollama.model_name,
                "temperature": self.ollama.temperature,
                "max_tokens": self.ollama.max_tokens,
                "base_url": self.ollama.base_url,
            }
        elif provider == "openai":
            return self.openai
        elif provider == "anthropic":
            return self.anthropic
        else:
            raise ValueError(f"Unsupported provider: {provider}")


# 全局配置实例
model_config = ModelConfig.from_env()
