#!/usr/bin/env python3
"""统计代码行数的辅助脚本"""

import sys

if len(sys.argv) < 2:
    print("用法: count_lines.py <文件路径>")
    sys.exit(1)

filepath = sys.argv[1]
try:
    with open(filepath, "r") as f:
        lines = f.readlines()
    total = len(lines)
    code = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
    print(f"总行数: {total}, 代码行: {code}, 注释/空行: {total - code}")
except FileNotFoundError:
    print(f"文件不存在: {filepath}")
