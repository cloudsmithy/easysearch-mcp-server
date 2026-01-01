"""
CAT API 工具（监控和诊断）
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_cat_tools(mcp: FastMCP):
    """注册 CAT API 工具"""
    
    @mcp.tool()
    def cat_health(ts: bool = True) -> list:
        """
        获取集群健康状态（简洁格式）
        
        参数:
            ts: 是否显示时间戳
        """
        client = get_client()
        params = {"format": "json"}
        if not ts:
            params["ts"] = "false"
        return client.get("/_cat/health", params)
    
    @mcp.tool()
    def cat_nodes(full_id: bool = False) -> list:
        """
        获取节点信息
        
        参数:
            full_id: 是否显示完整节点 ID
        
        返回节点名称、IP、角色、负载、内存使用等
        """
        client = get_client()
        h = "name,ip,role,load_1m,load_5m,load_15m,cpu,heap.percent,ram.percent,node.role,master"
        params = {"format": "json", "h": h}
        if full_id:
            params["full_id"] = "true"
        return client.get("/_cat/nodes", params)
    
    @mcp.tool()
    def cat_indices(index: str = None, health: str = None, pri: bool = False, 
                    sort_by: str = None, order: str = "asc") -> list:
        """
        获取索引列表
        
        参数:
            index: 索引名称/模式（可选）
            health: 健康状态过滤 green/yellow/red
            pri: 仅显示主分片统计
            sort_by: 排序字段 如 store.size/docs.count
            order: 排序方向 asc/desc
        
        返回索引名称、健康状态、文档数、存储大小等
        """
        client = get_client()
        path = f"/_cat/indices/{index}" if index else "/_cat/indices"
        params = {"format": "json"}
        if health:
            params["health"] = health
        if pri:
            params["pri"] = "true"
        if sort_by:
            params["s"] = f"{sort_by}:{order}"
        return client.get(path, params)
    
    @mcp.tool()
    def cat_shards(index: str = None) -> list:
        """
        获取分片分布信息
        
        参数:
            index: 索引名称（可选）
        
        返回分片状态、大小、所在节点等
        """
        client = get_client()
        path = f"/_cat/shards/{index}" if index else "/_cat/shards"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_allocation(node_id: str = None) -> list:
        """
        获取节点磁盘分配信息
        
        参数:
            node_id: 节点 ID（可选）
        
        返回每个节点的分片数、磁盘使用情况
        """
        client = get_client()
        path = f"/_cat/allocation/{node_id}" if node_id else "/_cat/allocation"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_thread_pool(thread_pool: str = None) -> list:
        """
        获取线程池状态
        
        参数:
            thread_pool: 线程池名称（可选）如 search/write/get
        
        返回各线程池的活跃线程数、队列大小、拒绝数
        """
        client = get_client()
        path = f"/_cat/thread_pool/{thread_pool}" if thread_pool else "/_cat/thread_pool"
        h = "node_name,name,active,queue,rejected,size,type"
        return client.get(path, {"format": "json", "h": h})
    
    @mcp.tool()
    def cat_master() -> list:
        """获取当前主节点信息"""
        client = get_client()
        return client.get("/_cat/master", {"format": "json"})
    
    @mcp.tool()
    def cat_segments(index: str = None) -> list:
        """
        获取段信息
        
        参数:
            index: 索引名称（可选）
        
        返回每个分片的段数量、大小、文档数等
        """
        client = get_client()
        path = f"/_cat/segments/{index}" if index else "/_cat/segments"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_count(index: str = None) -> list:
        """
        获取文档计数
        
        参数:
            index: 索引名称（可选）
        """
        client = get_client()
        path = f"/_cat/count/{index}" if index else "/_cat/count"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_recovery(index: str = None, active_only: bool = False) -> list:
        """
        获取分片恢复状态
        
        参数:
            index: 索引名称（可选）
            active_only: 仅显示进行中的恢复
        """
        client = get_client()
        path = f"/_cat/recovery/{index}" if index else "/_cat/recovery"
        params = {"format": "json"}
        if active_only:
            params["active_only"] = "true"
        return client.get(path, params)
    
    @mcp.tool()
    def cat_pending_tasks() -> list:
        """获取待处理的集群任务"""
        client = get_client()
        return client.get("/_cat/pending_tasks", {"format": "json"})
    
    @mcp.tool()
    def cat_aliases(name: str = None) -> list:
        """
        获取别名列表
        
        参数:
            name: 别名名称（可选）
        """
        client = get_client()
        path = f"/_cat/aliases/{name}" if name else "/_cat/aliases"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_templates(name: str = None) -> list:
        """
        获取索引模板列表
        
        参数:
            name: 模板名称（可选）
        """
        client = get_client()
        path = f"/_cat/templates/{name}" if name else "/_cat/templates"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_plugins() -> list:
        """获取已安装的插件列表"""
        client = get_client()
        return client.get("/_cat/plugins", {"format": "json"})
    
    @mcp.tool()
    def cat_fielddata(fields: str = None) -> list:
        """
        获取 fielddata 内存使用
        
        参数:
            fields: 字段名（可选，逗号分隔）
        """
        client = get_client()
        path = f"/_cat/fielddata/{fields}" if fields else "/_cat/fielddata"
        return client.get(path, {"format": "json"})
    
    @mcp.tool()
    def cat_nodeattrs() -> list:
        """获取节点属性"""
        client = get_client()
        return client.get("/_cat/nodeattrs", {"format": "json"})
    
    @mcp.tool()
    def cat_repositories() -> list:
        """获取快照仓库列表"""
        client = get_client()
        return client.get("/_cat/repositories", {"format": "json"})
    
    @mcp.tool()
    def cat_snapshots(repository: str) -> list:
        """
        获取快照列表
        
        参数:
            repository: 仓库名称
        """
        client = get_client()
        return client.get(f"/_cat/snapshots/{repository}", {"format": "json"})
    
    @mcp.tool()
    def cat_tasks(detailed: bool = False, parent_task_id: str = None) -> list:
        """
        获取正在执行的任务
        
        参数:
            detailed: 是否显示详细信息
            parent_task_id: 父任务 ID
        """
        client = get_client()
        params = {"format": "json"}
        if detailed:
            params["detailed"] = "true"
        if parent_task_id:
            params["parent_task_id"] = parent_task_id
        return client.get("/_cat/tasks", params)
