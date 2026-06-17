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
    additional_instructions="""
    不能记录用户的以下信息：年龄和性别
    """,

    # 进一步定制化，比如线上线上环境，进制删除记忆
    delete_memories=False,
    #update_memories=True,
    #add_memories= True,
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
    3. 王五，女，法官，20岁，山东人''')
    print(f"\n回复：{ret.content}\n")

# 查看具体记忆了哪些内容信息
def see_memory():
    mems = agent.get_user_memories() #Note: 为什么这么特殊？
    pprint.pprint(mems)

first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()
    see_memory()

def remove_memory():
    ret = agent.run('''
    删除王五的信息''')
    print(f"\n回复：{ret.content}\n")

# remove_memory() #Note：为什么不生效
#
# ret = agent.run("王五是谁，多大年龄？")
# print(f"\n回复：{ret.content}\n")


def mem_retrive():
    see_memory()
    ret = myMemManager.search_user_memories(
        user_id="张三",
        retrieval_method="last_n",
    )
    print(f"\n检索结果：{ret}\n") # 为什么不生效

mem_retrive()