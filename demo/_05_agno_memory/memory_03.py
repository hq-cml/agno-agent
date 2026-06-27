# demo05_03: 自定义记忆管理，更加可控的、定制化记忆
import pprint
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mem_manager.db")
myDb = SqliteDb(db_file=DB_PATH)


# 自定义Manager
myMemManager = MemoryManager(
    model=myModel, # 这需要模型，说明这个Manager可能是一个子agent？
    db=myDb,

    # 定制化记忆需求
    additional_instructions="""
    不能记录用户的以下信息：年龄和性别
    """,

    # 进一步定制化，比如某些线上环境，禁止修改
    # 实际验证下来发现这几个属性，要么有bug，要么LLM可能会绕过，实际就别用了
    #update_memories=False,
    #add_memories= True,
    #delete_memories=False,
    #clear_memories= False,
)
agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    memory_manager=myMemManager,
    db=myDb,
    update_memory_on_run=True,
)

def store_memory():
    ret = agent.run('''
    1. 李四，男，土木工作者，80岁，江苏人;
    2. 张三，女，Python开发者，60岁，北京人;
    3. 王五，女，法官，20岁，山东人''', user_id="10001")
    print(f"\n回复：{ret.content}\n")

# 查看具体记忆了哪些内容信息
def see_memory():
    mems = agent.get_user_memories(user_id="10001")
    pprint.pprint(mems)

def update_memory():
    ret = agent.run('''
    王五其实是河北人''', user_id="10001")
    print(f"\n回复：{ret.content}\n")

# 记忆检索，三种模式：
# first_n: 检索出最开始的n条
# last_n:  检索出最后的n条
# agentic: 需要搭配query进行，不过deepseek不支持这种模式，因为不支持response_format type
def mem_retrieve():
    see_memory()
    ret = myMemManager.search_user_memories(
        user_id = "10001",
        limit=1,
        #retrieval_method="first_n",
        retrieval_method="last_n",
        # retrieval_method="agentic",
        # query="王五是哪里人",
    )
    print(f"\n检索结果：{ret}\n") # 为什么不生效


first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()
else:
    #see_memory()

    # update_memory()
    # see_memory()

    # ret = agent.run("王五是谁，多大年龄？", user_id="10001")
    # print(f"\n回复：{ret.content}\n")

    mem_retrieve()