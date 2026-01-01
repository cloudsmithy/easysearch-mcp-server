"""
Ingest Pipeline 相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_ingest_tools(mcp: FastMCP):
    """注册 Ingest Pipeline 工具"""
    
    @mcp.tool()
    def pipeline_get(id: str = None) -> dict:
        """
        获取 Ingest Pipeline
        
        参数:
            id: Pipeline ID（可选，支持通配符）
        """
        client = get_client()
        path = f"/_ingest/pipeline/{id}" if id else "/_ingest/pipeline"
        return client.get(path)
    
    @mcp.tool()
    def pipeline_create(id: str, description: str, processors: list, on_failure: list = None) -> dict:
        """
        创建 Ingest Pipeline
        
        参数:
            id: Pipeline ID
            description: 描述
            processors: 处理器列表
            on_failure: 失败处理器列表
        
        示例:
            pipeline_create("my-pipeline", "Add timestamp", processors=[
                {"set": {"field": "@timestamp", "value": "{{_ingest.timestamp}}"}}
            ])
        
        常用处理器:
            - set: 设置字段值
            - remove: 删除字段
            - rename: 重命名字段
            - convert: 类型转换
            - grok: 正则解析
            - date: 日期解析
            - json: JSON 解析
            - split: 字符串分割
            - trim: 去除空白
            - lowercase/uppercase: 大小写转换
            - script: 脚本处理
        """
        client = get_client()
        body = {
            "description": description,
            "processors": processors
        }
        if on_failure:
            body["on_failure"] = on_failure
        return client.put(f"/_ingest/pipeline/{id}", body)
    
    @mcp.tool()
    def pipeline_delete(id: str) -> dict:
        """
        删除 Ingest Pipeline
        
        参数:
            id: Pipeline ID
        """
        client = get_client()
        return client.delete(f"/_ingest/pipeline/{id}")
    
    @mcp.tool()
    def pipeline_simulate(id: str = None, pipeline: dict = None, docs: list = None, verbose: bool = False) -> dict:
        """
        模拟 Pipeline 执行
        
        参数:
            id: 已存在的 Pipeline ID
            pipeline: 内联 Pipeline 定义
            docs: 测试文档列表
            verbose: 是否显示每个处理器的输出
        
        示例:
            pipeline_simulate(
                pipeline={"processors": [{"set": {"field": "foo", "value": "bar"}}]},
                docs=[{"_source": {"name": "test"}}]
            )
        """
        client = get_client()
        body = {"docs": docs or []}
        if pipeline:
            body["pipeline"] = pipeline
        
        path = f"/_ingest/pipeline/{id}/_simulate" if id else "/_ingest/pipeline/_simulate"
        params = {"verbose": "true"} if verbose else None
        return client.post(path, body)
    
    @mcp.tool()
    def ingest_stats(node_id: str = None) -> dict:
        """
        获取 Ingest 统计信息
        
        参数:
            node_id: 节点 ID（可选）
        """
        client = get_client()
        path = f"/_nodes/{node_id}/stats/ingest" if node_id else "/_nodes/stats/ingest"
        return client.get(path)
    
    @mcp.tool()
    def ingest_processor_grok() -> dict:
        """获取内置的 Grok 模式列表"""
        client = get_client()
        return client.get("/_ingest/processor/grok")
