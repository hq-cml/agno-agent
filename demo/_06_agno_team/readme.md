### 单Agent的瓶颈：

* 工具过多，容易调用混了
* 指令互相干扰
* 无法并行

### Team的原则
分而治之

### Team角色
* Leader：本身也是一个Agent，负责分发任务
* Member：也是一个Agent，负责具体领域，工具等也只配备必要的

### 四种模式
* 协调模式：Leader负责分配任务，按需选择Member，Member执行任务，最终返回结果，由Leader汇总（默认模式）
* 路由模式：Leader负责分配任务，根据任务只会选一个最合适的Member负责执行任务，最终返回结果，各个Member直接返回，Leader不做聚合加工（适用于完全并行无关联的任务，比如多语言翻译）
* 广播模式：Leader不分析任务，而是直接广播给所有Member，Member执行任务各自给出专业领域结论，Leader负责最终的决策、评审、聚合（适用场景如团队讨论）
* 任务模式：Leader将任务拆分成子任务列表，分配给Member执行并追踪结果，可多轮迭代，直到所有子任务完成（试用场景：项目规划、复杂任务；例如cursor、opencode这类agent，就是这种模式）

### 实践建议
* 每个Agent分配工具不要过多
* 每个Member拥有清晰的role和instructions
* 开启show_members_responses
* 复杂任务可以嵌套Team
* db持久化