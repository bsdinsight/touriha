# Touriha Mobile (HDV) — Đặc tả chức năng

> App di động cho **Hướng dẫn viên / Trưởng đoàn** — người dẫn đoàn ngoài hiện trường.
> Dùng để (1) thiết kế UI mobile bằng Claude Design, (2) làm cơ sở code React Native (Expo), **offline-first**.
> Trạng thái: bản nháp v0.1 — 2026-06-09.

---

## 0. Định vị & persona
**Touriha App** là "trợ lý hiện trường" của HDV: nhận phân công → dẫn đoàn theo lịch trình → điểm danh khách → quản phòng/ăn/vé/xe → ghi chi phí tạm ứng → xử lý sự cố → báo cáo & đánh giá. Là **cánh tay nối dài của ERP Touriha** ra hiện trường.

**Persona — HDV:** luôn tay luôn chân, ngoài trời, **thường mất sóng**, cần thao tác nhanh (điểm danh, gọi điện, ghi chi phí), nút to, đọc được dưới nắng.

## 1. Nguyên tắc thiết kế cốt lõi
- **Offline-first:** tải trọn gói tour trước khi đi; mọi thứ xem được offline; mọi thao tác (điểm danh, chi phí, ảnh, báo cáo) ghi offline → **tự đồng bộ** khi có mạng.
- **Today/Now-focused:** mở app thấy ngay tour đang chạy + việc cần làm bây giờ.
- **Tối giản thao tác:** hành động quan trọng ≤ 2 chạm (điểm danh, gọi office, ghi chi phí, SOS).
- **Field-optimized:** nút lớn, tương phản cao (đọc dưới nắng), ít chữ nhiều icon, tiết kiệm pin/data.

## 2. Cấu trúc điều hướng (IA)
**Bottom tab:**
- 🏠 **Trang chủ** — tour hôm nay/đang chạy, cảnh báo, việc cần làm, quick actions
- 🧳 **Chuyến đi** — danh sách tour (sắp tới/đang chạy/đã xong) → chi tiết
- 👥 **Đoàn** — đoàn khách của tour đang chạy (điểm danh, phòng, liên hệ)
- 💰 **Chi phí** — tạm ứng, ghi chi phí, quyết toán
- ⋯ **Thêm** — hồ sơ, tài liệu, báo cáo, công cụ, cài đặt

**"Active Tour Hub"** (khi đang dẫn tour): màn trung tâm gom nhanh — Lịch trình · Điểm danh · Voucher · Chi phí · Liên lạc · Sự cố · Báo cáo. **Nút SOS** + **FAB quick action** (ghi chi phí/điểm danh) hiện xuyên suốt.

---

## 3. Chức năng chi tiết

### 1) Tài khoản & hồ sơ HDV
- Đăng nhập SĐT/email + **OTP**, **đăng nhập sinh trắc** (vân tay/Face ID), nhớ phiên.
- Hồ sơ: ảnh, **thẻ HDV/chứng chỉ**, ngôn ngữ, chuyên môn (inbound/outbound/loại tour), khu vực.
- **Lịch rảnh/bận** (set ngày nhận tour) → office phân công.
- Cài đặt thông báo, đa ngôn ngữ VI/EN, chỉ báo **trạng thái mạng/đồng bộ**.

### 2) Phân công & Dashboard
- **Trang chủ:** tour hôm nay/đang chạy, đếm ngược khởi hành, cảnh báo, **việc cần làm (task)**, quick actions.
- **Danh sách tour:** sắp tới / đang chạy / đã hoàn tất; lịch (calendar) phân công.
- **Nhận/Từ chối phân công** (kèm lý do).
- **Chi tiết tour:** mã, tên, ngày, loại, số pax, tuyến/điểm đến, **điểm hẹn + giờ tập trung**, brief từ office.

### 3) Lịch trình (Itinerary)
- **Timeline theo ngày** (mỗi ngày: chuỗi hoạt động + giờ + địa điểm).
- Chi tiết hoạt động: giờ, nơi, mô tả, ghi chú, **bản đồ/chỉ đường**.
- **Map view** toàn tuyến + điểm dừng; **bản đồ offline**.
- **"Đang ở bước nào"** — hiện hoạt động hiện tại & kế tiếp.
- HDV **thêm ghi chú** riêng; office **đổi lịch → đẩy thông báo**.

### 4) Đoàn khách (Passengers)
- **Danh sách khách:** tên, ảnh, loại (NL/trẻ em/em bé), SĐT, hộ chiếu, nhu cầu đặc biệt, **nhóm phòng/gia đình**.
- **ĐIỂM DANH / Headcount** tại mỗi điểm (chạm để đánh dấu có mặt) — chống sót khách; **tổng kết X/Y** mỗi checkpoint; bộ **đếm nhanh (tap counter)**.
- **Chi tiết khách:** liên hệ + **liên hệ khẩn cấp**, hộ chiếu/visa, **ghi chú y tế/ăn kiêng**, phòng được xếp.
- Gom theo nhóm phòng/gia đình; **chạm để gọi/nhắn** khách; cảnh báo **sinh nhật/dịp đặc biệt** trong tour.
- **Giấy tờ khách** (ảnh hộ chiếu/visa) xem offline; đánh dấu vắng/no-show.

