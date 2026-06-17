# 记忆共享

import pprint
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mem_share.db")
myDb = SqliteDb(db_file=DB_PATH)


agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    db=myDb,
    update_memory_on_run=True,
)

def store_memory():
    ret = agent.run(
        input='''
            1. 李四，男，土木工作者，80岁，江苏人;
            2. 张三，女，Python开发者，60岁，北京人;
            3. 王五，女，法官，20岁，山东人''',
        user_id="user_101",
    )
    print(f"\n回复：{ret.content}\n")

# 查看具体记忆了哪些内容信息
def see_memory():
    mems = agent.get_user_memories(user_id="user_101")
    print("user_id:101的记忆：")
    pprint.pprint(mems)
    mems = agent.get_user_memories(user_id="user_102")
    print("user_id:102的记忆：")
    pprint.pprint(mems)

first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()
    see_memory()


ret = agent.run("王五是谁，多大年龄？", user_id="user_101")
print(f"\n回复：{ret.content}\n")