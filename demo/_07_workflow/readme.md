### 工作流的最大特点：
* 确定性！
* 有一些工作必须是按部就班的，所以不能随意用Agent和Team去实现，因为那会引入随机性

### 关于Step
* Step：最小执行单元
  * 每个step套结一个唯一的执行器，职责单一
  * 执行器有3种类型：agent、team、function
* StepInput：步骤的输入
  * 有如下关键参数
  * input:当前步骤收到的输入(字符串、字典或Pydantic模型)
  * previous_step_content:上一步 StepOutput 的 content 字段,最常用
  * previous_step_outputs:所有前序步骤的完整输出字典，key是步骤名
* StepOutput，步骤的输出
  * 如下关键参数
  * content: 输出内容
  * success: bool是否成功
  * stop: bool是否终止整个工作流
* Step串联
  * StepA的StepOutput.content --> StepB的StepInput.previous_step_content

### 关于Steps
* Step容器串联
  * 把一组Step封装成一个整体，带来如下特性
    * 复用:同一个Steps 可以在多个Workflow 中引用
    * 封装:对外暴露一个名称，隐藏内部细节
    * 组合:可以和其他Step、Condition、Loop混搭
* Workflow 的steps 列表中
  * 可以直接放Step 对象
  * 也可以放 Steps、Agent、Team
  * 甚至callable 函数--框架会自动包装。

### 四类控制流程
* Condition：条件if else
* Parallel：并行化
* Loop：循环
* Router：动态路由，根据运行时条件动态决定下一步骤
  * (与Condition的区别：Condition是二选一(if/else)，Router可以多选一甚至多选多)

### Session State
* 之前介绍的Input和Output，是串行的数据共享
* 要实现多步骤之间的数据共享，需要使用Session State
* 利用db实现

### Structured IO
* 结构化的IO：input_schema & output_schma
* 使用pydantic类，避免脏数据全流程污染

### Workflow嵌套
* 嵌套工作流，可以利用Steps 容器，将工作流封装成一个Steps，然后在另一个工作流中引用
* 嵌套的优势：1.复用 2.封装（内部细节屏蔽） 3.独立测试

### WorkfllowAgent
* 传统的workflow，每次都是从头到尾执行
* workflow_agent可以职能判断哪些步骤不需要重复执行

### CEL表达式

### 安全护栏
* 在步骤执行前/后进行安全检查
* 通过pre_hooks/post_hooks机制，拦截危险输入或不合规输出

### Early Stopping提前终止 
* 检测到异常时立即中断流程
* 通过StepOutput(stop=True)实现，后续步骤将不再执行

### Human in the Loop (HITL)
* 关键步骤要求人工确认