"""
Agent基类定义
Base Agent Definition

定义食品与生工领域多智能体系统的基础Agent类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, ClassVar
import json
from crewai import Agent
from crewai.tools import BaseTool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.model_config import model_config
from src.tools.search_tools import duckduckgo_search, tavily_search
from src.tools.science_tools import pubmed_search, patent_search


class BaseAgent(ABC):
    """
    Agent基类
    所有专业Agent的基类，提供通用的初始化和工具访问功能
    """

    def __init__(self, agent_name: str, agent_description: str,
                 tools: Optional[List[BaseTool]] = None):
        """
        初始化Agent

        Args:
            agent_name: Agent名称
            agent_description: Agent描述
            tools: Agent可用的工具列表
        """
        self.agent_name = agent_name
        self.agent_description = agent_description
        self.tools = tools or []

        # 初始化 Ollama 模型
        self.llm = ChatOllama(
            model=model_config.ollama.model_name,
            temperature=model_config.ollama.temperature,
            base_url=model_config.ollama.base_url,
            num_predict=model_config.ollama.max_tokens
        )

        # 创建 CrewAI Agent 实例
        # Pass langchain LLM directly to avoid CrewAI's OpenAI default provider
        self.crewai_agent = Agent(
            role=agent_description[:100],  # Use part of description as role
            goal=agent_description,  # Use full description as goal
            backstory=agent_description,  # Use description as backstory
            name=agent_name,
            description=agent_description,
            tools=self._create_crewai_tools(),
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm_kwargs={"model_name": model_config.ollama.model_name}
        )

    def _create_crewai_tools(self) -> List[BaseTool]:
        """创建 CrewAI 兼容的工具"""
        crewai_tools = []

        # 添加基础搜索工具
        if hasattr(self, '_create_search_tool'):
            search_tool = self._create_search_tool()
            if search_tool:
                crewai_tools.append(search_tool)

        # 添加专业工具
        if hasattr(self, '_create_professional_tools'):
            professional_tools = self._create_professional_tools()
            crewai_tools.extend(professional_tools)

        # 添加自定义工具
        crewai_tools.extend(self.tools)

        return crewai_tools

    def _create_search_tool(self):
        """创建搜索工具的通用方法，子类可以重写"""
        return None

    def _create_professional_tools(self):
        """创建专业工具的通用方法，子类可以重写"""
        return []

    @abstractmethod
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据，每个子类必须实现

        Args:
            context: 包含所有必要信息的上下文字典

        Returns:
            处理结果字典
        """
        pass

    async def run_task(self, task_description: str, context: Optional[Dict] = None) -> str:
        """
        运行任务

        Args:
            task_description: 任务描述
            context: 上下文信息

        Returns:
            任务执行结果
        """
        try:
            # 创建任务
            from crewai import Task

            task = Task(
                description=task_description,
                agent=self.crewai_agent,
                expected_output="详细的执行结果"
            )

            # 执行任务
            result = task.execute()
            return result

        except Exception as e:
            error_msg = f"任务执行失败: {str(e)}"
            print(error_msg)
            return error_msg

    def save_result(self, result: Dict[str, Any], filename: str):
        """保存结果到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {filename}")
        except Exception as e:
            print(f"保存结果失败: {str(e)}")

    def get_agent_info(self) -> Dict[str, Any]:
        """获取Agent信息"""
        return {
            "name": self.agent_name,
            "description": self.agent_description,
            "tools": [tool.name for tool in self.tools],
            "model": model_config.ollama.model_name
        }


class SearchTool(BaseTool):
    """基础搜索工具"""
    name: str = "搜索工具"
    description: str = "用于搜索相关信息"
    _search_func: Optional[callable] = None

    def __init__(self, search_func: Optional[callable] = None):
        super().__init__()
        if search_func is not None:
            self._search_func = search_func

    @property
    def search_func(self):
        """获取搜索函数"""
        return self._search_func

    @search_func.setter
    def search_func(self, value):
        """设置搜索函数"""
        self._search_func = value

    def _run(self, query: str) -> str:
        """执行搜索"""
        if self._search_func is None:
            return "搜索函数未定义"

        results = self._search_func(query)
        if not results:
            return "未找到相关结果"

        # 格式化结果
        formatted_results = []
        for i, result in enumerate(results[:5], 1):
            formatted_results.append(f"{i}. {result.get('title', '无标题')}")
            formatted_results.append(f"   链接: {result.get('url', '无链接')}")
            formatted_results.append(f"   摘要: {result.get('snippet', '无摘要')[:200]}...")
            formatted_results.append("")

        return "\n".join(formatted_results)


class ScienceDataTool(BaseTool):
    """科学数据分析工具"""
    name: str = "数据分析工具"
    description: str = "用于分析实验数据"

    def _run(self, data: str) -> str:
        """分析数据"""
        try:
            # 尝试解析JSON数据
            import json
            data_dict = json.loads(data) if isinstance(data, str) else data

            # 进行简单分析
            if isinstance(data_dict, dict):
                values = [v for v in data_dict.values() if isinstance(v, (int, float))]
                if values:
                    avg = sum(values) / len(values)
                    max_val = max(values)
                    min_val = min(values)
                    return f"数据统计: 平均值={avg:.2f}, 最大值={max_val}, 最小值={min_val}"

            return "数据分析完成"

        except Exception as e:
            return f"数据分析失败: {str(e)}"
