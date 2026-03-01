"""异常处理模块"""
from typing import Dict, Any
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class WallabagAPIError(Exception):
    """Wallabag API 相关异常基类"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(WallabagAPIError):
    """认证相关异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401)


class TokenExpiredError(WallabagAPIError):
    """令牌过期异常"""
    def __init__(self, message: str = "访问令牌已过期"):
        super().__init__(message, 401)


class InvalidURLError(WallabagAPIError):
    """无效 URL 异常"""
    def __init__(self, message: str = "无效的 URL"):
        super().__init__(message, 400)


def wallabag_api_exception_handler(request: Request, exc: WallabagAPIError):
    """Wallabag API 异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "success": False,
            "error_type": exc.__class__.__name__
        }
    )


def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "success": False
        }
    )


def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "服务器内部错误",
            "success": False,
            "error_type": exc.__class__.__name__
        }
    )