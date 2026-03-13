# 📖 使用示例

## 快速开始示例

### 示例1：茶多酚爆珠研发项目

```bash
python main.py
```

根据提示输入：
```
研发目标: 研发一款具有清新口气功能的茶多酚爆珠
资金预算: 50万元人民币
```

### 示例2：蛋白棒工艺优化

```bash
python main.py
```

根据提示输入：
```
研发目标: 冷加工蛋白棒的成型工艺优化
资金预算: 80万元人民币
```

## 编程方式调用示例

```python
import asyncio
from src.workflows.food_rd_workflow import run_food_rd_project

async def example_tea_polyphenol():
    """茶多酚爆珠研发示例"""
    result = await run_food_rd_project(
        research_goal="研发一款具有清新口气功能的茶多酚爆珠",
        funding="50万元人民币"
    )

    # 查看结果
    print("执行状态:", result.get("status"))
    print("执行时间:", result.get("execution_date"))

    # 获取各个阶段的结果
    outputs = result.get("outputs", {})
    if "intelligence_report" in outputs:
        print("情报报告已生成")
    if "final_report" in outputs:
        print("最终报告已生成")

# 运行示例
asyncio.run(example_tea_polyphenol())
```

## 高级用法示例

### 自定义工作流

```python
from src.workflows.food_rd_workflow import FoodRDWorkflow
import asyncio

async def custom_workflow_example():
    # 创建工作流实例
    workflow = FoodRDWorkflow()

    # 分步执行（可以单独使用某个阶段）

    # 1. 只进行行业情报研究
    intelligence_report = await workflow.run_intelligence_research(
        "茶多酚提取工艺优化",
        "30万元"
    )
    print("情报研究完成")

    # 2. 只进行实验设计
    sop_document = await workflow.run_experiment_design(
        "茶多酚提取工艺优化",
        {"final_plan": "简化版计划"}
    )
    print("实验设计完成")

asyncio.run(custom_workflow_example())
```

### 批量处理多个项目

```python
import asyncio
from src.workflows.food_rd_workflow import run_food_rd_project

async def batch_processing():
    """批量处理多个研发项目"""

    projects = [
        {
            "goal": "茶多酚口腔崩解片研发",
            "funding": "40万元"
        },
        {
            "goal": "益生菌蛋白棒工艺优化",
            "funding": "60万元"
        },
        {
            "goal": "功能性果蔬脆片开发",
            "funding": "50万元"
        }
    ]

    results = []

    for project in projects:
        print(f"\n开始处理: {project['goal']}")
        result = await run_food_rd_project(project['goal'], project['funding'])
        results.append({
            "project": project['goal'],
            "result": result
        })

    # 汇总结果
    successful = [r for r in results if r['result'].get('status') == 'completed']
    print(f"\n完成 {len(successful)}/{len(projects)} 个项目")

asyncio.run(batch_processing())
```

## 输出文档示例

### 行业情报报告片段
```json
{
  "document_type": "行业情报研究报告",
  "research_goal": "研发一款具有清新口气功能的茶多酚爆珠",
  "key_findings": [
    "茶多酚具有天然的抗菌作用",
    "口香糖市场规模达到50亿元",
    "功能性食品增长迅速"
  ],
  "technical_challenges": [
    {
      "challenge": "茶多酚稳定性问题",
      "solution": "采用微胶囊包埋技术"
    }
  ]
}
```

### 实验SOP片段
```json
{
  "document_type": "实验操作标准指南",
  "process_parameters": {
    "temperature_control": [
      {
        "parameter": "提取温度",
        "range": "60-80°C",
        "accuracy": "±0.5°C",
        "control_method": "恒温水浴锅"
      }
    ],
    "time_control": [
      {
        "parameter": "提取时间",
        "range": "30-60 min",
        "accuracy": "±1 min",
        "control_method": "定时器"
      }
    ]
  }
}
```

### 最终报告片段（Markdown）
```markdown
# 研发项目结题报告

## 执行摘要
本项目成功开发了具有清新口气功能的茶多酚爆珠产品，通过优化提取工艺和配方设计，产品各项指标均达到预期目标。

## 主要成果
- 提取率达到92.5%
- 产品纯度达到98.2%
- 生产成本降低15%
- 申请专利2项

## 未来展望
建议进一步开展工业化放大试验，完善质量控制体系，为市场推广做好准备。
```

## 故障排除

### 常见问题

1. **Ollama连接失败**
   ```
   确保Ollama服务正在运行:
   ollama serve
   ```

2. **模型下载失败**
   ```
   重新下载模型:
   ollama pull qwen3.5:cloud
   ```

3. **依赖包缺失**
   ```
   安装所有依赖:
   pip install -r requirements.txt
   ```

4. **内存不足**
   - 关闭其他占用内存的程序
   - 考虑使用swap空间

### 性能优化

1. **并行处理**
   - 使用多台机器
   - 调整并发数

2. **缓存优化**
   - 缓存搜索结果
   - 复用计算结果

3. **资源管理**
   - 监控内存使用
   - 及时清理临时文件

## 最佳实践

1. **输入描述要详细**
   - 明确技术指标
   - 说明质量要求
   - 提供参考标准

2. **预算要合理**
   - 参考市场价格
   - 预留备用资金
   - 考虑设备投入

3. **及时保存结果**
   - 定期备份文档
   - 保存重要数据
   - 记录实验过程

---

通过这些示例，您可以快速上手使用本系统，并根据实际需求进行定制和扩展。