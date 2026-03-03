#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务管理器 - 后台任务管理、进度跟踪、结果存储
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ChapterProgress:
    """章节处理进度"""
    name: str
    status: str  # pending, processing, completed, failed
    citations_found: int = 0
    total_citations: int = 0
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class TaskInfo:
    """任务信息"""
    task_id: str
    input_file: str
    output_file: Optional[str] = None
    status: str = "pending"
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: int = 0
    chapters: List[Dict] = None
    total_citations: int = 0
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.created_at == "":
            self.created_at = datetime.now().isoformat()
        if self.chapters is None:
            self.chapters = []


class TaskManager:
    """任务管理器"""

    def __init__(self, storage_dir: str = "data/task_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def create_task(self, input_file: str) -> str:
        """
        创建新任务

        Args:
            input_file: 输入文件路径

        Returns:
            任务ID
        """
        task_id = f"auto_cite_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        task_info = TaskInfo(
            task_id=task_id,
            input_file=input_file,
            status=TaskStatus.PENDING.value
        )

        self._save_task(task_info)
        return task_id

    def start_task(self, task_id: str) -> bool:
        """启动任务"""
        task_info = self.get_task(task_id)
        if not task_info:
            return False

        task_info.status = TaskStatus.PROCESSING.value
        task_info.started_at = datetime.now().isoformat()
        self._save_task(task_info)
        return True

    def update_progress(self, task_id: str, progress: int, chapter_updates: Optional[Dict] = None) -> bool:
        """
        更新任务进度

        Args:
            task_id: 任务ID
            progress: 进度百分比 (0-100)
            chapter_updates: 章节更新信息

        Returns:
            是否成功
        """
        task_info = self.get_task(task_id)
        if not task_info:
            return False

        task_info.progress = progress

        if chapter_updates:
            # 更新章节信息
            for chapter_name, chapter_info in chapter_updates.items():
                # 查找或创建章节记录
                chapter_record = None
                for ch in task_info.chapters:
                    if ch.get("name") == chapter_name:
                        chapter_record = ch
                        break

                if not chapter_record:
                    chapter_record = {"name": chapter_name}
                    task_info.chapters.append(chapter_record)

                # 更新章节信息
                chapter_record.update(chapter_info)

        self._save_task(task_info)
        return True

    def complete_task(self, task_id: str, output_file: str, total_citations: int) -> bool:
        """完成任务"""
        task_info = self.get_task(task_id)
        if not task_info:
            return False

        task_info.status = TaskStatus.COMPLETED.value
        task_info.completed_at = datetime.now().isoformat()
        task_info.output_file = output_file
        task_info.total_citations = total_citations
        task_info.progress = 100

        self._save_task(task_info)
        return True

    def fail_task(self, task_id: str, error_message: str) -> bool:
        """标记任务失败"""
        task_info = self.get_task(task_id)
        if not task_info:
            return False

        task_info.status = TaskStatus.FAILED.value
        task_info.completed_at = datetime.now().isoformat()
        task_info.error_message = error_message

        self._save_task(task_info)
        return True

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """获取任务信息"""
        task_file = self.storage_dir / f"{task_id}.json"

        if not task_file.exists():
            return None

        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TaskInfo(**data)
        except Exception as e:
            print(f"Error loading task: {e}")
            return None

    def get_progress(self, task_id: str) -> Optional[Dict]:
        """获取任务进度"""
        task_info = self.get_task(task_id)
        if not task_info:
            return None

        return {
            "task_id": task_id,
            "status": task_info.status,
            "progress": task_info.progress,
            "created_at": task_info.created_at,
            "started_at": task_info.started_at,
            "completed_at": task_info.completed_at,
            "chapters": task_info.chapters,
            "total_citations": task_info.total_citations,
            "error_message": task_info.error_message
        }

    def list_tasks(self, status: Optional[str] = None) -> List[str]:
        """列出所有任务"""
        tasks = []
        for task_file in self.storage_dir.glob("*.json"):
            task_id = task_file.stem

            if status:
                task_info = self.get_task(task_id)
                if task_info and task_info.status == status:
                    tasks.append(task_id)
            else:
                tasks.append(task_id)

        return sorted(tasks, reverse=True)

    def _save_task(self, task_info: TaskInfo) -> bool:
        """保存任务信息"""
        task_file = self.storage_dir / f"{task_info.task_id}.json"

        try:
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(task_info), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving task: {e}")
            return False

    def cleanup_old_tasks(self, days: int = 7) -> int:
        """清理旧任务"""
        from datetime import timedelta

        cutoff_time = datetime.now() - timedelta(days=days)
        deleted_count = 0

        for task_file in self.storage_dir.glob("*.json"):
            try:
                task_info = self.get_task(task_file.stem)
                if task_info and task_info.completed_at:
                    completed_time = datetime.fromisoformat(task_info.completed_at)
                    if completed_time < cutoff_time:
                        task_file.unlink()
                        deleted_count += 1
            except Exception as e:
                print(f"Error cleaning up task: {e}")

        return deleted_count


def main():
    """测试"""
    manager = TaskManager()
    # 这里可以添加测试代码
    pass


if __name__ == "__main__":
    main()