### 5) Phòng & Khách sạn (Rooming)
- **Danh sách phòng** (ai ở phòng nào); **công cụ xếp phòng** (kéo khách vào phòng).
- Mỗi đêm: tên KS, địa chỉ, giờ nhận/trả phòng, **liên hệ**, mã xác nhận/voucher, **chỉ đường**.
- Theo dõi **check-in/out**; **voucher KS** xem offline.

### 6) Ăn uống (Meals)
- **Lịch bữa ăn** (bữa nào, ở đâu, khi nào).
- Nhà hàng: tên, địa chỉ, liên hệ, mã đặt, **số suất gửi nhà hàng** (NL/trẻ em), **danh sách ăn kiêng/chay/dị ứng**, menu/set, voucher.

### 7) Vận chuyển & Tài xế (Transport)
- Thông tin xe: loại, **biển số**, **tài xế + SĐT**, sức chứa; **chạm gọi tài xế**.
- Điểm & giờ đón; **sơ đồ ghế** (tùy chọn); chia sẻ/theo dõi vị trí xe.

### 8) Vé & Điểm tham quan (Tickets)
- Lịch điểm tham quan: tên, giờ vào, loại vé, **số lượng vé** (NL/trẻ em).
- **E-voucher/vé offline** (QR/barcode); giờ mở cửa, liên hệ, ghi chú.

### 9) Voucher & Tài liệu (Documents) — offline
- **Tất cả voucher** một chỗ (KS/nhà hàng/xe/vé); chương trình tour (PDF), danh sách đoàn.
- Giấy tờ HDV (thẻ/hợp đồng); **SOP/quy trình khẩn cấp** của công ty; **bảo hiểm** (số hợp đồng + hotline).
- Lưu trữ tài liệu **offline**.

### 10) Tạm ứng & Chi phí (Expenses) — rất quan trọng
- **Tạm ứng nhận** từ office; **số dư còn lại** (tạm ứng − đã chi) cập nhật realtime.
- **Ghi chi phí trên đường:** hạng mục (ăn/vé/tip/xăng/phát sinh/khẩn cấp), số tiền, **chụp hóa đơn** (offline), NCC.
- **Đa tiền tệ** (tour outbound); phân bổ chi phí theo dịch vụ/khách.
- **Quyết toán cuối tour** (settlement) → gửi office.

### 11) Liên lạc (Communication)
- **Chat với office** (realtime + hàng đợi offline); **broadcast tới đoàn** ("7h tập trung sảnh").
- Gọi **hotline office/khẩn cấp**, tài xế, NCC (chạm gọi); **push notification** từ office (đổi lịch/khẩn).

### 12) Sự cố & Khẩn cấp (Incident & SOS)
- **Báo sự cố** (loại, mô tả, ảnh, vị trí, giờ) → office; **nút SOS** (gọi hotline + chia sẻ vị trí).
- **Danh bạ khẩn cấp** (office, bảo hiểm, công an, bệnh viện, đại sứ quán cho outbound).
- Quy trình **khách lạc**; thông tin **y tế khách**; **nhật ký sự cố**.

### 13) Báo cáo & Checklist
- **Checklist trước khởi hành** (giấy tờ, đủ khách, vật phẩm); **checklist/báo cáo cuối ngày**.
- **Báo cáo cuối tour** (tóm tắt, vấn đề, chi phí, phản hồi); **nhật ký ảnh/album tour** (upload).
- **Task** office giao; gửi báo cáo (hàng đợi offline).

### 14) Đánh giá & Phản hồi (Reviews)
- **Thu phản hồi khách** cuối tour (khảo sát/rating trong app).
- **HDV chấm điểm NCC** (KS/nhà hàng/xe) sau dịch vụ → **chảy vào review Marketplace**.
- HDV được office & khách đánh giá; form phản hồi tùy biến.

### 15) Công cụ HDV (Guide Tools)
- **Thuyết minh/talking points** theo điểm; **POI offline**; thời tiết theo điểm đến.
- **Đổi tiền tệ** + **múi giờ** (outbound); câu giao tiếp/dịch nhanh; **tip/chia bill**; bộ **đếm khách nhanh**.

### 16) Thu nhập & Lịch làm việc
- Lịch sử tour đã dẫn; **thù lao/phí mỗi tour** + tip + quyết toán; **trạng thái thanh toán** từ office.
- Lịch/khả dụng; thống kê hiệu suất (số tour, rating, giờ).

### 17) Offline & Đồng bộ (cốt lõi)
- **Tải trọn gói tour** trước khởi hành (pre-cache: lịch trình, khách, voucher, tài liệu, bản đồ).
- **Ghi offline** mọi thao tác → **tự đồng bộ** khi có mạng (hàng đợi + xử lý xung đột).
- Chỉ báo **trạng thái đồng bộ**, đồng bộ thủ công, quản lý dung lượng/low-data.

