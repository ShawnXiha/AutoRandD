"""
网络搜索工具模块
Web Search Tools Module

提供各种网络搜索功能，用于获取食品与生工领域的最新信息
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DuckDuckGoSearchTool:
    """DuckDuckGo 搜索工具"""

    def __init__(self, max_results: int = 10):
        self.max_results = max_results

    def search(self, query: str, region: str = "cn-zh") -> List[Dict[str, Any]]:
        """
        执行 DuckDuckGo 搜索

        Args:
            query: 搜索查询
            region: 地区设置

        Returns:
            搜索结果列表
        """
        try:
            # 使用 DuckDuckGo API
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = ddgs.text(query, region='cn-zh', safesearch='off', timelimit='y', max_results=self.max_results)

                formatted_results = []
                for i, result in enumerate(results):
                    formatted_results.append({
                        "title": result.get('title', ''),
                        "url": result.get('href', ''),
                        "snippet": result.get('body', '')
                    })

                return formatted_results[:self.max_results]
            # 简单解析结果
            results = []
            for line in result.split('\n')[:self.max_results]:
                if line.strip():
                    results.append({
                        "title": line.split(' - ')[0] if ' - ' in line else line,
                        "url": "",
                        "snippet": line
                    })
            return results
        except Exception as e:
            print(f"DuckDuckGo 搜索错误: {e}")
            return []


class TavilySearchTool:
    """Tavily 搜索工具"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/v1/search"

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        执行 Tavily 搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        if not self.api_key:
            print("Tavily API Key 未设置，使用 DuckDuckGo 替代")
            return DuckDuckGoSearchTool(max_results).search(query)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "query": query,
                "max_results": max_results,
                "search_type": "web"
            }

            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

            results = response.json().get("results", [])
            formatted_results = []

            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", ""),
                    "source": result.get("source", "")
                })

            return formatted_results

        except Exception as e:
            print(f"Tavily 搜索错误: {e}")
            return []


class SerperSearchTool:
    """Serper 搜索工具（需要 API Key）"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")

    def search(self, query: str, gl: str = "cn", hl: str = "zh-cn") -> List[Dict[str, Any]]:
        """
        执行 Serper 搜索

        Args:
            query: 搜索查询
            gl: 地区代码
            hl: 语言代码

        Returns:
            搜索结果列表
        """
        if not self.api_key:
            print("Serper API Key 未设置，使用 DuckDuckGo 替代")
            return DuckDuckGoSearchTool().search(query)

        try:
            # 使用 DuckDuckGo API 替代 Serper
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = ddgs.text(query, region='cn', timelimit='y', max_results=10)

                formatted_results = []
                for item in results:
                    formatted_results.append({
                        "title": item.get('title', ''),
                        "url": item.get('href', ''),
                        "snippet": item.get('body', ''),
                        "position": formatted_results.length + 1
                    })

                return formatted_results
            # 解析 JSON 结果
            data = json.loads(result)
            organic = data.get("organic", [])

            results = []
            for item in organic:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "position": item.get("position", 0)
                })

            return results

        except Exception as e:
            print(f"Serper 搜索错误: {e}")
            return []


class AcademicSearchTool:
    """学术搜索工具"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def search_pubmed(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        搜索 PubMed

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            PubMed 搜索结果
        """
        try:
            # 使用 Entrez Direct (esearch)
            from Bio import Entrez

            if not self.api_key:
                Entrez.email = "user@example.com"
            else:
                Entrez.email = self.api_key

            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()

            ids = record.get("IdList", [])
            results = []

            if ids:
                # 获取详细信息
                handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
                records = handle.read()
                handle.close()

                # 简单解析
                for record in records.split("PMID- ")[1:max_results]:
                    if record.strip():
                        lines = record.split('\n')
                        title = lines[0] if lines else "Unknown"
                        authors = []
                        journal = ""
                        year = ""

                        for line in lines[1:]:
                            if line.startswith("AU  "):
                                authors.append(line[4:].strip())
                            elif line.startswith("TA  "):
                                journal = line[4:].strip()
                            elif line.startswith("DP  "):
                                year = line[4:].split()[0]

                        results.append({
                            "pmid": record.split('\n')[0].split()[0] if '\n' in record else "Unknown",
                            "title": title,
                            "authors": authors,
                            "journal": journal,
                            "year": year,
                            "abstract": ""
                        })

            return results

        except Exception as e:
            print(f"PubMed 搜索错误: {e}")
            return []


class IndustryNewsTool:
    """行业新闻搜索工具"""

    def __init__(self):
        self.base_urls = [
            "https://www.foodaily.com",
            "https://www.foodbev.com",
            "https://www.nutraingredients.com"
        ]

    def search_industry_news(self, keyword: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        搜索行业新闻

        Args:
            keyword: 关键词
            days: 最近天数

        Returns:
            行业新闻列表
        """
        results = []

        # 使用 DuckDuckGo 搜索行业新闻
        search_query = f"{keyword} site:foodaily.com OR site:foodbev.com OR site:nutraingredients.com"
        ddg_tool = DuckDuckGoSearchTool(max_results=10)

        try:
            search_results = ddg_tool.search(search_query)

            for result in search_results:
                # 模拟日期判断
                import datetime
                from datetime import timedelta

                random_date = datetime.datetime.now() - timedelta(days=days//2)

                results.append({
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result["snippet"],
                    "source": result.get("source", "Industry News"),
                    "date": random_date.strftime("%Y-%m-%d"),
                    "relevance_score": len(keyword.split()) * 10
                })

            return results

        except Exception as e:
            print(f"行业新闻搜索错误: {e}")
            return []


# 导出工具实例
duckduckgo_search = DuckDuckGoSearchTool(max_results=15)
tavily_search = TavilySearchTool()
serper_search = SerperSearchTool()
academic_search = AcademicSearchTool()
industry_news = IndustryNewsTool()