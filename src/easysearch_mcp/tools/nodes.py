"""
节点管理相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_nodes_tools(mcp: FastMCP):
    """注册节点管理工具"""
    
    @mcp.tool()
    def nodes_info(node_id: str = None, metric: str = None) -> dict:
        """
        获取节点信息
        
        参数:
            node_id: 节点 ID（可选，逗号分隔多个）
            metric: 信息类型 settings/os/process/jvm/thread_pool/transport/http/plugins/ingest
        
        返回节点配置、JVM 信息、线程池配置等
        """
        client = get_client()
        parts = ["/_nodes"]
        if node_id:
            parts.append(node_id)
        if metric:
            parts.append(metric)
        return client.get("/".join(parts))
    
    @mcp.tool()
    def nodes_stats(node_id: str = None, metric: str = None, index_metric: str = None) -> dict:
        """
        获取节点统计信息
        
        参数:
            node_id: 节点 ID（可选）
            metric: 统计类型 indices/os/process/jvm/thread_pool/fs/transport/http/breaker/script/discovery/ingest
            index_metric: 索引统计类型 docs/store/indexing/get/search/merge/refresh/flush/warmer/query_cache/fielddata/completion/segments/translog
        
        示例:
            nodes_stats()  # 所有统计
            nodes_stats(metric="jvm,fs")  # JVM 和文件系统
            nodes_stats(metric="indices", index_metric="search,indexing")  # 搜索和索引统计
        """
        client = get_client()
        parts = ["/_nodes"]
        if node_id:
            parts.append(node_id)
        parts.append("stats")
        if metric:
            parts.append(metric)
        if index_metric:
            parts.append(index_metric)
        return client.get("/".join(parts))
    
    @mcp.tool()
    def nodes_hot_threads(node_id: str = None, threads: int = 3, interval: str = "500ms", type: str = None) -> str:
        """
        获取节点热点线程
        
        参数:
            node_id: 节点 ID（可选）
            threads: 每个节点显示的线程数
            interval: 采样间隔
            type: 线程类型 cpu/wait/block
        
        用于诊断 CPU 高占用问题
        """
        client = get_client()
        parts = ["/_nodes"]
        if node_id:
            parts.append(node_id)
        parts.append("hot_threads")
        
        params = {"threads": threads, "interval": interval}
        if type:
            params["type"] = type
        
        # hot_threads 返回纯文本
        with client._client() as c:
            r = c.get("/".join(parts), params=params)
            return r.text
    
    @mcp.tool()
    def nodes_usage(node_id: str = None, metric: str = None) -> dict:
        """
        获取节点功能使用统计
        
        参数:
            node_id: 节点 ID（可选）
            metric: 统计类型 rest_actions/aggregations
        
        返回各 API 和聚合的使用次数
        """
        client = get_client()
        parts = ["/_nodes"]
        if node_id:
            parts.append(node_id)
        parts.append("usage")
        if metric:
            parts.append(metric)
        return client.get("/".join(parts))
    
    @mcp.tool()
    def nodes_reload_secure_settings(node_id: str = None, secure_settings_password: str = None) -> dict:
        """
        重新加载安全设置
        
        参数:
            node_id: 节点 ID（可选）
            secure_settings_password: keystore 密码
        """
        client = get_client()
        parts = ["/_nodes"]
        if node_id:
            parts.append(node_id)
        parts.append("reload_secure_settings")
        
        body = {}
        if secure_settings_password:
            body["secure_settings_password"] = secure_settings_password
        return client.post("/".join(parts), body if body else None)
