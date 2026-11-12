from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import ProductReport
from app.schemas import ProductReportCreate
from app.services.product_service_client import get_product
from app.services.order_service_client import get_all_order_items


class ProductReportController:
    @staticmethod
    def get_all_product_reports(db: Session) -> List[ProductReport]:
        return db.query(ProductReport).order_by(ProductReport.id.desc()).all()

    @staticmethod
    def get_product_report_by_id(db: Session, report_id: int) -> ProductReport:
        report = db.query(ProductReport).filter(ProductReport.id == report_id).first()
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Khong tim thay bao cao san pham co id = {report_id}"
            )
        return report

    @staticmethod
    async def create_product_report(
        db: Session,
        data: ProductReportCreate,
        token: Optional[str] = None
    ) -> ProductReport:
        # Kiem tra san pham co ton tai ben Product Service
        await get_product(data.product_id, token=token)

        cost_ratio = data.cost_ratio or Decimal("0.70")

        # Neu nguoi dung truyen truc tiep so lieu thi lay theo input
        if data.total_sold is not None and data.revenue is not None:
            total_sold = data.total_sold
            revenue = data.revenue
        else:
            # Tu dong tong hop tu Order Service
            all_items = await get_all_order_items(token=token)
            matching_items = [item for item in all_items if item.get("product_id") == data.product_id]
            total_sold = sum((int(item.get("quantity", 0)) for item in matching_items), 0)
            revenue = sum((Decimal(str(item.get("total_price", "0.00"))) for item in matching_items), Decimal("0.00"))

        if data.cost is not None:
            cost = data.cost
        else:
            cost = (revenue * cost_ratio).quantize(Decimal("0.01"))

        profit = revenue - cost

        new_report = ProductReport(
            order_report_id=data.order_report_id,
            product_id=data.product_id,
            total_sold=total_sold,
            revenue=revenue,
            cost=cost,
            profit=profit
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report

    @staticmethod
    def delete_product_report(db: Session, report_id: int) -> dict:
        report = ProductReportController.get_product_report_by_id(db, report_id)
        db.delete(report)
        db.commit()
        return {"message": f"Da xoa bao cao san pham id = {report_id}"}
