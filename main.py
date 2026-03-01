"""FastAPI 主应用"""
# Copyright (c) 2026 ailearncoder8@gmail.com
# MIT License

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="Wallabag API Proxy",
    description="Wallabag API 代理服务",
    version="0.1.0",
    debug=settings.debug
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)


@app.get("/")
async def root():
    """根路径，返回 API 信息"""
    return {
        "message": "Wallabag API Proxy Service",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "wallabag-api-proxy"
    }


if __name__ == "__main__":
    # 直接运行应用
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )