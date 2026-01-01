"""
任务管理相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_tasks_tools(mcp: FastMCP):
    """注册任务管理工具"""
    
    @mcp.tool()
    def tasks_list(actions: str = None, detailed: bool = False, parent_task_id: str = None,
                   nodes: str = None, group_by: str = None) -> dict:
        """
        获取正在执行的任务列表
        
        参数:
            actions: 动作过滤（支持通配符）如 cluster:* 或 indices:data/write/*
            detailed: 是否显示详细信息
            parent_task_id: 父任务 ID
            nodes: 节点过滤
            group_by: 分组方式 nodes/parents/none
        """
        client = get_client()
        params = {}
        if actions:
            params["actions"] = actions
        if detailed:
            params["detailed"] = "true"
        if parent_task_id:
            params["parent_task_id"] = parent_task_id
        if nodes:
            params["nodes"] = nodes
        if group_by:
            params["group_by"] = group_by
        return client.get("/_tasks", params or None)
    
    @mcp.tool()
    def tasks_get(task_id: str, wait_for_completion: bool = False, timeout: str = None) -> dict:
        """
        获取任务详情
        
        参数:
            task_id: 任务 ID（格式：node_id:task_number）
            wait_for_completion: 等待任务完成
            timeout: 等待超时时间
        """
        client = get_client()
        params = {}
        if wait_for_completion:
            params["wait_for_completion"] = "true"
        if timeout:
            params["timeout"] = timeout
        return client.get(f"/_tasks/{task_id}", params or None)
    
    @mcp.tool()
    def tasks_cancel(task_id: str = None, actions: str = None, nodes: str = None,
                     parent_task_id: str = None) -> dict:
        """
        取消任务
        
        参数:
            task_id: 任务 ID（可选）
            actions: 动作过滤
            nodes: 节点过滤
            parent_task_id: 父任务 ID
        
        示例:
            tasks_cancel(task_id="node1:12345")
            tasks_cancel(actions="*reindex*")
        """
        client = get_client()
        path = f"/_tasks/{task_id}/_cancel" if task_id else "/_tasks/_cancel"
        params = {}
        if actions:
            params["actions"] = actions
        if nodes:
            params["nodes"] = nodes
        if parent_task_id:
            params["parent_task_id"] = parent_task_id
        return client.post(path, params=params or None)
