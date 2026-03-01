#!/bin/bash

echo "=== Wallabag API 测试 ==="

# 测试服务状态
echo -e "\n1. 测试服务状态:"
curl -s -X GET http://localhost:8000/health | jq 2>/dev/null || curl -s -X GET http://localhost:8000/health

# 测试添加文章
echo -e "\n2. 测试添加文章:"
curl -s -X POST http://localhost:8000/api/wallabag/entries \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/Y50wDqffScij2_y5tvwLQw"}' | jq 2>/dev/null || curl -s -X POST http://localhost:8000/api/wallabag/entries \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/Y50wDqffScij2_y5tvwLQw"}'

# 测试令牌信息
echo -e "\n3. 查看令牌信息:"
curl -s -X GET http://localhost:8000/api/wallabag/token-info | jq 2>/dev/null || curl -s -X GET http://localhost:8000/api/wallabag/token-info

echo -e "\n=== 测试完成 ==="