### 18) Cross-cutting
- Đa ngôn ngữ VI/EN; **dark/outdoor mode** (tương phản cao); bảo mật sinh trắc; push notification; tiết kiệm pin/data; accessibility; cài đặt app.

---

## 4. Ưu tiên (để Claude Design dồn sức đúng chỗ)
- 🟢 **MVP (Phase 1):** Đăng nhập/OTP · Trang chủ (today + quick actions) · Chi tiết tour · **Lịch trình** · **Đoàn khách + Điểm danh** · **Voucher/Tài liệu offline** · **Tạm ứng & Chi phí** · Chat office + **SOS**. (Tất cả **offline-first**.)
- 🟡 **Phase 2:** Xếp phòng · Ăn/Vé/Xe chi tiết · Báo cáo & checklist · Đánh giá NCC (→ Marketplace) · Sự cố đầy đủ.
- 🔵 **Phase 3:** Công cụ HDV (thuyết minh/POI/thời tiết) · Thu nhập & lịch · Phản hồi khách · Album tour · thống kê.

## 5. Design language (mobile)
- **Cảm hứng:** brand Touriha (xanh ngọc/biển + cát ấm/coral) áp cho mobile; gọn như Google Trips × app field-ops.
- **Bố cục:** bottom tab + **Active Tour Hub**; **FAB quick action**; **nút SOS** đỏ nổi bật.
- **Field-first:** nút to, tương phản cao đọc dưới nắng, ít chữ nhiều icon, **timeline cho lịch trình**, card cho khách/voucher.
- **Trạng thái rõ:** badge online/offline + đồng bộ; số liệu điểm danh nổi bật (X/Y).
- **Thao tác nhanh:** điểm danh 1 chạm, chạm-gọi, ghi chi phí + chụp hóa đơn nhanh.

## 6. Màn cần design trước (đưa Claude Design lần lượt)
1. Đăng nhập + OTP
2. Trang chủ (tour hôm nay + quick actions + cảnh báo)
3. Chi tiết tour + Active Tour Hub
4. Lịch trình (timeline theo ngày + map)
5. Đoàn khách + **Điểm danh/headcount**
6. Voucher & tài liệu (offline viewer)
7. Tạm ứng & Chi phí (số dư + ghi chi phí + chụp hóa đơn)
8. Chat office + **SOS/Sự cố**
→ rồi 9. Xếp phòng · 10. Báo cáo cuối tour + đánh giá NCC · 11. Hồ sơ HDV.

## 7. Prompt mẫu cho Claude Design
```
Design a mobile app (iOS/Android, React Native style) called "Touriha" for tour guides
leading travel groups in the field — OFFLINE-FIRST, field-optimized (large tap targets,
high-contrast for sunlight, minimal taps). Brand: teal/ocean + warm sand-coral accents,
clean and modern. Bottom tab nav: Home, Tours, Group, Expenses, More — plus a floating
SOS button and a quick-action FAB. Bilingual VI/EN. Design these screens:
(1) Login with phone + OTP.
(2) Home dashboard: today's/active tour card, countdown, alerts, to-do tasks,
    quick actions (headcount, call office, log expense, SOS), online/sync status badge.
(3) Tour detail + "Active Tour Hub" gathering Itinerary, Headcount, Vouchers, Expenses,
    Communication, Incident, Report.
(4) Itinerary day-by-day timeline with current-step highlight and a map view.
(5) Passenger list with one-tap headcount/check-in, X/Y present counter, tap-to-call,
    grouped by rooming/family; passenger detail with emergency contact + medical/dietary notes.
(6) Vouchers & documents offline viewer (hotel/restaurant/transport/tickets, QR e-vouchers).
(7) Expenses: advance balance, log expense with category + receipt photo, settlement.
(8) Office chat + a prominent red SOS / incident-report screen with emergency contacts.
Emphasize offline indicators and big, glanceable numbers. Premium but practical.
```

---

## 8. Map sang ERP Odoo (data flow)
- **Tour / phân công:** `touriha.tour` + field `guide_id` (hr.employee). ERP → app: tour, lịch trình, khách, phòng, voucher, tạm ứng, danh bạ NCC, tài liệu.
- **Lịch trình:** model `touriha.tour.itinerary` (ngày/hoạt động) — cần bổ sung.
- **Khách:** `touriha.passenger`; điểm danh = field/model `touriha.passenger.checkin` (point, time, present).
- **Voucher:** sinh từ costing line / `purchase.order` đã confirm.
- **Chi phí/tạm ứng:** model mới `touriha.tour.advance` + `touriha.tour.expense` (hạng mục, ảnh hóa đơn, NCC, tiền tệ); quyết toán → office.
- **Sự cố:** model mới `touriha.tour.incident`.
- **Đánh giá NCC:** `touriha.supplier.review` (chung với Marketplace).
- **App ↔ ERP:** REST API + **endpoint token đăng nhập riêng cho mobile** (xem ghi chú `res.users.authenticate` Odoo 19); app dùng **local DB (SQLite/WatermelonDB)** + sync queue cho offline-first.
