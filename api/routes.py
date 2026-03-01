"""API 路由和控制器"""
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from core.client import WallabagClient, EntryRequest

router = APIRouter(prefix="/api/wallabag", tags=["wallabag"])

# 创建 Wallabag 客户端实例
client = WallabagClient()


class EntryResponse(BaseModel):
    """文章条目响应模型"""
    message: str
    data: Dict[str, Any]


@router.post("/entries", response_model=EntryResponse)
async def add_entry(request: EntryRequest):
    """
    添加文章到 Wallabag

    该接口会：
    1. 接收包含 URL 的 POST 请求
    2. 自动处理 OAuth2 认证
    3. 调用 Wallabag API 添加文章
    4. 返回 Wallabag 的原始响应
    """
    try:
        # 调用 Wallabag 客户端添加文章
        result = await client.add_entry(request.url)

        return EntryResponse(
            message="文章添加成功",
            data=result
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加文章失败: {str(e)}"
        )


@router.get("/token-info")
async def get_token_info():
    """获取当前令牌信息"""
    try:
        token_info = await client.get_token_info()
        if token_info:
            return {
                "message": "令牌信息获取成功",
                "data": token_info
            }
        else:
            return {
                "message": "暂无令牌信息",
                "data": None
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取令牌信息失败: {str(e)}"
        )


@router.post("/refresh-tokens")
async def refresh_tokens():
    """手动刷新令牌"""
    try:
        token_info = await client.refresh_tokens()
        return {
            "message": "令牌刷新成功",
            "data": token_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"令牌刷新失败: {str(e)}"
        )


@router.delete("/tokens")
async def clear_tokens():
    """清除所有令牌"""
    try:
        await client.clear_tokens()
        return {
            "message": "令牌清除成功"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"令牌清除失败: {str(e)}"
        )