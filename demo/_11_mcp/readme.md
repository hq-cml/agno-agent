### Agno接入MCP的2种方式：
* 手动connect/close，精确控制声明周期，在try-finally中手动控制
* async with：自动控制资源清理，代码简介

### Agno MCP的2种传输：
* stidio: 通过command启动，标准输入输出
* streamabel http: 流式响应，远程

### Agno MCP tool 过滤：
* 指定过滤，可以节省token
* include_tools 指定工具
* exclude_tools 排除工具