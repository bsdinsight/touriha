# Touriha Marketplace — Đặc tả chức năng

> Sàn B2B kết nối **công ty lữ hành (bên mua)** ⇄ **nhà cung cấp dịch vụ du lịch (bên bán)**.
> Tài liệu này dùng để (1) thiết kế UI bằng Claude Design và (2) làm cơ sở code (Odoo 19 + React).
> Trạng thái: bản nháp v0.1 — 2026-06-09.

---

## 0. Định vị một dòng
Khám phá → hỏi giá (RFQ) → so sánh → chọn → giao dịch (PO) → đánh giá; tích hợp ngược vào **ERP Touriha** của công ty lữ hành. Marketplace nằm trên **một "Touriha Hub" trung tâm** (1 Odoo + Website công khai tại touriha.com); mỗi lữ hành vẫn dùng ERP riêng và tìm/import/recommend NCC từ Hub.

## 1. Personas (4 "mặt")
| Persona | Vai trò |
|---|---|
| **Khách vãng lai** (chưa đăng nhập) | Duyệt, tìm, xem hồ sơ NCC — kênh SEO |
| **Nhà cung cấp / Supplier** | Đăng ký, dựng hồ sơ, báo giá, nhận lead, mua gói |
| **Công ty lữ hành / Operator (buyer)** | Tìm, RFQ, so sánh, import vào ERP, chấm điểm |
| **Touriha Admin** | Kiểm duyệt, monetization, vận hành, phân tích |

## 2. Phân loại NCC (taxonomy — dùng cho category tiles + filter)
- **Lưu trú:** khách sạn, resort, homestay, villa, tàu ngủ đêm
- **Vận chuyển:** xe 16–45 chỗ, limousine, cano/tàu, vé máy bay (đại lý), tàu hỏa
- **Ẩm thực:** nhà hàng, set menu, tiệc, catering
- **Hướng dẫn viên:** nội địa, quốc tế (theo ngôn ngữ), trưởng đoàn
- **Vé & điểm tham quan:** vé cổng, show diễn, bảo tàng, công viên
- **Trải nghiệm:** cooking class, trekking, lặn biển, team-building
- **DMC / land operator:** inbound–outbound theo điểm đến
- **Hỗ trợ:** bảo hiểm du lịch, visa, sim/wifi, nhiếp ảnh, MICE/sự kiện, cho thuê thiết bị, đặc sản/mua sắm

---

## 3. Chức năng chi tiết theo khu vực

### A. Public / Discovery (touriha.com)
- **Trang chủ:** hero + thanh tìm kiếm thông minh (dịch vụ + điểm đến + từ khóa), category tiles, NCC **nổi bật/được tài trợ**, **top-rated**, **mới tham gia/đã xác thực**, đếm số NCC–lữ hành (social proof), "Cách hoạt động" (2 luồng: cho lữ hành / cho NCC).
- **Tìm kiếm & kết quả:** bộ lọc (loại dịch vụ, khu vực/điểm đến, khoảng giá, rating, **đã xác thực**, ngôn ngữ, sức chứa/đội xe, tiện ích, còn trống); sắp xếp (liên quan/rating/giá/mới/khoảng cách); **list view ⇄ map view**; lưu bộ lọc + tạo cảnh báo.
- **Hồ sơ NCC** (màn "lung linh" nhất): cover + gallery ảnh/video; logo, tên, **badge xác thực**, sao + số review; tag dịch vụ; bản đồ vị trí; giới thiệu; **danh mục dịch vụ/sản phẩm + giá** (hoặc "Yêu cầu báo giá"); thông số riêng theo ngành (KS: hạng sao/số phòng/tiện ích; xe: đội xe/số ghế; HDV: ngôn ngữ/chứng chỉ); chứng chỉ–giấy phép–giải thưởng; **review + phân rã điểm**; tỉ lệ/tốc độ phản hồi, số năm, số deal hoàn tất; nút **Yêu cầu báo giá / Lưu / Nhắn tin / Thêm vào shortlist**; NCC tương tự.
- **Landing SEO:** theo điểm đến ("NCC tại Đà Nẵng"), theo danh mục ("Xe 45 chỗ tốt nhất"), blog/cẩm nang.
- **Trang tĩnh:** About, How it works (2 bản), Pricing, FAQ, Trust & Safety, Liên hệ, Điều khoản.
- **Toàn cục:** đổi **ngôn ngữ VI/EN**, đổi tiền tệ, đăng nhập/đăng ký (chọn vai NCC / Lữ hành).

