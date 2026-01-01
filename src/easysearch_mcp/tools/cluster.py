"""
集群管理相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_cluster_tools(mcp: FastMCP):
    """注册集群管理工具"""
    
    @mcp.tool()
    def cluster_health(index: str = None, level: str = None) -> dict:
        """
        获取集群健康状态
        
        参数:
            index: 指定索引（可选）
            level: 详细级别 cluster/indices/shards（可选）
        
        返回集群名称、状态（green/yellow/red）、节点数、分片数等
        """
        client = get_client()
        path = f"/_cluster/health/{index}" if index else "/_cluster/health"
        params = {"level": level} if level else None
        return client.get(path, params)
    
    @mcp.tool()
    def cluster_stats(node_id: str = None) -> dict:
        """
        获取集群统计信息
        
        参数:
            node_id: 指定节点 ID（可选）
        
        返回文档数、存储大小、索引数量、节点信息等
        """
        client = get_client()
        path = f"/_cluster/stats/nodes/{node_id}" if node_id else "/_cluster/stats"
        data = client.get(path)
        return {
            "cluster_name": data.get("cluster_name"),
            "status": data.get("status"),
            "timestamp": data.get("timestamp"),
            "nodes": data.get("nodes", {}).get("count", {}),
            "indices": {
                "count": data.get("indices", {}).get("count"),
                "docs": data.get("indices", {}).get("docs", {}),
                "store": data.get("indices", {}).get("store", {}),
                "shards": data.get("indices", {}).get("shards", {})
            }
        }
    
    @mcp.tool()
    def cluster_state(metric: str = None, index: str = None) -> dict:
        """
        获取集群状态
        
        参数:
            metric: 指标类型 version/master_node/nodes/routing_table/metadata/blocks（可选）
            index: 指定索引（可选）
        
        返回集群完整状态信息
        """
        client = get_client()
        parts = ["/_cluster/state"]
        if metric:
            parts.append(metric)
        if index:
            parts.append(index)
        return client.get("/".join(parts))
    
    @mcp.tool()
    def cluster_settings(include_defaults: bool = False, flat_settings: bool = False) -> dict:
        """
        获取集群设置
        
        参数:
            include_defaults: 是否包含默认设置
            flat_settings: 是否扁平化显示
        """
        client = get_client()
        params = {}
        if include_defaults:
            params["include_defaults"] = "true"
        if flat_settings:
            params["flat_settings"] = "true"
        return client.get("/_cluster/settings", params or None)
    
    @mcp.tool()
    def cluster_update_settings(persistent: dict = None, transient: dict = None) -> dict:
        """
        更新集群设置
        
        参数:
            persistent: 持久化设置（重启后保留）
            transient: 临时设置（重启后丢失）
        
        示例:
            cluster_update_settings(
                persistent={"cluster.routing.allocation.enable": "all"}
            )
        """
        client = get_client()
        body = {}
        if persistent:
            body["persistent"] = persistent
        if transient:
            body["transient"] = transient
        return client.put("/_cluster/settings", body)
    
    @mcp.tool()
    def cluster_pending_tasks() -> dict:
        """获取集群待处理任务列表"""
        client = get_client()
        return client.get("/_cluster/pending_tasks")
    
    @mcp.tool()
    def cluster_allocation_explain(index: str = None, shard: int = None, primary: bool = None) -> dict:
        """
        解释分片分配决策
        
        参数:
            index: 索引名称（可选，不传则解释第一个未分配分片）
            shard: 分片编号
            primary: 是否主分片
        
        用于诊断分片为什么未分配或分配到特定节点
        """
        client = get_client()
        body = {}
        if index:
            body["index"] = index
        if shard is not None:
            body["shard"] = shard
        if primary is not None:
            body["primary"] = primary
        return client.get("/_cluster/allocation/explain", body if body else None)
    
    @mcp.tool()
    def cluster_reroute(commands: list = None, dry_run: bool = False) -> dict:
        """
        手动重新路由分片
        
        参数:
            commands: 路由命令列表
            dry_run: 是否仅模拟执行
        
        示例 - 移动分片:
            cluster_reroute(commands=[{
                "move": {
                    "index": "test", "shard": 0,
                    "from_node": "node1", "to_node": "node2"
                }
            }])
        
        示例 - 取消分片:
            cluster_reroute(commands=[{
                "cancel": {"index": "test", "shard": 0, "node": "node1"}
            }])
        """
        client = get_client()
        body = {"commands": commands or []}
        params = {"dry_run": "true"} if dry_run else None
        return client.post("/_cluster/reroute", body, params=params)
