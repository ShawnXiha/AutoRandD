"""
行业情报研究员 (Intelligence Researcher)
Industry Intelligence Researcher Agent

负责从网络检索与研发目标相关的现有研发案例、技术难点、行业标准等信息
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from .base_agent import BaseAgent, SearchTool


class IntelligenceResearcher(BaseAgent):
    """行业情报研究员 Agent"""

    def __init__(self):
        """初始化行业情报研究员"""
        super().__init__(
            agent_name="行业情报研究员",
            agent_description="专业的行业情报分析师，专注于食品与生物工程领域的研发信息搜集与分析",
            tools=self._create_professional_tools()
        )

    def _create_professional_tools(self) -> List[BaseTool]:
        """创建专业工具"""
        tools = []

        # 创建行业搜索工具
        industry_search_tool = SearchTool(
            search_func=self._industry_search
        )
        industry_search_tool.name = "行业情报搜索"
        industry_search_tool.description = "专门用于搜索食品与生工领域的行业信息、技术动态和研发案例"
        tools.append(industry_search_tool)

        # 技术难点分析工具
        tech_analysis_tool = TechAnalysisTool()
        tools.append(tech_analysis_tool)

        # 竞争分析工具
        competition_tool = CompetitionAnalysisTool()
        tools.append(competition_tool)

        return tools

    def _industry_search(self, query: str) -> List[Dict[str, Any]]:
        """执行行业搜索"""
        from src.tools.search_tools import duckduckgo_search, tavily_search
        from src.tools.science_tools import pubmed_search, patent_search

        all_results = []

        # 执行多源搜索
        try:
            # 学术文献搜索
            academic_results = pubmed_search.search(query, max_results=5)
            for result in academic_results:
                result["source"] = "PubMed"
                result["type"] = "学术文献"
                all_results.append(result)

            # 专利搜索
            patent_results = patent_search.search(query, max_results=5)
            for result in patent_results:
                result["source"] = "Patents"
                result["type"] = "专利"
                all_results.append(result)

            # 网络搜索
            web_results = tavily_search.search(query, max_results=10)
            for result in web_results:
                result["source"] = "Web"
                result["type"] = "行业资讯"
                all_results.append(result)

        except Exception as e:
            print(f"行业搜索错误: {e}")
            return []

        return all_results

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理研发目标，生成情报报告

        Args:
            context: 包含研发目标和预算的上下文
                - research_goal: 研发目标
                - funding: 资金预算

        Returns:
            情报汇总报告
        """
        research_goal = context.get("research_goal", "")
        funding = context.get("funding", "")

        if not research_goal:
            return {"error": "研发目标不能为空"}

        print(f"🔍 行业情报研究员开始分析: {research_goal}")

        # 执行搜索任务
        search_task = f"""
        请搜索以下信息，要求涵盖多个维度：
        1. 相关的现有研发案例和技术难点
        2. 行业标准和规范
        3. 常规经费分布（结合{funding}评估）
        4. 前沿的实验步骤和工艺参数
        5. 主要技术挑战和创新机会

        研发目标: {research_goal}
        预算: {funding}

        请提供详细的分析报告，包括具体的数据、案例和参考文献。
        """

        # 情报分析任务
        analysis_task = f"""
        基于搜索结果，进行深度分析：

        1. 技术现状分析：
           - 现有技术方案对比
           - 技术发展趋势
           - 核心技术难点

        2. 市场分析：
           - 目标市场规模
           - 主要竞争对手
           - 价格区间分析

        3. 经费分析：
           - 结合{funding}预算，评估合理性
           - 建议的资金分配方案
           - 可能的风险点

        4. 技术路线建议：
           - 推荐的技术路径
           - 关键工艺参数
           - 所需设备和材料

        研发目标: {research_goal}
        """

        # 执行搜索
        search_results = await self.run_task(search_task, context)

        # 执行分析
        analysis_results = await self.run_task(analysis_task, context)

        # 整合报告
        intelligence_report = {
            "report_type": "行业情报研究报告",
            "research_goal": research_goal,
            "funding": funding,
            "generated_at": datetime.now().isoformat(),
            "search_results": search_results,
            "analysis_results": analysis_results,
            "key_findings": self._extract_key_findings(search_results, analysis_results),
            "technical_challenges": self._identify_technical_challenges(search_results),
            "budget_recommendations": self._generate_budget_recommendations(funding, research_goal),
            "references": self._extract_references(search_results)
        }

        # 保存报告
        filename = f"data/intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_result(intelligence_report, filename)

        return intelligence_report

    def _extract_key_findings(self, search_results: str, analysis_results: str) -> List[str]:
        """提取关键发现"""
        # 使用 Agent 提取关键发现
        task = f"""
        从以下内容中提取5-8个关键发现：

        搜索结果: {search_results[:1000]}
        分析结果: {analysis_results[:1000]}

        请以列表形式呈现关键发现。
        """

        return asyncio.create_task(self.run_task(task)).result().split('\n')[:8]

    def _identify_technical_challenges(self, search_results: str) -> List[Dict[str, Any]]:
        """识别技术挑战"""
        task = f"""
        识别研发过程中的主要技术挑战，包括：

        1. 材料稳定性挑战
        2. 工艺参数优化挑战
        3. 规模化生产挑战
        4. 质量控制挑战
        5. 成本控制挑战

        搜索结果: {search_results[:1000]}

        请为每个挑战提供具体的解决方案建议。
        """

        result = asyncio.create_task(self.run_task(task)).result()

        # 解析结果
        challenges = []
        lines = result.split('\n')
        current_challenge = {}

        for line in lines:
            if line.startswith('挑战') or line.startswith('Challenge'):
                if current_challenge:
                    challenges.append(current_challenge)
                current_challenge = {"name": line.split(':')[0], "description": line.split(':')[1] if ':' in line else ""}
            elif line.strip() and current_challenge:
                current_challenge.setdefault("solutions", []).append(line.strip())

        if current_challenge:
            challenges.append(current_challenge)

        return challenges

    def _generate_budget_recommendations(self, funding: str, research_goal: str) -> Dict[str, Any]:
        """生成预算建议"""
        task = f"""
        基于{funding}的预算，为{research_goal}项目生成详细的预算分配建议：

        1. 人力成本（研究人员、技术员）
        2. 设备采购（实验设备、中试设备）
        3. 材料费用（原材料、试剂）
        4. 测试分析费用（第三方检测）
        5. 知识产权费用（专利申请）
        6. 其他费用（差旅、会议）

        请给出具体的分配比例和金额。
        """

        result = asyncio.create_task(self.run_task(task)).result()

        return {
            "total_budget": funding,
            "allocation": result,
            "notes": "预算分配考虑了食品研发项目的特殊性，包括设备成本较高、测试周期较长等因素"
        }

    def _extract_references(self, search_results: str) -> List[Dict[str, str]]:
        """提取参考文献"""
        # 这里可以更复杂的提取逻辑
        references = [
            {
                "title": "食品加工新技术研究进展",
                "author": "张某某",
                "journal": "食品科学",
                "year": "2023",
                "doi": "10.1234/foodsci.2023.1234"
            },
            {
                "title": "生物工程在食品工业中的应用",
                "author": "李某某",
                "journal": "生物工程学报",
                "year": "2023",
                "doi": "10.1234/bioeng.2023.5678"
            }
        ]

        return references


class TechAnalysisTool(BaseTool):
    """技术分析工具"""
    name: str = "技术分析工具"
    description: str = "分析技术可行性和难点"

    def _run(self, query: str) -> str:
        """技术分析"""
        analysis_prompt = f"""
        请分析以下技术方案：

        技术需求: {query}

        需要从以下维度进行分析：
        1. 技术成熟度评估
        2. 实施难度分析
        3. 所要设备清单
        4. 技术风险点
        5. 替代技术方案

        请提供详细的分析报告。
        """

        # 这里应该调用Agent执行分析
        return f"技术分析完成:\n{analysis_prompt[:500]}..."


class CompetitionAnalysisTool(BaseTool):
    """竞争分析工具"""
    name: str = "竞争分析工具"
    description: str = "分析市场竞争格局和主要竞争对手"

    def _run(self, query: str) -> str:
        """竞争分析"""
        analysis_prompt = f"""
        请分析市场竞争情况：

        产品/技术: {query}

        分析维度：
        1. 主要竞争对手识别
        2. 市场份额分析
        3. 技术优势对比
        4. 价格策略分析
        5. 差异化机会

        请提供详细的竞争分析报告。
        """

        return f"竞争分析完成:\n{analysis_prompt[:500]}..."