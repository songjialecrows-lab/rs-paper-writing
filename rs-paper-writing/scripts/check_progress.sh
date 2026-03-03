#!/bin/bash
# 查询任务进度脚本
# 用法: bash scripts/check_progress.sh <task_id> [skill_root]

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="${2:-.}"

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: bash scripts/check_progress.sh <task_id> [skill_root]"
    echo ""
    echo "参数说明:"
    echo "  task_id    - 任务ID"
    echo "  skill_root - Skill根目录（可选，默认为当前目录）"
    echo ""
    echo "示例:"
    echo "  bash scripts/check_progress.sh auto_cite_20260303_001"
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

task_id = sys.argv[1]
task_file = sys.argv[2]

try:
    with open(task_file, 'r', encoding='utf-8') as f:
        task_info = json.load(f)

    status = task_info.get('status', 'unknown')
    progress = task_info.get('progress', 0)
    chapters = task_info.get('chapters', [])
    total_citations = task_info.get('total_citations', 0)
    error_message = task_info.get('error_message')

    # 显示进度条
    bar_length = 40
    filled = int(bar_length * progress / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\n进度: {bar} {progress}%")

    # 显示状态
    print(f"状态: {status}")

    # 显示章节信息
    if chapters:
        print(f"\n章节处理情况:")
        for chapter in chapters:
            ch_status = chapter.get('status', 'unknown')
            ch_citations = chapter.get('citations_found', 0)
            print(f"  {chapter['name']}: {ch_status} ({ch_citations}个引用)")

    # 显示总引用数
    print(f"\n已找到引用: {total_citations}个")

    # 显示错误信息
    if error_message:
        print(f"\n错误: {error_message}")

    print()

except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)

EOF "$TASK_ID" "$TASK_FILE"
