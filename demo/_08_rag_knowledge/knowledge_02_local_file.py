# demo08_02: 本地文件加载 - 从本地文本文件导入知识
# 演示如何加载本地txt/md文件到知识库
# ！！！！！！！重点：metadata标签的使用

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder
from agno.knowledge.reader.text_reader import TextReader

myModel = create_model()

CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_local_file")
FIRST_RUN = not os.path.isdir(CHROMA_PATH)

# 准备测试文件
TEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_doc.txt")
if not os.path.exists(TEST_FILE):
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("""Python是一种高级编程语言，由Guido van Rossum于1991年发布。
Python的设计哲学强调代码的可读性和简洁性。
Python支持多种编程范式，包括面向对象、函数式和过程式编程。
Python拥有丰富的标准库和第三方库生态系统。
常用的Python Web框架包括Django、Flask和FastAPI。
Python在数据科学领域广泛使用，主要库有NumPy、Pandas和Matplotlib。
机器学习常用的Python库包括Scikit-learn、TensorFlow和PyTorch。
""")

embedder = FastEmbedEmbedder(id="BAAI/bge-small-zh-v1.5", dimensions=512)

vector_db = ChromaDb(
    collection="local_file_knowledge",
    path=CHROMA_PATH,
    persistent_client=True,
    embedder=embedder,
)

knowledge = Knowledge(vector_db=vector_db)

agent = Agent(
    model=myModel,
    knowledge=knowledge,
    search_knowledge=True,
    description="基于本地文件知识库回答问题",
    instructions="用中文回答。只根据知识库内容回答，不知道就说不知道。",
)

# ======================== 导入本地文件 ========================
if FIRST_RUN:
    print("【首次运行】导入本地文件到知识库")
    # 方式1：通过path参数加载文件
    knowledge.insert(
        path=TEST_FILE,
        reader=TextReader(chunk_size=200),  # 每200字符切一块
        # metadata用于打标签，后续可以按标签过滤，在demo_05中有例子
        metadata={"source": "local", "topic": "python"},
    )
    print("✓ 本地文件导入成功")
else:
    # ======================== 问答测试 ========================
    print("\n=== 基于本地文件知识库问答 ===")
    agent.print_response("Python有哪些常用的Web框架？")
