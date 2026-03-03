#!/bin/bash
# 获取任务结果脚本
# 用法: bash scripts/get_result.sh <task_id> [skill_root]

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="${2:-.}"

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: bash scripts/get_result.sh <task_id> [skill_root]"
    echo ""
    echo "参数说明:"
    echo "  task_id    - 任务ID"
    echo "  skill_root - Skill根目录（可选，默认为当前目录）"
    echo ""
    echo "示例:"
    echo "  bash scripts/get_result.sh auto_cite_20260303_001"
    exit 1
fi

TASK_ID="$1"
TASK_FILE="$SKILL_ROOT/data/task_storage/${TASK_ID}.json"

# 检查任务文件
if [ ! -f "$TASK_FILE" ]; then
    echo "错误: 任务不存在: $TASK_ID"
    exit 1
fi

# 解析任务信息
python3 << 'EOF'
import json
import sys
from pathlib import Path

task_id = sys.argv[1]
task_file = sys.argv[2]

try:
    with open(task_file, 'r', encoding='utf-8') as f:
        task_info = json.load(f)

    status = task_info.get('status', 'unknown')
    output_file = task_info.get('output_file')
    total_citations = task_info.get('total_citations', 0)
    error_message = task_info.get('error_message')
    created_at = task_info.get('created_at', '')
    completed_at = task_info.get('completed_at', '')

    print()

    if status == 'completed':
        print("✓ 任务完成！")
        print()
        print(f"输出文件: {output_file}")
        print(f"添加引用: {total_citations}个")

        # 检查文件是否存在
        if output_file and Path(output_file).exists():
            file_size = Path(output_file).stat().st_size / 1024 / 1024
            print(f"文件大小: {file_size:.2f} MB")
        else:
            print("警告: 输出文件不存在")

        # 计算处理时间
        if created_at and completed_at:
            from datetime import datetime
            start = datetime.fromisoformat(created_at)
            end = datetime.fromisoformat(completed_at)
            duration = (end - start).total_seconds()
            print(f"处理耗时: {duration:.1f}秒")

    elif status == 'processing':
        print("⏳ 任务仍在处理中...")
        print()
        print("请稍后再试:")
        print(f"  bash scripts/check_progress.sh {task_id}")

    elif status == 'failed':
        print("✗ 任务失败")
        print()
        if error_message:
            print(f"错误信息: {error_message}")

    else:
        print(f"未知状态: {status}")

    print()

except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)

EOF "$TASK_ID" "$TASK_FILE"
