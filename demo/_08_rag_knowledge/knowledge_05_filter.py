# demo08_05: 知识过滤 - 通过metadata标签过滤检索范围
# 导入时打标签 → 检索时按标签过滤，缩小搜索范围提高精度

import sys, os
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder


CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_filter")
FIRST_RUN = not os.path.isdir(CHROMA_PATH)

embedder = FastEmbedEmbedder(id="BAAI/bge-small-zh-v1.5", dimensions=512)

vector_db = ChromaDb(
    collection="filter_demo",
    path=CHROMA_PATH,
    persistent_client=True,
    embedder=embedder,
)

knowledge = Knowledge(vector_db=vector_db)

# ======================== 导入带标签的内容 ========================
if FIRST_RUN:
    print("【首次运行】导入带标签的知识")
    # 前端相关知识
    knowledge.insert(
        text_content="React是一个用于构建用户界面的JavaScript库，由Facebook开发维护。",
        metadata={"domain": "frontend", "language": "javascript"},
    )
    knowledge.insert(
        text_content="Vue.js是一个渐进式JavaScript框架，易于上手，适合中小型项目。",
        metadata={"domain": "frontend", "language": "javascript"},
    )
    # 后端相关知识
    knowledge.insert(
        text_content="FastAPI是Python高性能Web框架，基于Starlette和Pydantic构建。",
        metadata={"domain": "backend", "language": "python"},
    )
    knowledge.insert(
        text_content="Spring Boot是Java企业级开发框架，内置Tomcat服务器。",
        metadata={"domain": "backend", "language": "java"},
    )
    print("✓ 导入完成\n")
else:
    # ======================== 带过滤条件的检索 ========================
    query = "推荐一个好用的框架"

    # 不过滤：所有领域都会返回
    print(f"查询: '{query}'")
    print("\n--- 无过滤（返回所有领域） ---")
    results = knowledge.search(query, max_results=4)
    for doc in results:
        print(f"  • {doc.content[:50]}...")

    # 按domain过滤：只搜索后端知识
    print("\n--- 过滤 domain=backend ---")
    results = knowledge.search(query, max_results=4, filters={"domain": "backend"})
    for doc in results:
        print(f"  • {doc.content[:50]}...")

    # 按language过滤：只搜索Python相关
    print("\n--- 过滤 language=python ---")
    results = knowledge.search(query, max_results=4, filters={"language": "python"})
    for doc in results:
        print(f"  • {doc.content[:50]}...")
