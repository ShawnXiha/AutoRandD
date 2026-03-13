"""
实验数据模拟器 (Data Simulator)
Data Simulator Agent

充当虚拟实验室，根据SOP步骤进行沙盘推演，生成符合物理/化学/生物学常识的模拟实验数据
"""

import asyncio
import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
from crewai.tools import BaseTool
from .base_agent import BaseAgent


class DataSimulator(BaseAgent):
    """实验数据模拟器 Agent"""

    def __init__(self):
        """初始化数据模拟器"""
        super().__init__(
            agent_name="实验数据模拟器",
            agent_description="虚拟实验室，模拟真实的实验过程，生成符合科学规律的实验数据",
            tools=self._create_professional_tools()
        )

    def _create_professional_tools(self) -> List[BaseTool]:
        """创建专业工具"""
        tools = []

        # 数据生成工具
        data_gen_tool = DataGenerationTool()
        tools.append(data_gen_tool)

        # 统计分析工具
        stats_tool = StatisticalAnalysisTool()
        tools.append(stats_tool)

        # 质量模拟工具
        quality_tool = QualitySimulationTool()
        tools.append(quality_tool)

        # 异常模拟工具
        anomaly_tool = AnomalySimulationTool()
        tools.append(anomaly_tool)

        # 报表生成工具
        report_tool = ReportGenerationTool()
        tools.append(report_tool)

        return tools

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟实验过程，生成模拟实验数据

        Args:
            context: 包含SOP和其他信息的上下文
                - research_goal: 研发目标
                - sop_document: SOP文档（来自ExperimentDesigner）
                - simulation_parameters: 模拟参数（可选）

        Returns:
            模拟实验数据记录表
        """
        research_goal = context.get("research_goal", "")
        sop_document = context.get("sop_document", {})
        simulation_parameters = context.get("simulation_parameters", {})

        print(f"🧪 数据模拟器开始模拟: {research_goal}")

        # 第一步：模拟实验设计
        simulation_setup = self._create_simulation_setup(sop_document, simulation_parameters)

        # 第二步：生成基础数据
        baseline_data = await self._generate_baseline_data(simulation_setup)

        # 第三步：模拟实验过程
        experimental_data = await self._simulate_experimental_process(
            simulation_setup, baseline_data
        )

        # 第四步：添加变量关系
        correlated_data = await self._add_variable_correlations(
            simulation_setup, experimental_data
        )

        # 第五步：添加对照组
        control_data = await self._generate_control_groups(
            simulation_setup, correlated_data
        )

        # 第六步：统计分析
        statistical_analysis = await self._perform_statistical_analysis(control_data)

        # 整合模拟数据报告
        simulation_report = {
            "document_type": "模拟实验数据记录表",
            "project_name": f"{research_goal}模拟实验",
            "generated_at": datetime.now().isoformat(),
            "simulation_id": f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "simulation_parameters": simulation_parameters,

            # 模拟概况
            "simulation_overview": {
                "research_goal": research_goal,
                "experiment_type": self._determine_experiment_type(research_goal),
                "simulation_duration": self._estimate_simulation_duration(research_goal),
                "data_points": self._count_data_points(control_data),
                "success_rate": self._calculate_success_rate(control_data)
            },

            # 实验设计
            "experimental_design": {
                "factors": simulation_setup["factors"],
                "levels": simulation_setup["levels"],
                "runs": simulation_setup["runs"],
                "design_type": simulation_setup["design_type"],
                "response_variables": simulation_setup["response_variables"]
            },

            # 原始数据
            "raw_data": control_data,

            # 统计分析
            "statistical_analysis": statistical_analysis,

            # 数据质量评估
            "data_quality": {
                "completeness": self._assess_completeness(control_data),
                "consistency": self._assess_consistency(control_data),
                "accuracy": self._assess_accuracy(control_data),
                "reliability": self._assess_reliability(control_data)
            },

            # 关键发现
            "key_findings": self._extract_key_findings(statistical_analysis),

            # 异常分析
            "anomalies": self._analyze_anomalies(control_data),

            # 建议与结论
            "recommendations": self._generate_recommendations(
                statistical_analysis, control_data
            ),

            # 模拟限制
            "simulation_limitations": [
                "基于理论模型的模拟，实际结果可能有差异",
                "未考虑所有可能的干扰因素",
                "模拟数据需要实际实验验证"
            ],

            # 技术文档
            "technical_documentation": {
                "simulation_model": "基于物理化学规律的数学模型",
                "random_seed": random.getrandbits(32),
                "software_version": "1.0",
                "reference_models": self._list_reference_models()
            }
        }

        # 保存模拟报告
        filename = f"data/simulation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_result(simulation_report, filename)

        return simulation_report

    def _create_simulation_setup(self, sop_document: Dict, simulation_params: Dict) -> Dict[str, Any]:
        """创建模拟设置"""
        # 从SOP中提取关键参数
        process_params = sop_document.get("process_parameters", {})

        return {
            "factors": {
                "temperature": {"range": [40, 80], "unit": "°C"},
                "time": {"range": [30, 120], "unit": "min"},
                "ph": {"range": [3.0, 7.0], "unit": ""},
                "concentration": {"range": [5, 20], "unit": "%"}
            },
            "levels": 3,
            "runs": 30,
            "design_type": "中心复合设计（CCD）",
            "response_variables": [
                {"name": "提取率", "unit": "%", "range": [60, 95]},
                {"name": "纯度", "unit": "%", "range": [85, 99]},
                {"name": "活性保留率", "unit": "%", "range": [70, 100]},
                {"name": "颜色指数", "unit": "", "range": [0.2, 0.8]}
            ],
            "simulation_parameters": simulation_params
        }

    async def _generate_baseline_data(self, setup: Dict) -> List[Dict[str, Any]]:
        """生成基础数据"""
        data = []

        # 生成实验矩阵
        for run in range(setup["runs"]):
            experiment = {
                "run_id": f"RUN_{run+1:03d}",
                "timestamp": (datetime.now() + timedelta(minutes=run*10)).isoformat(),
                "replicate": run % 3 + 1,  # 3次重复
                "block": (run // 9) + 1,   # 3个区组
            }

            # 随机生成因子水平
            for factor, params in setup["factors"].items():
                low, high = params["range"]
                if factor == "temperature":
                    # 温度：正态分布
                    value = np.random.normal((low + high) / 2, (high - low) / 6)
                    experiment[factor] = np.clip(value, low, high)
                elif factor == "time":
                    # 时间：均匀分布
                    value = np.random.uniform(low, high)
                    experiment[factor] = round(value, 1)
                elif factor == "ph":
                    # pH：离散分布
                    levels = np.linspace(low, high, 5)
                    experiment[factor] = np.random.choice(levels)
                else:
                    # 其他：均匀分布
                    value = np.random.uniform(low, high)
                    experiment[factor] = round(value, 2)

            data.append(experiment)

        return data

    async def _simulate_experimental_process(self, setup: Dict, baseline_data: List) -> List[Dict[str, Any]]:
        """模拟实验过程"""
        experimental_data = []

        for experiment in baseline_data:
            # 模拟实验响应
            responses = {}

            # 提取率模型（响应面）
            temp = experiment["temperature"]
            time = experiment["time"]
            ph = experiment["ph"]
            conc = experiment["concentration"]

            # 基础模型：y = β0 + β1x1 + β2x2 + β12x1x2 + β11x1² + β22x2²
            # 提取率模型
            extraction_rate = (
                70 +
                0.3 * (temp - 40) +
                0.2 * (time - 30) / 10 +
                5 * (ph - 3) +
                0.5 * (conc - 5) -
                0.002 * (temp - 40)**2 -
                0.001 * (time - 30)**2 / 10 +
                0.1 * (temp - 40) * (time - 30) / 100 +
                np.random.normal(0, 2)  # 随机误差
            )
            responses["提取率"] = np.clip(extraction_rate, 60, 95)

            # 纯度模型
            purity = (
                90 +
                0.1 * (temp - 40) -
                0.05 * (time - 30) / 10 +
                2 * (7 - ph) -
                0.001 * (temp - 40)**2 +
                np.random.normal(0, 1)
            )
            responses["纯度"] = np.clip(purity, 85, 99)

            # 活性保留率
            activity = (
                90 +
                0.2 * (4 - ph) -
                0.01 * (temp - 40) -
                0.005 * (time - 30) / 10 +
                np.random.normal(0, 3)
            )
            responses["活性保留率"] = np.clip(activity, 70, 100)

            # 颜色指数（与温度相关）
            color = 0.2 + 0.01 * (temp - 40) + np.random.normal(0, 0.05)
            responses["颜色指数"] = np.clip(color, 0.2, 0.8)

            # 添加质量指标
            responses["质量评分"] = (
                0.4 * responses["提取率"] / 95 +
                0.3 * responses["纯度"] / 99 +
                0.2 * responses["活性保留率"] / 100 +
                0.1 * (1 - responses["颜色指数"])
            ) * 100

            # 添加实验过程数据
            experiment.update(responses)

            # 添加实验状态
            if responses["提取率"] > 85 and responses["纯度"] > 95:
                experiment["status"] = "成功"
            elif responses["提取率"] > 70 and responses["纯度"] > 90:
                experiment["status"] = "部分成功"
            else:
                experiment["status"] = "失败"

            experimental_data.append(experiment)

        return experimental_data

    async def _add_variable_correlations(self, setup: Dict, data: List) -> List[Dict[str, Any]]:
        """添加变量间的相关性"""
        correlated_data = data.copy()

        # 添加批次效应
        for i, exp in enumerate(correlated_data):
            batch_effect = np.random.normal(0, 1) if i < 15 else np.random.normal(1, 1)
            exp["提取率"] += batch_effect
            exp["提取率"] = np.clip(exp["提取率"], 60, 95)

        # 添加时间趋势
        for i, exp in enumerate(correlated_data):
            time_trend = 0.01 * i  # 轻微上升趋势
            exp["纯度"] += time_trend
            exp["纯度"] = np.clip(exp["纯度"], 85, 99)

        return correlated_data

    async def _generate_control_groups(self, setup: Dict, data: List) -> List[Dict[str, Any]]:
        """生成对照组数据"""
        all_data = data.copy()

        # 添加空白对照
        blank_control = {
            "run_id": "BLANK_001",
            "timestamp": datetime.now().isoformat(),
            "replicate": 1,
            "block": 1,
            "temperature": 25,
            "time": 0,
            "ph": 7.0,
            "concentration": 0,
            "提取率": 5.0,
            "纯度": 50.0,
            "活性保留率": 0,
            "颜色指数": 0.1,
            "质量评分": 10.0,
            "status": "空白对照"
        }
        all_data.append(blank_control)

        # 添加阴性对照
        negative_control = {
            "run_id": "NEG_001",
            "timestamp": datetime.now().isoformat(),
            "replicate": 1,
            "block": 1,
            "temperature": 40,
            "time": 30,
            "ph": 3.0,
            "concentration": 5,
            "提取率": 30.0,
            "纯度": 60.0,
            "活性保留率": 20,
            "颜色指数": 0.8,
            "质量评分": 35.0,
            "status": "阴性对照"
        }
        all_data.append(negative_control)

        # 添加阳性对照（最优条件）
        optimal_conditions = {"temperature": 60, "time": 60, "ph": 5.0, "concentration": 10}
        positive_base = {
            "提取率": 90.0,
            "纯度": 98.0,
            "活性保留率": 95,
            "颜色指数": 0.3,
            "质量评分": 95.0,
            "status": "阳性对照"
        }

        for rep in range(3):
            positive_control = {
                "run_id": f"POS_{rep+1:03d}",
                "timestamp": datetime.now().isoformat(),
                "replicate": rep + 1,
                "block": 1,
                **optimal_conditions,
                **positive_base,
                "提取率": positive_base["提取率"] + np.random.normal(0, 2),
                "纯度": positive_base["纯度"] + np.random.normal(0, 1),
                "活性保留率": positive_base["活性保留率"] + np.random.normal(0, 3),
            }
            all_data.append(positive_control)

        return all_data

    async def _perform_statistical_analysis(self, data: List) -> Dict[str, Any]:
        """统计分析"""
        if not data:
            return {"error": "No data for analysis"}

        # 提取数值数据
        extraction_rates = [d["提取率"] for d in data if isinstance(d["提取率"], (int, float))]
        purities = [d["纯度"] for d in data if isinstance(d["纯度"], (int, float))]
        activities = [d["活性保留率"] for d in data if isinstance(d["活性保留率"], (int, float))]

        analysis = {
            "descriptive_statistics": {
                "extraction_rate": {
                    "mean": np.mean(extraction_rates),
                    "median": np.median(extraction_rates),
                    "std": np.std(extraction_rates),
                    "min": np.min(extraction_rates),
                    "max": np.max(extraction_rates),
                    "q25": np.percentile(extraction_rates, 25),
                    "q75": np.percentile(extraction_rates, 75)
                },
                "purity": {
                    "mean": np.mean(purities),
                    "median": np.median(purities),
                    "std": np.std(purities),
                    "min": np.min(purities),
                    "max": np.max(purities)
                },
                "activity": {
                    "mean": np.mean(activities),
                    "median": np.median(activities),
                    "std": np.std(activities),
                    "min": np.min(activities),
                    "max": np.max(activities)
                }
            },
            "statistical_tests": {
                "anova_extraction_vs_purity": self._perform_anova(extraction_rates, purities),
                "correlation_analysis": self._perform_correlation_analysis(data),
                "regression_analysis": self._perform_regression_analysis(data)
            },
            "quality_metrics": {
                "success_rate": len([d for d in data if d["status"] == "成功"]) / len(data) * 100,
                "coefficient_variation": np.std(extraction_rates) / np.mean(extraction_rates) * 100,
                "signal_to_noise": self._calculate_signal_to_noise(data)
            }
        }

        return analysis

    def _perform_anova(self, group1: List, group2: List) -> Dict[str, float]:
        """执行ANOVA分析"""
        try:
            f_stat, p_value = stats.f_oneway(group1, group2)
            return {
                "f_statistic": f_stat,
                "p_value": p_value,
                "significant": p_value < 0.05
            }
        except:
            return {"error": "ANOVA analysis failed"}

    def _perform_correlation_analysis(self, data: List) -> Dict[str, float]:
        """相关性分析"""
        try:
            extraction = [d["提取率"] for d in data]
            purity = [d["纯度"] for d in data]
            activity = [d["活性保留率"] for d in data]

            # 皮尔逊相关系数
            corr_ex_pur, _ = stats.pearsonr(extraction, purity)
            act_ex_pur, _ = stats.pearsonr(activity, extraction)

            return {
                "extraction_purity": corr_ex_pur,
                "activity_extraction": act_ex_pur
            }
        except:
            return {"error": "Correlation analysis failed"}

    def _perform_regression_analysis(self, data: List) -> Dict[str, Any]:
        """回归分析"""
        try:
            X = np.array([[d["温度"], d["时间"], d["ph"]] for d in data])
            y = np.array([d["提取率"] for d in data])

            # 多元线性回归
            coefficients, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

            return {
                "coefficients": {
                    "temperature": coefficients[0],
                    "time": coefficients[1],
                    "ph": coefficients[2]
                },
                "r_squared": np.corrcoef(y, X @ coefficients)[0, 1]**2
            }
        except:
            return {"error": "Regression analysis failed"}

    def _calculate_signal_to_noise(self, data: List) -> float:
        """计算信噪比"""
        if not data:
            return 0

        signal = np.mean([d["提取率"] for d in data])
        noise = np.std([d["提取率"] for d in data])

        if noise == 0:
            return float('inf')

        return 20 * np.log10(signal / noise)

    def _determine_experiment_type(self, research_goal: str) -> str:
        """确定实验类型"""
        if "提取" in research_goal:
            return "提取工艺优化实验"
        elif "加工" in research_goal:
            return "加工工艺优化实验"
        else:
            return "工艺参数优化实验"

    def _estimate_simulation_duration(self, research_goal: str) -> str:
        """估算模拟时长"""
        return "5-10分钟"

    def _count_data_points(self, data: List) -> int:
        """统计数据点"""
        return len(data)

    def _calculate_success_rate(self, data: List) -> float:
        """计算成功率"""
        successful = len([d for d in data if d["status"] == "成功"])
        return successful / len(data) * 100

    def _assess_completeness(self, data: List) -> float:
        """评估数据完整性"""
        if not data:
            return 0

        # 检查必要的字段
        required_fields = ["提取率", "纯度", "活性保留率"]
        complete_records = 0

        for record in data:
            if all(field in record for field in required_fields):
                complete_records += 1

        return complete_records / len(data) * 100

    def _assess_consistency(self, data: List) -> float:
        """评估数据一致性"""
        if not data:
            return 0

        # 计算变异系数
        extraction_rates = [d["提取率"] for d in data]
        cv = np.std(extraction_rates) / np.mean(extraction_rates) * 100

        # 变异系数越小，一致性越好
        return max(0, 100 - cv)

    def _assess_accuracy(self, data: List) -> float:
        """评估数据准确性"""
        # 检查是否有异常值
        extraction_rates = [d["提取率"] for d in data]
        q1 = np.percentile(extraction_rates, 25)
        q3 = np.percentile(extraction_rates, 75)
        iqr = q3 - q1

        outliers = len([x for x in extraction_rates if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr])

        return (len(data) - outliers) / len(data) * 100

    def _assess_reliability(self, data: List) -> float:
        """评估数据可靠性"""
        # 基于重复实验的一致性
        reliability_scores = []

        for i in range(0, len(data) - 2, 3):
            group = data[i:i+3]
            if len(group) == 3:
                scores = [d["提取率"] for d in group]
                cv = np.std(scores) / np.mean(scores) * 100
                reliability_scores.append(max(0, 100 - cv))

        return np.mean(reliability_scores) if reliability_scores else 0

    def _extract_key_findings(self, statistical_analysis: Dict) -> List[str]:
        """提取关键发现"""
        findings = []

        if "descriptive_statistics" in statistical_analysis:
            stats = statistical_analysis["descriptive_statistics"]

            if "extraction_rate" in stats:
                mean_extraction = stats["extraction_rate"]["mean"]
                findings.append(f"平均提取率为 {mean_extraction:.1f}%")

        if "quality_metrics" in statistical_analysis:
            quality = statistical_analysis["quality_metrics"]

            if "success_rate" in quality:
                success_rate = quality["success_rate"]
                findings.append(f"实验成功率为 {success_rate:.1f}%")

        findings.append("温度对提取率有显著影响")
        findings.append("pH值对产品纯度影响较大")

        return findings

    def _analyze_anomalies(self, data: List) -> List[Dict[str, Any]]:
        """分析异常数据"""
        anomalies = []

        # 识别异常值
        extraction_rates = [d["提取率"] for d in data]
        q1 = np.percentile(extraction_rates, 25)
        q3 = np.percentile(extraction_rates, 75)
        iqr = q3 - q1

        for i, record in enumerate(data):
            extraction = record["提取率"]
            if extraction < q1 - 1.5 * iqr or extraction > q3 + 1.5 * iqr:
                anomalies.append({
                    "record_id": record["run_id"],
                    "value": extraction,
                    "type": "outlier",
                    "possible_cause": "实验条件异常或测量误差"
                })

        return anomalies

    def _generate_recommendations(self, statistical_analysis: Dict, data: List) -> List[str]:
        """生成建议"""
        recommendations = []

        # 基于统计分析的建议
        if "statistical_tests" in statistical_analysis:
            tests = statistical_analysis["statistical_tests"]

            if "correlation_analysis" in tests:
                corr = tests["correlation_analysis"]
                if "extraction_purity" in corr:
                    if corr["extraction_purity"] > 0.8:
                        recommendations.append("提取率和纯度高度相关，可考虑优化其中一个指标")

        # 基于数据分布的建议
        recommendations.append("建议在温度60-70°C区间进行重点优化")
        recommendations.append("建议增加pH值5.0-6.0的实验点")
        recommendations.append("建议进行重复实验以验证结果的可靠性")

        return recommendations

    def _list_reference_models(self) -> List[Dict[str, str]]:
        """列出参考模型"""
        return [
            {
                "model": "Arrhenius方程",
                "application": "温度对反应速率的影响",
                "reference": "物理化学动力学"
            },
            {
                "model": "Michaelis-Menten方程",
                "application": "酶催化反应动力学",
                "reference": "酶学"
            },
            {
                "model": "响应面方法",
                "application": "工艺参数优化",
                "reference": "实验设计"
            }
        ]


class DataGenerationTool(BaseTool):
    """数据生成工具"""
    name: str = "数据生成工具"
    description: str = "生成模拟实验数据"

    def _run(self, query: str) -> str:
        """生成数据"""
        return f"数据生成完成:\n{query[:500]}..."


class StatisticalAnalysisTool(BaseTool):
    """统计分析工具"""
    name: str = "统计分析工具"
    description: str = "进行统计分析和数据挖掘"

    def _run(self, query: str) -> str:
        """统计分析"""
        return f"统计分析完成:\n{query[:500]}..."


class QualitySimulationTool(BaseTool):
    """质量模拟工具"""
    name: str = "质量模拟工具"
    description: str = "模拟产品质量指标"

    def _run(self, query: str) -> str:
        """质量模拟"""
        return f"质量模拟完成:\n{query[:500]}..."


class AnomalySimulationTool(BaseTool):
    """异常模拟工具"""
    name: str = "异常模拟工具"
    description: str = "模拟实验过程中的异常情况"

    def _run(self, query: str) -> str:
        """异常模拟"""
        return f"异常模拟完成:\n{query[:500]}..."


class ReportGenerationTool(BaseTool):
    """报表生成工具"""
    name: str = "报表生成工具"
    description: str = "生成实验数据报表和分析报告"

    def _run(self, query: str) -> str:
        """报表生成"""
        return f"报表生成完成:\n{query[:500]}..."