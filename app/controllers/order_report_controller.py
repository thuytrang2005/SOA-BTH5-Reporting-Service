from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import OrderReport, ProductReport
from app.schemas import OrderReportCreate
from app.services.order_service_client import get_order


class OrderReportController:
    @staticmethod
    def get_all_order_reports(db: Session) -> List[OrderReport]:
        return db.query(OrderReport).order_by(OrderReport.id.desc()).all()

    @staticmethod
    def get_order_report_by_id(db: Session, report_id: int) -> OrderReport:
        report = db.query(OrderReport).filter(OrderReport.id == report_id).first()
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Khong tim thay bao cao don hang co id = {report_id}"
            )
        return report

    @staticmethod
    async def create_order_report(
        db: Session,
        data: OrderReportCreate,
        token: Optional[str] = None
    ) -> OrderReport:
        # Goi Order Service lay thong tin don hang
        order_data = await get_order(data.order_id, token=token)

        total_revenue = Decimal(str(order_data.get("total_amount", "0.00")))
        cost_ratio = data.cost_ratio or Decimal("0.70")

        if data.total_cost is not None:
            total_cost = data.total_cost
        else:
            total_cost = (total_revenue * cost_ratio).quantize(Decimal("0.01"))

        total_profit = total_revenue - total_cost

        # Tao bao cao don hang
        new_report = OrderReport(
            order_id=data.order_id,
            total_revenue=total_revenue,
            total_cost=total_cost,
            total_profit=total_profit
        )
        db.add(new_report)
        db.flush()

        # Tu dong tao cac product_reports tu cac mat hang trong don
        order_items = order_data.get("items", [])
        for item in order_items:
            item_sold = int(item.get("quantity", 0))
            item_revenue = Decimal(str(item.get("total_price", "0.00")))
            item_cost = (item_revenue * cost_ratio).quantize(Decimal("0.01"))
            item_profit = item_revenue - item_cost

            prod_report = ProductReport(
                order_report_id=new_report.id,
                product_id=item.get("product_id"),
                total_sold=item_sold,
                revenue=item_revenue,
                cost=item_cost,
                profit=item_profit
            )
            db.add(prod_report)

        db.commit()
        db.refresh(new_report)
        return new_report

    @staticmethod
    def delete_order_report(db: Session, report_id: int) -> dict:
        report = OrderReportController.get_order_report_by_id(db, report_id)
        db.delete(report)
        db.commit()
        return {"message": f"Da xoa bao cao don hang id = {report_id}"}
