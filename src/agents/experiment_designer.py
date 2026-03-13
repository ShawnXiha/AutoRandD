"""
实验设计与操作员 (Experiment Designer)
Experiment Designer Agent

为最终研发计划设计具体的实验步骤，精确到工艺参数维度
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from .base_agent import BaseAgent


class ExperimentDesigner(BaseAgent):
    """实验设计与操作员 Agent"""

    def __init__(self):
        """初始化实验设计师"""
        super().__init__(
            agent_name="实验设计与操作员",
            agent_description="负责设计详细的实验方案，包括工艺参数、操作步骤和质量控制",
            tools=self._create_professional_tools()
        )

    def _create_professional_tools(self) -> List[BaseTool]:
        """创建专业工具"""
        tools = []

        # 工艺设计工具
        process_tool = ProcessDesignTool()
        tools.append(process_tool)

        # 参数优化工具
        param_tool = ParameterOptimizationTool()
        tools.append(param_tool)

        # 实验设计工具
        doe_tool = DesignOfExperimentsTool()
        tools.append(doe_tool)

        # SOP生成工具
        sop_tool = SOPGenerationTool()
        tools.append(sop_tool)

        # 质量控制工具
        qc_tool = QualityControlTool()
        tools.append(qc_tool)

        return tools

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        设计实验方案，生成详细的SOP

        Args:
            context: 包含最终研发计划和其他信息的上下文
                - research_goal: 研发目标
                - final_rd_plan: 最终研发计划（来自PlanReviewer）
                - experiment_requirements: 实验要求（可选）

        Returns:
            实验操作标准指南 (SOP)
        """
        research_goal = context.get("research_goal", "")
        final_rd_plan = context.get("final_rd_plan", {})
        experiment_requirements = context.get("experiment_requirements", {})

        print(f"🔬 实验设计师开始设计: {research_goal}")

        # 第一步：核心工艺设计
        process_design_task = f"""
        基于{research_goal}的最终研发计划，设计核心工艺方案：

        研发计划概要: {json.dumps(final_rd_plan, ensure_ascii=False)[:2000]}

        工艺设计要点：
        1. 工艺流程设计
           - 确定主要工艺单元操作
           - 设计工艺流程图
           - 确定各单元操作的功能

        2. 关键工艺参数设计
           - 温度范围设计（精确到±0.5°C）
           - 时间参数设计（精确到±1分钟）
           - 料液比设计（精确到±0.1）
           - pH值范围（精确到±0.1）
           - 剪切速率设计（精确到±50 rpm）
           - 压力参数设计（精确到±0.1 MPa）

        3. 设备选型和规格
           - 反应器规格（容积、材质、搅拌方式）
           - 分离设备规格
           - 干燥设备规格
           - 包装设备规格

        4. 工艺控制点设计
           - 关键控制参数
           - 控制频率和方法
           - 异常处理机制

        请设计详细的工艺方案。
        """

        process_design_results = await self.run_task(process_design_task, context)

        # 第二步：实验设计（DOE）
        doe_task = f"""
        为{research_goal}设计详细的实验方案：

        设计原则：
        1. 关键因素识别
           - 识别3-5个关键影响因素
           - 确定每个因素的合理范围
           - 选择合适的响应变量

        2. 实验设计方法
           - 响应面设计（RSM）或正交设计
           - 因素水平设置
           - 实验次数规划

        3. 对照实验设计
           - 空白对照
           - 阳性对照
           - 阴性对照
           - 平行实验设置

        4. 数据收集计划
           - 取样点设置
           - 检测指标选择
           - 数据记录格式

        请设计完整的实验方案。
        """

        doe_results = await self.run_task(doe_task, context)

        # 第三步：标准化操作流程（SOP）
        sop_task = f"""
        为{research_goal}生成详细的标准化操作流程（SOP）：

        SOP要求：
        1. 实验准备
           - 仪器设备清单
           - 试剂材料清单
           - 安全防护要求

        2. 详细操作步骤
           - 步骤分解到具体动作
           - 关键参数控制点
           - 时间节点控制

        3. 质量控制
           - 中间体检测方法
           - 成品质量标准
           - 不合格品处理流程

        4. 数据记录
           - 记录表格模板
           - 数据审核流程
           - 异常数据处理

        请生成详细的SOP文档。
        """

        sop_results = await self.run_task(sop_task, context)

        # 第四步：设备操作规程
        equipment_task = f"""
        设计详细的设备操作规程：

        设备包括：
        1. 反应设备操作规程
           - 开机检查
           - 参数设置
           - 运行监控
           - 停机清理

        2. 分离设备操作规程
           - 设备准备
           - 参数调整
           - 运行监控
           - 设备维护

        3. 干燥设备操作规程
           - 预处理
           - 干燥参数设置
           - 干燥过程控制
           - 成品收集

        4. 分析检测设备操作规程
           - 设校准
           - 样品制备
           - 检测操作
           - 数据分析

        请生成详细的设备操作规程。
        """

        equipment_results = await self.run_task(equipment_task, context)

        # 整合SOP文档
        sop_document = {
            "document_type": "实验操作标准指南 (SOP)",
            "project_name": f"{research_goal}实验SOP",
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "review_status": "待审核",

            # 文档信息
            "document_info": {
                "document_title": f"{research_goal}实验操作标准指南",
                "prepared_by": "实验设计与操作员",
                "approved_by": "技术负责人",
                "effective_date": datetime.now().strftime("%Y-%m-%d"),
                "revision_history": [
                    {
                        "version": "1.0",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "changes": "初始版本"
                    }
                ]
            },

            # 实验概况
            "experiment_overview": {
                "research_goal": research_goal,
                "experiment_type": self._determine_experiment_type(research_goal),
                "duration": self._estimate_experiment_duration(research_goal),
                "team_size": self._estimate_team_size(research_goal),
                "safety_level": self._assess_safety_level(research_goal)
            },

            # 第一部分：实验设计
            "experiment_design": {
                "objective": self._define_objectives(research_goal),
                "key_variables": self._identify_key_variables(research_goal),
                "experimental_matrix": self._create_experimental_matrix(doe_results),
                "control_groups": self._define_control_groups(),
                "sampling_plan": self._create_sampling_plan()
            },

            # 第二部分：工艺参数
            "process_parameters": {
                "temperature_control": self._define_temperature_parameters(),
                "time_control": self._define_time_parameters(),
                "ratio_control": self._define_ratio_parameters(),
                "ph_control": self._define_ph_parameters(),
                "pressure_control": self._define_pressure_parameters(),
                "agitation_control": self._define_agitation_parameters(),
                "concentration_control": self._define_concentration_parameters()
            },

            # 第三部分：材料与设备
            "materials_and_equipment": {
                "chemicals": self._list_chemicals(),
                "reagents": self._list_reagents(),
                "equipment": self._list_equipment(),
                "consumables": self._list_consumables(),
                "calibration_requirements": self._define_calibration_requirements()
            },

            # 第四部分：实验流程
            "experimental_procedure": {
                "pre_experiment": self._define_pre_experiment_steps(),
                "main_experiment": self._define_main_experiment_steps(),
                "post_experiment": self._define_post_experiment_steps(),
                "emergency_procedures": self._define_emergency_procedures()
            },

            # 第五部分：质量控制
            "quality_control": {
                "quality_standards": self._define_quality_standards(),
                "test_methods": self._define_test_methods(),
                "acceptance_criteria": self._define_acceptance_criteria(),
                "rejection_criteria": self._define_rejection_criteria(),
                "documentation_requirements": self._define_documentation_requirements()
            },

            # 第六部分：数据分析
            "data_analysis": {
                "statistical_methods": self._define_statistical_methods(),
                "reporting_format": self._define_reporting_format(),
                "interpretation_guidelines": self._define_interpretation_guidelines(),
                "follow_up_actions": self._define_follow_up_actions()
            },

            # 第七部分：安全规范
            "safety_regulations": {
                "personal_protection": self._define_ppe_requirements(),
                "chemical_safety": self._define_chemical_safety(),
                "equipment_safety": self._define_equipment_safety(),
                "emergency_contacts": self._define_emergency_contacts(),
                "waste_disposal": self._define_waste_disposal()
            },

            # 附录
            "appendix": {
                "standard_operating_procedures": sop_results,
                "equipment_manuals": equipment_results,
                "reference_standards": self._list_reference_standards(),
                "training_requirements": self._define_training_requirements(),
                "troubleshooting_guide": self._create_troubleshooting_guide()
            }
        }

        # 保存SOP文档
        filename = f"data/sop_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_result(sop_document, filename)

        return sop_document

    def _determine_experiment_type(self, research_goal: str) -> str:
        """确定实验类型"""
        if "茶多酚" in research_goal:
            return "提取工艺优化实验"
        elif "蛋白棒" in research_goal:
            return "加工工艺优化实验"
        else:
            return "工艺参数优化实验"

    def _estimate_experiment_duration(self, research_goal: str) -> str:
        """估算实验周期"""
        if "提取" in research_goal:
            return "2-4周"
        elif "加工" in research_goal:
            return "4-6周"
        else:
            return "3-5周"

    def _estimate_team_size(self, research_goal: str) -> Dict[str, int]:
        """估算团队规模"""
        return {
            "principal_investigator": 1,
            "research_assistants": 2,
            "technicians": 2,
            "analysts": 1,
            "total": 6
        }

    def _assess_safety_level(self, research_goal: str) -> str:
        """评估安全等级"""
        return "中等风险"

    def _define_objectives(self, research_goal: str) -> List[str]:
        """定义实验目标"""
        return [
            "优化关键工艺参数",
            "提高产品质量和稳定性",
            "降低生产成本",
            "缩短生产周期",
            "提高生产效率"
        ]

    def _identify_key_variables(self, research_goal: str) -> List[Dict[str, Any]]:
        """识别关键变量"""
        return [
            {
                "variable": "温度",
                "unit": "°C",
                "range": "40-80",
                "importance": "高",
                "description": "影响反应速率和产品质量"
            },
            {
                "variable": "时间",
                "unit": "min",
                "range": "30-120",
                "importance": "中",
                "description": "影响反应程度"
            },
            {
                "variable": "pH值",
                "unit": "",
                "range": "3.0-7.0",
                "importance": "高",
                "description": "影响产物稳定性"
            }
        ]

    def _create_experimental_matrix(self, doe_results: str) -> Dict[str, Any]:
        """创建实验矩阵"""
        return {
            "design_type": "响应面设计（Box-Behnken）",
            "factors": 3,
            "levels": 3,
            "runs": 15,
            "center_points": 3,
            "randomization": "完全随机化"
        }

    def _define_control_groups(self) -> List[Dict[str, Any]]:
        """定义对照组"""
        return [
            {
                "group": "空白对照",
                "description": "不加任何试剂的基础实验",
                "purpose": "验证背景影响"
            },
            {
                "group": "阳性对照",
                "description": "使用已知最优条件的实验",
                "purpose": "验证方法有效性"
            },
            {
                "group": "阴性对照",
                "description": "使用已知失败条件的实验",
                "purpose": "验证方法敏感性"
            }
        ]

    def _create_sampling_plan(self) -> Dict[str, Any]:
        """创建取样计划"""
        return {
            "sampling_points": ["0h", "1h", "2h", "4h", "6h", "24h"],
            "sample_types": ["液体样品", "固体样品"],
            "sample_volumes": ["10mL", "5g"],
            "storage_conditions": "-20°C保存",
            "analytical_methods": ["HPLC", "UV-Vis", "GC-MS"]
        }

    def _define_temperature_parameters(self) -> List[Dict[str, Any]]:
        """定义温度参数"""
        return [
            {
                "parameter": "反应温度",
                "range": "40-80°C",
                "accuracy": "±0.5°C",
                "control_method": "恒温水浴锅",
                "monitoring_frequency": "每30分钟记录一次"
            },
            {
                "parameter": "干燥温度",
                "range": "40-60°C",
                "accuracy": "±1°C",
                "control_method": "烘箱温度控制",
                "monitoring_frequency": "每小时记录一次"
            }
        ]

    def _define_time_parameters(self) -> List[Dict[str, Any]]:
        """定义时间参数"""
        return [
            {
                "parameter": "反应时间",
                "range": "30-120 min",
                "accuracy": "±1 min",
                "control_method": "定时器",
                "monitoring_frequency": "开始和结束时记录"
            },
            {
                "parameter": "搅拌时间",
                "range": "10-60 min",
                "accuracy": "±1 min",
                "control_method": "定时器",
                "monitoring_frequency": "持续监控"
            }
        ]

    def _define_ratio_parameters(self) -> List[Dict[str, Any]]:
        """定义比例参数"""
        return [
            {
                "parameter": "料液比",
                "range": "1:5-1:20",
                "accuracy": "±0.1",
                "unit": "g/mL",
                "control_method": "电子天平+量筒"
            },
            {
                "parameter": "溶剂比例",
                "range": "5-95%",
                "accuracy": "±1%",
                "unit": "%",
                "control_method": "体积比配制"
            }
        ]

    def _define_ph_parameters(self) -> List[Dict[str, Any]]:
        """定义pH参数"""
        return [
            {
                "parameter": "反应pH",
                "range": "3.0-7.0",
                "accuracy": "±0.1",
                "control_method": "pH计+酸碱调节",
                "monitoring_frequency": "每30分钟检测一次"
            },
            {
                "parameter": "储存pH",
                "range": "4.0-6.0",
                "accuracy": "±0.1",
                "control_method": "缓冲溶液调节",
                "monitoring_frequency": "每日检测"
            }
        ]

    def _define_pressure_parameters(self) -> List[Dict[str, Any]]:
        """定义压力参数"""
        return [
            {
                "parameter": "均质压力",
                "range": "20-40 MPa",
                "accuracy": "±0.5 MPa",
                "control_method": "高压均质机",
                "monitoring_frequency": "持续监控"
            },
            {
                "parameter": "真空度",
                "range": "-0.08--0.09 MPa",
                "accuracy": "±0.001 MPa",
                "control_method": "真空泵",
                "monitoring_frequency": "每小时检测"
            }
        ]

    def _define_agitation_parameters(self) -> List[Dict[str, Any]]:
        """定义搅拌参数"""
        return [
            {
                "parameter": "搅拌速率",
                "range": "100-1000 rpm",
                "accuracy": "±50 rpm",
                "control_method": "磁力搅拌器/机械搅拌器",
                "monitoring_frequency": "持续监控"
            },
            {
                "parameter": "剪切速率",
                "range": "100-1000 s⁻¹",
                "accuracy": "±50 s⁻¹",
                "control_method": "高剪切混合机",
                "monitoring_frequency": "持续监控"
            }
        ]

    def _define_concentration_parameters(self) -> List[Dict[str, Any]]:
        """定义浓度参数"""
        return [
            {
                "parameter": "原料浓度",
                "range": "5-20%",
                "accuracy": "±0.5%",
                "unit": "w/v",
                "control_method": "电子天平+溶剂配制"
            },
            {
                "parameter": "活性成分浓度",
                "range": "1-10 mg/mL",
                "accuracy": "±0.1 mg/mL",
                "unit": "mg/mL",
                "control_method": "HPLC检测"
            }
        ]

    def _list_chemicals(self) -> List[Dict[str, str]]:
        """列出化学品"""
        return [
            {"name": "茶多酚", "purity": "≥98%", "CAS": "84650-60-2", "supplier": "某生物科技公司"},
            {"name": "蛋白质", "purity": "≥90%", "CAS": "9004-34-6", "supplier": "某食品添加剂公司"}
        ]

    def _list_reagents(self) -> List[Dict[str, str]]:
        """列出试剂"""
        return [
            {"name": "乙醇", "grade": "分析纯", "concentration": "95%", "purpose": "提取溶剂"},
            {"name": "甲醇", "grade": "色谱纯", "concentration": "100%", "purpose": "HPLC流动相"}
        ]

    def _list_equipment(self) -> List[Dict[str, Any]]:
        """列出设备"""
        return [
            {
                "name": "高压均质机",
                "model": "GJJ-50",
                "capacity": "50L",
                "manufacturer": "某机械公司",
                "calibration_date": "2024-01-15"
            },
            {
                "name": "冷冻干燥机",
                "model": "FD-1A-50",
                "capacity": "50L",
                "manufacturer": "某冷冻设备公司",
                "calibration_date": "2024-01-15"
            }
        ]

    def _list_consumables(self) -> List[Dict[str, str]]:
        """列出耗材"""
        return [
            {"name": "离心管", "volume": "50mL", "material": "PP", "quantity": "100个"},
            {"name": "滤膜", "pore_size": "0.22μm", "diameter": "47mm", "quantity": "50张"}
        ]

    def _define_calibration_requirements(self) -> Dict[str, str]:
        """定义校准要求"""
        return {
            "equipment": "每季度校准一次",
            "temperature": "每年校准一次",
            "pressure": "每年校准一次",
            "pH计": "每月校准一次",
            "balance": "每年校准一次"
        }

    def _define_pre_experiment_steps(self) -> List[str]:
        """定义实验前步骤"""
        return [
            "检查仪器设备状态",
            "校准检测仪器",
            "准备试剂和材料",
            "清洁实验台面",
            "穿戴个人防护装备"
        ]

    def _define_main_experiment_steps(self) -> List[str]:
        """定义主要实验步骤"""
        return [
            "称取原料",
            "配制溶液",
            "调节pH值",
            "设置反应参数",
            "开始反应",
            "监控反应过程",
            "取样检测",
            "记录数据"
        ]

    def _define_post_experiment_steps(self) -> List[str]:
        """定义实验后步骤"""
        return [
            "停止反应",
            "冷却样品",
            "分离产物",
            "纯化处理",
            "包装储存",
            "清洁设备",
            "废弃物处理"
        ]

    def _define_emergency_procedures(self) -> Dict[str, str]:
        """定义应急程序"""
        return {
            "chemical_spill": "立即清理，佩戴防护装备",
            "equipment_failure": "立即停止操作，联系维修",
            "fire": "使用灭火器，疏散人员",
            "personal_injury": "立即就医，报告主管"
        }

    def _define_quality_standards(self) -> Dict[str, Any]:
        """定义质量标准"""
        return {
            "purity": "≥95%",
            "moisture": "≤5%",
            "heavy_metals": "≤10 ppm",
            "microbial": "≤1000 CFU/g",
            "appearance": "白色至淡黄色粉末"
        }

    def _define_test_methods(self) -> List[Dict[str, str]]:
        """定义测试方法"""
        return [
            {"parameter": "纯度", "method": "HPLC", "standard": "USP <467>"},
            {"parameter": "水分", "method": "卡尔费休法", "standard": "AOAC 926.12"},
            {"parameter": "重金属", "method": "ICP-MS", "standard": "EP 2.4.8"}
        ]

    def _define_acceptance_criteria(self) -> Dict[str, Any]:
        """定义接受标准"""
        return {
            "appearance": "符合标准",
            "assay": "90-110%",
            "impurities": "≤2.0%",
            "dissolution": "≥80%",
            "stability": "符合要求"
        }

    def _define_rejection_criteria(self) -> List[str]:
        """定义拒绝标准"""
        return [
            "外观异常",
            "含量不符合标准",
            "杂质超标",
            "微生物超标",
            "稳定性不符合要求"
        ]

    def _define_documentation_requirements(self) -> Dict[str, str]:
        """定义文档要求"""
        return {
            "lab_notebook": "实时记录",
            "electronic_records": "每日备份",
            "raw_data": "原始数据保存",
            "change_control": "变更记录",
            "review": "同行评审"
        }

    def _define_statistical_methods(self) -> List[str]:
        """定义统计方法"""
        return [
            "描述性统计",
            "方差分析（ANOVA）",
            "回归分析",
            "响应面分析",
            "实验设计分析"
        ]

    def _define_reporting_format(self) -> Dict[str, str]:
        """定义报告格式"""
        return {
            "report_template": "标准实验报告模板",
            "data_format": "Excel表格",
            "charts": "图表可视化",
            "statistics": "统计分析报告",
            "conclusions": "结论和建议"
        }

    def _define_interpretation_guidelines(self) -> List[str]:
        """定义解释指南"""
        return [
            "统计显著性判断",
            "效应量计算",
            "置信区间分析",
            "p值解读",
            "实际意义评估"
        ]

    def _define_follow_up_actions(self) -> List[str]:
        """定义后续行动"""
        return [
            "重复验证实验",
            "优化工艺参数",
            "放大试验",
            "稳定性研究",
            "工艺验证"
        ]

    def _define_ppe_requirements(self) -> Dict[str, List[str]]:
        """定义PPE要求"""
        return {
            "lab_coat": ["实验服"],
            "gloves": ["丁腈手套"],
            "eye_protection": ["安全眼镜"],
            "face_shield": ["面罩（高危险操作）"],
            "respirator": ["防毒面具（必要时）"]
        }

    def _define_chemical_safety(self) -> List[str]:
        """定义化学品安全"""
        return [
            "阅读化学品安全技术说明书",
            "在通风橱中操作",
            "避免直接接触",
            "妥善储存",
            "泄漏处理"
        ]

    def _define_equipment_safety(self) -> List[str]:
        """定义设备安全"""
        return [
            "操作前检查",
            "遵守操作规程",
            "定期维护",
            "安全装置完好",
            "异常情况处理"
        ]

    def _define_emergency_contacts(self) -> Dict[str, str]:
        """定义紧急联系人"""
        return {
            "supervisor": "张三 - 138-0000-0000",
            "safety_officer": "李四 - 139-0000-0000",
            "hospital": "120",
            "fire": "119"
        }

    def _define_waste_disposal(self) -> List[str]:
        """定义废物处理"""
        return [
            "分类收集",
            "有害废物专门处理",
            "有机废物焚烧",
            "废水处理",
            "固体废物填埋"
        ]

    def _list_reference_standards(self) -> List[Dict[str, str]]:
        """列出参考标准"""
        return [
            {"standard": "GB 1886.123-2016", "name": "食品添加剂 茶多酚"},
            {"standard": "GB 16740-2010", "name": "保健食品通用标准"},
            {"standard": "ICH Q7", "name": "原料药 GMP 指南"}
        ]

    def _define_training_requirements(self) -> Dict[str, str]:
        """定义培训要求"""
        return {
            "safety_training": "入职培训",
            "equipment_training": "操作培训",
            "procedure_training": "SOP培训",
            "emergency_training": "应急培训",
            "renewal": "每年更新"
        }

    def _create_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """创建故障排除指南"""
        return {
            "common_issues": [
                "温度波动大",
                "pH值不稳定",
                "设备故障",
                "结果重现性差"
            ],
            "solutions": [
                "检查温控系统",
                "校准pH计",
                "联系维修",
                "优化实验设计"
            ]
        }


