"""
Easysearch MCP Server 主入口

支持两种运行模式：
- stdio 模式（默认）：python -m easysearch_mcp.server
- HTTP/SSE 模式：python -m easysearch_mcp.server --sse --port 8080
"""

import argparse
from mcp.server.fastmcp import FastMCP
from .tools import register_all_tools

# 创建 MCP Server
mcp = FastMCP("easysearch")

# 注册所有工具
register_all_tools(mcp)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description="Easysearch MCP Server")
    parser.add_argument("--sse", action="store_true", help="以 HTTP/SSE 模式运行")
    parser.add_argument("--host", default="0.0.0.0", help="SSE 模式监听地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="SSE 模式监听端口 (默认: 8080)")
    args = parser.parse_args()

    if args.sse:
        import uvicorn
        print(f"Starting Easysearch MCP Server in SSE mode on {args.host}:{args.port}")
        uvicorn.run(mcp.sse_app(), host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
