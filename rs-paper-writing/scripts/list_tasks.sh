#!/bin/bash
# 列出所有任务脚本
# 用法: bash scripts/list_tasks.sh [status] [skill_root]

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="${2:-.}"
STATUS="${1:-all}"

# 检查任务存储目录
TASK_DIR="$SKILL_ROOT/data/task_storage"

if [ ! -d "$TASK_DIR" ]; then
    echo "没有任务"
    exit 0
fi

# 列出任务
python3 << 'EOF'
import json
import sys
from pathlib import Path

task_dir = sys.argv[1]
status_filter = sys.argv[2]

task_files = sorted(Path(task_dir).glob("*.json"), reverse=True)

if not task_files:
    print("没有任务")
    sys.exit(0)

print(f"\n任务列表 (共 {len(task_files)} 个):\n")
print(f"{'任务ID':<40} {'状态':<12} {'进度':<8} {'引用数':<8}")
print("-" * 70)

for task_file in task_files:
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            task_info = json.load(f)

        task_id = task_file.stem
        status = task_info.get('status', 'unknown')
        progress = task_info.get('progress', 0)
        total_citations = task_info.get('total_citations', 0)

        if status_filter != 'all' and status != status_filter:
            continue

        print(f"{task_id:<40} {status:<12} {progress:>6}% {total_citations:>7}")

    except Exception as e:
        print(f"错误读取任务: {e}")

print()

EOF "$TASK_DIR" "$STATUS"
