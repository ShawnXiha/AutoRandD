"""项目规划Agent"""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.schemas.agents import AgentRole, get_agent_role


class PlannerAgent(BaseAgent):
    """项目规划Agent"""

    def __init__(self, api_key: str = None):
        role = get_agent_role("planner")
        super().__init__(role, api_key)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理规划请求

        Args:
            input_data: 包含需求描述等信息的字典

        Returns:
            规划结果
        """
        requirement = input_data.get("requirement", "")
        context = input_data.get("context", "")

        prompt = f"""
请根据以下需求制定项目规划：

需求描述：
{requirement}

上下文信息：
{context}

请输出以下内容：
1. 需求分析
2. 任务分解（按优先级）
3. 技术方案建议
4. 风险评估
5. 时间估算
"""

        response = await self.chat(prompt)

        return {
            "role": "planner",
            "requirement": requirement,
            "plan": response,
            "status": "completed"
        }
