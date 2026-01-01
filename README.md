# Easysearch MCP Server

让 AI Agent 能够操作 [INFINI Easysearch](https://infinilabs.com/products/easysearch/)（兼容 Elasticsearch/OpenSearch API）的 MCP 服务器。

## 工具测试结果

共 115 个工具，测试结果如下：

### ✅ 已验证工具（100+）

| 分类 | 工具 | 状态 |
|------|------|------|
| **集群管理** | `cluster_health`, `cluster_stats`, `cluster_state`, `cluster_settings`, `cluster_update_settings`, `cluster_pending_tasks`, `cluster_allocation_explain`, `cluster_reroute` | ✅ |
| **索引管理** | `index_create`, `index_delete`, `index_exists`, `index_get`, `index_get_mapping`, `index_put_mapping`, `index_get_settings`, `index_put_settings`, `index_open`, `index_close`, `index_refresh`, `index_flush`, `index_forcemerge`, `index_clear_cache`, `index_stats`, `index_segments`, `index_recovery`, `index_shard_stores` | ✅ |
| **文档操作** | `doc_index`, `doc_get`, `doc_exists`, `doc_delete`, `doc_update`, `doc_bulk`, `doc_bulk_simple`, `doc_mget`, `doc_source`, `doc_delete_by_query`, `doc_update_by_query` | ✅ |
| **搜索功能** | `search`, `search_simple`, `search_template`, `msearch`, `count`, `validate_query`, `explain`, `aggregate`, `aggregate_simple`, `scroll_start`, `scroll_next`, `scroll_clear`, `field_caps`, `sql_query` | ✅ |
| **CAT API** | `cat_health`, `cat_nodes`, `cat_indices`, `cat_shards`, `cat_allocation`, `cat_thread_pool`, `cat_master`, `cat_segments`, `cat_count`, `cat_recovery`, `cat_pending_tasks`, `cat_aliases`, `cat_templates`, `cat_plugins`, `cat_fielddata`, `cat_nodeattrs`, `cat_repositories`, `cat_tasks` | ✅ |
| **节点管理** | `nodes_info`, `nodes_stats`, `nodes_hot_threads`, `nodes_usage`, `nodes_reload_secure_settings` | ✅ |
| **别名管理** | `alias_get`, `alias_create`, `alias_delete`, `alias_actions` | ✅ |
| **模板管理** | `template_get`, `template_create`, `template_delete` | ✅ |
| **Pipeline** | `pipeline_get`, `pipeline_create`, `pipeline_delete`, `pipeline_simulate`, `ingest_stats`, `ingest_processor_grok` | ✅ |
| **任务管理** | `tasks_list`, `tasks_cancel` | ✅ |
| **快照管理** | `snapshot_repo_get`, `snapshot_get`, `snapshot_status` | ✅ |
| **SLM** | `slm_policy_get`, `slm_policy_explain` | ✅ |
| **其他** | `reindex` | ✅ |

### ⚠️ 需要前置条件的工具

| 工具 | 说明 |
|------|------|
| `index_clone`, `index_split`, `index_shrink` | 需要源索引设置为只读 |
| `index_rollover` | 需要别名指向可写索引 |
| `snapshot_repo_create`, `snapshot_create`, `snapshot_restore`, `snapshot_delete`, `snapshot_clone` | 需要配置快照仓库路径 |
| `slm_policy_create`, `slm_policy_delete`, `slm_policy_start`, `slm_policy_stop` | 需要有效的快照仓库 |
| `knn_search` | 需要索引包含向量字段 |
| `cat_snapshots` | 需要快照仓库存在 |
| `tasks_get` | 需要有效的任务 ID |
| `scroll_clear` | 需要有效的 scroll_id |

### ❌ Easysearch 不支持的 API

| 工具 | 说明 |
|------|------|
| `sql_translate` | Easysearch 不支持 `/_sql/translate` 端点 |
| `terms_enum` | Easysearch 不支持 `/_terms_enum` API |

## 功能特性

### 集群管理
- `cluster_health` - 集群健康状态
- `cluster_stats` - 集群统计信息
- `cluster_state` - 集群状态
- `cluster_settings` - 获取/更新集群设置
- `cluster_pending_tasks` - 待处理任务
- `cluster_allocation_explain` - 分片分配解释
- `cluster_reroute` - 手动路由分片

### 索引管理
- `index_create/delete/exists/get` - 索引 CRUD
- `index_get_mapping/put_mapping` - 映射管理
- `index_get_settings/put_settings` - 设置管理
- `index_open/close` - 开关索引
- `index_refresh/flush/forcemerge` - 索引维护
- `index_clear_cache` - 清除缓存
- `index_stats/segments/recovery` - 索引统计
- `index_clone/split/shrink/rollover` - 索引操作
- `alias_*` - 别名管理
- `template_*` - 模板管理
- `reindex` - 重建索引

### 文档操作
- `doc_index/get/delete/update` - 文档 CRUD
- `doc_bulk/bulk_simple` - 批量操作
- `doc_mget` - 批量获取
- `doc_delete_by_query/update_by_query` - 按查询操作
- `doc_source` - 获取文档源

### 搜索功能
- `search` - DSL 搜索
- `search_simple` - 简单关键词搜索
- `search_template` - 模板搜索
- `msearch` - 多重搜索
- `count` - 文档计数
- `validate_query` - 验证查询
- `explain` - 解释评分
- `aggregate/aggregate_simple` - 聚合查询
- `scroll_*` - 滚动搜索
- `knn_search` - 向量搜索
- `sql_query/sql_translate` - SQL 查询

### CAT API（监控）
- `cat_health/nodes/indices/shards` - 基础信息
- `cat_allocation` - 磁盘分配
- `cat_thread_pool` - 线程池状态
- `cat_segments/count/recovery` - 索引信息
- `cat_aliases/templates/plugins` - 配置信息
- `cat_tasks/pending_tasks` - 任务信息

### 节点管理
- `nodes_info` - 节点信息
- `nodes_stats` - 节点统计
- `nodes_hot_threads` - 热点线程
- `nodes_usage` - 功能使用统计

### 快照恢复
- `snapshot_repo_*` - 仓库管理
- `snapshot_create/get/delete` - 快照管理
- `snapshot_restore/clone` - 恢复和克隆

### 快照生命周期管理 (SLM)
- `slm_policy_create` - 创建自动快照策略
- `slm_policy_get` - 获取策略
- `slm_policy_delete` - 删除策略
- `slm_policy_explain` - 解释策略（查看下次执行时间）
- `slm_policy_start/stop` - 启停策略

### 任务管理
- `tasks_list/get/cancel` - 任务操作

### Ingest Pipeline
- `pipeline_*` - Pipeline 管理
- `ingest_stats` - Ingest 统计

## 安装

```bash
# 使用 pip
pip install easysearch-mcp-server

# 或使用 uv
uv pip install easysearch-mcp-server
```

## 配置

### 环境变量

```bash
export EASYSEARCH_URL="https://localhost:9200"
export EASYSEARCH_USER="admin"
export EASYSEARCH_PASSWORD="your-password"
```

### Kiro MCP 配置

在 `.kiro/settings/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "easysearch": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/easysearch-mcp-server", "easysearch-mcp"],
      "env": {
        "EASYSEARCH_URL": "https://localhost:9200",
        "EASYSEARCH_USER": "admin",
        "EASYSEARCH_PASSWORD": "your-password"
      }
    }
  }
}
```

## 使用示例

### 集群监控

```python
# 检查集群健康
cluster_health()

# 查看节点状态
cat_nodes()

# 查看线程池
cat_thread_pool()

# 查看索引列表
cat_indices(sort_by="store.size", order="desc")
```

### 索引操作

```python
# 创建索引
index_create("products", 
    mappings={"properties": {"name": {"type": "text"}, "price": {"type": "float"}}},
    settings={"number_of_shards": 3}
)

# 写入文档
doc_index("products", {"name": "iPhone", "price": 999})

# 批量写入
doc_bulk_simple("products", [
    {"name": "iPad", "price": 799},
    {"name": "MacBook", "price": 1299}
])
```

### 搜索查询

```python
# 简单搜索
search_simple("products", "iPhone")

# DSL 搜索
search("products", query={
    "bool": {
        "must": [{"match": {"name": "phone"}}],
        "filter": [{"range": {"price": {"lte": 1000}}}]
    }
})

# 聚合统计
aggregate("orders", aggs={
    "by_status": {"terms": {"field": "status"}},
    "avg_amount": {"avg": {"field": "amount"}}
})

# SQL 查询
sql_query("SELECT * FROM products WHERE price > 500 ORDER BY price DESC")
```

### 快照备份

```python
# 创建仓库
snapshot_repo_create("my_backup", "fs", {"location": "/backups"})

# 创建快照
snapshot_create("my_backup", "snapshot_1", indices=["products", "orders"])

# 恢复快照
snapshot_restore("my_backup", "snapshot_1", indices=["products"])
```

### 快照生命周期管理

```python
# 创建每日备份策略
slm_policy_create("daily-backup", "每日备份", "my_backup",
    creation_schedule="0 2 * * *",  # 每天凌晨 2 点
    max_age="30d",
    max_count=30
)

# 查看策略详情
slm_policy_get("daily-backup")

# 查看下次执行时间
slm_policy_explain("daily*")

# 启停策略
slm_policy_start("daily-backup")
slm_policy_stop("daily-backup")
```

## 开发

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
ruff check src/

# 类型检查
mypy src/
```

## 许可证

MIT License
# easysearch-mcp-server
