#!/bin/bash
# 异步引用补全脚本 - 启动后台任务
# 用法: bash scripts/auto_cite_async.sh <input_file> [skill_root]

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="${2:-.}"

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: bash scripts/auto_cite_async.sh <input_file> [skill_root]"
    echo ""
    echo "参数说明:"
    echo "  input_file  - 输入的Word文档路径"
    echo "  skill_root  - Skill根目录（可选，默认为当前目录）"
    echo ""
    echo "示例:"
    echo "  bash scripts/auto_cite_async.sh thesis.docx"
    echo "  bash scripts/auto_cite_async.sh thesis.docx /path/to/skill"
    exit 1
fi

INPUT_FILE="$1"

# 检查输入文件
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 输入文件不存在: $INPUT_FILE"
    exit 1
fi

# 检查Python脚本
if [ ! -f "$SCRIPT_DIR/auto_cite_async.py" ]; then
    echo "错误: Python脚本不存在: $SCRIPT_DIR/auto_cite_async.py"
    exit 1
fi

# 创建任务存储目录
mkdir -p "$SKILL_ROOT/data/task_storage"

# 生成任务ID
TASK_ID="auto_cite_$(date +%Y%m%d_%H%M%S)_$(openssl rand -hex 4 2>/dev/null || echo 'xxxx')"

echo "启动异步引用补全任务..."
echo "任务ID: $TASK_ID"
echo "输入文件: $INPUT_FILE"
echo ""

# 启动后台任务
nohup python3 "$SCRIPT_DIR/auto_cite_async.py" \
    --task-id "$TASK_ID" \
    --input "$INPUT_FILE" \
    --skill-root "$SKILL_ROOT" \
    > "$SKILL_ROOT/data/task_storage/${TASK_ID}.log" 2>&1 &

TASK_PID=$!

echo "✓ 任务已启动！"
echo ""
echo "任务信息:"
echo "  任务ID: $TASK_ID"
echo "  进程ID: $TASK_PID"
echo "  预计耗时: 3-5分钟"
echo ""
echo "查询进度:"
echo "  bash scripts/check_progress.sh $TASK_ID"
echo ""
echo "获取结果:"
echo "  bash scripts/get_result.sh $TASK_ID"
echo ""
echo "你可以立即离开，稍后回来查看结果。"
