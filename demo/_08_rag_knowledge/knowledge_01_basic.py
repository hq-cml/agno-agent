"""
知识库 + RAG 示例

演示如何使用 agno 框架的 Knowledge 模块：
- ChromaDB 作为本地向量存储（底层其实是通过SQLite做的存储）
- 支持 URL 内容导入和语义搜索问答
"""
import sys, os

# SQLite 版本兼容性修复 (ChromaDB 需要 SQLite >= 3.35.0)
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.reader.website_reader import WebsiteReader
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder

# ChromaDB 持久化路径（是一个目录，不是文件）
CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_basic")
# 在ChromaDb初始化之前判断，因为ChromaDb()会自动创建该目录
FIRST_RUN = not os.path.isdir(CHROMA_PATH)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model
myModel = create_model()

# ============================================================
# 1. 配置 Embedding 模型 (API)
# ============================================================
# 例1：付费embedder演示
# 将text-embedding-3-small作为embed 模型，需要付费
# embedder = OpenAIEmbedder(
#     id="text-embedding-3-small", # 需要付费
#     dimensions=1536,
#     api_key="sk-xxx",
#     base_url="http://xxxx",
#     client_params={
#         "default_headers": {"X-Model-Provider-Id": "azure_openai"}
#     }
# )

# 例2：免费的embedder模型
# 需要从hugging face上提前下载，需要配置代理
# HuggingFace 镜像（国内无法直连 huggingface.co）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
embedder = FastEmbedEmbedder(
    id="BAAI/bge-small-zh-v1.5",  # 中文小模型，~100MB
    dimensions=512,
)

# ============================================================
# 2. 配置 ChromaDB 向量存储（同时注入Embedding 模型）
# ============================================================
vector_db = ChromaDb(
    collection="my_knowledge",
    path=CHROMA_PATH,
    persistent_client=True, # 持久化！数据存到磁盘（按指定的 path 目录），程序退出后数据不丢失，下次启动还能读取。
    embedder=embedder,
)

# ============================================================
# 3. 创建 Knowledge 知识库实例（基于向量存储）
# ============================================================
knowledge = Knowledge(
    vector_db=vector_db,
)

# ============================================================
# 5. 创建带知识库的 Agent
# ============================================================
agent = Agent(
    model=myModel,
    description="基于知识库回答问题的机器人",
    instructions="用中文回答问题。如果问题和知识库相关内容无关，直接回复不知道，不要自己尝试回答。",
    markdown=True,
    debug_mode=True,

    # 知识库相关
    knowledge=knowledge,
    search_knowledge=True,  # 启用 Agentic RAG
)

# 测试用 URL (欧拉传记 - St Andrews 数学史)
TEST_URL = "https://mathshistory.st-andrews.ac.uk/Biographies/Euler/"

# URL 抓取配置
URL_MAX_DEPTH = 1  # 抓取深度：1=只抓当前页，2+=递归抓取子链接
URL_MAX_LINKS = 1  # 最大抓取链接数

# ============================================================
# 主程序
# ============================================================
# ! 演示了两种：
# 基于URL 导入知识库，如若失败则基于文本内容导入
def store_knowledge():
    print(f"\n[1] 导入 URL 内容: {TEST_URL}")
    print(f"    配置: max_depth={URL_MAX_DEPTH}, max_links={URL_MAX_LINKS}")
    try:
        url_reader = WebsiteReader(max_depth=URL_MAX_DEPTH, max_links=URL_MAX_LINKS)
        knowledge.insert(url=TEST_URL, reader=url_reader)
        print("    ✓ URL 内容导入成功")
    except Exception as e:
        print(f"    ✗ URL 导入失败: {e}")
        print("    尝试使用备用文本内容...")
        knowledge.insert(
            content="""
            Agno 是一个轻量级的 AI Agent 框架。
            它支持多种 LLM 后端，包括 OpenAI、Anthropic 等。
            Agno 的核心特性包括：
            1. 简单易用的 Agent API
            2. 内置的 Tool 支持
            3. Knowledge 知识库模块
            4. Memory 记忆模块
            """
        )
        print("    ✓ 备用文本导入成功")

# 基于知识库问答
def use_knowledge():
    print("\n[2] 基于知识库问答")
    print("-" * 60)

    # question = "Agno 框架有哪些核心特性？"
    question = "你知道有个数学家叫欧拉吗？"
    # question = "你知道有个数学家叫高斯吗？"
    print(f"问题: {question}\n")

    # agent.print_response(question)
    agent.run(question)
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)

if FIRST_RUN:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_knowledge()
else:
    use_knowledge()