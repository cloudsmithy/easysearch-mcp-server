"""
搜索相关工具
"""

from mcp.server.fastmcp import FastMCP
from ..client import get_client


def register_search_tools(mcp: FastMCP):
    """注册搜索工具"""
    
    @mcp.tool()
    def search(index: str, query: dict = None, size: int = 10, from_: int = 0, 
               sort: list = None, source: list = None, aggs: dict = None,
               highlight: dict = None, track_total_hits: bool = True) -> dict:
        """
        执行搜索查询
        
        参数:
            index: 索引名称（支持通配符和逗号分隔多个索引）
            query: DSL 查询条件
            size: 返回数量
            from_: 起始位置（分页）
            sort: 排序规则
            source: 返回的字段列表
            aggs: 聚合定义
            highlight: 高亮配置
            track_total_hits: 是否精确统计总数
        
        示例 - 全文搜索:
            search("products", query={"match": {"name": "iPhone"}})
        
        示例 - 复合查询:
            search("products", query={
                "bool": {
                    "must": [{"match": {"name": "phone"}}],
                    "filter": [{"range": {"price": {"lte": 1000}}}]
                }
            })
        
        示例 - 带排序和分页:
            search("products", query={"match_all": {}}, 
                   sort=[{"price": "desc"}], from_=10, size=10)
        """
        client = get_client()
        body = {"size": size, "from": from_}
        
        if query:
            body["query"] = query
        if sort:
            body["sort"] = sort
        if source:
            body["_source"] = source
        if aggs:
            body["aggs"] = aggs
        if highlight:
            body["highlight"] = highlight
        if track_total_hits is not None:
            body["track_total_hits"] = track_total_hits
        
        result = client.post(f"/{index}/_search", body)
        hits = result.get("hits", {})
        
        response = {
            "took_ms": result.get("took"),
            "timed_out": result.get("timed_out"),
            "total": hits.get("total", {}).get("value", 0),
            "max_score": hits.get("max_score"),
            "hits": [{
                "_index": h.get("_index"),
                "_id": h.get("_id"),
                "_score": h.get("_score"),
                "_source": h.get("_source"),
                "highlight": h.get("highlight")
            } for h in hits.get("hits", [])]
        }
        
        if "aggregations" in result:
            response["aggregations"] = result["aggregations"]
        
        return response
    
    @mcp.tool()
    def search_simple(index: str, keyword: str, field: str = None, size: int = 10) -> dict:
        """
        简单关键词搜索
        
        参数:
            index: 索引名称
            keyword: 搜索关键词
            field: 搜索字段（可选，不传则全字段搜索）
            size: 返回数量
        
        示例:
            search_simple("products", "iPhone")
            search_simple("logs", "error", field="message")
        """
        if field:
            query = {"match": {field: keyword}}
        else:
            query = {"query_string": {"query": keyword}}
        
        return search(index, query=query, size=size)
    
    @mcp.tool()
    def search_template(index: str, id: str = None, source: str = None, params: dict = None) -> dict:
        """
        使用搜索模板
        
        参数:
            index: 索引名称
            id: 已存储的模板 ID
            source: 内联模板
            params: 模板参数
        
        示例:
            search_template("products", id="my-template", params={"query_string": "iPhone"})
        """
        client = get_client()
        body = {"params": params or {}}
        if id:
            body["id"] = id
        if source:
            body["source"] = source
        return client.post(f"/{index}/_search/template", body)
    
    @mcp.tool()
    def msearch(searches: list) -> dict:
        """
        多重搜索（一次请求执行多个搜索）
        
        参数:
            searches: 搜索列表，每项包含 header 和 body
        
        示例:
            msearch([
                {"header": {"index": "products"}, "body": {"query": {"match": {"name": "iPhone"}}}},
                {"header": {"index": "products"}, "body": {"query": {"match": {"name": "iPad"}}}}
            ])
        """
        client = get_client()
        import json
        lines = []
        for s in searches:
            lines.append(json.dumps(s.get("header", {})))
            lines.append(json.dumps(s.get("body", {})))
        body = "\n".join(lines) + "\n"
        return client.post("/_msearch", content=body, headers={"Content-Type": "application/x-ndjson"})
    
    @mcp.tool()
    def count(index: str, query: dict = None) -> dict:
        """
        统计文档数量
        
        参数:
            index: 索引名称
            query: 查询条件（可选）
        
        示例:
            count("products")
            count("products", query={"term": {"status": "active"}})
        """
        client = get_client()
        body = {"query": query} if query else None
        return client.post(f"/{index}/_count", body)
    
    @mcp.tool()
    def validate_query(index: str, query: dict, explain: bool = False, rewrite: bool = False) -> dict:
        """
        验证查询语法
        
        参数:
            index: 索引名称
            query: 查询条件
            explain: 是否返回详细解释
            rewrite: 是否返回重写后的查询
        """
        client = get_client()
        body = {"query": query}
        params = {}
        if explain:
            params["explain"] = "true"
        if rewrite:
            params["rewrite"] = "true"
        return client.post(f"/{index}/_validate/query", body)
    
    @mcp.tool()
    def explain(index: str, id: str, query: dict) -> dict:
        """
        解释文档评分
        
        参数:
            index: 索引名称
            id: 文档 ID
            query: 查询条件
        
        返回文档为什么匹配/不匹配查询，以及评分计算过程
        """
        client = get_client()
        body = {"query": query}
        return client.post(f"/{index}/_explain/{id}", body)
    
    @mcp.tool()
    def aggregate(index: str, aggs: dict, query: dict = None, size: int = 0) -> dict:
        """
        执行聚合查询
        
        参数:
            index: 索引名称
            aggs: 聚合定义
            query: 过滤条件（可选）
            size: 返回文档数（默认 0，仅返回聚合结果）
        
        示例 - 分组统计:
            aggregate("orders", aggs={
                "by_status": {"terms": {"field": "status"}}
            })
        
        示例 - 多级聚合:
            aggregate("orders", aggs={
                "by_category": {
                    "terms": {"field": "category"},
                    "aggs": {
                        "avg_price": {"avg": {"field": "price"}}
                    }
                }
            })
        
        示例 - 日期直方图:
            aggregate("logs", aggs={
                "by_day": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "calendar_interval": "day"
                    }
                }
            })
        """
        client = get_client()
        body = {"size": size, "aggs": aggs}
        if query:
            body["query"] = query
        result = client.post(f"/{index}/_search", body)
        return {
            "took_ms": result.get("took"),
            "total": result.get("hits", {}).get("total", {}).get("value", 0),
            "aggregations": result.get("aggregations", {})
        }
    
    @mcp.tool()
    def aggregate_simple(index: str, field: str, agg_type: str = "terms", size: int = 10) -> dict:
        """
        简化的聚合查询
        
        参数:
            index: 索引名称
            field: 聚合字段
            agg_type: 聚合类型 terms/avg/sum/min/max/cardinality/stats/extended_stats
            size: 返回桶数量（仅 terms 有效）
        
        示例:
            aggregate_simple("orders", "status", "terms")
            aggregate_simple("orders", "amount", "avg")
            aggregate_simple("users", "email", "cardinality")  # 去重计数
        """
        if agg_type == "terms":
            agg_body = {"terms": {"field": field, "size": size}}
        elif agg_type in ["stats", "extended_stats"]:
            agg_body = {agg_type: {"field": field}}
        else:
            agg_body = {agg_type: {"field": field}}
        
        result = aggregate(index, aggs={"result": agg_body})
        return result.get("aggregations", {}).get("result", {})
    
    @mcp.tool()
    def scroll_start(index: str, query: dict = None, size: int = 100, scroll: str = "5m", sort: list = None) -> dict:
        """
        开始滚动搜索（用于遍历大量数据）
        
        参数:
            index: 索引名称
            query: 查询条件
            size: 每批数量
            scroll: 滚动上下文保持时间
            sort: 排序规则
        
        返回 scroll_id 用于后续获取
        """
        client = get_client()
        body = {"size": size}
        if query:
            body["query"] = query
        if sort:
            body["sort"] = sort
        
        result = client.post(f"/{index}/_search?scroll={scroll}", body)
        return {
            "scroll_id": result.get("_scroll_id"),
            "total": result.get("hits", {}).get("total", {}).get("value", 0),
            "hits": result.get("hits", {}).get("hits", [])
        }
    
    @mcp.tool()
    def scroll_next(scroll_id: str, scroll: str = "5m") -> dict:
        """
        获取下一批滚动结果
        
        参数:
            scroll_id: 滚动 ID
            scroll: 滚动上下文保持时间
        """
        client = get_client()
        body = {"scroll": scroll, "scroll_id": scroll_id}
        result = client.post("/_search/scroll", body)
        return {
            "scroll_id": result.get("_scroll_id"),
            "hits": result.get("hits", {}).get("hits", [])
        }
    
    @mcp.tool()
    def scroll_clear(scroll_id: str = None, all: bool = False) -> dict:
        """
        清除滚动上下文
        
        参数:
            scroll_id: 滚动 ID
            all: 是否清除所有滚动上下文
        """
        client = get_client()
        if all:
            return client.delete("/_search/scroll/_all")
        else:
            return client.delete("/_search/scroll", {"scroll_id": [scroll_id]})
    
    @mcp.tool()
    def field_caps(index: str, fields: list) -> dict:
        """
        获取字段能力信息
        
        参数:
            index: 索引名称
            fields: 字段列表
        
        返回字段在各索引中的类型和能力
        """
        client = get_client()
        params = {"fields": ",".join(fields)}
        return client.get(f"/{index}/_field_caps", params)
    
    @mcp.tool()
    def terms_enum(index: str, field: str, string: str = None, size: int = 10) -> dict:
        """
        枚举字段的词项（用于自动补全）
        
        参数:
            index: 索引名称
            field: 字段名
            string: 前缀字符串
            size: 返回数量
        """
        client = get_client()
        body = {"field": field, "size": size}
        if string:
            body["string"] = string
        return client.post(f"/{index}/_terms_enum", body)
    
    @mcp.tool()
    def knn_search(index: str, field: str, query_vector: list, k: int = 10, num_candidates: int = 100, filter: dict = None) -> dict:
        """
        K近邻向量搜索
        
        参数:
            index: 索引名称
            field: 向量字段名
            query_vector: 查询向量
            k: 返回最近邻数量
            num_candidates: 候选数量
            filter: 过滤条件
        
        示例:
            knn_search("products", "embedding", [0.1, 0.2, 0.3, ...], k=10)
        """
        client = get_client()
        body = {
            "knn": {
                "field": field,
                "query_vector": query_vector,
                "k": k,
                "num_candidates": num_candidates
            }
        }
        if filter:
            body["knn"]["filter"] = filter
        
        result = client.post(f"/{index}/_search", body)
        return {
            "took_ms": result.get("took"),
            "hits": [{
                "_id": h.get("_id"),
                "_score": h.get("_score"),
                "_source": h.get("_source")
            } for h in result.get("hits", {}).get("hits", [])]
        }
    
    @mcp.tool()
    def sql_query(query: str, format: str = "json", fetch_size: int = 1000) -> dict:
        """
        执行 SQL 查询
        
        参数:
            query: SQL 查询语句
            format: 返回格式 json/csv/txt/yaml
            fetch_size: 每次获取的行数
        
        示例:
            sql_query("SELECT * FROM products WHERE price > 100 LIMIT 10")
            sql_query("SELECT category, COUNT(*) FROM products GROUP BY category")
        """
        client = get_client()
        body = {"query": query, "fetch_size": fetch_size}
        return client.post(f"/_sql?format={format}", body)
    
    @mcp.tool()
    def sql_translate(query: str) -> dict:
        """
        将 SQL 转换为 DSL
        
        参数:
            query: SQL 查询语句
        
        返回等效的 Elasticsearch DSL 查询
        """
        client = get_client()
        body = {"query": query}
        return client.post("/_sql/translate", body)
