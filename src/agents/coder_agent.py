"""代码生成Agent"""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.schemas.agents import AgentRole, get_agent_role


class CoderAgent(BaseAgent):
    """代码生成Agent"""

    def __init__(self, api_key: str = None):
        role = get_agent_role("coder")
        super().__init__(role, api_key)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理代码生成请求

        Args:
            input_data: 包含设计文档、技术栈等信息的字典

        Returns:
            生成的代码
        """
        design_doc = input_data.get("design_doc", "")
        tech_stack = input_data.get("tech_stack", "")
        requirements = input_data.get("requirements", "")

        prompt = f"""
请根据以下设计文档生成代码：

技术栈：
{tech_stack}

需求说明：
{requirements}

设计文档：
{design_doc}

请生成完整、可用的代码，包括：
1. 主要功能实现
2. 错误处理
3. 代码注释
4. 必要的导入和配置
"""

        response = await self.chat(prompt)

        return {
            "role": "coder",
            "code": response,
            "tech_stack": tech_stack,
            "status": "completed"
        }
