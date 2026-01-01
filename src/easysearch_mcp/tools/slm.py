"""
快照生命周期管理 (SLM) 相关工具
Easysearch 特有的 API
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_slm_tools(mcp: FastMCP):
    """注册 SLM 工具"""
    
    @mcp.tool()
    def slm_policy_create(name: str, description: str, repository: str, indices: str = "*",
                          creation_schedule: str = "0 8 * * *", creation_timezone: str = "Asia/Shanghai",
                          deletion_schedule: str = "0 1 * * *", deletion_timezone: str = "Asia/Shanghai",
                          max_age: str = "7d", max_count: int = 21, min_count: int = 7,
                          include_global_state: bool = False) -> dict:
        """
        创建快照生命周期策略
        
        参数:
            name: 策略名称
            description: 策略描述
            repository: 快照仓库名称
            indices: 要备份的索引（默认 *）
            creation_schedule: 创建快照的 cron 表达式（默认每天 8:00）
            creation_timezone: 创建时区
            deletion_schedule: 删除快照的 cron 表达式（默认每天 1:00）
            deletion_timezone: 删除时区
            max_age: 快照最大保留时间
            max_count: 最大快照数量
            min_count: 最小快照数量
            include_global_state: 是否包含全局状态
        
        示例:
            slm_policy_create("daily-backup", "每日备份", "my_backup",
                creation_schedule="0 2 * * *",
                max_age="30d", max_count=30
            )
        """
        client = get_client()
        body = {
            "description": description,
            "creation": {
                "schedule": {
                    "cron": {
                        "expression": creation_schedule,
                        "timezone": creation_timezone
                    }
                },
                "time_limit": "1h"
            },
            "deletion": {
                "schedule": {
                    "cron": {
                        "expression": deletion_schedule,
                        "timezone": deletion_timezone
                    }
                },
                "condition": {
                    "max_age": max_age,
                    "max_count": max_count,
                    "min_count": min_count
                },
                "time_limit": "1h"
            },
            "snapshot_config": {
                "date_format": "yyyy-MM-dd-HH:mm",
                "date_format_timezone": creation_timezone,
                "indices": indices,
                "repository": repository,
                "ignore_unavailable": "true",
                "include_global_state": str(include_global_state).lower(),
                "partial": "true"
            }
        }
        return client.post(f"/_slm/policies/{name}", body)
    
    @mcp.tool()
    def slm_policy_get(name: str = None) -> dict:
        """
        获取快照生命周期策略
        
        参数:
            name: 策略名称（可选，支持通配符如 daily*）
        """
        client = get_client()
        path = f"/_slm/policies/{name}" if name else "/_slm/policies"
        return client.get(path)
    
    @mcp.tool()
    def slm_policy_delete(name: str) -> dict:
        """
        删除快照生命周期策略
        
        参数:
            name: 策略名称
        """
        client = get_client()
        return client.delete(f"/_slm/policies/{name}")
    
    @mcp.tool()
    def slm_policy_explain(name: str) -> dict:
        """
        解释快照生命周期策略
        
        参数:
            name: 策略名称（支持通配符如 daily*）
        
        返回策略的详细解释，包括下次创建/删除快照的时间
        """
        client = get_client()
        return client.get(f"/_slm/policies/{name}/_explain")
    
    @mcp.tool()
    def slm_policy_start(name: str) -> dict:
        """
        启动快照生命周期策略
        
        参数:
            name: 策略名称
        """
        client = get_client()
        return client.post(f"/_slm/policies/{name}/_start")
    
    @mcp.tool()
    def slm_policy_stop(name: str) -> dict:
        """
        停止快照生命周期策略
        
        参数:
            name: 策略名称
        """
        client = get_client()
        return client.post(f"/_slm/policies/{name}/_stop")
