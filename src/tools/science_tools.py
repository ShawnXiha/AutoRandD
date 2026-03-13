"""
科学专业工具模块
Scientific Professional Tools Module

提供食品科学和生物工程领域的专业搜索和分析工具
"""

from typing import List, Dict, Any, Optional
import requests
import json
import os
from datetime import datetime, timedelta


class PubMedSearchTool:
    """PubMed 学术文献搜索工具"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        搜索 PubMed 文献

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            文献列表
        """
        try:
            # esearch 请求
            search_url = f"{self.base_url}/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json",
                "api_key": self.api_key
            }

            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            ids = data.get("esearchresult", {}).get("idlist", [])
            if not ids:
                return []

            # efetch 获取详细信息
            fetch_url = f"{self.base_url}/efetch.fcgi"
            params = {
                "db": "pubmed",
                "id": ",".join(ids),
                "rettype": "medline",
                "retmode": "text"
            }

            response = requests.get(fetch_url, params=params)
            response.raise_for_status()

            # 解析 MEDLINE 格式
            records = self._parse_medline(response.text)
            return records

        except Exception as e:
            print(f"PubMed 搜索错误: {e}")
            return []

    def _parse_medline(self, text: str) -> List[Dict[str, Any]]:
        """解析 MEDLINE 格式文本"""
        records = []
        current_record = {}
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                if current_record:
                    records.append(current_record)
                    current_record = {}
                continue

            if line.startswith("PMID- "):
                current_record["pmid"] = line[6:]
            elif line.startswith("TI  "):
                current_record["title"] = line[5:]
            elif line.startswith("AU  "):
                if "authors" not in current_record:
                    current_record["authors"] = []
                current_record["authors"].append(line[5:])
            elif line.startswith("JT  "):
                current_record["journal"] = line[5:]
            elif line.startswith("DP  "):
                current_record["date"] = line[5:]
            elif line.startswith("AB  "):
                current_record["abstract"] = line[5:]

        if current_record:
            records.append(current_record)

        return records


