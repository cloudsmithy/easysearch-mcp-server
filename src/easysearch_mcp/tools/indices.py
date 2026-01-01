"""
索引管理相关工具
"""

import json
from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_indices_tools(mcp: FastMCP):
    """注册索引管理工具"""
    
    @mcp.tool()
    def index_create(index: str, mappings: dict = None, settings: dict = None, aliases: dict = None) -> dict:
        """
        创建索引
        
        参数:
            index: 索引名称
            mappings: 字段映射定义
            settings: 索引设置（分片数、副本数等）
            aliases: 别名定义
        
        示例:
            index_create("products", 
                mappings={"properties": {"name": {"type": "text"}, "price": {"type": "float"}}},
                settings={"number_of_shards": 3, "number_of_replicas": 1}
            )
        """
        client = get_client()
        body = {}
        if mappings:
            body["mappings"] = mappings
        if settings:
            body["settings"] = settings
        if aliases:
            body["aliases"] = aliases
        return client.put(f"/{index}", body if body else None)
    
    @mcp.tool()
    def index_delete(index: str) -> dict:
        """
        删除索引（危险操作）
        
        参数:
            index: 索引名称，支持通配符如 logs-*
        """
        client = get_client()
        return client.delete(f"/{index}")
    
    @mcp.tool()
    def index_exists(index: str) -> bool:
        """
        检查索引是否存在
        
        参数:
            index: 索引名称
        """
        client = get_client()
        return client.head(f"/{index}")
    
    @mcp.tool()
    def index_get(index: str) -> dict:
        """
        获取索引详情（mappings、settings、aliases）
        
        参数:
            index: 索引名称，支持通配符
        """
        client = get_client()
        return client.get(f"/{index}")
    
    @mcp.tool()
    def index_get_mapping(index: str) -> dict:
        """
        获取索引映射
        
        参数:
            index: 索引名称
        """
        client = get_client()
        return client.get(f"/{index}/_mapping")
    
    @mcp.tool()
    def index_put_mapping(index: str, properties: dict, dynamic: str = None) -> dict:
        """
        更新索引映射（只能添加字段，不能修改已有字段）
        
        参数:
            index: 索引名称
            properties: 字段定义
            dynamic: 动态映射策略 true/false/strict
        
        示例:
            index_put_mapping("products", 
                properties={"category": {"type": "keyword"}}
            )
        """
        client = get_client()
        body = {"properties": properties}
        if dynamic:
            body["dynamic"] = dynamic
        return client.put(f"/{index}/_mapping", body)
    
    @mcp.tool()
    def index_get_settings(index: str, include_defaults: bool = False) -> dict:
        """
        获取索引设置
        
        参数:
            index: 索引名称
            include_defaults: 是否包含默认设置
        """
        client = get_client()
        params = {"include_defaults": "true"} if include_defaults else None
        return client.get(f"/{index}/_settings", params)
    
    @mcp.tool()
    def index_put_settings(index: str, settings: dict) -> dict:
        """
        更新索引设置
        
        参数:
            index: 索引名称
            settings: 设置项
        
        示例:
            index_put_settings("products", {"index.refresh_interval": "30s"})
        """
        client = get_client()
        return client.put(f"/{index}/_settings", settings)
    
    @mcp.tool()
    def index_open(index: str) -> dict:
        """
        打开索引
        
        参数:
            index: 索引名称
        """
        client = get_client()
        return client.post(f"/{index}/_open")
    
    @mcp.tool()
    def index_close(index: str) -> dict:
        """
        关闭索引（关闭后无法读写，但保留数据）
        
        参数:
            index: 索引名称
        """
        client = get_client()
        return client.post(f"/{index}/_close")
    
    @mcp.tool()
    def index_refresh(index: str = None) -> dict:
        """
        刷新索引（使最近写入的文档可搜索）
        
        参数:
            index: 索引名称（可选，不传则刷新所有）
        """
        client = get_client()
        path = f"/{index}/_refresh" if index else "/_refresh"
        return client.post(path)
    
    @mcp.tool()
    def index_flush(index: str = None, force: bool = False) -> dict:
        """
        刷新索引到磁盘
        
        参数:
            index: 索引名称（可选）
            force: 是否强制刷新
        """
        client = get_client()
        path = f"/{index}/_flush" if index else "/_flush"
        params = {"force": "true"} if force else None
        return client.post(path, params=params)
    
    @mcp.tool()
    def index_forcemerge(index: str = None, max_num_segments: int = None, only_expunge_deletes: bool = False) -> dict:
        """
        强制合并索引段
        
        参数:
            index: 索引名称（可选）
            max_num_segments: 合并到的最大段数
            only_expunge_deletes: 仅清除已删除文档
        
        注意：这是资源密集型操作，建议在低峰期执行
        """
        client = get_client()
        path = f"/{index}/_forcemerge" if index else "/_forcemerge"
        params = {}
        if max_num_segments:
            params["max_num_segments"] = max_num_segments
        if only_expunge_deletes:
            params["only_expunge_deletes"] = "true"
        return client.post(path, params=params or None)
    
    @mcp.tool()
    def index_clear_cache(index: str = None, fielddata: bool = False, query: bool = False, request: bool = False) -> dict:
        """
        清除索引缓存
        
        参数:
            index: 索引名称（可选）
            fielddata: 清除 fielddata 缓存
            query: 清除查询缓存
            request: 清除请求缓存
        """
        client = get_client()
        path = f"/{index}/_cache/clear" if index else "/_cache/clear"
        params = {}
        if fielddata:
            params["fielddata"] = "true"
        if query:
            params["query"] = "true"
        if request:
            params["request"] = "true"
        return client.post(path, params=params or None)
    
    @mcp.tool()
    def index_stats(index: str = None, metric: str = None) -> dict:
        """
        获取索引统计信息
        
        参数:
            index: 索引名称（可选）
            metric: 指标类型 docs/store/indexing/get/search/merge/refresh/flush/warmer/query_cache/fielddata/completion/segments/translog
        """
        client = get_client()
        parts = []
        if index:
            parts.append(index)
        parts.append("_stats")
        if metric:
            parts.append(metric)
        return client.get("/" + "/".join(parts))
    
    @mcp.tool()
    def index_segments(index: str = None) -> dict:
        """
        获取索引段信息
        
        参数:
            index: 索引名称（可选）
        """
        client = get_client()
        path = f"/{index}/_segments" if index else "/_segments"
        return client.get(path)
    
    @mcp.tool()
    def index_recovery(index: str = None, active_only: bool = False) -> dict:
        """
        获取索引恢复状态
        
        参数:
            index: 索引名称（可选）
            active_only: 仅显示进行中的恢复
        """
        client = get_client()
        path = f"/{index}/_recovery" if index else "/_recovery"
        params = {"active_only": "true"} if active_only else None
        return client.get(path, params)
    
    @mcp.tool()
    def index_shard_stores(index: str = None, status: str = None) -> dict:
        """
        获取分片存储信息
        
        参数:
            index: 索引名称（可选）
            status: 状态过滤 green/yellow/red/all
        """
        client = get_client()
        path = f"/{index}/_shard_stores" if index else "/_shard_stores"
        params = {"status": status} if status else None
        return client.get(path, params)
    
    @mcp.tool()
    def index_set_readonly(index: str, readonly: bool = True) -> dict:
        """
        设置索引为只读（clone/split/shrink 的前置条件）
        
        参数:
            index: 索引名称
            readonly: True 设为只读，False 取消只读
        
        示例:
            index_set_readonly("my-index", True)   # 设为只读
            index_set_readonly("my-index", False)  # 取消只读
        """
        client = get_client()
        body = {
            "settings": {
                "index.blocks.write": readonly
            }
        }
        return client.put(f"/{index}/_settings", body)
    
    @mcp.tool()
    def index_prepare_for_shrink(index: str, target_node: str = None) -> dict:
        """
        准备索引用于收缩（shrink 的前置条件）
        
        将索引设为只读，并将所有分片迁移到同一节点
        
        参数:
            index: 索引名称
            target_node: 目标节点名称（可选，不传则使用第一个数据节点）
        """
        client = get_client()
        
        # 如果没指定节点，获取第一个数据节点
        if not target_node:
            nodes = client.get("/_cat/nodes?format=json")
            for node in nodes:
                if 'd' in node.get('node.role', ''):
                    target_node = node.get('name')
                    break
        
        body = {
            "settings": {
                "index.routing.allocation.require._name": target_node,
                "index.blocks.write": True
            }
        }
        return client.put(f"/{index}/_settings", body)
    
    @mcp.tool()
    def index_create_with_write_alias(index: str, alias: str, mappings: dict = None, settings: dict = None) -> dict:
        """
        创建带可写别名的索引（rollover 的前置条件）
        
        参数:
            index: 索引名称（建议使用 name-000001 格式）
            alias: 别名名称
            mappings: 字段映射
            settings: 索引设置
        
        示例:
            index_create_with_write_alias("logs-000001", "logs", 
                mappings={"properties": {"@timestamp": {"type": "date"}}})
        """
        client = get_client()
        body = {
            "aliases": {
                alias: {"is_write_index": True}
            }
        }
        if mappings:
            body["mappings"] = mappings
        if settings:
            body["settings"] = settings
        return client.put(f"/{index}", body)
    
    @mcp.tool()
    def index_clone(source: str, target: str, settings: dict = None) -> dict:
        """
        克隆索引
        
        参数:
            source: 源索引名称
            target: 目标索引名称
            settings: 目标索引设置
        
        注意：源索引必须是只读的
        """
        client = get_client()
        body = {"settings": settings} if settings else None
        return client.post(f"/{source}/_clone/{target}", body)
    
    @mcp.tool()
    def index_split(source: str, target: str, settings: dict = None) -> dict:
        """
        拆分索引（增加分片数）
        
        参数:
            source: 源索引名称
            target: 目标索引名称
            settings: 目标索引设置（必须包含 number_of_shards）
        
        注意：新分片数必须是原分片数的倍数
        """
        client = get_client()
        body = {"settings": settings} if settings else None
        return client.post(f"/{source}/_split/{target}", body)
    
    @mcp.tool()
    def index_shrink(source: str, target: str, settings: dict = None) -> dict:
        """
        收缩索引（减少分片数）
        
        参数:
            source: 源索引名称
            target: 目标索引名称
            settings: 目标索引设置
        
        注意：源索引必须是只读的，且所有分片在同一节点
        """
        client = get_client()
        body = {"settings": settings} if settings else None
        return client.post(f"/{source}/_shrink/{target}", body)
    
    @mcp.tool()
    def index_rollover(alias: str, conditions: dict = None, settings: dict = None, mappings: dict = None) -> dict:
        """
        滚动索引
        
        参数:
            alias: 别名名称
            conditions: 滚动条件
            settings: 新索引设置
            mappings: 新索引映射
        
        示例:
            index_rollover("logs", conditions={
                "max_age": "7d",
                "max_docs": 1000000,
                "max_size": "5gb"
            })
        """
        client = get_client()
        body = {}
        if conditions:
            body["conditions"] = conditions
        if settings:
            body["settings"] = settings
        if mappings:
            body["mappings"] = mappings
        return client.post(f"/{alias}/_rollover", body if body else None)
    
    @mcp.tool()
    def alias_get(name: str = None, index: str = None) -> dict:
        """
        获取别名
        
        参数:
            name: 别名名称（可选）
            index: 索引名称（可选）
        """
        client = get_client()
        if index and name:
            path = f"/{index}/_alias/{name}"
        elif index:
            path = f"/{index}/_alias"
        elif name:
            path = f"/_alias/{name}"
        else:
            path = "/_alias"
        return client.get(path)
    
    @mcp.tool()
    def alias_create(index: str, name: str, filter: dict = None, routing: str = None) -> dict:
        """
        创建别名
        
        参数:
            index: 索引名称
            name: 别名名称
            filter: 过滤条件
            routing: 路由值
        
        示例:
            alias_create("logs-2024.01", "logs-current")
            alias_create("users", "active-users", filter={"term": {"status": "active"}})
        """
        client = get_client()
        body = {}
        if filter:
            body["filter"] = filter
        if routing:
            body["routing"] = routing
        return client.put(f"/{index}/_alias/{name}", body if body else None)
    
    @mcp.tool()
    def alias_delete(index: str, name: str) -> dict:
        """
        删除别名
        
        参数:
            index: 索引名称
            name: 别名名称
        """
        client = get_client()
        return client.delete(f"/{index}/_alias/{name}")
    
    @mcp.tool()
    def alias_actions(actions: list) -> dict:
        """
        批量操作别名
        
        参数:
            actions: 操作列表
        
        示例 - 原子切换别名:
            alias_actions([
                {"remove": {"index": "logs-old", "alias": "logs"}},
                {"add": {"index": "logs-new", "alias": "logs"}}
            ])
        """
        client = get_client()
        return client.post("/_aliases", {"actions": actions})
    
    @mcp.tool()
    def template_get(name: str = None) -> dict:
        """
        获取索引模板
        
        参数:
            name: 模板名称（可选，支持通配符）
        """
        client = get_client()
        # 使用旧版模板 API（兼容 Easysearch）
        path = f"/_template/{name}" if name else "/_template"
        return client.get(path)
    
    @mcp.tool()
    def template_create(name: str, index_patterns: list, template: dict, priority: int = None, composed_of: list = None) -> dict:
        """
        创建索引模板
        
        参数:
            name: 模板名称
            index_patterns: 匹配的索引模式列表
            template: 模板内容（mappings、settings、aliases）
            priority: 优先级
            composed_of: 组件模板列表
        
        示例:
            template_create("logs-template", 
                index_patterns=["logs-*"],
                template={
                    "settings": {"number_of_shards": 3},
                    "mappings": {"properties": {"@timestamp": {"type": "date"}}}
                },
                priority=100
            )
        """
        client = get_client()
        # 使用旧版模板 API（兼容 Easysearch）
        body = {
            "index_patterns": index_patterns,
            **template  # 直接展开 mappings/settings/aliases
        }
        if priority is not None:
            body["order"] = priority  # 旧版 API 使用 order 而非 priority
        return client.put(f"/_template/{name}", body)
    
    @mcp.tool()
    def template_delete(name: str) -> dict:
        """
        删除索引模板
        
        参数:
            name: 模板名称
        """
        client = get_client()
        # 使用旧版模板 API（兼容 Easysearch）
        return client.delete(f"/_template/{name}")
    
    @mcp.tool()
    def reindex(source: dict, dest: dict, script: dict = None, max_docs: int = None) -> dict:
        """
        重建索引
        
        参数:
            source: 源配置 {"index": "old-index", "query": {...}}
            dest: 目标配置 {"index": "new-index"}
            script: 转换脚本
            max_docs: 最大文档数
        
        示例:
            reindex(
                source={"index": "old-index"},
                dest={"index": "new-index"}
            )
        """
        client = get_client()
        body = {"source": source, "dest": dest}
        if script:
            body["script"] = script
        if max_docs:
            body["max_docs"] = max_docs
        return client.post("/_reindex", body)
