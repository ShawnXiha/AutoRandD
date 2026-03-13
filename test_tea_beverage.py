#!/usr/bin/env python3
"""
测试脚本 - 运行指定参数的研发项目
基于 USAGE_EXAMPLE.md 示例
"""

import asyncio
import os
from src.workflows.food_rd_workflow import run_food_rd_project

async def main():
    """运行测试 - 西湖龙井与安吉白茶混合拼配冷萃液的香气保留工艺"""
    research_goal = "西湖龙井与安吉白茶混合拼配冷萃液的香气保留工艺"
    funding = "20万元人民币"

    print(f"开始研发项目: {research_goal}")
    print(f"资金预算: {funding}")
    print("=" * 50)

    # 运行完整工作流
    result = await run_food_rd_project(
        research_goal=research_goal,
        funding=funding
    )

    print("=" * 50)
    print("研发项目完成！")
    print("\n执行状态:", result.get("status"))
    print("执行时间:", result.get("execution_date"))

    # 获取各个阶段的结果
    outputs = result.get("outputs", {})
    print("\n已生成的文档:")
    if "intelligence_report" in outputs:
        print("  ✓ 行业情报报告已生成")
    if "rd_plan" in outputs:
        print("  ✓ 研发计划书已生成")
    if "final_rd_plan" in outputs:
        print("  ✓ 最终版计划已生成")
    if "sop_document" in outputs:
        print("  ✓ 实验SOP已生成")
    if "simulation_report" in outputs:
        print("  ✓ 模拟数据报告已生成")
    if "final_report" in outputs:
        print("  ✓ 最终项目报告已生成")

    # 保存最终报告
    if "final_report" in outputs and outputs["final_report"]:
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"data/final_report_{timestamp}.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(outputs["final_report"])
            print(f"\n最终报告已保存到: {report_path}")
        except Exception as e:
            print(f"\n保存报告失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())