class PatentSearchTool:
    """专利搜索工具（Google Patents API）"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_PATENTS_API_KEY")

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索专利

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            专利列表
        """
        if not self.api_key:
            print("Google Patents API Key 未设置，返回模拟数据")
            return self._get_mock_patents(query)

        try:
            url = "https://patent.googleapis.com/v1/patents/search"
            params = {
                "q": query,
                "maxResults": max_results,
                "apiKey": self.api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            patents = []
            for item in data.get("results", []):
                patent = {
                    "publication_number": item.get("publicationNumber", ""),
                    "title": item.get("title", ""),
                    "abstract": item.get("abstract", ""),
                    "assignee": item.get("assignee", ""),
                    "filing_date": item.get("filingDate", ""),
                    "grant_date": item.get("grantDate", ""),
                    "inventors": [inv.get("name", "") for inv in item.get("inventors", [])],
                    "cpc_classifications": [cp.get("code", "") for cp in item.get("cpcClassifications", [])],
                    "url": f"https://patents.google.com/patent/{item.get('publicationNumber', '')}"
                }
                patents.append(patent)

            return patents

        except Exception as e:
            print(f"专利搜索错误: {e}")
            return self._get_mock_patents(query)

    def _get_mock_patents(self, query: str) -> List[Dict[str, Any]]:
        """生成模拟专利数据"""
        mock_patents = [
            {
                "publication_number": "CN1234567A",
                "title": f"基于{query}的新型食品加工工艺",
                "abstract": "本发明涉及一种新型食品加工工艺，通过...",
                "assignee": "某食品科技有限公司",
                "filing_date": "2023-01-15",
                "grant_date": "2023-12-20",
                "inventors": ["张三", "李四"],
                "cpc_classifications": ["A23L33/10", "A23L33/125"],
                "url": "https://patents.google.com/patent/CN1234567A"
            },
            {
                "publication_number": "CN987654B",
                "title": f"{query}的制备方法及其应用",
                "abstract": "本公开提供了一种{query}的制备方法...",
                "assignee": "某生物工程研究院",
                "filing_date": "2022-05-10",
                "grant_date": "2023-08-15",
                "inventors": ["王五", "赵六"],
                "cpc_classifications": ["C07C209/00", "A61K31/00"],
                "url": "https://patents.google.com/patent/CN987654B"
            }
        ]
        return mock_patents


class ScienceDataAnalyzer:
    """科学数据分析工具"""

    @staticmethod
    def analyze_experimental_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析实验数据

        Args:
            data: 实验数据列表

        Returns:
            分析结果
        """
        try:
            import statistics
            import numpy as np

            # 提取数值数据
            values = []
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, (int, float)):
                            values.append(value)

            if not values:
                return {"error": "No numerical data found"}

            # 计算统计指标
            result = {
                "count": len(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std": statistics.stdev(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values),
                "q25": np.percentile(values, 25),
                "q75": np.percentile(values, 75),
            }

            return result

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_correlation(x: List[float], y: List[float]) -> Dict[str, Any]:
        """
        计算两个变量间的相关性

        Args:
            x: 变量 x 的值
            y: 变量 y 的值

        Returns:
            相关性分析结果
        """
        try:
            import statistics
            from scipy import stats

            if len(x) != len(y) or len(x) < 2:
                return {"error": "Invalid data length"}

            # 计算皮尔逊相关系数
            pearson_r, pearson_p = stats.pearsonr(x, y)

            # 计算斯皮尔曼相关系数
            spearman_r, spearman_p = stats.spearmanr(x, y)

            result = {
                "pearson_correlation": pearson_r,
                "pearson_p_value": pearson_p,
                "spearman_correlation": spearman_r,
                "spearman_p_value": spearman_p,
                "interpretation": ScienceDataAnalyzer._interpret_correlation(pearson_r)
            }

            return result

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _interpret_correlation(r: float) -> str:
        """解释相关系数"""
        abs_r = abs(r)
        if abs_r >= 0.8:
            return "极强相关"
        elif abs_r >= 0.6:
            return "强相关"
        elif abs_r >= 0.4:
            return "中等相关"
        elif abs_r >= 0.2:
            return "弱相关"
        else:
            return "极弱相关"


class FoodScienceDatabase:
    """食品科学数据库工具"""

    @staticmethod
    def get_food_ingredients(food_name: str) -> Dict[str, Any]:
        """
        获取食品成分信息

        Args:
            food_name: 食品名称

        Returns:
            成分信息
        """
        # 模拟数据库
        food_database = {
            "茶多酚": {
                "chemical_formula": "C17H22O11",
                "molecular_weight": 346.34,
                "solubility": "可溶于热水、乙醇",
                "stability": "pH 3-7稳定，高温易分解",
                "functions": ["抗氧化剂", "防腐剂", "风味增强剂"],
                "applications": ["饮料", "糖果", "保健品"]
            },
            "蛋白质": {
                "chemical_formula": "Variable",
                "molecular_weight": "10-1000 kDa",
                "solubility": "溶于水、稀盐溶液",
                "stability": "60-80°C开始变性",
                "functions": ["营养", "乳化", "起泡"],
                "applications": ["肉制品", "乳制品", "烘焙"]
            }
        }

        return food_database.get(food_name, {
            "error": "Food ingredient not found in database"
        })

    @staticmethod
    def get_processing_parameters(process_type: str) -> Dict[str, Any]:
        """
        获取加工工艺参数

        Args:
            process_type: 加工类型

        Returns:
            工艺参数
        """
        process_database = {
            "均质": {
                "temperature": "60-80°C",
                "pressure": "20-40 MPa",
                "time": "5-30 min",
                "equipment": "高压均质机",
                "key_parameters": ["压力", "温度", "循环次数"]
            },
            "萃取": {
                "temperature": "40-80°C",
                "solvent_ratio": "1:5-1:20",
                "time": "30-120 min",
                "equipment": "提取罐",
                "key_parameters": ["温度", "时间", "料液比", "pH值"]
            },
            "干燥": {
                "temperature": "40-60°C",
                "humidity": "10-30%",
                "time": "6-24 h",
                "equipment": "烘箱、喷雾干燥机",
                "key_parameters": ["温度", "风速", "湿度"]
            }
        }

        return process_database.get(process_type, {
            "error": "Process type not found in database"
        })


# 导出工具实例
pubmed_search = PubMedSearchTool()
patent_search = PatentSearchTool()
science_analyzer = ScienceDataAnalyzer()
food_database = FoodScienceDatabase()