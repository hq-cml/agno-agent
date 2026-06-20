# 手动建立连接

mcp = MCPTools(command="uvx mcp-server-git")

await mcp.connect() #建立连接

try:
    agent = Agent(
        model=0penAIResponses (),
        tools=[mcp]
    )
    await agent.aprint_response("查看最近提交")
finally:
    await mcp.close()  #保证释放