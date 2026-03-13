"""
食品与生工领域多智能体研发模拟系统
Food & Bioengineering R&D Multi-Agent Simulation System
"""

__version__ = "1.0.0"
__author__ = "AI R&D System"

from src.agents.industry_researcher import IntelligenceResearcher
from src.agents.rd_planner import RAndDPlanner
from src.agents.plan_reviewer import PlanReviewer
from src.agents.experiment_designer import ExperimentDesigner
from src.agents.data_simulator import DataSimulator
from src.agents.report_analyst import ReportAnalyst
from src.workflows.food_rd_workflow import FoodRDWorkflow
from src.config.model_config import ModelConfig
from src.tools.search_tools import DuckDuckGoSearchTool, TavilySearchTool

__all__ = [
    "IntelligenceResearcher",
    "RAndDPlanner",
    "PlanReviewer",
    "ExperimentDesigner",
    "DataSimulator",
    "ReportAnalyst",
    "FoodRDWorkflow",
    "ModelConfig",
    "DuckDuckGoSearchTool",
    "TavilySearchTool",
]
