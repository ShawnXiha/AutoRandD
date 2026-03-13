"""
首席研发规划师 (R&D Planner)
Chief R&D Planner Agent

基于行业情报，设计合理的研发计划，包括项目阶段划分、资金分配、时间表和预期里程碑
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from .base_agent import BaseAgent


class RAndDPlanner(BaseAgent):
    """首席研发规划师 Agent"""

    def __init__(self):
        """初始化首席研发规划师"""
        super().__init__(
            agent_name="首席研发规划师",
            agent_description="负责制定系统性的研发计划，包括项目规划、资源配置和时间管理",
            tools=self._create_professional_tools()
        )

    def _create_professional_tools(self) -> List[BaseTool]:
        """创建专业工具"""
        tools = []

        # 项目规划工具
        planning_tool = ProjectPlanningTool()
        tools.append(planning_tool)

        # 资源分配工具
        resource_tool = ResourceAllocationTool()
        tools.append(resource_tool)

        # 风险评估工具
        risk_tool = RiskAssessmentTool()
        tools.append(risk_tool)

        # 时间规划工具
        timeline_tool = TimelinePlanningTool()
        tools.append(timeline_tool)

        return tools

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理情报报告，生成研发计划

        Args:
            context: 包含情报报告和其他信息的上下文
                - research_goal: 研发目标
                - funding: 资金预算
                - intelligence_report: 情报报告（来自IndustryResearcher）

        Returns:
            项目研发计划书
        """
        research_goal = context.get("research_goal", "")
        funding = context.get("funding", "")
        intelligence_report = context.get("intelligence_report", {})

        print(f"📋 首席研发规划师开始制定计划: {research_goal}")

        # 第一步：项目总体规划
        planning_task = f"""
        基于{research_goal}的研发目标，制定总体项目规划：

        1. 项目目标分解：
           - 主要技术指标
           - 产品质量标准
           - 成本控制目标
           - 时间节点要求

        2. 项目阶段划分（建议6-12个月）：
           - 可行性研究阶段（1-2个月）
           - 实验室研发阶段（2-4个月）
           - 中试放大阶段（2-3个月）
           - 工业化验证阶段（1-2个月）

        3. 关键里程碑设定：
           - 技术方案确定
           - 实验室小试成功
           - 中试产品达标
           - 工艺参数优化完成

        预算: {funding}
        情报报告: {json.dumps(intelligence_report, ensure_ascii=False)[:2000]}
        """

        planning_results = await self.run_task(planning_task, context)

        # 第二步：详细资源配置
        resource_task = f"""
        制定详细的资源配置计划：

        1. 人力资源配置：
           - 项目负责人（1人）
           - 研发工程师（2-3人）
           - 实验技术员（1-2人）
           - 分析检测人员（1人）
           - 薪资标准和市场行情

        2. 设备资源配置：
           - 实验室设备清单及预算
           - 中试设备需求
           - 分析检测设备
           - 设备采购/租赁成本

        3. 材料资源配置：
           - 原材料清单
           - 试剂耗材需求
           - 包装材料需求
           - 供应商选择标准

        4. 经费详细分配：
           - 各阶段经费明细
           - 风险备用金（10-15%）
           - 不可预见费（5-10%）

        预算: {funding}
        """

        resource_results = await self.run_task(resource_task, context)

        # 第三步：时间表制定
        timeline_task = f"""
        制定详细的项目时间表：

        1. 网络图制定：
           - 各任务之间的依赖关系
           - 关键路径识别
           - 并行任务规划

        2. 详细时间安排：
           - 按周制定时间计划
           - 考虑节假日和缓冲期
           - 里程碑时间节点

        3. 进度监控机制：
           - 周报制度
           - 阶段评审点
           - 风险预警机制

        研发目标: {research_goal}
        预算: {funding}
        """

        timeline_results = await self.run_task(timeline_task, context)

        # 整合研发计划书
        rd_plan = {
            "document_type": "项目研发计划书",
            "project_name": f"{research_goal}研发项目",
            "generated_at": datetime.now().isoformat(),
            "research_goal": research_goal,
            "total_budget": funding,

            # 项目概况
            "project_overview": {
                "project_objective": research_goal,
                "project_duration": self._estimate_project_duration(research_goal),
                "team_size": self._estimate_team_size(research_goal),
                "key_success_factors": self._identify_success_factors(intelligence_report)
            },

            # 项目阶段
            "project_phases": self._create_project_phases(),

            # 资源配置
            "resource_allocation": {
                "human_resources": self._parse_human_resources(resource_results),
                "equipment_resources": self._parse_equipment_resources(resource_results),
                "material_resources": self._parse_material_resources(resource_results),
                "budget_breakdown": self._parse_budget_breakdown(resource_results)
            },

            # 时间计划
            "timeline": self._parse_timeline(timeline_results),

            # 里程碑
            "milestones": self._create_milestones(),

            # 风险管理
            "risk_management": self._create_risk_management(),

            # 预期成果
            "expected_outcomes": self._define_expected_outcomes(research_goal),

            # 附录
            "appendix": {
                "references": intelligence_report.get("references", []),
                "technical_specifications": planning_results,
                "contact_information": self._get_contact_info()
            }
        }

        # 保存计划书
        filename = f"data/rd_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_result(rd_plan, filename)

        return rd_plan

    def _estimate_project_duration(self, research_goal: str) -> str:
        """估算项目周期"""
        if "茶多酚" in research_goal or "简单" in research_goal:
            return "6-8个月"
        elif "蛋白棒" in research_goal or "工艺优化" in research_goal:
            return "8-10个月"
        else:
            return "10-12个月"

    def _estimate_team_size(self, research_goal: str) -> Dict[str, int]:
        """估算团队规模"""
        return {
            "project_manager": 1,
            "research_engineers": 2,
            "technicians": 2,
            "analysts": 1,
            "total": 6
        }

    def _identify_success_factors(self, intelligence_report: Dict) -> List[str]:
        """识别成功因素"""
        return [
            "技术路线选择正确",
            "实验参数控制精确",
            "质量控制严格",
            "团队协作高效",
            "资源配置合理",
            "风险管理到位"
        ]

    def _create_project_phases(self) -> List[Dict[str, Any]]:
        """创建项目阶段"""
        return [
            {
                "phase": "可行性研究阶段",
                "duration": "1-2个月",
                "objectives": ["技术可行性分析", "市场需求调研", "初步方案制定"],
                "deliverables": ["可行性研究报告", "技术路线选择", "初步预算"],
                "budget_ratio": 15
            },
            {
                "phase": "实验室研发阶段",
                "duration": "2-4个月",
                "objectives": ["工艺参数优化", "配方确定", "小试成功"],
                "deliverables": ["实验室工艺文件", "样品测试报告", "中试方案"],
                "budget_ratio": 40
            },
            {
                "phase": "中试放大阶段",
                "duration": "2-3个月",
                "objectives": ["中试设备调试", "工艺参数验证", "质量标准制定"],
                "deliverables": ["中试工艺文件", "中试产品报告", "工业化方案"],
                "budget_ratio": 30
            },
            {
                "phase": "工业化验证阶段",
                "duration": "1-2个月",
                "objectives": ["工业化生产验证", "成本核算", "技术文档完善"],
                "deliverables": ["工业化工艺文件", "成本分析报告", "最终技术报告"],
                "budget_ratio": 15
            }
        ]

    def _parse_human_resources(self, resource_results: str) -> Dict[str, Any]:
        """解析人力资源配置"""
        # 这里应该更精确地解析结果
        return {
            "project_manager": {
                "role": "项目经理",
                "quantity": 1,
                "monthly_salary": 25000,
                "total_cost": "根据项目周期计算"
            },
            "research_engineers": {
                "role": "研发工程师",
                "quantity": 2,
                "monthly_salary": 20000,
                "total_cost": "根据项目周期计算"
            },
            "technicians": {
                "role": "实验技术员",
                "quantity": 2,
                "monthly_salary": 12000,
                "total_cost": "根据项目周期计算"
            }
        }

    def _parse_equipment_resources(self, resource_results: str) -> List[Dict[str, Any]]:
        """解析设备资源配置"""
        return [
            {
                "equipment": "高压均质机",
                "purpose": "物料均质处理",
                "budget": "15-20万元",
                "acquisition_method": "采购"
            },
            {
                "equipment": "冻干机",
                "purpose": "物料冷冻干燥",
                "budget": "25-30万元",
                "acquisition_method": "采购"
            },
            {
                "equipment": "分析检测仪器",
                "purpose": "产品质量检测",
                "budget": "10-15万元",
                "acquisition_method": "租赁"
            }
        ]

    def _parse_material_resources(self, resource_results: str) -> Dict[str, Any]:
        """解析材料资源配置"""
        return {
            "raw_materials": {
                "budget_ratio": 30,
                "description": "主要原料采购"
            },
            "chemical_reagents": {
                "budget_ratio": 15,
                "description": "化学试剂和助剂"
            },
            "packaging_materials": {
                "budget_ratio": 10,
                "description": "包装材料采购"
            }
        }

    def _parse_budget_breakdown(self, resource_results: str) -> Dict[str, Any]:
        """解析预算分解"""
        return {
            "personnel_costs": {
                "ratio": 40,
                "description": "人力成本"
            },
            "equipment_costs": {
                "ratio": 25,
                "description": "设备采购和租赁"
            },
            "material_costs": {
                "ratio": 20,
                "description": "材料采购"
            },
            "testing_costs": {
                "ratio": 10,
                "description": "测试分析"
            },
            "other_costs": {
                "ratio": 5,
                "description": "其他费用"
            }
        }

    def _parse_timeline(self, timeline_results: str) -> Dict[str, Any]:
        """解析时间计划"""
        # 创建详细的时间表
        start_date = datetime.now()
        phases = []

        # 可行性研究阶段
        phases.append({
            "phase": "可行性研究",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=60)).strftime("%Y-%m-%d"),
            "tasks": ["市场调研", "技术评估", "方案设计"]
        })

        # 实验室研发阶段
        phases.append({
            "phase": "实验室研发",
            "start_date": (start_date + timedelta(days=61)).strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=150)).strftime("%Y-%m-%d"),
            "tasks": ["工艺开发", "配方优化", "小试实验"]
        })

        # 中试放大阶段
        phases.append({
            "phase": "中试放大",
            "start_date": (start_date + timedelta(days=151)).strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=240)).strftime("%Y-%m-%d"),
            "tasks": ["中试设计", "工艺验证", "质量测试"]
        })

        # 工业化验证阶段
        phases.append({
            "phase": "工业化验证",
            "start_date": (start_date + timedelta(days=241)).strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=300)).strftime("%Y-%m-%d"),
            "tasks": ["工业化生产", "成本核算", "文档整理"]
        })

        return {"phases": phases, "total_duration": "10个月"}

    def _create_milestones(self) -> List[Dict[str, Any]]:
        """创建里程碑"""
        return [
            {
                "milestone": "技术方案确定",
                "date": "第1个月末",
                "criteria": "技术路线选择完成",
                "deliverables": ["可行性研究报告"]
            },
            {
                "milestone": "实验室小试成功",
                "date": "第4个月末",
                "criteria": "关键工艺参数确定",
                "deliverables": ["实验室工艺文件", "样品"]
            },
            {
                "milestone": "中试产品达标",
                "date": "第7个月末",
                "criteria": "中试产品符合质量标准",
                "deliverables": ["中试报告", "检测数据"]
            },
            {
                "milestone": "工艺优化完成",
                "date": "第9个月末",
                "criteria": "工艺参数稳定优化",
                "deliverables": ["优化工艺文件", "成本分析"]
            },
            {
                "milestone": "项目验收",
                "date": "第10个月末",
                "criteria": "所有目标达成",
                "deliverables": ["最终报告", "技术文档", "样品"]
            }
        ]

    def _create_risk_management(self) -> Dict[str, Any]:
        """创建风险管理计划"""
        return {
            "risk_identification": [
                {
                    "risk": "技术风险",
                    "description": "技术路线选择不当或工艺参数难以控制",
                    "probability": "中等",
                    "impact": "高"
                },
                {
                    "risk": "时间风险",
                    "description": "研发周期延误",
                    "probability": "中等",
                    "impact": "中等"
                },
                {
                    "risk": "成本风险",
                    "description": "预算超支",
                    "probability": "低",
                    "impact": "高"
                }
            ],
            "risk_mitigation": [
                {
                    "risk": "技术风险",
                    "mitigation": "前期充分调研，制定备选方案",
                    "contingency": "预留技术风险备用金"
                },
                {
                    "risk": "时间风险",
                    "mitigation": "制定详细时间表，设置缓冲期",
                    "contingency": "调整资源分配，加班赶工"
                },
                {
                    "risk": "成本风险",
                    "mitigation": "严格控制采购成本",
                    "contingency": "预备备用金"
                }
            ]
        }

    def _define_expected_outcomes(self, research_goal: str) -> List[str]:
        """定义预期成果"""
        return [
            "完成技术路线设计和工艺参数优化",
            "开发出符合要求的产品原型",
            "形成完整的技术文档和工艺文件",
            "申请相关专利1-2项",
            "建立质量标准和检测方法",
            "形成可工业化的技术方案"
        ]

    def _get_contact_info(self) -> Dict[str, str]:
        """获取联系信息"""
        return {
            "project_manager": "张三 (项目经理)",
            "technical_director": "李四 (技术总监)",
            "contact_email": "rd_company@example.com"
        }


class ProjectPlanningTool(BaseTool):
    """项目规划工具"""
    name: str = "项目规划工具"
    description: str = "帮助制定详细的项目计划"

    def _run(self, query: str) -> str:
        """项目规划"""
        return f"项目规划分析:\n{query[:500]}..."


class ResourceAllocationTool(BaseTool):
    """资源分配工具"""
    name: str = "资源分配工具"
    description: str = "优化资源配置和预算分配"

    def _run(self, query: str) -> str:
        """资源分配"""
        return f"资源分配分析:\n{query[:500]}..."


class RiskAssessmentTool(BaseTool):
    """风险评估工具"""
    name: str = "风险评估工具"
    description: str = "识别和评估项目风险"

    def _run(self, query: str) -> str:
        """风险评估"""
        return f"风险评估分析:\n{query[:500]}..."


class TimelinePlanningTool(BaseTool):
    """时间规划工具"""
    name: str = "时间规划工具"
    description: str = "制定项目时间表和进度计划"

    def _run(self, query: str) -> str:
        """时间规划"""
        return f"时间规划分析:\n{query[:500]}..."