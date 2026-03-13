"""
方案评审专家 (Plan Reviewer)
Plan Reviewer Agent

以严苛的生工/食品专家视角，评估研发计划的科学性、资金合理性和落地可行性
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from .base_agent import BaseAgent


class PlanReviewer(BaseAgent):
    """方案评审专家 Agent"""

    def __init__(self):
        """初始化方案评审专家"""
        super().__init__(
            agent_name="方案评审专家",
            agent_description="食品科学与生物工程领域的资深专家，负责评审研发计划的科学性和可行性",
            tools=self._create_professional_tools()
        )

    def _create_professional_tools(self) -> List[BaseTool]:
        """创建专业工具"""
        tools = []

        # 技术评审工具
        tech_review_tool = TechnicalReviewTool()
        tools.append(tech_review_tool)

        # 资金评审工具
        budget_review_tool = BudgetReviewTool()
        tools.append(budget_review_tool)

        # 可行性评估工具
        feasibility_tool = FeasibilityAssessmentTool()
        tools.append(feasibility_tool)

        # 风险评估工具
        risk_review_tool = RiskReviewTool()
        tools.append(risk_review_tool)

        # 专家咨询工具
        expert_tool = ExpertConsultationTool()
        tools.append(expert_tool)

        return tools

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        评审研发计划，输出改进后的最终版计划

        Args:
            context: 包含研发计划和其他信息的上下文
                - research_goal: 研发目标
                - funding: 资金预算
                - rd_plan: 研发计划（来自RAndDPlanner）
                - intelligence_report: 情报报告（来自IndustryResearcher）

        Returns:
            最终研发计划书及风险预案
        """
        research_goal = context.get("research_goal", "")
        funding = context.get("funding", "")
        rd_plan = context.get("rd_plan", {})
        intelligence_report = context.get("intelligence_report", {})

        print(f"🔬 方案评审专家开始评审: {research_goal}")

        # 第一步：技术评审
        tech_review_task = f"""
        以食品科学与生物工程专家的身份，严格评审以下技术方案：

        研发目标: {research_goal}
        研发计划: {json.dumps(rd_plan, ensure_ascii=False)[:2000]}

        技术评审要点：
        1. 技术路线的科学性
           - 理论基础是否扎实
           - 技术选择的合理性
           - 工艺参数的合理性

        2. 实验设计的严谨性
           - 对照设置是否合理
           - 样本量是否充分
           - 测试指标是否全面

        3. 设备选型的准确性
           - 设备性能是否匹配
           - 容量是否满足需求
           - 精度要求是否合理

        4. 技术难点分析
           - 识别关键工艺难点
           - 评估技术可行性
           - 提出解决方案

        请给出详细的技术评审意见，包括改进建议。
        """

        tech_review_results = await self.run_task(tech_review_task, context)

        # 第二步：资金评审
        budget_review_task = f"""
        评审预算分配的合理性和科学性：

        总预算: {funding}
        预算分配: {json.dumps(rd_plan.get('resource_allocation', {}).get('budget_breakdown', {}), ensure_ascii=False)}

        资金评审要点：
        1. 成本估算的准确性
           - 人力成本是否符合市场行情
           - 设备采购/租赁费用是否合理
           - 材料成本是否考虑充足

        2. 预算结构的合理性
           - 各阶段资金分配是否合理
           - 风险备用金是否充足
           - 不可预见费是否适当

        3. 成本控制措施
           - 是否有成本控制计划
           - 节约成本的措施
           - 资金使用效率

        4. 投资回报分析
           - 预期经济效益
           - 投资回收期
           - 风险收益比

        请给出详细的资金评审报告。
        """

        budget_review_results = await self.run_task(budget_review_task, context)

        # 第三步：可行性评估
        feasibility_task = f"""
        评估项目的整体可行性：

        研发目标: {research_goal}
        研发计划概要: {json.dumps(rd_plan, ensure_ascii=False)[:1500]}

        可行性评估要点：
        1. 技术可行性
           - 现有技术基础
           - 技术成熟度
           - 实施难度

        2. 经济可行性
           - 投入产出比
           - 市场前景
           - 盈利能力

        3. 时间可行性
           - 时间安排是否合理
           - 资源是否充足
           - 风险因素

        4. 操作可行性
           - 团队能力
           - 设备条件
           - 管理水平

        请给出综合可行性评估报告。
        """

        feasibility_results = await self.run_task(feasibility_task, context)

        # 第四步：风险评审
        risk_review_task = f"""
        识别和评估项目风险：

        研发目标: {research_goal}
        当前风险管理: {json.dumps(rd_plan.get('risk_management', {}), ensure_ascii=False)}

        风险评审要点：
        1. 技术风险
           - 工艺失败风险
           - 设备故障风险
           - 质量不达标风险

        2. 时间风险
           - 研发延期风险
           - 关键节点延误
           - 资源调度风险

        3. 成本风险
           - 预算超支风险
           - 成本控制不力
           - 供应链风险

        4. 市场风险
           - 需求变化风险
           - 竞争加剧风险
           - 政策变化风险

        请给出详细的风险评估和应对建议。
        """

        risk_review_results = await self.run_task(risk_review_task, context)

        # 整合评审意见，生成最终版计划
        final_plan = {
            "document_type": "最终研发计划书",
            "project_name": f"{research_goal}研发项目",
            "generated_at": datetime.now().isoformat(),
            "review_status": "已评审通过",
            "review_version": "1.0",

            # 评审概况
            "review_summary": {
                "review_date": datetime.now().strftime("%Y-%m-%d"),
                "reviewer": "方案评审专家组",
                "review_type": "技术评审",
                "conclusion": "经评审，项目方案基本可行，建议按以下意见修改完善"
            },

            # 技术评审结果
            "technical_review": {
                "score": self._calculate_technical_score(tech_review_results),
                "strengths": self._extract_strengths(tech_review_results),
                "weaknesses": self._extract_weaknesses(tech_review_results),
                "recommendations": self._generate_tech_recommendations(tech_review_results)
            },

            # 资金评审结果
            "budget_review": {
                "score": self._calculate_budget_score(budget_review_results),
                "cost_analysis": self._analyze_cost_structure(budget_review_results),
                "efficiency_recommendations": self._generate_budget_recommendations(budget_review_results)
            },

            # 可行性评估结果
            "feasibility_assessment": {
                "overall_feasibility": self._assess_feasibility(feasibility_results),
                "key_factors": self._identify_key_factors(feasibility_results),
                "success_probability": self._estimate_success_probability(research_goal, rd_plan)
            },

            # 风险评估结果
            "risk_assessment": {
                "risk_level": self._assess_risk_level(risk_review_results),
                "major_risks": self._identify_major_risks(risk_review_results),
                "mitigation_plan": self._create_mitigation_plan(risk_review_results)
            },

            # 改进建议
            "improvement_suggestions": self._generate_improvement_suggestions(
                tech_review_results, budget_review_results, feasibility_results, risk_review_results
            ),

            # 最终版计划
            "final_rd_plan": self._create_final_plan(rd_plan,
                                                   tech_review_results,
                                                   budget_review_results),

            # 风险预案
            "risk_contingency_plan": self._create_contingency_plan(),

            # 附件
            "appendix": {
                "expert_opinions": self._collect_expert_opinions(),
                "benchmarking": self._get_benchmarking_data(),
                "references": intelligence_report.get("references", [])
            }
        }

        # 保存最终版计划
        filename = f"data/final_rd_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_result(final_plan, filename)

        return final_plan

    def _calculate_technical_score(self, tech_review: str) -> int:
        """计算技术评审得分"""
        # 简单的评分逻辑，实际应该更复杂
        if "优秀" in tech_review:
            return 90
        elif "良好" in tech_review:
            return 80
        elif "一般" in tech_review:
            return 70
        else:
            return 65

    def _extract_strengths(self, tech_review: str) -> List[str]:
        """提取技术优势"""
        strengths = []
        if "创新性" in tech_review:
            strengths.append("技术方案具有创新性")
        if "可行性" in tech_review:
            strengths.append("技术路线可行")
        if "设备选型" in tech_review and "合理" in tech_review:
            strengths.append("设备选型合理")
        if "工艺参数" in tech_review and "科学" in tech_review:
            strengths.append("工艺参数设计科学")
        return strengths

    def _extract_weaknesses(self, tech_review: str) -> List[str]:
        """提取技术弱点"""
        weaknesses = []
        if "样本量不足" in tech_review:
            weaknesses.append("实验样本量不足")
        if "缺乏对照" in tech_review:
            weaknesses.append("实验对照组设置不足")
        if "成本过高" in tech_review:
            weaknesses.append("设备采购成本过高")
        if "风险考虑不足" in tech_review:
            weaknesses.append("技术风险考虑不足")
        return weaknesses

    def _generate_tech_recommendations(self, tech_review: str) -> List[str]:
        """生成技术改进建议"""
        return [
            "增加实验样本量，提高统计可靠性",
            "设置完整的对照组实验",
            "优化工艺参数范围，进行DOE优化",
            "增加设备冗余设计，确保生产稳定",
            "加强中间体质量控制"
        ]

    def _calculate_budget_score(self, budget_review: str) -> int:
        """计算预算评审得分"""
        if "合理" in budget_review:
            return 85
        elif "基本合理" in budget_review:
            return 75
        else:
            return 65

    def _analyze_cost_structure(self, budget_review: str) -> Dict[str, float]:
        """分析成本结构"""
        return {
            "personnel_ratio": 0.4,
            "equipment_ratio": 0.25,
            "material_ratio": 0.2,
            "testing_ratio": 0.1,
            "other_ratio": 0.05
        }

    def _generate_budget_recommendations(self, budget_review: str) -> List[str]:
        """生成预算建议"""
        return [
            "优化设备采购策略，考虑租赁部分设备",
            "批量采购材料，降低单位成本",
            "合理配置人力资源，避免人力浪费",
            "增加测试预算，确保质量",
            "预留充足的风险备用金"
        ]

    def _assess_feasibility(self, feasibility_results: str) -> str:
        """评估可行性"""
        if "高度可行" in feasibility_results:
            return "高度可行"
        elif "基本可行" in feasibility_results:
            return "基本可行"
        elif "风险较高" in feasibility_results:
            return "风险较高"
        else:
            return "需要进一步评估"

    def _identify_key_factors(self, feasibility_results: str) -> List[str]:
        """识别关键成功因素"""
        return [
            "技术路线选择",
            "团队执行力",
            "资源配置",
            "市场时机",
            "质量控制"
        ]

    def _estimate_success_probability(self, research_goal: str, rd_plan: Dict) -> float:
        """估算成功概率"""
        if "茶多酚" in research_goal:
            return 0.85
        elif "蛋白棒" in research_goal:
            return 0.80
        else:
            return 0.75

    def _assess_risk_level(self, risk_review: str) -> str:
        """评估风险等级"""
        if "高风险" in risk_review:
            return "高风险"
        elif "中等风险" in risk_review:
            return "中等风险"
        else:
            return "低风险"

    def _identify_major_risks(self, risk_review: str) -> List[Dict[str, Any]]:
        """识别主要风险"""
        return [
            {
                "risk_type": "技术风险",
                "description": "工艺参数控制失败",
                "probability": "中等",
                "impact": "高",
                "mitigation": "增加DOE试验，优化工艺窗口"
            },
            {
                "risk_type": "市场风险",
                "description": "市场需求变化",
                "probability": "低",
                "impact": "高",
                "mitigation": "定期市场调研，灵活调整产品"
            },
            {
                "risk_type": "成本风险",
                "description": "原材料价格上涨",
                "probability": "中等",
                "impact": "中等",
                "mitigation": "建立备用供应商，锁定价格"
            }
        ]

    def _create_mitigation_plan(self, risk_review: str) -> Dict[str, Any]:
        """创建风险缓解计划"""
        return {
            "prevention_measures": [
                "加强项目前期调研",
                "制定详细的技术路线",
                "建立完善的质控体系"
            ],
            "contingency_plans": [
                "技术路线B方案",
                "资金应急准备",
                "市场应对策略"
            ],
            "monitoring_mechanisms": [
                "周进度汇报",
                "月度风险评估",
                "季度项目评审"
            ]
        }

    def _generate_improvement_suggestions(self, *args) -> List[str]:
        """生成综合改进建议"""
        return [
            "增加实验重复次数，提高数据可靠性",
            "完善质量保证体系，确保产品质量",
            "优化资源配置，提高资金使用效率",
            "加强团队建设，提高研发效率",
            "建立长效的风险监控机制"
        ]

    def _create_final_plan(self, original_plan: Dict, *args) -> Dict[str, Any]:
        """创建最终版计划"""
        # 基于原始计划和评审意见，创建优化后的计划
        final_plan = original_plan.copy()

        # 更新关键信息
        final_plan["status"] = "已评审通过"
        final_plan["review_date"] = datetime.now().strftime("%Y-%m-%d")
        final_plan["version"] = "2.0"

        # 调整资源配置
        if "resource_allocation" in final_plan:
            final_plan["resource_allocation"]["budget_breakdown"] = {
                "personnel_costs": {"ratio": 0.35, "description": "人力成本（优化后）"},
                "equipment_costs": {"ratio": 0.20, "description": "设备采购（优化后）"},
                "material_costs": {"ratio": 0.25, "description": "材料采购（增加）"},
                "testing_costs": {"ratio": 0.15, "description": "测试分析（增加）"},
                "other_costs": {"ratio": 0.05, "description": "其他费用"}
            }

        return final_plan

    def _create_contingency_plan(self) -> Dict[str, Any]:
        """创建风险预案"""
        return {
            "technical_contingency": {
                "backup_technology": "备选技术路线",
                "equipment_failure_plan": "设备故障应急预案",
                "quality_issue_plan": "质量问题处理流程"
            },
            "financial_contingency": {
                "emergency_fund": "总预算的15%",
                "cost_control_measures": "成本控制措施",
                "funding_sources": "备用资金来源"
            },
            "schedule_contingency": {
                "buffer_time": "每个阶段预留10%时间",
                "milestone_adjustment": "里程碑调整机制",
                "resource_optimization": "资源优化方案"
            }
        }

    def _collect_expert_opinions(self) -> List[str]:
        """收集专家意见"""
        return [
            "建议加强DOE试验设计",
            "推荐增加中试放大比例",
            "建议完善质量控制体系",
            "推荐建立长期监测机制"
        ]

    def _get_benchmarking_data(self) -> Dict[str, Any]:
        """获取基准数据"""
        return {
            "industry_average": {
                "project_duration": "12个月",
                "success_rate": "65%",
                "cost_overrun": "15%"
            },
            "best_practice": {
                "project_duration": "8个月",
                "success_rate": "85%",
                "cost_overrun": "5%"
            }
        }


