# demo08_06: Traditional RAG vs Agentic RAG
# - Traditional: 每次提问都检索知识库（search_knowledge=False + add_knowledge_to_context=True）
# - Agentic: Agent自主决定是否需要检索（search_knowledge=True，默认模式）
# Agentic模式更省Token，因为不相关的问题不会触发检索

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

myModel = create_model()

CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_mode")
FIRST_RUN = not os.path.isdir(CHROMA_PATH)

embedder = FastEmbedEmbedder(id="BAAI/bge-small-zh-v1.5", dimensions=512)
vector_db = ChromaDb(collection="mode_demo", path=CHROMA_PATH, persistent_client=True, embedder=embedder)
knowledge = Knowledge(vector_db=vector_db)

if FIRST_RUN:
    print("【首次运行】导入知识")
    knowledge.insert(text_content="Python的GIL（全局解释器锁）限制了多线程的并行执行，但不影响I/O密集型任务。")
    knowledge.insert(text_content="要实现CPU密集型的并行计算，推荐使用multiprocessing模块或第三方库如Joblib。")
    knowledge.insert(text_content="张三是一个计算机工程师，30岁。")
    print("✓ 导入完成\n")
else:
    # ======================== 模式1：Traditional RAG ========================
    # 每次run都会检索知识库，不管问题是否相关
    print("=" * 60)
    print("模式1：Traditional RAG（每次都检索）")
    print("=" * 60)

    traditional_agent = Agent(
        model=myModel,
        knowledge=knowledge,
        search_knowledge=False,             # 关闭Agentic模式
        add_knowledge_to_context=True,      # 开启传统模式：每次都把检索结果塞进context
        instructions="简洁回答，50字以内",
        debug_mode=True,
    )

    # 即使问无关问题，也会触发检索（浪费Token）
    print("\n问无关问题：'今天天气怎么样'")
    traditional_agent.print_response("今天天气怎么样")

    # ======================== 模式2：Agentic RAG ========================
    # Agent自主判断：相关问题才检索，无关问题直接回答
    print("\n" + "=" * 60)
    print("模式2：Agentic RAG（Agent自主判断是否检索）")
    print("=" * 60)

    agentic_agent = Agent(
        model=myModel,
        knowledge=knowledge,
        search_knowledge=True,              # 开启Agentic模式（默认）
        instructions="简洁回答，50字以内",
        debug_mode=True,
    )

    # 无关问题：Agent判断不需要检索，直接回答
    print("\n问无关问题：'今天天气怎么样'")
    agentic_agent.print_response("今天天气怎么样")

    # 相关问题：Agent判断需要检索，调用search_knowledge_base工具
    print("\n问相关问题：'张三是谁'")
    agentic_agent.print_response("张三是谁")
