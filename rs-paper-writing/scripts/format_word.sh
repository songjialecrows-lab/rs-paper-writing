#!/bin/bash
# Word格式自动调整脚本 - RS-Paper-Writing Skill
# 用法: bash scripts/format_word.sh <input_file> <template_name> [output_file]

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: bash scripts/format_word.sh <input_file> <template_name> [output_file]"
    echo ""
    echo "参数说明:"
    echo "  input_file    - 输入的Word文档路径"
    echo "  template_name - 模板名称（如: default, your_school_name等）"
    echo "  output_file   - 输出文件路径（可选，默认为input_file_formatted.docx）"
    echo ""
    echo "示例:"
    echo "  bash scripts/format_word.sh thesis.docx default"
    echo "  bash scripts/format_word.sh thesis.docx your_school formatted_thesis.docx"
    exit 1
fi

INPUT_FILE="$1"
TEMPLATE_NAME="$2"
OUTPUT_FILE="${3:-${INPUT_FILE%.*}_formatted.docx}"

# 检查输入文件
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 输入文件不存在: $INPUT_FILE"
    exit 1
fi

# 检查Python脚本
if [ ! -f "$SCRIPT_DIR/format_to_word.py" ]; then
    echo "错误: Python脚本不存在: $SCRIPT_DIR/format_to_word.py"
    exit 1
fi

# 运行Python脚本
echo "正在格式化文档..."
echo "输入文件: $INPUT_FILE"
echo "模板: $TEMPLATE_NAME"
echo "输出文件: $OUTPUT_FILE"
echo ""

python3 "$SCRIPT_DIR/format_to_word.py" \
    --input "$INPUT_FILE" \
    --template "$TEMPLATE_NAME" \
    --output "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 格式化成功！"
    echo "输出文件: $OUTPUT_FILE"
else
    echo ""
    echo "✗ 格式化失败，请检查输入文件和模板配置"
    exit 1
fi
