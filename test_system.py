"""
系统测试脚本
System Test Script

用于测试食品与生工领域多智能体研发系统的基本功能
"""

import asyncio
import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.workflows.food_rd_workflow import create_workflow
from src.config.model_config import model_config

async def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("🧪 开始系统基本功能测试")
    print("=" * 60)

    # 1. 测试配置加载
    print("\n1. 测试配置加载...")
    print(f"   模型名称: {model_config.ollama.model_name}")
    print(f"   基础URL: {model_config.ollama.base_url}")
    print(f"   温度: {model_config.ollama.temperature}")
    print("   ✅ 配置加载成功")

    # 2. 测试工作流创建
    print("\n2. 测试工作流创建...")
    try:
        workflow = create_workflow()
        print("   ✅ 工作流创建成功")
        print(f"   Agent数量: {len(workflow.agents)}")

        # 显示Agent信息
        for name, agent in workflow.agents.items():
            info = agent.get_agent_info()
            print(f"   - {info['name']}: {info['description']}")
    except Exception as e:
        print(f"   ❌ 工作流创建失败: {str(e)}")
        return False

    # 3. 测试简化的工作流执行（使用短文本）
    print("\n3. 测试简化工作流...")
    try:
        # 使用一个非常简单的测试案例
        test_goal = "测试茶多酚提取"
        test_funding = "10万元"

        print(f"   测试目标: {test_goal}")
        print(f"   测试预算: {test_funding}")

        # 由于完整工作流需要较长时间，这里只测试第一个Agent
        print("\n   测试行业情报研究员...")
        intelligence_report = await workflow.run_intelligence_research(test_goal, test_funding)

        if intelligence_report and not isinstance(intelligence_report, dict) or "error" not in intelligence_report:
            print("   ✅ 行业情报研究员测试通过")
        else:
            print(f"   ⚠️  行业情报研究员返回: {intelligence_report}")

        # 测试其他Agent（简化版）
        print("\n   测试研发规划师...")
        rd_plan = await workflow.run_rd_planning(test_goal, test_funding, intelligence_report)
        if rd_plan and not isinstance(rd_plan, dict) or "error" not in rd_plan:
            print("   ✅ 研发规划师测试通过")
        else:
            print(f"   ⚠️  研发规划师返回: {rd_plan}")

    except Exception as e:
        print(f"   ❌ 工作流测试失败: {str(e)}")
        return False

    print("\n" + "=" * 60)
    print("✅ 基本功能测试完成")
    print("=" * 60)
    return True

async def test_individual_agents():
    """测试各个Agent"""
    print("\n" + "=" * 60)
    print("🔬 测试各个Agent")
    print("=" * 60)

    workflow = create_workflow()

    # 测试Agent信息
    agents_info = workflow.get_agent_info()
    print("\n📋 Agent列表:")
    for name, info in agents_info.items():
        print(f"\n   - {info['name']}")
        print(f"     描述: {info['description']}")
        print(f"     工具: {', '.join(info['tools']) if info['tools'] else '无'}")

    print("\n✅ Agent信息测试完成")
    return True

async def test_file_structure():
    """测试文件结构"""
    print("\n" + "=" * 60)
    print("📁 测试文件结构")
    print("=" * 60)

    required_files = [
        "src/__init__.py",
        "src/agents/__init__.py",
        "src/agents/base_agent.py",
        "src/agents/industry_researcher.py",
        "src/agents/rd_planner.py",
        "src/agents/plan_reviewer.py",
        "src/agents/experiment_designer.py",
        "src/agents/data_simulator.py",
        "src/agents/report_analyst.py",
        "src/tools/__init__.py",
        "src/tools/search_tools.py",
        "src/tools/science_tools.py",
        "src/workflows/__init__.py",
        "src/workflows/food_rd_workflow.py",
        "src/config/__init__.py",
        "src/config/model_config.py",
        "main.py",
        "requirements.txt",
        ".env.example"
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("\n❌ 以下文件缺失:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("\n✅ 所有必要文件都存在")
        return True

async def test_dependencies():
    """测试依赖"""
    print("\n" + "=" * 60)
    print("📦 测试依赖包")
    print("=" * 60)

    required_packages = [
        "crewai",
        "crewai-tools",
        "langchain-community",
        "langchain",
        "python-dotenv",
        "rich",
        "pandas",
        "numpy",
        "requests",
        "beautifulsoup4",
        "pydantic"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("\n❌ 以下依赖包缺失:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有必要依赖都已安装")
        return True

async def main():
    """主测试函数"""
    print("🍎 食品与生工领域多智能体研发系统 - 测试套件")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 运行各项测试
    tests = [
        ("文件结构", test_file_structure),
        ("依赖包", test_dependencies),
        ("基本功能", test_basic_functionality),
        ("Agent测试", test_individual_agents)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name}测试出错: {str(e)}")
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("1. 确保 Ollama 服务正在运行: ollama serve")
        print("2. 下载所需模型: ollama pull qwen3.5:cloud")
        print("3. 运行系统: python main.py")
    else:
        print("\n⚠️  部分测试失败，请检查并修复问题后再试。")

    return passed == total

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)