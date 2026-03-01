# Wallabag API Proxy Service

这是一个使用 FastAPI 构建的 Wallabag API 代理服务，用于简化 Wallabag API 的调用流程。

## 功能特性

- 接收 POST 请求并提取 URL
- 自动处理 Wallabag OAuth2 认证
- 智能管理访问令牌和刷新令牌
- 代理 Wallabag API 调用
- 返回 Wallabag API 的原始响应

## 环境变量配置

复制 `.env.example` 文件为 `.env` 并修改配置：

```bash
cp .env.example .env
```

修改 `.env` 文件中的配置：

```env
# Wallabag 服务器配置
WALLABAG_URL=your_wallabag_server_url

# OAuth2 客户端配置
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

# 用户凭证
USERNAME=your_username
PASSWORD=your_password

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 安装和运行

### 使用 uv 管理依赖

```bash
# 安装依赖
uv sync

# 运行开发服务器
uv run uvicorn main:app --reload

# 或者直接运行
uv run python main.py
```

## API 接口

### 添加文章

```http
POST /api/wallabag/entries HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "url": "https://mp.weixin.qq.com/s/sJ7LqNtQQCMSNBy-UnAtpA"
}
```

响应：
```json
{
  "message": "文章添加成功",
  "data": {
    "is_archived": false,
    "is_starred": false,
    "user_name": "user",
    "user_email": "user@gmail.com",
    "user_id": 1,
    "tags": [],
    "is_public": false,
    "id": 123,
    "uid": null,
    "title": "文章标题",
    "url": "https://mp.weixin.qq.com/s/sJ7LqNtQQCMSNBy-UnAtpA",
    "hashed_url": "hashed_value",
    "origin_url": null,
    "given_url": "https://mp.weixin.qq.com/s/sJ7LqNtQQCMSNBy-UnAtpA",
    "hashed_given_url": "hashed_value",
    "archived_at": null,
    "content": "<p>文章内容...</p>",
    "created_at": "2024-01-01T00:00:00+0000",
    "updated_at": "2024-01-01T00:00:00+0000",
    "published_at": null,
    "published_by": [],
    "starred_at": null,
    "annotations": [],
    "mimetype": "text/html",
    "language": "zh",
    "reading_time": 5,
    "domain_name": "mp.weixin.qq.com",
    "preview_picture": null,
    "http_status": "200",
    "headers": "HTTP headers"
  }
}
```

### 其他管理接口

```http
# 获取令牌信息
GET /api/wallabag/token-info

# 手动刷新令牌
POST /api/wallabag/refresh-tokens

# 清除令牌
DELETE /api/wallabag/tokens
```

## 测试命令

### 基础测试

```bash
# 测试服务是否正常运行
curl -X GET http://localhost:8000/health

# 获取服务信息
curl -X GET http://localhost:8000/
```

### 功能测试

```bash
# 添加文章到 Wallabag
curl -X POST http://localhost:8000/api/wallabag/entries \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/sJ7LqNtQQCMSNBy-UnAtpA"}'

# 添加测试文章
curl -X POST http://localhost:8000/api/wallabag/entries \
  -H "Content-Type: application/json" \
  -d '{"url":"https://httpbin.org/html"}'
```

### 令牌管理测试

```bash
# 查看当前令牌信息
curl -X GET http://localhost:8000/api/wallabag/token-info

# 手动刷新令牌
curl -X POST http://localhost:8000/api/wallabag/refresh-tokens

# 清除所有令牌
curl -X DELETE http://localhost:8000/api/wallabag/tokens
```

### 批量测试脚本

创建测试脚本 `test_api.sh`：

```bash
#!/bin/bash

echo "=== Wallabag API 测试 ==="

# 测试服务状态
echo "\n1. 测试服务状态:"
curl -s -X GET http://localhost:8000/health | jq

# 测试添加文章
echo "\n2. 测试添加文章:"
curl -s -X POST http://localhost:8000/api/wallabag/entries \
  -H "Content-Type: application/json" \
  -d '{"url":"https://httpbin.org/html"}' | jq

# 测试令牌信息
echo "\n3. 查看令牌信息:"
curl -s -X GET http://localhost:8000/api/wallabag/token-info | jq

echo "\n=== 测试完成 ==="
```

使用方法：
```bash
chmod +x test_api.sh
./test_api.sh
```

> 注意：需要安装 `jq` 工具来格式化 JSON 输出

## 项目结构

```
wallabag_api/
├── api/              # API 路由和控制器
│   └── routes.py     # API 路由定义
├── core/             # 核心业务逻辑
│   ├── auth.py       # 认证管理
│   └── client.py     # Wallabag 客户端
├── utils/            # 工具函数
│   ├── helpers.py    # 辅助函数
│   └── exceptions.py # 异常处理
├── main.py          # 应用入口
├── config.py        # 配置管理
├── .env             # 环境变量配置
├── .env.example     # 环境变量示例
├── pyproject.toml   # 项目配置
└── README.md        # 项目说明
```

## 开发

### 代码格式化

```bash
uv run black .
uv run isort .
```

### 类型检查

```bash
uv run mypy .
```

### 运行测试

```bash
uv run pytest
```

## 认证流程

1. 首次请求时使用用户名密码获取访问令牌
2. 令牌信息自动保存到 `tokens.json` 文件
3. 后续请求优先使用保存的访问令牌
4. 访问令牌过期时自动使用刷新令牌获取新令牌
5. 刷新令牌过期时重新使用用户名密码认证

## 错误处理

服务提供完善的错误处理机制：
- HTTP 状态码标准化
- 详细的错误信息返回
- 日志记录
- 异常分类处理