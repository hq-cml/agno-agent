# demo04: 使用db - 演示多轮对话记忆持久化
#
# sqllite是一种本地轻量级嵌入式数据库，主要特点：
# 无需安装服务，直接读写本地文件；单个 .db 文件；适用于移动端、桌面应用、小型项目、原型开发
# 目前系统sqllite太太旧了，所以用 pysqlite3 替换系统自带的旧版 sqlite3（系统版本3.7不支持UPSERT语法）
# pysqlite3 是一种驱动sqllite，但是它自带了一个新版本的 SQLite 引擎（编译好的 .so 动态库），打包在 Python 包里。
# 所以代码里做的这个替换：
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# 效果是：让 Python 的 import sqlite3 实际加载 pysqlite3，从而使用它自带的新版 SQLite 引擎，绕过了系统旧版本的限制。

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
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent.db")
myDb = SqliteDb(db_file=DB_PATH)

SESSION_ID = "demo04-test-session"

# Note：三个参数的关系：
# session_id → 对话的唯一标识，每次对话有很多轮问答，甚至可以重新发起
#   如果不指定session_id，则每次随机生成新ID，这样就找不到上次的对话了
#   所以这里指定一个固定的session_id，才能起到记忆作用，否则的话即便开启了记忆，也会找不到
# add_history_to_context → 找到历史后要不要发给模型（不开启则模型看不到历史，等于不记得）
# num_history_runs → 最多发几轮历史给模型（防止历史太多导致 token 超限）

agent = Agent(
    name="agno v0.1",
    model=myModel,
    description="你是一个通用Agent，负责回答各类问题。",
    instructions="请记住用户告诉你的信息，后续对话中可以引用。",
    debug_mode=True,
    db=myDb,
    session_id=SESSION_ID, # 这里可以换一个随机的session_id尝试，会发现即便开启了db，仍然找不到对应的会话，记忆也将失效
    add_history_to_context=True,
    num_history_runs=5,
)

first_run = not os.path.exists(DB_PATH)
if first_run:
    # 首次运行：告诉 Agent 信息，写入 db print("=" * 60)
    print("【首次运行】告诉Agent信息，写入数据库")
    print("=" * 60)
    ret = agent.run("我叫张三，我是一名Python开发者，今年28岁。")
    print(f"\n回复：{ret.content}\n")
    print("提示：再次运行本脚本，验证 Agent 是否还记得你")
else:
    # 非首次运行：直接问问题，验证持久化记忆
    print("=" * 60)
    print("【再次运行】验证 Agent 是否记住了上次的信息")
    print("=" * 60)
    ret = agent.run("我叫什么名字？我是做什么的？今年多大？")
    print(f"\n回复：{ret.content}\n")
    print("提示：删除 agent.db 后再运行，Agent 就不记得了")