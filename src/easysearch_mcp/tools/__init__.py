"""
Easysearch MCP 工具模块
"""

from .cluster import register_cluster_tools
from .indices import register_indices_tools
from .documents import register_document_tools
from .search import register_search_tools
from .cat import register_cat_tools
from .nodes import register_nodes_tools
from .snapshot import register_snapshot_tools
from .slm import register_slm_tools
from .tasks import register_tasks_tools
from .ingest import register_ingest_tools
from .ilm import register_ilm_tools


def register_all_tools(mcp):
    """注册所有工具"""
    register_cluster_tools(mcp)
    register_indices_tools(mcp)
    register_document_tools(mcp)
    register_search_tools(mcp)
    register_cat_tools(mcp)
    register_nodes_tools(mcp)
    register_snapshot_tools(mcp)
    register_slm_tools(mcp)
    register_tasks_tools(mcp)
    register_ingest_tools(mcp)
    register_ilm_tools(mcp)
