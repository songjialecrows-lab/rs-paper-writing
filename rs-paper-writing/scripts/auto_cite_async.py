#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步引用补全主程序 - 后台处理论文、自动搜索文献、补全引用
"""

import sys
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import Dict

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from chapter_analyzer import ChapterAnalyzer, ChapterType
from task_manager import TaskManager
from smart_search import SmartSearch
from citation_inserter import CitationInserter

try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed")
    exit(1)


class AsyncCiteProcessor:
    """异步引用补全处理器"""

    def __init__(self, skill_root: str = "."):
        self.skill_root = Path(skill_root)
        self.chapter_analyzer = ChapterAnalyzer()
        self.task_manager = TaskManager(str(self.skill_root / "data" / "task_storage"))
        self.smart_search = SmartSearch(str(self.skill_root))
        self.citation_inserter = CitationInserter()

    def process(self, task_id: str, input_file: str) -> bool:
        """
        处理论文，补全引用

        Args:
            task_id: 任务ID
            input_file: 输入文件路径

        Returns:
            是否成功
        """
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始处理任务: {task_id}")

            # 第1步：启动任务
            self.task_manager.start_task(task_id)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 任务已启动")

            # 第2步：分析论文结构
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 分析论文结构...")
            chapters = self.chapter_analyzer.analyze_document(input_file)
            if not chapters:
                raise Exception("Failed to analyze document")

            print(f"[{datetime.now().strftime('%H:%M:%S')}] 识别到 {len(chapters)} 个章节")

            # 获取搜索优先级
            priority_chapters = self.chapter_analyzer.get_search_priority()

            # 第3步：按优先级处理每个章节
            all_citations = {}
            total_citations_found = 0

            for chapter, priority in priority_chapters:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 处理章节: {chapter.name} (优先级: {priority})")

                # 提取关键概念
                concepts = self.smart_search.extract_key_concepts(chapter.content)
                print(f"  提取关键概念: {concepts[:5]}...")

                # 生成搜索查询
                queries = self.smart_search.generate_search_queries(
                    chapter.type.value,
                    concepts
                )
                print(f"  生成 {len(queries)} 个搜索查询")

                # 批量搜索
                search_results = self.smart_search.batch_search(queries, limit=5)

                # 合并和排序结果
                chapter_citations = {}
                for query, results in search_results.items():
                    ranked_results = self.smart_search.rank_references(results)
                    for result in ranked_results[:3]:  # 每个查询取前3个
                        key = result.get("paperId", f"ref_{len(chapter_citations)}")
                        if key not in chapter_citations:
                            chapter_citations[key] = result
                            total_citations_found += 1

                all_citations.update(chapter_citations)

                # 更新进度
                progress = int((priority_chapters.index((chapter, priority)) + 1) / len(priority_chapters) * 100)
                self.task_manager.update_progress(
                    task_id,
                    progress,
                    {
                        chapter.name: {
                            "status": "completed",
                            "citations_found": len(chapter_citations),
                            "total_citations": chapter.get_estimated_citations()
                        }
                    }
                )

                print(f"  找到 {len(chapter_citations)} 个引用 (进度: {progress}%)")

            # 第4步：生成输出文件
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 生成输出文件...")
            output_file = self._generate_output(input_file, all_citations)

            # 第5步：完成任务
            self.task_manager.complete_task(task_id, output_file, total_citations_found)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 任务完成！")
            print(f"  输出文件: {output_file}")
            print(f"  找到引用: {total_citations_found}")

            return True

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 错误: {str(e)}")
            self.task_manager.fail_task(task_id, str(e))
            return False

    def _generate_output(self, input_file: str, citations: Dict) -> str:
        """生成输出文件"""
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_with_citations.docx"

        # 复制原文件
        doc = Document(input_file)

        # 生成BibTeX
        bibtex_entries = {}
        for key, citation in citations.items():
            bibtex = self.citation_inserter.generate_bibtex(citation)
            bibtex_entries[key] = bibtex

        # 更新参考文献
        self.citation_inserter.update_bibliography(doc, bibtex_entries)

        # 保存
        doc.save(str(output_file))

        return str(output_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="异步引用补全处理器")
    parser.add_argument("--task-id", required=True, help="任务ID")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--skill-root", default=".", help="Skill根目录")

    args = parser.parse_args()

    processor = AsyncCiteProcessor(args.skill_root)
    success = processor.process(args.task_id, args.input)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
