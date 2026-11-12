from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ProductReportBase(BaseModel):
    product_id: int
    total_sold: int = 0
    revenue: Decimal = Decimal("0.00")
    cost: Decimal = Decimal("0.00")
    profit: Decimal = Decimal("0.00")


class ProductReportCreate(BaseModel):
    product_id: int
    order_report_id: Optional[int] = None
    total_sold: Optional[int] = None
    revenue: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    cost_ratio: Optional[Decimal] = Decimal("0.70")


class ProductReportResponse(BaseModel):
    id: int
    order_report_id: Optional[int] = None
    product_id: int
    total_sold: int
    revenue: Decimal
    cost: Decimal
    profit: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderReportBase(BaseModel):
    order_id: int
    total_revenue: Decimal = Decimal("0.00")
    total_cost: Decimal = Decimal("0.00")
    total_profit: Decimal = Decimal("0.00")


class OrderReportCreate(BaseModel):
    order_id: int
    total_cost: Optional[Decimal] = None
    cost_ratio: Optional[Decimal] = Decimal("0.70")


class OrderReportResponse(BaseModel):
    id: int
    order_id: int
    total_revenue: Decimal
    total_cost: Decimal
    total_profit: Decimal
    created_at: datetime
    updated_at: datetime
    product_reports: List[ProductReportResponse] = []

    model_config = ConfigDict(from_attributes=True)
