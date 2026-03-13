#!/usr/bin/env python3
"""
测试脚本 - 运行指定参数的研发项目
"""

import asyncio
import os
from src.workflows.food_rd_workflow import run_food_rd_project

async def main():
    """运行测试"""
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
    print("\n最终报告预览:")
    print("-" * 30)
    print(result.get("final_report", "")[:1000] + "..." if len(result.get("final_report", "")) > 1000 else result.get("final_report", ""))

if __name__ == "__main__":
    asyncio.run(main())