# demo08_03: 分块策略 - 不同的文档切割方式
# 分块质量直接影响检索效果：
#   块太大→噪声多
#   块太小→语义不完整

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from agno.knowledge.reader.text_reader import TextReader
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.chunking.recursive import RecursiveChunking

# 测试文本
SAMPLE_TEXT = """
# Python简介

Python是一种解释型、面向对象的高级编程语言。它由Guido van Rossum于1989年底发明，第一个公开发行版发行于1991年。

## 核心特性

Python的设计哲学强调代码的可读性。它使用缩进来标识代码块，而不是使用大括号或关键字。Python支持多种编程范式，包括结构化编程、面向对象编程和函数式编程。

## 应用领域

Python广泛应用于Web开发、数据分析、人工智能、科学计算、自动化运维等领域。它拥有超过30万个第三方库，涵盖了几乎所有计算需求。

## 版本历史

Python 2.0于2000年发布，引入了列表推导式和垃圾回收机制。Python 3.0于2008年发布，是一个不完全向后兼容的版本，修复了许多设计缺陷。目前Python 2已经停止维护，推荐使用Python 3。
"""

# 手动读取并分块查看效果
from agno.knowledge.document.base import Document
doc = Document(content=SAMPLE_TEXT)

# ======================== 对比不同分块策略 ========================
print("=" * 60)
print("对比不同分块策略的切割效果")
print("=" * 60)

# 策略1：固定大小切割
print("\n--- FixedSize (chunk_size=100, overlap=20) ---")
fixed_reader = TextReader(
    chunk_size=100,
    chunking_strategy=FixedSizeChunking(chunk_size=100, overlap=20),
)
fixed_chunks = fixed_reader.chunk_document(doc)
for i, chunk in enumerate(fixed_chunks[:]):
    print(f"  块{i+1} ({len(chunk.content)}字): {chunk.content[:]}...")

# 策略2：递归切割（按段落→句子→字符递归）
print("\n--- Recursive (chunk_size=150, overlap=30) ---")
recursive_reader = TextReader(
    chunk_size=150,
    chunking_strategy=RecursiveChunking(chunk_size=150, overlap=30),
)
recursive_chunks = recursive_reader.chunk_document(doc)
for i, chunk in enumerate(recursive_chunks[:]):
    print(f"  块{i+1} ({len(chunk.content)}字): {chunk.content[:]}...")

# why 效果并不好
print(f"\n固定切割: {len(fixed_chunks)} 块")
print(f"递归切割: {len(recursive_chunks)} 块")
print("\n递归切割通常更好，因为它尽量在段落/句子边界切分，保持语义完整。")
