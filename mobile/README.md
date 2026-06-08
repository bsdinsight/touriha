# Touriha App (HDV)

App cho **Hướng dẫn viên** on-tour — **React Native (Expo)**, offline-first.

## Tính năng dự kiến (MVP HDV)
- Đăng nhập + đồng bộ tour được phân công.
- Passenger manifest + rooming list (xem offline).
- Nhập chi phí thực tế (actual cost) + chụp hóa đơn.
- Nút **SOS** (gửi GPS + cảnh báo khẩn về ERP).
- Nhắc bài hàng ngày (push notification).

## Kết nối backend
- Gọi API Odoo qua controller `type='jsonrpc'` (Odoo 19) + auth portal/JWT.
- Push: **FCM HTTP v1 + OAuth2** — KHÔNG dùng FCM legacy (`fcm.googleapis.com/fcm/send` đã bị Google tắt 2024).

## Trạng thái
⏳ Chưa scaffold. Sẽ khởi tạo bằng `create-expo-app` ở vòng làm mobile.
MVP hiện ưu tiên **backend operator ERP** (CRM→Costing→PO) cho Lửa Việt trước.
