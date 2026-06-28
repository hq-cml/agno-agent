# demo11_01: 远程MCP服务器 - Streamable HTTP传输
# 与 stdio 模式不同，这里不启动本地进程，而是直接连接远程MCP服务器
# 传输方式：streamable-http（通过URL连接，适合云端部署的MCP服务）

import nest_asyncio
nest_asyncio.apply()

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.tools.mcp import MCPTools

myModel = create_model()

async def main():
    # 远程MCP服务器：DeepWiki（开源项目文档查询服务）
    # 通过url参数连接，无需本地启动任何进程
    async with MCPTools(
        url="https://mcp.deepwiki.com/mcp",  # 远程MCP服务器地址
        # transport 会自动设为 "streamable-http"（因为提供了url）
        timeout_seconds=30,
    ) as mcp:
        tools = [t.name for t in mcp.functions.values()]
        print(f"远程MCP服务器提供的工具: {tools}")
        # 输出: ['read_wiki_structure', 'read_wiki_contents', 'ask_question']

        agent = Agent(
            model=myModel,
            tools=[mcp],
            instructions=["简洁回答，用中文，100字以内"],
        )

        # Agent自动调用远程MCP工具查询开源项目文档
        await agent.aprint_response(
            "用read_wiki_structure查看 agno-agi/agno 这个项目有哪些主要章节",
        )

asyncio.run(main())
