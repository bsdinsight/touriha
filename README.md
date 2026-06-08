# Touriha

**Touriha** — nền tảng **quản lý tour & lữ hành** mã nguồn mở, xây trên [Odoo 19 Community](https://github.com/odoo/odoo) + app Hướng dẫn viên (React Native / Expo). Một sản phẩm của [BSD Insight](https://bsdinsight.com).

> CRM → Báo giá (passenger grid) → Điều hành & định mức tự động → Costing 3 giai đoạn → Mua dịch vụ (PO) → Cổng đối tác → App HDV → Kế toán quản trị P&L.

## Phiên bản (open-core)

| Tầng | Giấy phép | Dành cho |
|---|---|---|
| **Community** (repo này) | LGPL-3 | Tự cài, đầy đủ nghiệp vụ cơ bản, **không giới hạn** |
| **Enterprise** (`touriha-enterprise`, private) | Thương mại (OPL-1) | Recommendation engine, dashboard BI, payment, automation nâng cao |
| **Touriha Cloud** (SaaS) | — | Bản host sẵn; gói Free **100 tours / 50 pax** → trả phí mở rộng |

Cần bản Enterprise/Cloud hoặc nâng giới hạn: **daibt@bsdinsight.com** · **0918 339 689** (Đại).

## Module

- `touriha_base` — menu gốc + nền tảng chung.
- `touriha_operations` — **Tour + passenger grid** (đã có).
- `touriha_crm`, `touriha_costing`, `touriha_portal` — đang phát triển (xem [`docs/architecture.md`](docs/architecture.md)).

## Chạy thử (Docker)

```bash
git clone https://github.com/bsdinsight/touriha.git && cd touriha
cp config/odoo.conf.example config/odoo.conf   # đổi admin_passwd
docker compose up -d
```

Mở http://localhost:8169 → tạo database → cài app **Touriha**.
(Cổng 8169 để không đụng các stack Odoo khác đang chạy 8069.)

Cập nhật module bằng dòng lệnh:

```bash
docker compose run --rm touriha_odoo odoo -d touriha -u touriha_operations --stop-after-init
```

## Tài liệu

- Kiến trúc & lộ trình: [`docs/architecture.md`](docs/architecture.md)
- Hướng dẫn cho dev / Claude: [`CLAUDE.md`](CLAUDE.md)
- Demo: https://touriha.bsdinsights.com

## License

Community: **LGPL-3** (xem [`LICENSE`](LICENSE)). Module Enterprise phát hành riêng theo giấy phép thương mại.
