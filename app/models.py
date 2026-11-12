from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class OrderReport(Base):
    __tablename__ = "orders_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, nullable=False, index=True)
    total_revenue = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_cost = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_profit = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Lien ket voi product_reports
    product_reports = relationship(
        "ProductReport",
        back_populates="order_report",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class ProductReport(Base):
    __tablename__ = "product_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_report_id = Column(Integer, ForeignKey("orders_reports.id", ondelete="CASCADE"), nullable=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    total_sold = Column(Integer, nullable=False, default=0)
    revenue = Column(Numeric(10, 2), nullable=False, default=0.00)
    cost = Column(Numeric(10, 2), nullable=False, default=0.00)
    profit = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    order_report = relationship("OrderReport", back_populates="product_reports")
