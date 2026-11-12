from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.order_report_controller import OrderReportController
from app.schemas import OrderReportCreate, OrderReportResponse

router = APIRouter(prefix="/reports/orders", tags=["Order Reports"])


@router.get("", response_model=List[OrderReportResponse])
def get_order_reports(db: Session = Depends(get_db)):
    """GET /reports/orders - Lấy danh sách tất cả các báo cáo theo đơn hàng"""
    return OrderReportController.get_all_order_reports(db)


@router.get("/{report_id}", response_model=OrderReportResponse)
def get_order_report(report_id: int, db: Session = Depends(get_db)):
    """GET /reports/orders/{id} - Lấy chi tiết báo cáo cho một đơn hàng"""
    return OrderReportController.get_order_report_by_id(db, report_id)


@router.post(
    "",
    response_model=OrderReportResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_order_report(
    data: OrderReportCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """POST /reports/orders - Tạo báo cáo đơn hàng mới"""
    token = getattr(request.state, "token", None)
    return await OrderReportController.create_order_report(db, data, token=token)


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
def delete_order_report(report_id: int, db: Session = Depends(get_db)):
    """DELETE /reports/orders/{id} - Xóa báo cáo đơn hàng"""
    return OrderReportController.delete_order_report(db, report_id)
