# async with - 开发推荐

async with MCPTools(
    command="uvx mcp-server-git"
)as mcp:
    agent = Agent(
        model=openAIResponses (id="gpt-5.5"),
        tools=[mcp],
    )
    await agent.aprint_response("查看提交记录")