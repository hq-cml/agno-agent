# demo11_02: MCP基础 - 手动管理连接生命周期
# MCP (Model Context Protocol) 让 Agent 能使用外部工具服务器提供的工具
# 手动connect/close方式：适合需要精确控制连接时机的场景

import nest_asyncio
nest_asyncio.apply()

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.tools.mcp import MCPTools

myModel = create_model()

async def main():
    # 创建MCP连接（stdio模式：通过命令启动本地MCP服务器进程）
    # mcp-server-fetch 提供一个 "fetch" 工具，能抓取URL内容
    mcp = MCPTools(
        command="/usr/local/python/bin/uvx mcp-server-fetch", # 本地启动mcp server
        timeout_seconds=30,
    )

    # 手动管理连接生命周期
    await mcp.connect()
    try:
        # 查看MCP服务器提供了哪些工具
        tools = [t.name for t in mcp.functions.values()]
        print(f"MCP服务器提供的工具: {tools}")

        # 创建Agent并挂载MCP工具
        agent = Agent(
            model=myModel,
            tools=[mcp],
            instructions=["简洁回答，用中文"],
        )

        # Agent会自动调用fetch工具来获取URL内容
        await agent.aprint_response("用fetch获取 https://httpbin.org/headers 的内容，简要说明返回了什么")
    finally:
        # 保证资源释放（即使出错也要close）
        await mcp.close()

asyncio.run(main())
