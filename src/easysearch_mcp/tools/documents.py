"""
文档操作相关工具
"""

import json
from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_document_tools(mcp: FastMCP):
    """注册文档操作工具"""
    
    @mcp.tool()
    def doc_index(index: str, document: dict, id: str = None, refresh: str = None, routing: str = None) -> dict:
        """
        写入文档
        
        参数:
            index: 索引名称
            document: 文档内容
            id: 文档 ID（可选，不传则自动生成）
            refresh: 刷新策略 true/false/wait_for
            routing: 路由值
        
        示例:
            doc_index("products", {"name": "iPhone", "price": 999})
            doc_index("products", {"name": "iPad", "price": 799}, id="ipad-001")
        """
        client = get_client()
        params = {}
        if refresh:
            params["refresh"] = refresh
        if routing:
            params["routing"] = routing
        
        if id:
            return client.put(f"/{index}/_doc/{id}", document)
        else:
            return client.post(f"/{index}/_doc", document)
    
    @mcp.tool()
    def doc_get(index: str, id: str, source: list = None, source_excludes: list = None, routing: str = None) -> dict:
        """
        获取文档
        
        参数:
            index: 索引名称
            id: 文档 ID
            source: 返回的字段列表
            source_excludes: 排除的字段列表
            routing: 路由值
        """
        client = get_client()
        params = {}
        if source:
            params["_source"] = ",".join(source)
        if source_excludes:
            params["_source_excludes"] = ",".join(source_excludes)
        if routing:
            params["routing"] = routing
        return client.get(f"/{index}/_doc/{id}", params or None)
    
    @mcp.tool()
    def doc_exists(index: str, id: str, routing: str = None) -> bool:
        """
        检查文档是否存在
        
        参数:
            index: 索引名称
            id: 文档 ID
            routing: 路由值
        """
        client = get_client()
        return client.head(f"/{index}/_doc/{id}")
    
    @mcp.tool()
    def doc_delete(index: str, id: str, refresh: str = None, routing: str = None) -> dict:
        """
        删除文档
        
        参数:
            index: 索引名称
            id: 文档 ID
            refresh: 刷新策略
            routing: 路由值
        """
        client = get_client()
        params = {}
        if refresh:
            params["refresh"] = refresh
        if routing:
            params["routing"] = routing
        return client.delete(f"/{index}/_doc/{id}")
    
    @mcp.tool()
    def doc_update(index: str, id: str, doc: dict = None, script: dict = None, upsert: dict = None, refresh: str = None) -> dict:
        """
        更新文档
        
        参数:
            index: 索引名称
            id: 文档 ID
            doc: 部分更新的字段
            script: 脚本更新
            upsert: 文档不存在时插入的内容
            refresh: 刷新策略
        
        示例 - 部分更新:
            doc_update("products", "1", doc={"price": 899})
        
        示例 - 脚本更新:
            doc_update("products", "1", script={
                "source": "ctx._source.price -= params.discount",
                "params": {"discount": 100}
            })
        """
        client = get_client()
        body = {}
        if doc:
            body["doc"] = doc
        if script:
            body["script"] = script
        if upsert:
            body["upsert"] = upsert
        params = {"refresh": refresh} if refresh else None
        return client.post(f"/{index}/_update/{id}", body)
    
    @mcp.tool()
    def doc_bulk(operations: list, refresh: str = None) -> dict:
        """
        批量操作文档
        
        参数:
            operations: 操作列表，每个操作是 {"action": {...}, "doc": {...}} 格式
            refresh: 刷新策略
        
        示例:
            doc_bulk([
                {"index": {"_index": "products", "_id": "1"}, "doc": {"name": "A"}},
                {"index": {"_index": "products", "_id": "2"}, "doc": {"name": "B"}},
                {"delete": {"_index": "products", "_id": "3"}}
            ])
        """
        client = get_client()
        lines = []
        for op in operations:
            if "doc" in op:
                # index/create/update 操作
                action = {k: v for k, v in op.items() if k != "doc"}
                lines.append(json.dumps(action))
                lines.append(json.dumps(op["doc"]))
            else:
                # delete 操作
                lines.append(json.dumps(op))
        
        body = "\n".join(lines) + "\n"
        result = client.post("/_bulk", content=body, headers={"Content-Type": "application/x-ndjson"})
        return {
            "took": result.get("took"),
            "errors": result.get("errors"),
            "items_count": len(result.get("items", []))
        }
    
    @mcp.tool()
    def doc_bulk_simple(index: str, documents: list, refresh: str = None) -> dict:
        """
        简化的批量写入（仅支持 index 操作）
        
        参数:
            index: 索引名称
            documents: 文档列表
            refresh: 刷新策略
        
        示例:
            doc_bulk_simple("products", [
                {"name": "A", "price": 100},
                {"name": "B", "price": 200}
            ])
        """
        client = get_client()
        lines = []
        for doc in documents:
            lines.append(json.dumps({"index": {"_index": index}}))
            lines.append(json.dumps(doc))
        
        body = "\n".join(lines) + "\n"
        result = client.post("/_bulk", content=body, headers={"Content-Type": "application/x-ndjson"})
        return {
            "took": result.get("took"),
            "errors": result.get("errors"),
            "items_count": len(result.get("items", []))
        }
    
    @mcp.tool()
    def doc_mget(docs: list = None, index: str = None, ids: list = None, source: list = None) -> dict:
        """
        批量获取文档
        
        参数:
            docs: 文档列表 [{"_index": "idx", "_id": "1"}, ...]
            index: 默认索引（与 ids 配合使用）
            ids: ID 列表（与 index 配合使用）
            source: 返回的字段列表
        
        示例:
            doc_mget(docs=[
                {"_index": "products", "_id": "1"},
                {"_index": "products", "_id": "2"}
            ])
            
            doc_mget(index="products", ids=["1", "2", "3"])
        """
        client = get_client()
        body = {}
        if docs:
            body["docs"] = docs
        if ids:
            body["ids"] = ids
        if source:
            body["_source"] = source
        
        path = f"/{index}/_mget" if index else "/_mget"
        return client.post(path, body)
    
    @mcp.tool()
    def doc_delete_by_query(index: str, query: dict, refresh: bool = False, conflicts: str = "abort") -> dict:
        """
        按查询删除文档
        
        参数:
            index: 索引名称
            query: 查询条件
            refresh: 是否刷新
            conflicts: 冲突处理 abort/proceed
        
        示例:
            doc_delete_by_query("logs", {"range": {"@timestamp": {"lt": "2024-01-01"}}})
        """
        client = get_client()
        body = {"query": query}
        params = {"refresh": str(refresh).lower(), "conflicts": conflicts}
        return client.post(f"/{index}/_delete_by_query", body)
    
    @mcp.tool()
    def doc_update_by_query(index: str, query: dict = None, script: dict = None, refresh: bool = False) -> dict:
        """
        按查询更新文档
        
        参数:
            index: 索引名称
            query: 查询条件（可选，不传则匹配所有）
            script: 更新脚本
            refresh: 是否刷新
        
        示例:
            doc_update_by_query("products", 
                query={"term": {"category": "electronics"}},
                script={"source": "ctx._source.on_sale = true"}
            )
        """
        client = get_client()
        body = {}
        if query:
            body["query"] = query
        if script:
            body["script"] = script
        return client.post(f"/{index}/_update_by_query", body if body else None)
    
    @mcp.tool()
    def doc_source(index: str, id: str, source: list = None) -> dict:
        """
        仅获取文档 _source（不含元数据）
        
        参数:
            index: 索引名称
            id: 文档 ID
            source: 返回的字段列表
        """
        client = get_client()
        params = {"_source": ",".join(source)} if source else None
        return client.get(f"/{index}/_source/{id}", params)
