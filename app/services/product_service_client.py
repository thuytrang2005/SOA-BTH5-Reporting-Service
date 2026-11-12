import os
from typing import Optional, Dict, Any, List

import httpx
from fastapi import HTTPException, status

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")


async def get_product(product_id: int, token: Optional[str] = None) -> Dict[str, Any]:
    # Lay thong tin san pham tu Product Service
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Khong the ket noi den Product Service o {PRODUCT_SERVICE_URL}: {str(exc)}"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Khong tim thay san pham co id = {product_id}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Loi tu Product Service: {response.text}"
        )

    return response.json()


async def get_all_products(token: Optional[str] = None) -> List[Dict[str, Any]]:
    # Lay danh sach tat ca san pham
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{PRODUCT_SERVICE_URL}/products"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Khong the ket noi den Product Service o {PRODUCT_SERVICE_URL}: {str(exc)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Loi tu Product Service: {response.text}"
        )

    return response.json()
