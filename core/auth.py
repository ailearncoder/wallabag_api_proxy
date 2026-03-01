"""认证模块 - 处理 OAuth2 认证和令牌管理"""
import json
import time
from typing import Dict, Optional
from pathlib import Path

import httpx
from pydantic import BaseModel

from config import settings


class TokenInfo(BaseModel):
    """令牌信息模型"""
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str
    scope: Optional[str] = None
    created_at: Optional[float] = None

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = time.time()
        super().__init__(**data)

    @property
    def is_expired(self) -> bool:
        """检查访问令牌是否过期"""
        if not self.created_at:
            return True
        return time.time() > (self.created_at + self.expires_in - 300)  # 提前5分钟刷新

    @property
    def authorization_header(self) -> str:
        """获取授权头部"""
        return f"Bearer {self.access_token}"


class AuthManager:
    """认证管理器"""

    def __init__(self):
        self.tokens_file = Path(settings.tokens_file)
        self._token_info: Optional[TokenInfo] = None
        self._load_tokens()

    def _load_tokens(self) -> None:
        """从文件加载令牌信息"""
        if self.tokens_file.exists():
            try:
                with open(self.tokens_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._token_info = TokenInfo(**data)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"加载令牌文件失败: {e}")
                self._token_info = None

    def _save_tokens(self) -> None:
        """保存令牌信息到文件"""
        if self._token_info:
            try:
                with open(self.tokens_file, 'w', encoding='utf-8') as f:
                    json.dump(self._token_info.model_dump(), f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"保存令牌文件失败: {e}")

    async def _request_new_tokens(self) -> TokenInfo:
        """请求新的访问令牌"""
        async with httpx.AsyncClient(verify=settings.verify_ssl) as client:
            response = await client.post(
                settings.oauth_token_url,
                data={
                    "grant_type": "password",
                    "client_id": settings.client_id,
                    "client_secret": settings.client_secret,
                    "username": settings.username,
                    "password": settings.password
                }
            )
            response.raise_for_status()
            data = response.json()
            return TokenInfo(**data)

    async def _refresh_tokens(self, refresh_token: str) -> TokenInfo:
        """使用刷新令牌获取新的访问令牌"""
        async with httpx.AsyncClient(verify=settings.verify_ssl) as client:
            response = await client.post(
                settings.oauth_token_url,
                data={
                    "grant_type": "refresh_token",
                    "client_id": settings.client_id,
                    "client_secret": settings.client_secret,
                    "refresh_token": refresh_token
                }
            )
            response.raise_for_status()
            data = response.json()
            return TokenInfo(**data)

    async def get_valid_token(self) -> str:
        """获取有效的访问令牌"""
        # 如果没有令牌信息或访问令牌过期
        if not self._token_info or self._token_info.is_expired:
            try:
                # 尝试使用刷新令牌
                if self._token_info and self._token_info.refresh_token:
                    try:
                        new_tokens = await self._refresh_tokens(self._token_info.refresh_token)
                        self._token_info = new_tokens
                        self._save_tokens()
                        return self._token_info.authorization_header
                    except Exception as e:
                        print(f"刷新令牌失败: {e}")

                # 获取新的令牌
                new_tokens = await self._request_new_tokens()
                self._token_info = new_tokens
                self._save_tokens()
                return self._token_info.authorization_header

            except Exception as e:
                print(f"获取访问令牌失败: {e}")
                raise

        return self._token_info.authorization_header

    def get_token_info(self) -> Optional[TokenInfo]:
        """获取当前令牌信息"""
        return self._token_info

    async def clear_tokens(self) -> None:
        """清除令牌信息"""
        self._token_info = None
        if self.tokens_file.exists():
            self.tokens_file.unlink()