### B. Supplier (bên bán)
- **Onboarding wizard:** tạo tài khoản (email + **OTP SĐT/Zalo**) → chọn danh mục → **xác minh DN** (giấy phép/MST/CCCD → badge) → dựng hồ sơ (logo/cover/mô tả/vị trí) → thêm **dịch vụ + bảng giá** → upload ảnh/video → khu vực phục vụ → ngôn ngữ/sức chứa/chứng chỉ → thông tin thanh toán → **chọn gói**.
- **Dashboard NCC:** tổng quan (lượt xem hồ sơ, lead, RFQ, tỉ lệ chuyển đổi, rating, **thứ hạng tìm kiếm**); **thanh hoàn thiện hồ sơ** (gamification).
- **Lead/RFQ inbox:** yêu cầu đến từ lữ hành → **soạn báo giá** (line-item, hiệu lực, điều khoản, đính kèm); trạng thái (đã xem/chấp nhận/từ chối/hết hạn).
- **Bookings/PO:** PO nhận từ lữ hành → confirm/reject (kết nối `touriha_portal` đã có).
- **Lịch & tồn/giá:** quản lý còn trống, **giá theo mùa**, chặn ngày, tồn phòng/ghế.
- **Khuyến mãi:** tạo deal/ưu đãi để hút lữ hành.
- **Reviews:** xem + **phản hồi** đánh giá.
- **Analytics:** lượt xuất hiện tìm kiếm, CTR, xu hướng lead, **benchmark đối thủ**.
- **Gói & thanh toán:** gói hiện tại, hóa đơn, nâng cấp, **mua Featured/Boost**.
- **Hồ sơ & media library**, **tài khoản nhân sự** (nhiều user/NCC), cài đặt thông báo.

### C. Operator / Buyer (bên mua — công ty lữ hành)
- Đăng ký hoặc **SSO từ ERP Touriha**.
- **Dashboard:** shortlist/NCC đã lưu; **RFQ của tôi** (đã gửi/đã có báo giá); **so sánh báo giá** (cạnh nhau: giá/rating/điều khoản); NCC đã import vào ERP; **NCC được gợi ý** (theo điểm đến/theo tour); review chờ viết (sau tour); danh sách/favourite theo điểm đến–loại tour.
- **RFQ:** gửi 1 NCC; **đăng RFQ broadcast** ("cần xe 16 chỗ, Đà Nẵng, 3N2Đ, dd/mm" → nhiều NCC chào giá — **reverse marketplace**); **RFQ ngay trong itinerary** (tích hợp ERP).
- **So sánh & shortlist** → **Import NCC → res.partner** (1 chạm, đồng bộ ERP).
- **Gợi ý tại itinerary:** khi dựng tour trong ERP, Touriha đề xuất NCC theo từng dịch vụ/điểm đến.
- **Chấm điểm sau tour** (kích hoạt từ ERP khi tour hoàn tất).
- **Spend analytics:** mua của ai, bao nhiêu, hợp đồng/agreement.

### D. RFQ / Quote / Matching engine (trái tim B2B)
Đăng RFQ có cấu trúc (dịch vụ, điểm đến, ngày, số lượng/pax, yêu cầu, ngân sách) · **auto-match NCC phù hợp** · NCC nộp **báo giá có cấu trúc** · **so sánh báo giá** · luồng **thương lượng/nhắn tin theo RFQ** · **chốt → tạo booking/PO** · hết hạn + nhắc · template RFQ.

