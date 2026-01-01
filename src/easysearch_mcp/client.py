"""
Easysearch HTTP 客户端
"""

import os
from contextlib import contextmanager
from typing import Generator, Any
import httpx


class EasysearchClient:
    """Easysearch HTTP 客户端封装"""
    
    def __init__(
        self,
        url: str = None,
        user: str = None,
        password: str = None,
        verify_ssl: bool = False,
        timeout: float = 30.0
    ):
        self.url = url or os.getenv("EASYSEARCH_URL", "https://localhost:9200")
        self.user = user or os.getenv("EASYSEARCH_USER", "admin")
        self.password = password or os.getenv("EASYSEARCH_PASSWORD", "")
        self.verify_ssl = verify_ssl
        self.timeout = timeout
    
    @contextmanager
    def _client(self) -> Generator[httpx.Client, None, None]:
        """创建 HTTP 客户端上下文"""
        with httpx.Client(
            base_url=self.url,
            auth=(self.user, self.password),
            verify=self.verify_ssl,
            timeout=self.timeout
        ) as client:
            yield client
    
    def get(self, path: str, params: dict = None) -> Any:
        """GET 请求"""
        with self._client() as client:
            r = client.get(path, params=params)
            r.raise_for_status()
            return r.json()
    
    def post(self, path: str, json: dict = None, content: str = None, headers: dict = None, params: dict = None) -> Any:
        """POST 请求"""
        with self._client() as client:
            if content:
                r = client.post(path, content=content, headers=headers, params=params)
            else:
                r = client.post(path, json=json, params=params)
            r.raise_for_status()
            return r.json()
    
    def put(self, path: str, json: dict = None) -> Any:
        """PUT 请求"""
        with self._client() as client:
            r = client.put(path, json=json)
            r.raise_for_status()
            return r.json()
    
    def delete(self, path: str, json: dict = None) -> Any:
        """DELETE 请求"""
        with self._client() as client:
            r = client.request("DELETE", path, json=json)
            r.raise_for_status()
            return r.json()
    
    def head(self, path: str) -> bool:
        """HEAD 请求，检查资源是否存在"""
        with self._client() as client:
            r = client.head(path)
            return r.status_code == 200


# 全局客户端实例
_client = None


def get_client() -> EasysearchClient:
    """获取全局客户端实例"""
    global _client
    if _client is None:
        _client = EasysearchClient()
    return _client