class ProcessDesignTool(BaseTool):
    """工艺设计工具"""
    name: str = "工艺设计工具"
    description: str = "设计工艺流程和参数"

    def _run(self, query: str) -> str:
        """工艺设计"""
        return f"工艺设计分析:\n{query[:500]}..."


class ParameterOptimizationTool(BaseTool):
    """参数优化工具"""
    name: str = "参数优化工具"
    description: str = "优化工艺参数"

    def _run(self, query: str) -> str:
        """参数优化"""
        return f"参数优化分析:\n{query[:500]}..."


class DesignOfExperimentsTool(BaseTool):
    """实验设计工具"""
    name: str = "实验设计工具"
    description: str = "设计实验方案（DOE）"

    def _run(self, query: str) -> str:
        """实验设计"""
        return f"实验设计分析:\n{query[:500]}..."


class SOPGenerationTool(BaseTool):
    """SOP生成工具"""
    name: str = "SOP生成工具"
    description: str = "生成标准操作流程"

    def _run(self, query: str) -> str:
        """SOP生成"""
        return f"SOP生成分析:\n{query[:500]}..."


class QualityControlTool(BaseTool):
    """质量控制工具"""
    name: str = "质量控制工具"
    description: str = "设计和执行质量控制"

    def _run(self, query: str) -> str:
        """质量控制"""
        return f"质量控制分析:\n{query[:500]}..."