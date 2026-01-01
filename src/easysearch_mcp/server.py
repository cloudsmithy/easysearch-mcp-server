"""
Easysearch MCP Server 主入口
"""

from mcp.server.fastmcp import FastMCP
from .tools import register_all_tools

# 创建 MCP Server
mcp = FastMCP("easysearch")

# 注册所有工具
register_all_tools(mcp)


def main():
    """主入口"""
    mcp.run()


if __name__ == "__main__":
    main()
