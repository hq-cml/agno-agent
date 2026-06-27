### Agno两种RAG模式：
* Traditional RAG: 每次提问都检索并将检索结果追加到context
* Agentic RAG: 默认模式（省Token），Agent自主判断是否检索，无关问题不被追加到context

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

### Agno RAG 搜索类型：
* Vector：语义（向量）相似度，适合意图模糊的问题
* KeyWord：关键字匹配，适合精确术语查询
* Hybrid：两者结合（推荐），兼顾语义和精确匹配

### Agno RAG 知识检索&过滤：
* 静态过滤：规则写死
* Agentic过滤：LLM自主决定
* 重点：预先打标签，否则无从过滤

### Agno RAG 加载：
* 接口统一，支持多种渠道（重点是加载的同时打标签）
  * 本地文件加载
  * URL远程加载


