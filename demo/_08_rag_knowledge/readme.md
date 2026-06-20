### Agno两种RAG模式：
* Traditional RAG: 每次提问都检索
* Agentic RAG: Agent自主判断是否检索，默认模式（省Token）

### Agno RAG 五个组成部分：
* Contents DB: 存储元信息
* Vector DB: 向量存储和检索
* Embedder: 负责向量化
* Reader: 负责读取
* Reranker: 结果重排

### Agno RAG 选型：
* 开发阶段：chromaDB, LanceDB
* 生产自部署: PgVector, Qdrant
* 云托管: Pinecone, Weaviate

### Agno RAG 分块策略：
* FixedSize：固定长度切割，通用默认
* Recursive：段落句子字符递归，最佳起步
* Semantic：语义相似度分组，混合主题
* Document：按页/节结构拆分，结构化文档
* Markdown：按标题层级拆分，Markdown
* Agentic：LLM决定切分点，最精确成本最高

### Agno RAG 搜索类型与重排：
* Vector：按向量相似度
* KeyWord：按关键字
* Hybrid：混合（推荐）

### Agno RAG 知识过滤：
* 静态过滤：规则写死
* Agentic过滤：LLM自主决定
* 重点：预先打标签，否则无从过滤

### Agno RAG 加载：
* 接口统一，支持多种渠道（重点是打标签）
  * 本地文件
  * URL远程加载


### 参考资料：
* Agno官方的CookBook