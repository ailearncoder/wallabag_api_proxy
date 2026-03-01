#!/usr/bin/env python3
"""测试脚本"""
# Copyright (c) 2026 ailearncoder8@gmail.com
# MIT License

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.auth import AuthManager
from core.client import WallabagClient
from config import settings


async def test_auth_manager():
    """测试认证管理器"""
    print("=== 测试认证管理器 ===")

    # 检查配置
    print(f"Wallabag URL: {settings.wallabag_url}")
    print(f"Client ID: {settings.client_id[:10]}..." if settings.client_id else "Client ID: 未设置")
    print(f"Username: {settings.username}" if settings.username else "Username: 未设置")

    if not settings.validate_credentials():
        print("❌ 配置不完整，请检查 .env 文件")
        return False

    auth_manager = AuthManager()

    try:
        # 测试获取令牌
        token = await auth_manager.get_valid_token()
        print(f"✅ 成功获取令牌: {token[:50]}...")

        # 检查令牌信息
        token_info = auth_manager.get_token_info()
        if token_info:
            print(f"✅ 令牌信息:")
            print(f"  - 访问令牌: {token_info.access_token[:30]}...")
            print(f"  - 刷新令牌: {token_info.refresh_token[:30]}...")
            print(f"  - 过期时间: {token_info.expires_in} 秒")
            print(f"  - 令牌类型: {token_info.token_type}")

        return True

    except Exception as e:
        print(f"❌ 认证测试失败: {e}")
        return False


async def test_wallabag_client():
    """测试 Wallabag 客户端"""
    print("\n=== 测试 Wallabag 客户端 ===")

    client = WallabagClient()

    try:
        # 测试获取令牌信息
        token_info = await client.get_token_info()
        if token_info:
            print("✅ 当前令牌信息:")
            print(f"  - 访问令牌: {token_info['access_token'][:30]}...")
            print(f"  - 过期时间: {token_info['expires_in']} 秒")
        else:
            print("ℹ️  暂无令牌信息")

        # 测试添加文章（使用测试 URL）
        test_url = "https://httpbin.org/html"
        print(f"\n🔄 尝试添加测试文章: {test_url}")

        result = await client.add_entry(test_url)
        print("✅ 文章添加成功:")
        print(f"  - 响应类型: {type(result)}")
        print(f"  - 响应大小: {len(str(result))} 字符")

        return True

    except Exception as e:
        print(f"❌ Wallabag 客户端测试失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("🚀 开始测试 Wallabag API 代理服务")
    print("=" * 50)

    # 测试认证管理器
    auth_success = await test_auth_manager()

    # 测试 Wallabag 客户端
    client_success = await test_wallabag_client()

    print("\n" + "=" * 50)
    if auth_success and client_success:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)