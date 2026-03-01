#!/usr/bin/env python3
"""配置检查脚本"""
# Copyright (c) 2026 ailearncoder8@gmail.com
# MIT License

import os
from config import settings

print("=== 配置检查 ===")
print(f"WALLABAG_URL: {settings.wallabag_url}")
print(f"CLIENT_ID: {settings.client_id}")
print(f"CLIENT_SECRET: {settings.client_secret[:10]}..." if settings.client_secret else "CLIENT_SECRET: 未设置")
print(f"USERNAME: {settings.username}")
print(f"PASSWORD: {'*' * len(settings.password) if settings.password else '未设置'}")
print(f"VERIFY_SSL: {settings.verify_ssl}")
print(f"OAuth Token URL: {settings.oauth_token_url}")
print(f"Entries URL: {settings.entries_url}")
print(f"配置验证: {'✅ 通过' if settings.validate_credentials() else '❌ 失败'}")