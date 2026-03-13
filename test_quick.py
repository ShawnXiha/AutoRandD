"""
快速测试脚本
Quick Test Script

用于快速测试系统基本功能，无需安装完整依赖
"""

import json
import os
from datetime import datetime

def test_basic_structure():
    """测试基本文件结构"""
    print("🧪 测试基本文件结构...")

    required_files = [
        "src/__init__.py",
        "src/agents/__init__.py",
        "src/agents/base_agent.py",
        "src/agents/industry_researcher.py",
        "src/tools/__init__.py",
        "src/tools/search_tools.py",
        "main.py",
        "requirements.txt",
        ".env.example"
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有基本文件都存在")
        return True

def test_imports():
    """测试导入功能（如果依赖已安装）"""
    print("\n📦 测试模块导入...")

    try:
        # 测试基本Python模块
        import json
        import os
        from datetime import datetime
        print("✅ 标准库导入成功")

        # 测试第三方库（如果已安装）
        try:
            import pandas as pd
            print("✅ pandas 导入成功")
        except ImportError:
            print("⚠️  pandas 未安装")

        try:
            import numpy as np
            print("✅ numpy 导入成功")
        except ImportError:
            print("⚠️  numpy 未安装")

        try:
            import rich
            print("✅ rich 导入成功")
        except ImportError:
            print("⚠️  rich 未安装")

        return True

    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def simulate_research_process():
    """模拟研究过程（无需调用实际模型）"""
    print("\n🔬 模拟研究过程...")

    # 模拟输入
    research_goal = "西湖龙井与安吉白茶混合拼配冷萃液的香气保留工艺"
    funding = "20万元"

    print(f"研发目标: {research_goal}")
    print(f"资金预算: {funding}")

    # 模拟生成一些简单的结果
    mock_results = {
        "intelligence_report": {
            "research_goal": research_goal,
            "funding": funding,
            "key_findings": [
                "龙井茶以清香型为主，安吉白茶以毫香型为主",
                "冷萃工艺能更好地保留茶叶香气",
                "混合拼配可以创造独特的风味 profile"
            ],
            "technical_challenges": [
                "香气成分稳定性",
                "工艺参数优化",
                "质量控制标准"
            ]
        },
        "rd_plan": {
            "project_duration": "6个月",
            "budget_allocation": {
                "equipment": "40%",
                "materials": "30%",
                "personnel": "20%",
                "testing": "10%"
            }
        },
        "final_report": {
            "conclusions": [
                "成功优化了冷萃工艺参数",
                "香气保留率达到85%以上",
                "产品质量稳定可靠"
            ]
        }
    }

    # 保存模拟结果
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"mock_results_{timestamp}.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mock_results, f, ensure_ascii=False, indent=2)

    print(f"✅ 模拟结果已保存到: {output_file}")
    return True

def show_usage_guide():
    """显示使用指南"""
    print("\n" + "="*60)
    print("📖 使用指南")
    print("="*60)

    print("""
要完整运行本系统，请按以下步骤操作：

1. 安装 Python 依赖：
   pip install -r requirements.txt

   或者使用 conda：
   conda install -c conda-forge pandas numpy scipy requests
   pip install crewai crewai-tools langchain-community rich

2. 安装并启动 Ollama：
   # 安装 Ollama（根据操作系统）
   # macOS: curl -fsSL https://ollama.com/install.sh | sh
   # Linux: curl -fsSL https://ollama.com/install.sh | sh
   # Windows: 下载安装包

3. 启动 Ollama 服务：
   ollama serve

4. 下载模型：
   ollama pull qwen3.5:cloud

5. 运行系统：
   python main.py

6. 输入测试案例：
   研发目标: 西湖龙井与安吉白茶混合拼配冷萃液的香气保留工艺
   资金预算: 20万元
    """)

def main():
    """主函数"""
    print("🍎 食品与生工领域多智能体研发系统 - 快速测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 运行测试
    tests = [
        ("基本结构", test_basic_structure),
        ("模块导入", test_imports),
        ("模拟研究", simulate_research_process)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试出错: {str(e)}")
            results.append((test_name, False))

    # 显示汇总
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 基本测试通过！")
        show_usage_guide()
    else:
        print("\n⚠️  部分测试失败，请检查安装。")

if __name__ == "__main__":
    main()