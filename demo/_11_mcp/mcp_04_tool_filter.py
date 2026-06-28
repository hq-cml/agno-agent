# demo11_03: MCP工具过滤 - include_tools / exclude_tools
# MCP服务器可能提供很多工具，但不是全部都需要
# 通过过滤减少注入到prompt中的工具描述，节省token

import nest_asyncio
nest_asyncio.apply()

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.tools.mcp import MCPTools

myModel = create_model()

async def main():
    # 不过滤：加载所有工具
    print("=== 不过滤（加载所有工具） ===")
    async with MCPTools(
        command="/usr/local/python/bin/uvx mcp-server-fetch",
        timeout_seconds=30,
    ) as mcp:
        all_tools = [t.name for t in mcp.functions.values()]
        print(f"所有工具: {all_tools}")

    # include_tools：只加载指定的工具
    print("\n=== include_tools=['fetch'] ===")
    async with MCPTools(
        command="/usr/local/python/bin/uvx mcp-server-fetch",
        include_tools=["fetch"],  # 只包含fetch工具
        timeout_seconds=30,
    ) as mcp:
        included = [t.name for t in mcp.functions.values()]
        print(f"过滤后工具: {included}")

    # exclude_tools：排除指定的工具
    # 假设某个MCP服务器有多个工具，可以排除不需要的
    print("\n=== exclude_tools=['fetch'] ===")
    async with MCPTools(
        command="/usr/local/python/bin/uvx mcp-server-fetch",
        exclude_tools=["fetch"],  # 排除fetch工具
        timeout_seconds=30,
    ) as mcp:
        excluded = [t.name for t in mcp.functions.values()]
        print(f"排除后工具: {excluded}")  # 应该为空（只有fetch一个工具）

asyncio.run(main())
