"""配置管理模块"""
# Copyright (c) 2026 ailearncoder8@gmail.com
# MIT License

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()


class Settings(BaseModel):
    """应用配置设置"""

    # Wallabag 服务器配置
    wallabag_url: str = Field(
        default_factory=lambda: os.getenv("WALLABAG_URL", "https://wallabag.mac.axyz.cc:30923"),
        description="Wallabag 服务器地址"
    )

    # OAuth2 客户端配置
    client_id: str = Field(
        default_factory=lambda: os.getenv("CLIENT_ID", ""),
        description="OAuth2 客户端 ID"
    )

    client_secret: str = Field(
        default_factory=lambda: os.getenv("CLIENT_SECRET", ""),
        description="OAuth2 客户端密钥"
    )

    # 用户凭证
    username: str = Field(
        default_factory=lambda: os.getenv("USERNAME", ""),
        description="用户名"
    )

    password: str = Field(
        default_factory=lambda: os.getenv("PASSWORD", ""),
        description="密码"
    )

    # 服务器配置
    host: str = Field(
        default_factory=lambda: os.getenv("HOST", "0.0.0.0"),
        description="服务器主机地址"
    )

    port: int = Field(
        default_factory=lambda: int(os.getenv("PORT", "8000")),
        description="服务器端口"
    )

    debug: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "False").lower() == "true",
        description="调试模式"
    )

    # 令牌文件路径
    tokens_file: str = Field(
        default="tokens.json",
        description="令牌存储文件路径"
    )

    # SSL 配置
    verify_ssl: bool = Field(
        default_factory=lambda: os.getenv("VERIFY_SSL", "True").lower() == "true",
        description="是否验证 SSL 证书"
    )

    @property
    def oauth_token_url(self) -> str:
        """OAuth2 令牌获取 URL"""
        return f"{self.wallabag_url}/oauth/v2/token"

    @property
    def entries_url(self) -> str:
        """文章条目 API URL"""
        return f"{self.wallabag_url}/api/entries.json"

    def validate_credentials(self) -> bool:
        """验证必要配置是否存在"""
        required_fields = [
            self.client_id,
            self.client_secret,
            self.username,
            self.password
        ]
        return all(field for field in required_fields)


# 全局配置实例
settings = Settings()