### E. Reviews & Trust
**Review đã xác minh** (chỉ lữ hành đã giao dịch mới được chấm) · điểm đa chiều (giá/chất lượng/giao tiếp/đúng hẹn/tin cậy) · NCC **phản hồi review** · **điểm tổng + phân rã** · badge (đã xác minh giấy phép/định danh/**Touriha Certified**) · số năm, tỉ lệ phản hồi, số deal · báo cáo/khiếu nại, xử lý tranh chấp · **Touriha Trust Score** tổng hợp.

### F. Recommendation / Discovery
Gợi ý cá nhân hóa cho lữ hành (theo tour/điểm đến/lịch sử) · "NCC tương tự" · trending theo điểm đến · **smart-match cho RFQ** · gợi ý **trong itinerary builder của ERP** · recently viewed, saved search + **alert NCC mới khớp**.

### G. Messaging / Collaboration
Chat trong sàn (lữ hành ⇄ NCC) · thread theo RFQ · đính kèm/chia sẻ báo giá · read receipt · thông báo **in-app/email/SMS/Zalo**.

### H. Monetization (doanh thu Touriha)
**Gói NCC** Free/Pro/Premium (số listing, analytics, ưu tiên hiển thị) · **Featured/Sponsored** (lên top tìm kiếm + vị trí trang chủ + ưu tiên recommend) · **pay-per-lead** · **hoa hồng** trên booking (nếu giao dịch qua sàn) · **badge xác thực trả phí** · slot quảng cáo · gói premium cho lữ hành · billing/hóa đơn/**cổng thanh toán VNPay–Momo–thẻ**.

### I. Admin (back-office Touriha)
Hàng đợi **duyệt NCC + soát giấy tờ** · kiểm duyệt nội dung/ảnh · quản lý **danh mục & điểm đến** · kiểm duyệt review/tranh chấp · quản lý slot Featured · quản lý gói/giá · **analytics nền tảng** (GMV, lead, conversion, NCC/lữ hành active, doanh thu, funnel) · CMS (blog/landing/banner) · user & phân quyền · cấu hình phí/hoa hồng · chống gian lận/spam · hỗ trợ/ticket · template thông báo · quản lý SEO.

### J. Cross-cutting
Auth (email/OTP/social/**SSO ERP**) · đa ngôn ngữ VI–EN · đa tiền tệ · notification center · search hạ tầng (full-text + filter + geo) · **responsive/PWA** · SEO (structured data, sitemap) · privacy/terms · analytics tracking.

### K. Tích hợp ERP Touriha
SSO Hub ⇄ ERP · **import NCC → res.partner** · đẩy review sau tour từ ERP → Hub · gợi ý NCC trong itinerary · đồng bộ trạng thái PO/booking (portal hiện có) · đồng bộ dữ liệu spend.

---

## 4. Ưu tiên (để Claude Design dồn sức đúng chỗ)
- 🟢 **MVP (Lớp 1 — thiết kế trước):** Trang chủ · Tìm kiếm/kết quả · **Hồ sơ NCC** · Onboarding NCC · Dashboard NCC (overview + sửa hồ sơ + lead) · Auth chọn vai.
- 🟡 **Phase 2:** RFQ + so sánh báo giá · Dashboard lữ hành (shortlist + gợi ý + import) · Chat.
- 🔵 **Phase 3:** Reviews/Trust đầy đủ · Monetization/billing · Admin · Analytics nâng cao · Lịch–tồn–giá.

## 5. Design language ("lung linh")
- **Cảm hứng:** Airbnb (card + trust + ảnh lớn) × GetYourGuide (trải nghiệm) × TBO/Alibaba (RFQ B2B).
- **Tông màu:** xanh ngọc/biển (tin cậy) + cát ấm/coral (điểm nhấn), nền trắng nhiều khoảng thở.
- **Yếu tố:** hero ảnh điểm đến VN tuyệt đẹp, **card bo góc + hover nâng nhẹ**, **badge xác thực**, sao rating, **map view**, glassmorphism nhẹ ở search bar, micro-interaction mượt, typography mạnh, iconography du lịch.
- **Nguyên tắc:** ảnh là chủ đạo (NCC sống nhờ hình ảnh) · trust hiện rõ (badge/review/số liệu) · mobile-first · VI/EN.

## 6. Danh sách màn nên thiết kế trước (đưa cho Claude Design lần lượt)
1. Homepage marketplace
2. Search results (list + map + filter)
3. Hồ sơ NCC
4. Onboarding NCC (wizard 5 bước)
5. Supplier dashboard
6. Auth (chọn vai)
→ rồi 7. RFQ + so sánh báo giá · 8. Operator dashboard.

## 7. Prompt mẫu cho Claude Design
```
Design a modern B2B tourism marketplace called Touriha connecting tour operators
with travel suppliers (hotels, coaches, restaurants, guides, tickets, DMCs).
Aesthetic: trustworthy and aspirational like Airbnb × GetYourGuide, large destination
photography, teal/ocean + warm sand-coral accents, rounded cards with soft hover,
verification badges, star ratings, map view, subtle glassmorphism on the search bar.
Bilingual VI/EN, mobile-first, responsive. Design these screens:
(1) Homepage with hero smart-search + category tiles + featured/top-rated suppliers + "how it works".
(2) Search results with left filter rail, supplier cards, list⇄map toggle.
(3) Supplier profile page with cover gallery, verified badge, ratings, services & pricing,
    specs, reviews, "Request quote/Save/Message".
(4) Supplier onboarding wizard (account→categories→verification→profile→services & pricing).
(5) Supplier dashboard (KPIs, profile-completeness, lead/RFQ inbox).
Clean, premium, lots of whitespace.
```

---

## 8. Map sang Odoo (ghi chú khi code)
- **NCC** = `res.partner` (supplier) + model mở rộng `touriha.supplier.profile` (danh mục, khu vực, mô tả, ngôn ngữ, chứng chỉ, published, rating tổng).
- **Dịch vụ/sản phẩm NCC** = `touriha.supplier.service` (giá/đơn vị/mô tả/ảnh).
- **Public front** = Odoo **Website** (directory + profile + form đăng ký) cho MVP; bản custom React "siêu lung linh" để V2.
- **RFQ** = `touriha.rfq` + `touriha.rfq.quote` (báo giá); chốt → tạo `purchase.order` (đã có `tour_id`).
- **Review** = `touriha.supplier.review` (đa chiều, gắn tour đã hoàn tất); rating tổng compute lên profile.
- **Monetization** = field gói/featured trên profile + tích hợp payment (VNPay/Momo).
