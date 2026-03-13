"""
模型配置模块
Model Configuration Module

定义系统使用的所有模型配置，包括 Ollama 模型设置
"""

import os
from typing import Dict, Any
from pydantic import BaseModel, Field


class OllamaConfig(BaseModel):
    """Ollama 模型配置"""
    model_name: str = "qwen3.5:cloud"
    base_url: str = "http://localhost:11434/v1"
    temperature: float = 0.7
    max_tokens: int = 4000

    class Config:
        extra = "allow"


class ModelConfig(BaseModel):
    """全局模型配置"""
    # 默认使用 Ollama 配置
    ollama: OllamaConfig = OllamaConfig()

    # 可以根据需要添加其他模型配置
    openai: Dict[str, Any] = Field(default_factory=dict)
    anthropic: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "ModelConfig":
        """从环境变量加载配置"""
        config = cls()

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