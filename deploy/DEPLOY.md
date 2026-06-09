# Touriha → VPS · Deploy Guide

Đưa Touriha lên VPS theo mô hình chuẩn: **1 stack compose độc lập + Cloudflare Tunnel riêng, KHÔNG mở host port** (cloudflared cùng network reach `odoo:8069`). 1 Postgres + 1 Odoo phục vụ nhiều DB, route bằng `dbfilter=^%d$` (sub-domain = tên DB) — sẵn sàng đa-tenant.

Hiện tại: 1 DB demo `touriha` ↔ `touriha.bsdinsights.com`.

## 0. Tiền điều kiện
- VPS Ubuntu + Docker + compose plugin.
- Cloudflare Zero Trust; zone `bsdinsights.com` đã trỏ NS Cloudflare.
- Không cần mở port vào (tunnel = outbound). Firewall chỉ mở SSH (22).

## 1. Clone + chuẩn bị
```bash
ssh root@<VPS_HOST>
cd /root && git clone https://github.com/bsdinsight/touriha && cd touriha
cp deploy/.env.example .env
nano .env                 # POSTGRES_PASSWORD (mạnh) + TUNNEL_TOKEN (xem §2)
nano deploy/odoo.conf     # đổi admin_passwd = <master mạnh>
```
> ⚠ Đặt `POSTGRES_PASSWORD` TRƯỚC lần `up -d db` đầu — Postgres chỉ áp khi init data dir rỗng.

## 2. Cloudflare Tunnel
Tái dùng tunnel touriha hiện có (đang chạy trên laptop) hoặc tạo mới:
1. Zero Trust → Networks → Tunnels → (tunnel touriha) → copy **token** → dán vào `.env` ở `TUNNEL_TOKEN=` (KHÔNG commit / paste chat).
2. Tab **Public Hostnames**: `touriha`.`bsdinsights.com` → Service **HTTP** `http://odoo:8069`, Path **để TRỐNG**.
3. **Tắt cloudflared trên laptop** để chỉ VPS phục vụ tunnel này (`pkill cloudflared` hoặc xoá route laptop).

## 3. Bật stack
```bash
cd /root/touriha
docker compose -f docker-compose.vps.yml up -d db
docker compose -f docker-compose.vps.yml logs -f db     # chờ "database system is ready"
docker compose -f docker-compose.vps.yml up -d odoo
docker compose -f docker-compose.vps.yml logs -f odoo   # chờ "HTTP service running"
docker compose -f docker-compose.vps.yml --profile tunnel up -d cloudflared
```
> `--profile tunnel` BẮT BUỘC để cloudflared join network `touriha_default`.

## 4. Tạo DB demo `touriha`
```bash
docker compose -f docker-compose.vps.yml exec -T db psql -U odoo -d postgres \
  -c 'CREATE DATABASE "touriha" OWNER odoo;'
docker compose -f docker-compose.vps.yml exec odoo odoo -d touriha \
  -i touriha_crm,touriha_costing --stop-after-init --no-http
# đóng băng URL:
docker compose -f docker-compose.vps.yml exec -T db psql -U odoo -d touriha \
  -c "UPDATE ir_config_parameter SET value='https://touriha.bsdinsights.com' WHERE key='web.base.url';"
docker compose -f docker-compose.vps.yml restart odoo
```
(Thêm `--without-demo=True` nếu muốn DB sạch không demo data.)

## 5. Smoke test
`https://touriha.bsdinsights.com` → trang **login** (KHÔNG phải selector) → đăng nhập admin → **đổi password ngay**.

## 6. Backup hằng ngày
```bash
crontab -e
# 0 3 * * *  /root/touriha/deploy/backup.sh > /var/log/touriha-backup.log 2>&1
```

## Cập nhật code sau khi push GitHub
```bash
cd /root/touriha && git pull
docker compose -f docker-compose.vps.yml exec -T odoo odoo -d touriha \
  -u touriha_crm,touriha_costing --stop-after-init --no-http
docker compose -f docker-compose.vps.yml restart odoo
```

## Thêm tenant mới (đa-khách-hàng, sau này)
1. `CREATE DATABASE "<khach>" OWNER odoo;`
2. `odoo -d <khach> -i touriha_crm,touriha_costing --stop-after-init --no-http`
3. Cloudflare → Public Hostnames → `<khach>.touriha.com → http://odoo:8069`.

## Gotchas
- **404 từ tunnel** → `dbfilter=^%d$` cần sub-domain TRÙNG tên DB (DB phải tên `touriha`).
- **`lookup odoo ... no such host`** → cloudflared chạy rời, thiếu `--profile tunnel`.
- **Postgres không nhận password** → `up -d db` khi `.env` chưa có pwd. Stop, `rm -rf postgres-data/`, set pwd, up lại.
- **Filestore PermissionError** sau restore → `docker compose -f docker-compose.vps.yml exec --user root odoo chown -R odoo:odoo /var/lib/odoo`.
- **OOM** → giảm `workers = 1` trong `deploy/odoo.conf`.

## Bảo mật
- `.env` trong `.gitignore` — không commit. Đổi `admin_passwd` (master) + password admin từng DB sang chuỗi mạnh.
- Firewall chỉ mở SSH; Cloudflare tunnel outbound, không cần mở cổng vào.
