# Touriha — Kiến trúc & Lộ trình

## Mô hình open-core (3 tầng)
- **Community** (repo `touriha`, LGPL-3): nghiệp vụ cơ bản, self-host, không giới hạn.
- **Enterprise** (repo `touriha-enterprise`, private, OPL-1): tính năng cao cấp.
- **Touriha Cloud** (SaaS): nơi enforce giới hạn số lượng (Free 100 tours/50 pax).

Lý do: cap chỉ enforce được khi BSD kiểm soát hạ tầng → đặt ở tầng Cloud, KHÔNG nhồi vào mã nguồn mở (vừa vô nghĩa vì xoá được, vừa mất thiện cảm cộng đồng).

## Bản đồ module

### Community (repo này)
| Module | Vai trò | Trạng thái |
|---|---|---|
| `touriha_base` | Menu gốc, nền tảng chung | ✅ |
| `touriha_operations` | Tour + passenger grid, vòng đời tour | ✅ (cơ bản) |
| `touriha_crm` | Lead → báo giá → tạo tour (mở rộng crm/sale) | ⏳ |
| `touriha_costing` | Costing 3 giai đoạn (estimate/finalized/actual) + tạo PO | ⏳ |
| `touriha_portal` | Cổng Supplier & B2B cơ bản | ⏳ |
| `touriha_cancellation` | Hủy tour & hoàn tiền cơ bản | ⏳ |

### Enterprise (repo `touriha-enterprise`)
| Module | Vai trò |
|---|---|
| `touriha_knowledge` | Recommendation engine (rule-based + tag, KHÔNG Neo4j) |
| `touriha_dashboard` | Executive / Operation / Sales dashboards |
| `touriha_payment` | VNPay / Momo / Stripe / PayPal + đối soát |
| `touriha_exception_pro` | Tự động xử lý ngoại lệ + escalation |
| `touriha_license` | Enforce giới hạn số lượng (cloud-only) |

## MVP (ưu tiên cho Lửa Việt)
Operator ERP core: **CRM → Passenger Grid → Operations/Auto-Quantity (cơ bản) → Costing 3 giai đoạn (đơn giản) → PO → Supplier portal cơ bản**.
Bắt buộc có sớm: phân quyền + hủy/hoàn tiền cơ bản.
Để sau (V2+): knowledge graph (tag trước), payment phức tạp, dashboard nâng cao, mobile nâng cao.

## Vòng đời (state machines)
- **Tour:** `draft → confirmed → in_progress → completed` (| `cancelled`).
- **Costing line:** `estimate → finalized → actual`.
- **PO (supplier):** `draft → sent → confirmed/rejected → done/cancelled`.

Sơ đồ chi tiết: BRD gốc — `../touriha-enterprise/docs/brd/Sơ đồ luồng và Bảng trạng thái.md`.

## ⚠️ Lưu ý kỹ thuật
BRD gốc viết code theo Odoo ≤16 — phải viết lại cho Odoo 19. Xem `CLAUDE.md` mục "Quy ước Odoo 19".
