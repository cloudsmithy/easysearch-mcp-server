# Easysearch MCP Server

<p align="center">
  <a href="https://github.com/infinilabs/easysearch-mcp-server/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://pypi.org/project/easysearch-mcp-server/"><img src="https://img.shields.io/pypi/v/easysearch-mcp-server.svg" alt="PyPI"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python"></a>
</p>

让 AI Agent 能够操作 [INFINI Easysearch](https://infinilabs.com/products/easysearch/)（兼容 Elasticsearch/OpenSearch API）的 MCP 服务器。

## 特性

- 🔧 **118 个工具** - 覆盖集群、索引、文档、搜索、监控等全部功能
- 🔌 **即插即用** - 支持 Kiro、Claude Desktop 等 MCP 客户端
- 🔒 **安全连接** - 支持 HTTPS 和基础认证
- ⚡ **高性能** - 基于 httpx 异步 HTTP 客户端

## 安装

```bash
# PyPI 安装
pip install easysearch-mcp-server

# 或使用 uv
uv pip install easysearch-mcp-server
```

## 快速开始

### 1. 配置 MCP 客户端

**Kiro** (`.kiro/settings/mcp.json`):
```json
{
  "mcpServers": {
    "easysearch": {
      "command": "uvx",
      "args": ["easysearch-mcp-server"],
      "env": {
        "EASYSEARCH_URL": "https://localhost:9200",
        "EASYSEARCH_USER": "admin",
        "EASYSEARCH_PASSWORD": "your-password"
      }
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "easysearch": {
      "command": "uvx",
      "args": ["easysearch-mcp-server"],
      "env": {
        "EASYSEARCH_URL": "https://localhost:9200",
        "EASYSEARCH_USER": "admin",
        "EASYSEARCH_PASSWORD": "your-password"
      }
    }
  }
}
```

### 2. 开始使用

配置完成后，AI Agent 就可以直接操作 Easysearch 了：

- "查看集群健康状态"
- "创建一个 products 索引"
- "搜索价格大于 100 的商品"
- "统计每个分类的订单数量"

## 工具列表

### 集群管理 (8)
| 工具 | 说明 |
|------|------|
| `cluster_health` | 集群健康状态 |
| `cluster_stats` | 集群统计信息 |
| `cluster_state` | 集群状态详情 |
| `cluster_settings` | 获取集群设置 |
| `cluster_update_settings` | 更新集群设置 |
| `cluster_pending_tasks` | 待处理任务 |
| `cluster_allocation_explain` | 分片分配解释 |
| `cluster_reroute` | 手动路由分片 |

### 索引管理 (25)
| 工具 | 说明 |
|------|------|
| `index_create` | 创建索引 |
| `index_delete` | 删除索引 |
| `index_exists` | 检查索引是否存在 |
| `index_get` | 获取索引详情 |
| `index_get_mapping` | 获取映射 |
| `index_put_mapping` | 更新映射 |
| `index_get_settings` | 获取设置 |
| `index_put_settings` | 更新设置 |
| `index_open` | 打开索引 |
| `index_close` | 关闭索引 |
| `index_refresh` | 刷新索引 |
| `index_flush` | 刷盘 |
| `index_forcemerge` | 强制合并段 |
| `index_clear_cache` | 清除缓存 |
| `index_stats` | 索引统计 |
| `index_segments` | 段信息 |
| `index_recovery` | 恢复状态 |
| `index_shard_stores` | 分片存储信息 |
| `index_set_readonly` | 设置只读（clone/split/shrink 前置条件）|
| `index_prepare_for_shrink` | 准备收缩（shrink 前置条件）|
| `index_create_with_write_alias` | 创建带可写别名的索引（rollover 前置条件）|
| `index_clone` | 克隆索引 |
| `index_split` | 拆分索引 |
| `index_shrink` | 收缩索引 |
| `index_rollover` | 滚动索引 |

### 别名管理 (4)
| 工具 | 说明 |
|------|------|
| `alias_get` | 获取别名 |
| `alias_create` | 创建别名 |
| `alias_delete` | 删除别名 |
| `alias_actions` | 批量别名操作 |

### 模板管理 (3)
| 工具 | 说明 |
|------|------|
| `template_get` | 获取模板 |
| `template_create` | 创建模板 |
| `template_delete` | 删除模板 |

### 文档操作 (11)
| 工具 | 说明 |
|------|------|
| `doc_index` | 写入文档 |
| `doc_get` | 获取文档 |
| `doc_exists` | 检查文档是否存在 |
| `doc_delete` | 删除文档 |
| `doc_update` | 更新文档 |
| `doc_bulk` | 批量操作 |
| `doc_bulk_simple` | 简化批量写入 |
| `doc_mget` | 批量获取 |
| `doc_source` | 获取文档源 |
| `doc_delete_by_query` | 按查询删除 |
| `doc_update_by_query` | 按查询更新 |

### 搜索功能 (16)
| 工具 | 说明 |
|------|------|
| `search` | DSL 搜索 |
| `search_simple` | 简单关键词搜索 |
| `search_template` | 模板搜索 |
| `msearch` | 多重搜索 |
| `count` | 文档计数 |
| `validate_query` | 验证查询 |
| `explain` | 解释评分 |
| `aggregate` | 聚合查询 |
| `aggregate_simple` | 简化聚合 |
| `scroll_start` | 开始滚动搜索 |
| `scroll_next` | 获取下一批 |
| `scroll_clear` | 清除滚动上下文 |
| `field_caps` | 字段能力 |
| `knn_search` | 向量搜索 |
| `sql_query` | SQL 查询 |
| `sql_translate` | SQL 转 DSL（Easysearch 不支持）|

### CAT API (18)
| 工具 | 说明 |
|------|------|
| `cat_health` | 集群健康 |
| `cat_nodes` | 节点列表 |
| `cat_indices` | 索引列表 |
| `cat_shards` | 分片分布 |
| `cat_allocation` | 磁盘分配 |
| `cat_thread_pool` | 线程池状态 |
| `cat_master` | 主节点信息 |
| `cat_segments` | 段信息 |
| `cat_count` | 文档计数 |
| `cat_recovery` | 恢复状态 |
| `cat_pending_tasks` | 待处理任务 |
| `cat_aliases` | 别名列表 |
| `cat_templates` | 模板列表 |
| `cat_plugins` | 插件列表 |
| `cat_fielddata` | Fielddata 使用 |
| `cat_nodeattrs` | 节点属性 |
| `cat_repositories` | 快照仓库 |
| `cat_snapshots` | 快照列表 |
| `cat_tasks` | 任务列表 |

### 节点管理 (5)
| 工具 | 说明 |
|------|------|
| `nodes_info` | 节点信息 |
| `nodes_stats` | 节点统计 |
| `nodes_hot_threads` | 热点线程 |
| `nodes_usage` | 功能使用统计 |
| `nodes_reload_secure_settings` | 重载安全设置 |

### 快照管理 (10)
| 工具 | 说明 |
|------|------|
| `snapshot_repo_create` | 创建仓库 |
| `snapshot_repo_get` | 获取仓库 |
| `snapshot_repo_delete` | 删除仓库 |
| `snapshot_repo_verify` | 验证仓库 |
| `snapshot_create` | 创建快照 |
| `snapshot_get` | 获取快照 |
| `snapshot_status` | 快照状态 |
| `snapshot_delete` | 删除快照 |
| `snapshot_restore` | 恢复快照 |
| `snapshot_clone` | 克隆快照 |

### 快照生命周期管理 SLM (6)
| 工具 | 说明 |
|------|------|
| `slm_policy_create` | 创建策略 |
| `slm_policy_get` | 获取策略 |
| `slm_policy_delete` | 删除策略 |
| `slm_policy_explain` | 解释策略 |
| `slm_policy_start` | 启动策略 |
| `slm_policy_stop` | 停止策略 |

### 任务管理 (3)
| 工具 | 说明 |
|------|------|
| `tasks_list` | 任务列表 |
| `tasks_get` | 任务详情 |
| `tasks_cancel` | 取消任务 |

### Ingest Pipeline (6)
| 工具 | 说明 |
|------|------|
| `pipeline_get` | 获取 Pipeline |
| `pipeline_create` | 创建 Pipeline |
| `pipeline_delete` | 删除 Pipeline |
| `pipeline_simulate` | 模拟 Pipeline |
| `ingest_stats` | Ingest 统计 |
| `ingest_processor_grok` | Grok 模式列表 |

### 其他 (1)
| 工具 | 说明 |
|------|------|
| `reindex` | 重建索引 |

## 使用示例

### 集群监控
```
查看集群健康状态
→ cluster_health()

查看所有节点
→ cat_nodes()

查看线程池状态
→ cat_thread_pool()

按大小排序查看索引
→ cat_indices(sort_by="store.size", order="desc")
```

### 索引操作
```
创建索引
→ index_create("products", 
    mappings={"properties": {"name": {"type": "text"}, "price": {"type": "float"}}},
    settings={"number_of_shards": 3})

写入文档
→ doc_index("products", {"name": "iPhone", "price": 999})

批量写入
→ doc_bulk_simple("products", [
    {"name": "iPad", "price": 799},
    {"name": "MacBook", "price": 1299}
])
```

### 搜索查询
```
简单搜索
→ search_simple("products", "iPhone")

DSL 搜索
→ search("products", query={
    "bool": {
        "must": [{"match": {"name": "phone"}}],
        "filter": [{"range": {"price": {"lte": 1000}}}]
    }
})

聚合统计
→ aggregate("orders", aggs={
    "by_status": {"terms": {"field": "status"}},
    "avg_amount": {"avg": {"field": "amount"}}
})

SQL 查询
→ sql_query("SELECT * FROM products WHERE price > 500 ORDER BY price DESC")
```

### 索引克隆/拆分/收缩
```
# 克隆索引（需要先设置只读）
→ index_set_readonly("my-index", True)
→ index_clone("my-index", "my-index-clone")
→ index_set_readonly("my-index", False)

# 收缩索引（需要准备）
→ index_prepare_for_shrink("my-index")
→ index_shrink("my-index", "my-index-shrunk", {"index.number_of_shards": 1})

# 滚动索引（需要可写别名）
→ index_create_with_write_alias("logs-000001", "logs")
→ index_rollover("logs", conditions={"max_docs": 1000000})
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `EASYSEARCH_URL` | Easysearch 地址 | `https://localhost:9200` |
| `EASYSEARCH_USER` | 用户名 | `admin` |
| `EASYSEARCH_PASSWORD` | 密码 | - |

## 开发

```bash
# 克隆仓库
git clone https://github.com/infinilabs/easysearch-mcp-server.git
cd easysearch-mcp-server

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
ruff check src/
```

## 许可证

MIT License
