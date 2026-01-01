"""
ILM 索引生命周期管理工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_ilm_tools(mcp: FastMCP):
    """注册 ILM 工具"""
    
    @mcp.tool()
    def ilm_policy_get(policy_id: str = None) -> dict:
        """
        获取 ILM 策略
        
        参数:
            policy_id: 策略 ID（可选，不传则获取所有策略）
        """
        client = get_client()
        path = f"/_ilm/policy/{policy_id}" if policy_id else "/_ilm/policy"
        return client.get(path)
    
    @mcp.tool()
    def ilm_policy_create(policy_id: str, hot: dict = None, warm: dict = None, 
                          cold: dict = None, delete: dict = None, description: str = None) -> dict:
        """
        创建 ILM 策略
        
        参数:
            policy_id: 策略 ID
            hot: 热阶段配置
            warm: 温阶段配置
            cold: 冷阶段配置
            delete: 删除阶段配置
            description: 策略描述
        
        示例 - 基本策略:
            ilm_policy_create("logs-policy",
                hot={
                    "min_age": "0ms",
                    "actions": {
                        "rollover": {"max_size": "50gb", "max_age": "30d"}
                    }
                },
                delete={
                    "min_age": "90d",
                    "actions": {"delete": {}}
                }
            )
        
        示例 - 完整生命周期:
            ilm_policy_create("full-lifecycle",
                hot={
                    "min_age": "0ms",
                    "actions": {
                        "rollover": {"max_size": "50gb", "max_age": "7d"},
                        "set_priority": {"priority": 100}
                    }
                },
                warm={
                    "min_age": "30d",
                    "actions": {
                        "shrink": {"number_of_shards": 1},
                        "forcemerge": {"max_num_segments": 1},
                        "set_priority": {"priority": 50}
                    }
                },
                cold={
                    "min_age": "60d",
                    "actions": {
                        "set_priority": {"priority": 0}
                    }
                },
                delete={
                    "min_age": "90d",
                    "actions": {"delete": {}}
                }
            )
        
        常用 actions:
            - rollover: 滚动索引 (max_size, max_age, max_docs)
            - shrink: 收缩分片数
            - forcemerge: 合并段
            - set_priority: 设置恢复优先级
            - allocate: 分配到特定节点
            - readonly: 设为只读
            - delete: 删除索引
        """
        client = get_client()
        
        phases = {}
        if hot:
            phases["hot"] = hot
        if warm:
            phases["warm"] = warm
        if cold:
            phases["cold"] = cold
        if delete:
            phases["delete"] = delete
        
        body = {"policy": {"phases": phases}}
        if description:
            body["policy"]["description"] = description
        
        return client.put(f"/_ilm/policy/{policy_id}", body)
    
    @mcp.tool()
    def ilm_policy_delete(policy_id: str) -> dict:
        """
        删除 ILM 策略
        
        参数:
            policy_id: 策略 ID
        """
        client = get_client()
        return client.delete(f"/_ilm/policy/{policy_id}")
    
    @mcp.tool()
    def ilm_add_policy(index: str, policy_id: str) -> dict:
        """
        给索引绑定 ILM 策略
        
        参数:
            index: 索引名称
            policy_id: ILM 策略 ID
        
        示例:
            ilm_add_policy("logs-000001", "logs-policy")
        """
        client = get_client()
        body = {
            "index.lifecycle.name": policy_id
        }
        return client.put(f"/{index}/_settings", body)
    
    @mcp.tool()
    def ilm_remove_policy(index: str) -> dict:
        """
        从索引移除 ILM 策略
        
        参数:
            index: 索引名称
        """
        client = get_client()
        body = {
            "index.lifecycle.name": None
        }
        return client.put(f"/{index}/_settings", body)
