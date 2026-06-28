### 两个概念：
* prompt工程：关注"怎么写"，设计和优化文本，引导模型生成期望输出
* context工程：关注"怎么组装"，设计和控制发送给模型的全部信息结构
* 两者关系：互补关系，写得好但是组装不合理，结果一样不好

### agent.run()到底向LLM发出了什么：
* System Message：Agent 配置自动构建，Agent的"身份证":角色+行为规则
* User Message：用户输入+动态注入，当前任务+***知识库引用***+依赖数据
* Chat History：数据库存储的对话历史，多轮对话连续性
* Additional Input：Few-shot 示例等，训练Agent 的行为模式

### System Message
* description：角色定位，一句话
* instruction：行为指令，做什么、怎么做
* 其他信息（开的越多，token消耗越大，按需开启）
  * add_datetime_to_context=True         # 注入当前时间
  * add_location_to_context=True         # 注入地理位置
  * add_name_to_context=True             # 注入Agent 名称
  * add_session_summary_to_context=True  # 注入会话摘要
  * add_memories_to_context=True         # 注入用户记忆
  * add_session_state_to_context=True    # 注入会话状态

### User Message
* 每次发给Agent的问题
* 其他信息
  * add_knowledge_to_context=True   # 每次run 时检索知识库，相关文档块以<references>标签追加到 user message
    * （如上一章所言，这种属于Traditional RAG，不推荐；推荐做法是Agentic RAG，即search_knowledge=True）
  * dependencies={"key":"val"}      # dependencies 内容以JSON 格式追加到user message，Agent 可在回复中引用

### System Message和User Message区别
* System Message：全局规则，每轮都带
* User Message：单次请求信息

### 历史记忆
* add_history_to_context=True   # 是否加载历史记忆，需要配置db持久化
* num_history_runs=5            # 加载最近5轮，如果5轮对话内调了很多tool，仍然可能导致窗口占满，则需要下一个选项
* max_tool_calls_from_history=2 # 只保留最近 2 次工具调用，这个东西主要是为了防止tool的返回过长，导致窗口被占满

### 关于SESSION ID的问题
* 它是对话history的抓手（注意不是user_id，两者有区别！user_id只是记忆桶的标识）
* 一轮对话中，如果没有手动指定Session id，那么如果agent实例不重启，会有自动的同一个session id
* 一旦Agent重启了，则session id将丢失，所以要想记忆对话历史，应该指定session id或者不重启agent

### Few-shot
* additional_input=[{"role":"user","content":"xxx"},{"role":"assistant","content":"xxx"}]
* 给LLM一些例子，通常效果会比instruction要好

### 如何看到到底发送了什么？
* debug_mode=True







