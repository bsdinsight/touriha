# Touriha — Hướng dẫn cho Claude

Touriha là ERP **quản lý tour/lữ hành** (open-core) của **BSD Insight**, xây trên **Odoo 19 Community** + app HDV **React Native (Expo)**. Đây là repo **PUBLIC** (community). Module enterprise nằm ở repo riêng **`touriha-enterprise`** (private, cạnh repo này: `../touriha-enterprise`).

## Mô hình kinh doanh (open-core 3 tầng)
- **Community** (repo này, LGPL-3, self-host): đầy đủ nghiệp vụ cơ bản, KHÔNG giới hạn.
- **Enterprise** (repo `touriha-enterprise`, OPL-1): tính năng cao cấp (recommendation engine, dashboard BI, payment, automation ngoại lệ...).
- **Touriha Cloud** (SaaS BSD host): nơi đặt giới hạn số lượng (Free 100 tours/50 pax → gói trả phí). Liên hệ: daibt@bsdinsight.com / 0918 339 689 (Đại).

## Kiến trúc module (community)
- `touriha_base` — menu gốc + nền tảng chung.
- `touriha_operations` — Tour + passenger grid (ĐÃ CÓ).
- `touriha_crm` — lead → báo giá → tour (kế tiếp).
- `touriha_costing` — costing 3 giai đoạn + tạo PO (kế tiếp).
- `touriha_portal` — supplier/B2B portal cơ bản (kế tiếp).

MVP: operator ERP core = CRM → Operations/Auto-Quantity → Costing 3 giai đoạn → PO. Khách hàng đầu tiên: **Lửa Việt**.

## ⚠️ Quy ước Odoo 19 — BẮT BUỘC
Các tài liệu BRD gốc (`~/Downloads/touriha/*.md` và `../touriha-enterprise/docs/brd/`) GIÀU ý tưởng nhưng CODE viết theo cú pháp Odoo ≤16 — **KHÔNG copy nguyên**. Khác biệt phải tuân thủ:
- View: KHÔNG dùng `attrs=` / `states=` (bỏ từ Odoo 17) → dùng `invisible="..."`, `required="..."`, `readonly="..."` trực tiếp.
- `<tree>` → `<list>`.
- Chatter trong form: `<chatter/>`.
- `res.groups`: KHÔNG dùng `category_id` (bỏ ở 19). Theo quy ước frm-pro: dùng `base.group_user` trong `ir.model.access.csv`, chưa tự định nghĩa group cho tới khi cần (lúc đó dùng `privilege_id`).
- `_sql_constraints` → `models.Constraint`.
- `product`: bỏ `uom_po_id`.
- KHÔNG có API `self.env.user.notify_info/notify_warning/notify_success` hay `message_post_with_template` — dùng `display_notification` action / `template.send_mail`.
- Controller: `type='jsonrpc'` (KHÔNG phải `type='json'`).
- Push mobile: FCM HTTP v1 + OAuth2 (FCM legacy bị Google tắt 2024).

Tham khảo phong cách: bộ module `frm_*` tại `/Users/bsd/frm-pro-odoo/addons` (cùng tác giả, cùng Odoo 19).

## Chạy local (Docker)
```bash
cp config/odoo.conf.example config/odoo.conf   # chỉnh admin_passwd
docker compose up -d
# Odoo: http://localhost:8569  (8569 để không đụng frm-pro ở 8069)
```
Cài/cập nhật một module:
```bash
docker compose run --rm touriha_odoo odoo -d touriha -i touriha_operations --stop-after-init
```

## Domain (DỄ NHẦM — kiểm tra kỹ)
- `touriha.com` — sản phẩm/landing (Cloudflare).
- `doc.bsdinsight.com` / `bsdinsight.com` — docs + site công ty (KHÔNG 's').
- `touriha.bsdinsights.com` — demo qua Cloudflare tunnel (zone `bsdinsights.com` CÓ 's', khác `bsdinsight.com` của site công ty).
