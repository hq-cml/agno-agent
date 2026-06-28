# demo11_04: 多MCP服务器 - 一个Agent同时使用多个MCP服务器的工具
# MultiMCPTools 可以同时连接多个MCP服务器，Agent能使用所有服务器的工具

import nest_asyncio
nest_asyncio.apply()

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools

myModel = create_model()

async def main():
    # 同时连接多个MCP服务器（这里用两个fetch实例演示，实际可以是不同服务器）
    async with MultiMCPTools(
        commands=[
            "/usr/local/python/bin/uvx mcp-server-fetch",
            "/usr/local/python/bin/uvx mcp-server-time",
            "npx -y @modelcontextprotocol/server-filesystem /tmp",
        ],
        timeout_seconds=30,
    ) as mcp:
        tools = [t.name for t in mcp.functions.values()]
        print(f"所有MCP服务器提供的工具: {tools}")

        agent = Agent(
            model=myModel,
            tools=[mcp],
            instructions=["简洁回答，用中文"],
        )
        await agent.aprint_response("用fetch获取 https://httpbin.org/user-agent 的内容")

asyncio.run(main())