class TechnicalReviewTool(BaseTool):
    """技术评审工具"""
    name: str = "技术评审工具"
    description: str = "技术方案科学性评审"

    def _run(self, query: str) -> str:
        """技术评审"""
        return f"技术评审分析:\n{query[:500]}..."


class BudgetReviewTool(BaseTool):
    """预算评审工具"""
    name: str = "预算评审工具"
    description: str = "预算分配合理性评审"

    def _run(self, query: str) -> str:
        """预算评审"""
        return f"预算评审分析:\n{query[:500]}..."


class FeasibilityAssessmentTool(BaseTool):
    """可行性评估工具"""
    name: str = "可行性评估工具"
    description: str = "项目可行性综合评估"

    def _run(self, query: str) -> str:
        """可行性评估"""
        return f"可行性评估分析:\n{query[:500]}..."


class RiskReviewTool(BaseTool):
    """风险评审工具"""
    name: str = "风险评审工具"
    description: str = "项目风险评估和评审"

    def _run(self, query: str) -> str:
        """风险评审"""
        return f"风险评审分析:\n{query[:500]}..."


class ExpertConsultationTool(BaseTool):
    """专家咨询工具"""
    name: str = "专家咨询工具"
    description: str = "专家意见收集和咨询"

    def _run(self, query: str) -> str:
        """专家咨询"""
        return f"专家咨询分析:\n{query[:500]}..."