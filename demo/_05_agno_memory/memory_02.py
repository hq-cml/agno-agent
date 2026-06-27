# demo05_02: 记忆系统：agentic模式
# Note：它和自动记忆的区别：
# 自动记忆：每次run()即每轮对话后台额外调用一次LLM提炼并存储，Agent无感，不知道后台有进行存储动作，所以也无法主动删除记忆
# Agentic模式：给Agent提供Mem相关tool，Agent知道自己拥有了tool，所以在对话中会自主调用tool进行记忆，也可以调用删除tool删除记忆

import pprint
import sys, os
#将项目根目录（当前文件所在目录向上两级）添加到Python模块搜索路径的最前面，确保能优先从该目录导入模块，解决create_model跨目录导入问题。
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mem_agentic.db")
myDb = SqliteDb(db_file=DB_PATH)

agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    db=myDb,
    enable_agentic_memory=True,# 开启agentic记忆
)

# 查看具体记忆了哪些内容信息
def see_memory():
    mems = agent.get_user_memories(
        user_id="10001"
    )
    pprint.pprint(mems)

def store_memory():
    ret = agent.run(
        input='''
    1. 李四，土木工作者，80岁;
    2. 张三，Python开发者;
    3. 王五，法官，在江苏''',
        user_id="10001",
    )
    print(f"\n回复：{ret.content}\n")

def remove_memory():
    ret = agent.run(
        input='''
    删除王五的信息''',
        user_id="10001",)
    print(f"\n回复：{ret.content}\n")


first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()
else:
    #see_memory()

    ret = agent.run("王五是谁，今年多少岁？", user_id="10001")
    print(f"\n回复：{ret.content}\n")

    #remove_memory()


