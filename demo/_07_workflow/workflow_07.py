#Session State，多步骤之间的数据共享
#利用db来实现

import sys, os
#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_state.db")
myDb = SqliteDb(db_file=DB_PATH)