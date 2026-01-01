"""
快照和恢复相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_snapshot_tools(mcp: FastMCP):
    """注册快照工具"""
    
    @mcp.tool()
    def snapshot_repo_create(name: str, type: str, settings: dict) -> dict:
        """
        创建快照仓库
        
        参数:
            name: 仓库名称
            type: 仓库类型 fs/s3/hdfs/azure/gcs
            settings: 仓库设置
        
        示例 - 文件系统仓库:
            snapshot_repo_create("my_backup", "fs", {"location": "/mount/backups"})
        
        示例 - S3 仓库:
            snapshot_repo_create("s3_backup", "s3", {
                "bucket": "my-bucket",
                "region": "us-east-1"
            })
        """
        client = get_client()
        body = {"type": type, "settings": settings}
        return client.put(f"/_snapshot/{name}", body)
    
    @mcp.tool()
    def snapshot_repo_get(name: str = None) -> dict:
        """
        获取快照仓库信息
        
        参数:
            name: 仓库名称（可选，支持通配符）
        """
        client = get_client()
        path = f"/_snapshot/{name}" if name else "/_snapshot"
        return client.get(path)
    
    @mcp.tool()
    def snapshot_repo_delete(name: str) -> dict:
        """
        删除快照仓库
        
        参数:
            name: 仓库名称
        """
        client = get_client()
        return client.delete(f"/_snapshot/{name}")
    
    @mcp.tool()
    def snapshot_repo_verify(name: str) -> dict:
        """
        验证快照仓库
        
        参数:
            name: 仓库名称
        """
        client = get_client()
        return client.post(f"/_snapshot/{name}/_verify")
    
    @mcp.tool()
    def snapshot_create(repository: str, snapshot: str, indices: list = None, 
                        ignore_unavailable: bool = False, include_global_state: bool = True,
                        wait_for_completion: bool = False) -> dict:
        """
        创建快照
        
        参数:
            repository: 仓库名称
            snapshot: 快照名称
            indices: 索引列表（可选，不传则备份所有）
            ignore_unavailable: 忽略不存在的索引
            include_global_state: 包含集群状态
            wait_for_completion: 等待完成
        
        示例:
            snapshot_create("my_backup", "snapshot_1")
            snapshot_create("my_backup", "snapshot_2", indices=["logs-*", "metrics-*"])
        """
        client = get_client()
        body = {
            "ignore_unavailable": ignore_unavailable,
            "include_global_state": include_global_state
        }
        if indices:
            body["indices"] = ",".join(indices)
        
        params = {"wait_for_completion": str(wait_for_completion).lower()}
        return client.put(f"/_snapshot/{repository}/{snapshot}", body)
    
    @mcp.tool()
    def snapshot_get(repository: str, snapshot: str = None, verbose: bool = True) -> dict:
        """
        获取快照信息
        
        参数:
            repository: 仓库名称
            snapshot: 快照名称（可选，支持通配符，_all 获取所有）
            verbose: 是否显示详细信息
        """
        client = get_client()
        path = f"/_snapshot/{repository}/{snapshot}" if snapshot else f"/_snapshot/{repository}/_all"
        params = {"verbose": str(verbose).lower()}
        return client.get(path, params)
    
    @mcp.tool()
    def snapshot_status(repository: str = None, snapshot: str = None) -> dict:
        """
        获取快照状态
        
        参数:
            repository: 仓库名称（可选）
            snapshot: 快照名称（可选）
        
        返回正在进行的快照的详细进度
        """
        client = get_client()
        if repository and snapshot:
            path = f"/_snapshot/{repository}/{snapshot}/_status"
        elif repository:
            path = f"/_snapshot/{repository}/_status"
        else:
            path = "/_snapshot/_status"
        return client.get(path)
    
    @mcp.tool()
    def snapshot_delete(repository: str, snapshot: str) -> dict:
        """
        删除快照
        
        参数:
            repository: 仓库名称
            snapshot: 快照名称
        """
        client = get_client()
        return client.delete(f"/_snapshot/{repository}/{snapshot}")
    
    @mcp.tool()
    def snapshot_restore(repository: str, snapshot: str, indices: list = None,
                         ignore_unavailable: bool = False, include_global_state: bool = False,
                         rename_pattern: str = None, rename_replacement: str = None,
                         wait_for_completion: bool = False) -> dict:
        """
        恢复快照
        
        参数:
            repository: 仓库名称
            snapshot: 快照名称
            indices: 要恢复的索引列表
            ignore_unavailable: 忽略不存在的索引
            include_global_state: 恢复集群状态
            rename_pattern: 重命名模式（正则）
            rename_replacement: 重命名替换
            wait_for_completion: 等待完成
        
        示例 - 恢复并重命名:
            snapshot_restore("my_backup", "snapshot_1",
                indices=["logs-*"],
                rename_pattern="(.+)",
                rename_replacement="restored_$1"
            )
        """
        client = get_client()
        body = {
            "ignore_unavailable": ignore_unavailable,
            "include_global_state": include_global_state
        }
        if indices:
            body["indices"] = ",".join(indices)
        if rename_pattern:
            body["rename_pattern"] = rename_pattern
        if rename_replacement:
            body["rename_replacement"] = rename_replacement
        
        params = {"wait_for_completion": str(wait_for_completion).lower()}
        return client.post(f"/_snapshot/{repository}/{snapshot}/_restore", body)
    
    @mcp.tool()
    def snapshot_clone(repository: str, source_snapshot: str, target_snapshot: str, indices: str) -> dict:
        """
        克隆快照
        
        参数:
            repository: 仓库名称
            source_snapshot: 源快照名称
            target_snapshot: 目标快照名称
            indices: 要克隆的索引（逗号分隔）
        """
        client = get_client()
        body = {"indices": indices}
        return client.put(f"/_snapshot/{repository}/{source_snapshot}/_clone/{target_snapshot}", body)
