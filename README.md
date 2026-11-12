# BTH5 - Reporting Service

Bài thực hành 5 môn SOA - Dịch vụ báo cáo (FastAPI).

## Kiến trúc

- Reporting Service (BTH5): port 8003, DB reports.db
- Order Service (BTH4): port 8002, DB orders.db
- Product Service (BTH3): port 8001, DB products.db
- Auth Service (BTH2): port 8000, DB users.db
- Xác thực qua JWT dùng chung SECRET_KEY từ Auth Service (TH2)
- Thu thập dữ liệu từ Product Service (TH3) và Order Service (TH4) để tính toán báo cáo doanh thu, chi phí, lợi nhuận

## Danh sách API

### Báo cáo sản phẩm (Product Reports)
- `GET /reports/products`: Lấy danh sách tất cả các báo cáo theo sản phẩm
- `GET /reports/products/{id}`: Lấy chi tiết báo cáo cho một sản phẩm
- `POST /reports/products`: Tạo báo cáo sản phẩm mới dựa trên dữ liệu từ dịch vụ sản phẩm và đơn hàng
- `DELETE /reports/products/{id}`: Xóa báo cáo sản phẩm

### Báo cáo đơn hàng (Order Reports)
- `GET /reports/orders`: Lấy danh sách tất cả các báo cáo theo đơn hàng
- `GET /reports/orders/{id}`: Lấy chi tiết báo cáo cho một đơn hàng
- `POST /reports/orders`: Tạo báo cáo đơn hàng mới dựa trên dữ liệu từ dịch vụ quản lý đơn hàng
- `DELETE /reports/orders/{id}`: Xóa báo cáo đơn hàng

## Cài đặt và chạy

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8003 --reload
```
