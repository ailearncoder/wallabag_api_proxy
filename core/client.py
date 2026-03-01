"""Wallabag API 客户端"""
import urllib.parse
from typing import Dict, Any, Optional

import httpx
from pydantic import BaseModel

from config import settings
from core.auth import AuthManager


class EntryRequest(BaseModel):
    """文章条目请求模型"""
    url: str


class WallabagClient:
    """Wallabag API 客户端"""

    def __init__(self):
        self.auth_manager = AuthManager()
        self.base_url = settings.wallabag_url

    async def add_entry(self, url: str) -> Dict[str, Any]:
        """
        添加文章条目到 Wallabag

        Args:
            url: 要添加的文章 URL

        Returns:
            Wallabag API 响应数据

        Raises:
            httpx.HTTPError: HTTP 请求错误
            Exception: 其他错误
        """
        # 获取有效的认证令牌
        auth_header = await self.auth_manager.get_valid_token()

        # 构建请求 URL (使用 .json 后缀)
        api_url = f"{settings.entries_url}"

        # 发送 POST 请求
        async with httpx.AsyncClient(verify=settings.verify_ssl) as client:
            response = await client.post(
                api_url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": auth_header
                },
                json={"url": url}  # 使用 JSON 格式发送 URL
            )

            # 检查响应状态
            response.raise_for_status()

            # 返回 JSON 响应
            return response.json()

    async def get_token_info(self) -> Optional[Dict[str, Any]]:
        """获取当前令牌信息"""
        token_info = self.auth_manager.get_token_info()
        if token_info:
            return token_info.model_dump()
        return None

    async def refresh_tokens(self) -> Dict[str, Any]:
        """手动刷新令牌"""
        auth_header = await self.auth_manager.get_valid_token()
        token_info = self.auth_manager.get_token_info()
        if token_info:
            return token_info.model_dump()
        return {}

    async def clear_tokens(self) -> None:
        """清除所有令牌"""
        await self.auth_manager.clear_tokens()