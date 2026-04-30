# 中医图谱·智能问诊 (TCM-GraphRAG)

本项目是一个基于 **Text2Cypher** 架构的中医知识图谱智能问诊系统。
彻底抛弃了传统的“向量检索(Vector RAG)”与“固定状态机”，采用大模型 Agent 实时将用户的自然语言转化为 Cypher 图数据库查询语句，实现多跳逻辑推理与精准的数据抓取。

## 核心技术栈
* **前端交互**: Streamlit (提供极简、跨平台的 WebUI)
* **核心中枢**: n8n (Tools Agent 智能体架构)
* **知识图谱**: Neo4j (存储 1800+ 节点，4000+ 关系，涵盖疾病、症状、方剂、药材)
* **大语言模型**: DeepSeek Chat API

## 快速部署指南

### 1. 准备图数据库 (Neo4j)
1. 启动 Neo4j 社区版实例（推荐使用 Docker 或本地安装）。
2. 运行 `data_pipeline/kg_builder.py` 脚本，将中医基础数据写入数据库，完成图谱初始化。

### 2. 部署 AI 智能体 (n8n)
1. 安装并启动 n8n。
2. 在 n8n 界面选择 `Import from File`，导入 `backend_n8n/TCM_Agent_Workflow.json`。

###  3.导入数据库 

​	这里有两种方法

1. 直接导入：导入neo4j_data目录里的```neo4j.dump``` 文件到neo4j里面，这里可能需要其他工具
2. 使用脚本：请阅读data_pipeline里的代码，根据自己的环境修改内容，再将自己的txt文本命名为```xiaoer.txt```,运行```kg_builder.py```，即可导入自己的知识图谱

### 4.运行项目前端

1. 运行```frontend.py```，可能需要修改配置，依据你自己的环境来。之后打开```ip:8501```即可展示前端界面。

### 一些注意事项

1. **关键配置**:
   * 打开 `HTTP Request Tool` 节点，修改 URL 为你的 Neo4j 地址（默认 `http://localhost:7474/db/neo4j/tx/commit`）。
   * 配置 Neo4j 的 Basic Auth 账号密码。
   * 配置 OpenAI/DeepSeek 节点的 API Key。
2. 将工作流右上角的开关设置为 **Published (Active)**。
3. 双击 `Chat Trigger` 节点，复制其 Production URL。

### 3. 启动问诊终端 (Streamlit)
1. 进入前端目录并安装硬核兼容依赖：
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. 修改 `frontend.py` 中的 `webhook_url`，将其替换为你刚才在 n8n 中复制的地址。

3. 点火启动：

```Bash
streamlit run frontend.py
```

4. 打开浏览器访问 `http://localhost:8501`，开始问诊。

### 4.配置n8n

- n8n 的 Webhook URL 必须是纯正的 API 模式，绝对不可包含 `/chat` 网页路由后缀（除非使用 Embedded 模式）。
- 为了保障 JSON 解析稳定性，n8n 工具节点内已内置 `JSON.stringify` 强转义逻辑。