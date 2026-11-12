import os
from typing import Optional, Dict, Any, List

import httpx
from fastapi import HTTPException, status

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8002")


async def get_order(order_id: int, token: Optional[str] = None) -> Dict[str, Any]:
    # Lay thong tin don hang tu Order Service
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{ORDER_SERVICE_URL}/orders/{order_id}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Khong the ket noi den Order Service o {ORDER_SERVICE_URL}: {str(exc)}"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Khong tim thay don hang co id = {order_id}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Loi tu Order Service: {response.text}"
        )

    return response.json()


async def get_all_orders(token: Optional[str] = None) -> List[Dict[str, Any]]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{ORDER_SERVICE_URL}/orders"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Khong the ket noi den Order Service o {ORDER_SERVICE_URL}: {str(exc)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Loi tu Order Service: {response.text}"
        )

    return response.json()


async def get_all_order_items(order_id: Optional[int] = None, token: Optional[str] = None) -> List[Dict[str, Any]]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{ORDER_SERVICE_URL}/order_items"
    if order_id is not None:
        url += f"?order_id={order_id}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Khong the ket noi den Order Service o {ORDER_SERVICE_URL}: {str(exc)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Loi tu Order Service: {response.text}"
        )

    return response.json()
