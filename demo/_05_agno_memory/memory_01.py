# demo05_01: 记忆系统：自动记忆
# demo04中使用的db，是基于一次session id，并不实用，所以它只是演示了db怎么用
# Note：本实例则是更加适合实际使用的db，自动记忆每次对话Agent会自动提炼内容记载到db中

import pprint
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
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mem_auto.db")
myDb = SqliteDb(db_file=DB_PATH)

agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    debug_mode=True,
    db=myDb,
    update_memory_on_run=True,# 开启自动记忆功能：自动提炼并存储记忆
)

# 查看具体记忆了哪些内容信息
def see_memory():
    mems = agent.get_user_memories(
        user_id="10001"              # !!! 可以试试看不传user_id，会发现无法看到存储的记忆
    )
    pprint.pprint(mems)

# 存储记忆
def store_memory():
    ret = agent.run(
        input='''
    1. 李四，土木工作者，40岁，在北京，爱好是看书;
    2. 张三，Python开发者，今年28岁。在北京，爱好是周末爬山;
    3. 王五，法官，55岁，在江苏，爱好是游泳''',
        user_id="10001",               # !!!! 这个user_id不代表张三、李四或者其他什么人，他只是记忆的分区标识
    )
    print(f"\n回复：{ret.content}\n")
    # 不要立刻查看，因为记忆系统是LLM自动提取的，所以需要等待LLM生成结果，再查看
    # 直接查看有一定概率会查看到空的结果
    #see_memory()

#变更记忆
def change_memory():
    ret = agent.run(
        input = '''
        王五的爱好变了，爱看电影了''',
        user_id="10001",
    )
    print(f"\n回复：{ret.content}\n")



first_run = not os.path.exists(DB_PATH)
if first_run:
    print("【首次运行】告诉Agent信息，写入数据库")
    store_memory()



#see_memory()

#change_memory()

# 这样是查看不到记忆的，因为没有user_id
# ret = agent.run("王五是谁？")
# print(f"\n回复：{ret.content}\n")

ret = agent.run("王五是谁？", user_id="10001")
print(f"\n回复：{ret.content}\n")