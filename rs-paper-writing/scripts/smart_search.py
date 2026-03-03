#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能搜索引擎 - 根据章节类型调整搜索深度、提取关键概念、批量搜索
"""

import json
import re
from typing import List, Dict, Optional
from pathlib import Path

try:
    import subprocess
except ImportError:
    print("Error: subprocess module not available")
    exit(1)


class SmartSearch:
    """智能搜索引擎"""

    # 搜索策略配置
    SEARCH_STRATEGIES = {
        "abstract": {"depth": "light", "queries_per_concept": 1},
        "introduction": {"depth": "deep", "queries_per_concept": 3},
        "related_work": {"depth": "standard", "queries_per_concept": 2},
        "method": {"depth": "light", "queries_per_concept": 1},
        "experiment": {"depth": "light", "queries_per_concept": 1},
        "result": {"depth": "light", "queries_per_concept": 1},
        "discussion": {"depth": "standard", "queries_per_concept": 2},
        "conclusion": {"depth": "light", "queries_per_concept": 1},
        "other": {"depth": "light", "queries_per_concept": 1},
    }

    def __init__(self, skill_root: str = "."):
        self.skill_root = Path(skill_root)
        self.scripts_dir = self.skill_root / "scripts"

    def extract_key_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        提取关键概念

        Args:
            text: 文本内容
            max_concepts: 最多提取的概念数

        Returns:
            关键概念列表
        """
        # 简单的关键词提取（可以用更复杂的NLP方法）
        # 移除常见词
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "can", "this",
            "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
            "的", "了", "和", "是", "在", "有", "一", "个", "这", "那", "我", "你",
            "他", "她", "它", "们", "中", "上", "下", "左", "右", "前", "后"
        }

        # 分词
        words = re.findall(r'\b\w+\b', text.lower())

        # 过滤
        concepts = [w for w in words if w not in stop_words and len(w) > 2]

        # 统计频率
        from collections import Counter
        concept_freq = Counter(concepts)

        # 返回最频繁的概念
        return [concept for concept, _ in concept_freq.most_common(max_concepts)]

    def generate_search_queries(self, chapter_type: str, concepts: List[str]) -> List[str]:
        """
        生成搜索查询

        Args:
            chapter_type: 章节类型
            concepts: 关键概念列表

        Returns:
            搜索查询列表
        """
        strategy = self.SEARCH_STRATEGIES.get(chapter_type, self.SEARCH_STRATEGIES["other"])
        queries = []

        for concept in concepts:
            if strategy["depth"] == "deep":
                # 深度搜索：多个查询角度
                queries.extend([
                    concept,
                    f"{concept} review",
                    f"{concept} survey",
                    f"{concept} state of the art"
                ])
            elif strategy["depth"] == "standard":
                # 标准搜索：2个查询角度
                queries.extend([concept, f"{concept} method"])
            else:
                # 轻量搜索：1个查询
                queries.append(concept)

        # 限制查询数量
        max_queries = strategy["queries_per_concept"] * len(concepts)
        return queries[:max_queries]

    def search_references(self, query: str, limit: int = 5) -> List[Dict]:
        """
        搜索文献

        Args:
            query: 搜索查询
            limit: 返回结果数量

        Returns:
            搜索结果列表
        """
        try:
            # 调用s2_search.sh脚本
            result = subprocess.run(
                ["bash", str(self.scripts_dir / "s2_search.sh"), query, str(limit)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 解析结果
                try:
                    results = json.loads(result.stdout)
                    return results if isinstance(results, list) else []
                except json.JSONDecodeError:
                    return []
            else:
                print(f"Search error: {result.stderr}")
                return []

        except subprocess.TimeoutExpired:
            print(f"Search timeout for query: {query}")
            return []
        except Exception as e:
            print(f"Error searching references: {e}")
            return []

    def batch_search(self, queries: List[str], limit: int = 5) -> Dict[str, List[Dict]]:
        """
        批量搜索

        Args:
            queries: 搜索查询列表
            limit: 每个查询的返回结果数量

        Returns:
            {query: [results], ...}
        """
        results = {}

        for query in queries:
            print(f"Searching: {query}")
            search_results = self.search_references(query, limit)
            results[query] = search_results

        return results

    def evaluate_quality(self, reference: Dict) -> int:
        """
        评估文献质量（0-100分）

        Args:
            reference: 文献信息

        Returns:
            质量分数
        """
        score = 50  # 基础分

        # 引用量
        citations = reference.get("citationCount", 0)
        if citations > 1000:
            score += 30
        elif citations > 100:
            score += 20
        elif citations > 10:
            score += 10

        # 发表年份
        year = reference.get("year", 0)
        if year >= 2020:
            score += 15
        elif year >= 2015:
            score += 10
        elif year >= 2010:
            score += 5

        # 期刊/会议质量（如果有信息）
        venue = reference.get("venue", "")
        if any(top_venue in venue for top_venue in ["Nature", "Science", "IEEE", "ACM"]):
            score += 10

        return min(100, score)

    def rank_references(self, references: List[Dict]) -> List[Dict]:
        """
        按质量排序文献

        Args:
            references: 文献列表

        Returns:
            排序后的文献列表
        """
        # 为每个文献计算质量分数
        for ref in references:
            ref["quality_score"] = self.evaluate_quality(ref)

        # 按质量分数排序
        return sorted(references, key=lambda x: x.get("quality_score", 0), reverse=True)


def main():
    """测试"""
    search = SmartSearch()
    # 这里可以添加测试代码
    pass


if __name__ == "__main__":
    main()
