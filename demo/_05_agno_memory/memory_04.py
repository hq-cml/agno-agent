# 记忆共享
# 生产环境中，必然是多会话、多用户并行的，所以记忆共享就很重要
# 记忆共享的抓手：user_id
# 通过这个抓手，可以实现：多轮对话共享记忆、多Agent之间共享记忆

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

# 定义两个并行的Agent
agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    db=myDb,
    update_memory_on_run=True,
)

agent2 = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    db=myDb,
    update_memory_on_run=True,
)

SESSION_ID_1 = "session_id_1"
SESSION_ID_2 = "session_id_2"

USER_ID_1 = "10001"
USER_ID_2 = "10002"

first_run = not os.path.exists(DB_PATH)
if first_run:
    # 用户1在会话1中录入记忆
    ret = agent.run(
        input='''李四，男，土木工作者，80岁，江苏人''',
        user_id=USER_ID_1,
        session_id=SESSION_ID_1,
    )
    print(f"\n用户1录入记忆：{ret.content}\n")

    # 用户2在会话1中录入记忆
    ret = agent.run(
        input='''张三，女，Python开发者，60岁，北京人''',
        user_id=USER_ID_2,
        session_id=SESSION_ID_1,
    )
    print(f"\n用户2录入记忆：{ret.content}\n")
else:
    # 例1：用户1在会话2中，仍能读取到用户1在会话1中录入的记忆
    ret = agent.run(
            input='''李四是谁''',
            user_id=USER_ID_1,
            session_id=SESSION_ID_2,
        )
    print(f"\n用户1回忆：{ret.content}\n")

    # 例2：多Agent也能共享记忆，只要是同一个User_id
    ret = agent2.run(
            input='''李四是谁''',
            user_id=USER_ID_1,
        )
    print(f"\nAgent2读取user_id的回忆：{ret.content}\n")