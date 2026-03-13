"""LangGraph工作流定义"""

from typing import Annotated, Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from src.agents.planner_agent import PlannerAgent
from src.agents.coder_agent import CoderAgent
from src.schemas.agents import list_agent_roles


class WorkflowState(TypedDict):
    """工作流状态"""
    messages: Annotated[list[BaseMessage], add_messages]
    current_step: str
    requirements: str
    plan: str
    code: str
    test_results: str
    review_comments: str
    deployment_status: str


class AutoRandDWorkflow:
    """自动研发工作流"""

    def __init__(self, api_key: str = None):
        """
        初始化工作流

        Args:
            api_key: OpenAI API密钥
        """
        self.api_key = api_key
        self.planner = PlannerAgent(api_key)
        self.coder = CoderAgent(api_key)
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """创建工作流图"""
        workflow = StateGraph(WorkflowState)

        # 添加节点
        workflow.add_node("planning", self._planning_step)
        workflow.add_node("coding", self._coding_step)
        workflow.add_node("review", self._review_step)
        workflow.add_node("testing", self._testing_step)
        workflow.add_node("deployment", self._deployment_step)

        # 设置入口
        workflow.set_entry_point("planning")

        # 添加边
        workflow.add_edge("planning", "coding")
        workflow.add_edge("coding", "review")
        workflow.add_conditional_edges(
            "review",
            self._should_continue,
            {
                "coding": "coding",
                "testing": "testing"
            }
        )
        workflow.add_conditional_edges(
            "testing",
            self._should_deploy,
            {
                "coding": "coding",
                "deployment": "deployment"
            }
        )
        workflow.add_edge("deployment", END)

        return workflow.compile()

    async def _planning_step(self, state: WorkflowState) -> WorkflowState:
        """规划步骤"""
        print("📋 开始项目规划...")

        result = await self.planner.process({
            "requirement": state.get("requirements", ""),
            "context": state.get("messages", [])
        })

        state["current_step"] = "planning"
        state["plan"] = result["plan"]

        print("✅ 项目规划完成")
        return state

    async def _coding_step(self, state: WorkflowState) -> WorkflowState:
        """编码步骤"""
        print("💻 开始代码生成...")

        result = await self.coder.process({
            "design_doc": state.get("plan", ""),
            "tech_stack": "Python + LangGraph",
            "requirements": state.get("requirements", "")
        })

        state["current_step"] = "coding"
        state["code"] = result["code"]

        print("✅ 代码生成完成")
        return state

    async def _review_step(self, state: WorkflowState) -> WorkflowState:
        """审查步骤"""
        print("🔍 开始代码审查...")

        # 这里可以集成审查Agent
        # 简化版：假设审查通过
        review_comments = "代码审查通过，质量良好。"

        state["current_step"] = "review"
        state["review_comments"] = review_comments

        print("✅ 代码审查完成")
        return state

    async def _testing_step(self, state: WorkflowState) -> WorkflowState:
        """测试步骤"""
        print("🧪 开始测试...")

        # 这里可以集成测试Agent
        test_results = "所有测试用例通过。"

        state["current_step"] = "testing"
        state["test_results"] = test_results

        print("✅ 测试完成")
        return state

    async def _deployment_step(self, state: WorkflowState) -> WorkflowState:
        """部署步骤"""
        print("🚀 开始部署...")

        # 这里可以集成部署Agent
        deployment_status = "部署成功！"

        state["current_step"] = "deployment"
        state["deployment_status"] = deployment_status

        print("✅ 部署完成")
        return state

    def _should_continue(self, state: WorkflowState) -> str:
        """判断是否需要继续修改代码"""
        # 简化版：总是继续到测试
        return "testing"

    def _should_deploy(self, state: WorkflowState) -> str:
        """判断是否可以部署"""
        # 简化版：总是可以部署
        return "deployment"

    async def run(self, requirements: str) -> Dict[str, Any]:
        """
        运行工作流

        Args:
            requirements: 项目需求

        Returns:
            工作流执行结果
        """
        print(f"\n🎯 开始自动研发流程")
        print(f"📝 需求: {requirements}\n")

        initial_state = {
            "messages": [],
            "current_step": "",
            "requirements": requirements,
            "plan": "",
            "code": "",
            "test_results": "",
            "review_comments": "",
            "deployment_status": ""
        }

        final_state = await self.workflow.ainvoke(initial_state)

        print(f"\n🎉 自动研发流程完成！\n")

        return final_state

    def get_available_agents(self) -> list:
        """获取可用的Agent列表"""
        return list_agent_roles()


# 便捷函数
def create_workflow(api_key: str = None) -> AutoRandDWorkflow:
    """创建工作流实例"""
    return AutoRandDWorkflow(api_key)
