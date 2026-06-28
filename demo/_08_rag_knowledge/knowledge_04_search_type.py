# demo08_04: 搜索类型 - Vector / Keyword / Hybrid
# 不同搜索方式适合不同场景：
# - Vector: 语义相似度，适合意图模糊的问题
# - Keyword: 关键字匹配，适合精确术语查询
# - Hybrid: 两者结合（推荐），兼顾语义和精确匹配

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder

myModel = create_model()

CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_search")
FIRST_RUN = not os.path.isdir(CHROMA_PATH)

embedder = FastEmbedEmbedder(id="BAAI/bge-small-zh-v1.5", dimensions=512)

# ======================== 配置不同搜索类型 ========================
# 通过 search_type 参数控制检索方式
vector_db = ChromaDb(
    collection="search_demo",
    path=CHROMA_PATH,
    persistent_client=True,
    embedder=embedder,
    # 搜索类型：SearchType.vector | SearchType.keyword | SearchType.hybrid
    search_type=SearchType.hybrid, # !!!!!指定搜索类型
)

knowledge = Knowledge(vector_db=vector_db)

# 导入测试数据
if FIRST_RUN:
    print("【首次运行】导入测试数据")
    knowledge.insert(text_content="Django是一个全功能的Python Web框架，内置ORM、Admin后台和认证系统。")
    knowledge.insert(text_content="Flask是一个轻量级的Python微框架，灵活可扩展，适合小型项目。")
    knowledge.insert(text_content="FastAPI是一个现代高性能Python Web框架，基于类型提示自动生成文档。")
    knowledge.insert(text_content="NumPy是Python科学计算的基础库，提供高效的多维数组操作。")
    knowledge.insert(text_content="Pandas是Python数据分析库，提供DataFrame数据结构，擅长表格数据处理。")
    print("✓ 导入完成\n")
else:
    # ======================== 对比搜索效果 ========================
    query = "高性能的web开发框架"

    print(f"查询: '{query}'")
    print("=" * 60)

    # 直接调用knowledge.search可以看到原始检索结果
    results = knowledge.search(query, max_results=3)
    print(f"\n搜索结果（{vector_db.search_type.value}模式，top 3）：")
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.content[:]}...")
    print("-------------------------------------------------")

    # 也可以通过Agent使用（Agentic RAG模式）
    agent = Agent(
        model=myModel,
        knowledge=knowledge,
        search_knowledge=True,
        instructions="根据知识库回答，如果没有相关内容，请回答不知道。",
    )
    print(f"\nAgent回答：")
    agent.print_response(query)

    # why 搜索结果不对
