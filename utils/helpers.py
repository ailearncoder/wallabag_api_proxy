"""工具函数模块"""
# Copyright (c) 2026 ailearncoder8@gmail.com
# MIT License

import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def safe_json_load(file_path: str) -> Optional[Dict[str, Any]]:
    """
    安全地加载 JSON 文件

    Args:
        file_path: JSON 文件路径

    Returns:
        解析的 JSON 数据或 None
    """
    try:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError, Exception) as e:
        logger.error(f"加载 JSON 文件失败 {file_path}: {e}")
    return None


def safe_json_save(data: Dict[str, Any], file_path: str) -> bool:
    """
    安全地保存 JSON 文件

    Args:
        data: 要保存的数据
        file_path: JSON 文件路径

    Returns:
        保存是否成功
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (TypeError, IOError, Exception) as e:
        logger.error(f"保存 JSON 文件失败 {file_path}: {e}")
        return False


def validate_url(url: str) -> bool:
    """
    验证 URL 格式

    Args:
        url: 要验证的 URL

    Returns:
        URL 是否有效
    """
    if not url or not isinstance(url, str):
        return False

    url = url.strip()
    return url.startswith(('http://', 'https://'))


def format_response(message: str, data: Any = None, success: bool = True) -> Dict[str, Any]:
    """
    格式化 API 响应

    Args:
        message: 响应消息
        data: 响应数据
        success: 是否成功

    Returns:
        格式化的响应字典
    """
    response = {
        "message": message,
        "success": success
    }

    if data is not None:
        response["data"] = data

    return response


def get_client_ip(request) -> str:
    """
    从请求中获取客户端 IP

    Args:
        request: FastAPI 请求对象

    Returns:
        客户端 IP 地址
    """
    # 尝试从各种头部获取真实 IP
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip

    # 回退到客户端 IP
    return request.client.host if request.client else "unknown"