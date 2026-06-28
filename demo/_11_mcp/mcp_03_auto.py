# demo11_03: MCP基础 - async with 自动管理（推荐写法）
# 与 mcp_01 功能相同，但用 async with 自动处理connect/close
# 代码更简洁，不用担心忘记close导致资源泄漏

import nest_asyncio
nest_asyncio.apply()

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.tools.mcp import MCPTools

myModel = create_model()

async def main():
    # async with 自动管理连接（进入时connect，退出时close）
    async with MCPTools(
        command="/usr/local/python/bin/uvx mcp-server-fetch", # 本地启动mcp server
        timeout_seconds=30,
    ) as mcp:
        print(f"可用工具: {[t.name for t in mcp.functions.values()]}")

        agent = Agent(
            model=myModel,
            tools=[mcp],
            instructions=["简洁回答，用中文"],
        )
        await agent.aprint_response("用fetch获取 https://httpbin.org/ip 告诉我IP地址是什么")

asyncio.run(main())
