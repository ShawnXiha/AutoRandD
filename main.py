"""
食品与生工领域多智能体研发模拟系统
Food & Bioengineering R&D Multi-Agent Simulation System

主程序入口 - 使用 CrewAI 和 Ollama 构建的专业研发系统
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown

from src.workflows.food_rd_workflow import create_workflow, run_food_rd_project
from src.config.model_config import model_config

# 初始化 Rich 控制台
console = Console()

# 加载环境变量
load_dotenv()


def display_welcome():
    """显示欢迎界面"""
    welcome_text = """
# 🍎 食品与生工领域多智能体研发模拟系统

## 🚀 系统简介
本系统采用 CrewAI 框架，集成了 6 个专业智能体，为您提供完整的食品与生物工程研发解决方案。
当前默认模型：{model_config.ollama.model_name}

## 🤖 系统架构
- **行业情报研究员**: 搜集行业信息，分析技术难点
- **首席研发规划师**: 制定研发计划，配置资源
- **方案评审专家**: 评估方案可行性，优化改进
- **实验设计与操作员**: 设计实验方案，制定SOP
- **实验数据模拟器**: 模拟实验过程，生成数据
- **报告总结分析师**: 整合成果，生成报告

## 🎯 工作流程
1. 行业情报研究 → 2. 研发规划 → 3. 方案评审 →
4. 实验设计 → 5. 数据模拟 → 6. 报告生成
"""
    console.print(Panel(Markdown(welcome_text), title="🌟 欢迎使用", expand=False))


def display_agent_info():
    """显示Agent信息"""
    workflow = create_workflow()
    agents = workflow.get_agent_info()

    table = Table(title="🤖 系统智能体")
    table.add_column("Agent名称", style="cyan", no_wrap=True)
    table.add_column("角色描述", style="magenta")
    table.add_column("专业领域", style="green")

    for agent_name, info in agents.items():
        table.add_row(
            info["name"],
            info["description"],
            ", ".join(info["tools"]) if info["tools"] else "通用",
        )

    console.print(table)


async def run_interactive_mode():
    """运行交互模式"""
    # 获取用户输入
    console.print("\n📝 请输入您的研发需求：")

    research_goal = console.input("\n[bold blue]1. 研发目标:[/] ").strip()
    if not research_goal:
        console.print("❌ 研发目标不能为空！")
        return

    funding = console.input("\n[bold blue]2. 资金预算:[/] ").strip()
    if not funding:
        console.print("❌ 资金预算不能为空！")
        return

    model_hint = console.input(
        "\n[bold blue]3. 模型(可选, glm/kimi/qwen/具体模型名):[/] "
    ).strip()
    selected_model = model_hint if model_hint else model_config.ollama.model_name

    console.print(f"\n🎯 开始执行研发项目...")
    console.print(f"   研发目标: {research_goal}")
    console.print(f"   资金预算: {funding}")
    console.print(f"   模型配置: {selected_model}")
    console.print("")

    # 运行工作流
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在执行研发流程...", total=None)

        try:
            result = await run_food_rd_project(
                research_goal,
                funding,
                model_name=selected_model,
            )
            progress.update(task, description="✅ 研发项目执行完成")

            # 显示结果摘要
            display_results_summary(result)

        except Exception as e:
            progress.update(task, description=f"❌ 执行失败: {str(e)}")
            console.print(f"\n❌ 工作流执行失败: {str(e)}")


def display_results_summary(result: dict):
    """显示结果摘要"""
    console.print("\n" + "=" * 60)
    console.print("🎉 研发项目执行完成！", style="bold green")
    console.print("=" * 60)

    # 显示执行状态
    status = result.get("status", "unknown")
    if status == "completed":
        console.print("✅ 所有阶段执行成功", style="green")
    else:
        console.print("⚠️  部分阶段执行出现问题", style="yellow")

    # 显示生成的文档
    outputs = result.get("outputs", {})
    if outputs:
        console.print("\n📄 生成的文档:")
        for doc_type, doc_data in outputs.items():
            if "error" not in doc_data:
                console.print(f"   ✅ {doc_type}: data/{doc_type}_*.json")
            else:
                console.print(f"   ❌ {doc_type}: 执行失败 - {doc_data['error']}")

    # 显示执行时间
    execution_date = result.get("execution_date", "")
    if execution_date:
        exec_time = datetime.fromisoformat(execution_date).strftime("%Y-%m-%d %H:%M:%S")
        console.print(f"\n⏰ 执行时间: {exec_time}")

    console.print("\n" + "=" * 60)


def display_help():
    """显示帮助信息"""
    help_text = """
## 📖 使用说明

### 快速开始
```bash
python main.py
```

### 系统要求
- Python 3.8+
- Ollama 服务 (http://localhost:11434)
- CrewAI 和相关依赖

### 配置说明
在 `.env` 文件中设置以下参数：
```
OLLAMA_MODEL=qwen3.5:cloud
MODEL_PROFILE=glm
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=4000
```

可用别名：`glm`→`glm-5:cloud`，`kimi`→`kimi-k2:latest`，`qwen`→`qwen3.5:cloud`

### 输入参数
1. **研发目标**: 具体的研发项目描述
   - 示例: "研发一款具有清新口气功能的茶多酚爆珠"
   - 示例: "冷加工蛋白棒的成型工艺优化"

2. **资金预算**: 项目资金预算
   - 示例: "50万元人民币"
   - 示例: "100万人民币"

### 输出文档
系统将生成以下文档：
1. 行业情报报告 (.json)
2. 研发计划书 (.json)
3. 最终版研发计划 (.json)
4. 实验操作SOP (.json)
5. 模拟实验数据 (.json)
6. 最终项目报告 (.md)
"""
    console.print(Panel(Markdown(help_text), title="📖 帮助信息", expand=False))


async def main():
    """主函数"""
    display_welcome()

    while True:
        console.print("\n" + "=" * 50)
        console.print("🔧 主菜单", style="bold blue")
        console.print("=" * 50)

        choices = [
            ("开始新的研发项目", "1"),
            ("查看系统信息", "2"),
            ("显示帮助信息", "3"),
            ("退出系统", "4"),
        ]

        for choice, key in choices:
            console.print(f"[{key}] {choice}")

        action = console.input("\n请选择操作 (1-4): ").strip()

        if action == "1":
            await run_interactive_mode()
        elif action == "2":
            display_agent_info()
        elif action == "3":
            display_help()
        elif action == "4":
            console.print("👋 感谢使用，再见！")
            break
        else:
            console.print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    asyncio.run(main())
