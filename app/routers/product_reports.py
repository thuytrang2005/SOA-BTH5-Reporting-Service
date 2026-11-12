from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.product_report_controller import ProductReportController
from app.schemas import ProductReportCreate, ProductReportResponse

router = APIRouter(prefix="/reports/products", tags=["Product Reports"])


@router.get("", response_model=List[ProductReportResponse])
def get_product_reports(db: Session = Depends(get_db)):
    """GET /reports/products - Lấy danh sách tất cả các báo cáo theo sản phẩm"""
    return ProductReportController.get_all_product_reports(db)


@router.get("/{report_id}", response_model=ProductReportResponse)
def get_product_report(report_id: int, db: Session = Depends(get_db)):
    """GET /reports/products/{id} - Lấy chi tiết báo cáo cho một sản phẩm"""
    return ProductReportController.get_product_report_by_id(db, report_id)


@router.post(
    "",
    response_model=ProductReportResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product_report(
    data: ProductReportCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """POST /reports/products - Tạo báo cáo sản phẩm mới"""
    token = getattr(request.state, "token", None)
    return await ProductReportController.create_product_report(db, data, token=token)


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
def delete_product_report(report_id: int, db: Session = Depends(get_db)):
    """DELETE /reports/products/{id} - Xóa báo cáo sản phẩm"""
    return ProductReportController.delete_product_report(db, report_id)
