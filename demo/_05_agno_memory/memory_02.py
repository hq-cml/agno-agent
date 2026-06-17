# demo05_02: 记忆系统：智能记忆
# Note：它和自动记忆的区别？

import sys, os
#将项目根目录（当前文件所在目录向上两级）添加到Python模块搜索路径的最前面，确保能优先从该目录导入模块，解create_model决跨目录导入问题。
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

def store_memory():
    ret = agent.run('''
    1. 李四，土木工作者，80岁;
    2. 张三，Python开发者;
    3. 王五，法官，在江苏''')
    print(f"\n回复：{ret.content}\n")

first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()


def remove_memory():
    ret = agent.run('''
    删除王五的信息''')
    print(f"\n回复：{ret.content}\n")


#remove_memory()


ret = agent.run("王五是谁，今年多少岁？")
print(f"\n回复：{ret.content}\n")
