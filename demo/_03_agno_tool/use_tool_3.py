# demo03_3: 使用工具进阶---数据库相关
from agno.agent import Agent
from agno.tools import tool

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

import sys
# 用 pysqlite3 替换标准库 sqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

def init_db():
    """初始化数据库：创建 user 表（如果不存在）"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            )
        ''')
        conn.commit()

@tool
def insert_users(users: List[Dict[str, Any]]) -> int:
    """
    插入多条用户数据到 user 表

    Args:
        users: 用户字典列表，每个字典应包含 'name', 'age', 'email' 键
               例如: [{"name": "张三", "age": 25, "email": "zhangsan@example.com"}, ...]

    Returns:
        成功插入的行数
    """
    if not users:
        return 0

    init_db()  # 确保表存在

    inserted = 0
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for user in users:
            try:
                cursor.execute('''
                    INSERT INTO user (name, age, email)
                    VALUES (?, ?, ?)
                ''', (user['name'], user['age'], user['email']))
                inserted += 1
            except sqlite3.IntegrityError as e:
                print(f"插入失败 (可能邮箱重复): {user}, 错误: {e}")
                # 继续插入其他记录
        conn.commit()
    return inserted

@tool
def query_users(conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    根据条件查询用户信息

    Args:
        conditions: 查询条件字典，支持 'name', 'age', 'email' 键，支持模糊匹配（使用 '__contains' 后缀）
                    例如: {"name": "张"}  -> 精确匹配
                          {"name__contains": "张"} -> 模糊匹配
                          {"age": 25} -> 精确年龄
                    如果为 None 或空字典，则返回所有用户

    Returns:
        用户字典列表，每个字典包含 id, name, age, email
    """
    init_db()

    query = "SELECT id, name, age, email FROM user"
    params = []
    where_clauses = []

    if conditions:
        for key, value in conditions.items():
            if key.endswith("__contains"):
                field = key[:-10]
                if field in ['name', 'email']:
                    where_clauses.append(f"{field} LIKE ?")
                    params.append(f"%{value}%")
            else:
                if key in ['name', 'age', 'email']:
                    where_clauses.append(f"{key} = ?")
                    params.append(value)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY id"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

class DataipaseQuery(BaseModel):
    """结构化的数据库查询请求"""
    table_name: str = Field(description="要查询的表名")
    columns: Optional[List[str]] = Field(
        description="要查询的列名列表，为空则查所有列",default=None
    )
    condition: Optional[str] = Field(
        description="WHERE 条件, 'age > 18", default=None
    )
    limit: int = Field(description="返回行数上限",default=20)

class QueryResult(BaseModel):
    """结构化的查询结果"""
    table_name: str = Field(description="查询的表名")
    row_count: int = Field(description="返回的行数")
    columns: List[str] = Field(description="列名列表")
    summary:str=Field(description="查询结果的自然语言摘要")
    has_more:bool= Field(description="是否还有更多数据未返回")

# 准备一个模型
myModel = create_model()

agent = Agent(
    name="agno v0.1",
    model=myModel,
    tools=[
        insert_users,
        query_users,
    ],
    description="你是一个通用Agent，负责回答各类问题或者执行一些力所能及的任务。",
    instructions="如果有符合条件的tool，优先使用tool！",
    debug_mode=True,
    input_schema=DataipaseQuery,
    output_schema=QueryResult,
)

ret = agent.run("看下年龄25岁的都有谁")

print(f"\n\n\n-----------------------------\n运行结果如下：\n{ret.reasoning_content}")

# ----------------- 示例用法 -----------------
# if __name__ == "__main__":
#     # 插入几条数据
#     sample_users = [
#         {"name": "张三", "age": 25, "email": "zhangsan@example.com"},
#         {"name": "李四", "age": 30, "email": "lisi@example.com"},
#         {"name": "王五", "age": 28, "email": "wangwu@example.com"},
#         {"name": "赵六", "age": 25, "email": "zhaoliu@example.com"},
#     ]
#     inserted_count = insert_users(sample_users)
#     print(f"成功插入 {inserted_count} 条记录")
#
#     # 查询所有用户
#     all_users = query_users()
#     print("\n所有用户:")
#     for user in all_users:
#         print(user)
#
#     # 条件查询：精确匹配年龄 25
#     age_25_users = query_users({"age": 25})
#     print("\n年龄为25的用户:")
#     for user in age_25_users:
#         print(user)
#
#     # 模糊查询：名字包含 '张'
#     name_like_users = query_users({"name__contains": "张"})
#     print("\n名字包含'张'的用户:")
#     for user in name_like_users:
#         print(user)
#
#     # 组合条件：年龄 25 并且邮箱包含 'li'
#     complex_users = query_users({"age": 25, "email__contains": "li"})
#     print("\n年龄25且邮箱包含'li'的用户:")
#     for user in complex_users:
#         print(user)