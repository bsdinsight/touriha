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

## 2. Cloudflare Tunnel — tunnel RIÊNG cho touriha (local-managed)
> ⚠️ Mỗi app 1 tunnel riêng. ĐỪNG ké tunnel app khác (vd "Agrione VPS"): connector của nó nằm ở
> docker-network khác → `odoo:8069` trỏ sang odoo app đó (không có DB touriha) → "database selector".

Trên máy đã `cloudflared tunnel login` (có `~/.cloudflared/cert.pem`):
```bash
cloudflared tunnel create touriha-vps
cloudflared tunnel route dns --overwrite-dns touriha-vps touriha.bsdinsights.com   # repoint DNS
scp ~/.cloudflared/<UUID>.json root@<VPS_HOST>:/root/touriha/cloudflare/tunnel-creds.json
ssh root@<VPS_HOST> 'chmod 644 /root/touriha/cloudflare/tunnel-creds.json'   # cloudflared non-root phải đọc được
```
Tạo `/root/touriha/cloudflare/config.yml`:
```yaml
tunnel: <UUID>
credentials-file: /etc/cloudflared/tunnel-creds.json
ingress:
  - hostname: touriha.bsdinsights.com
    service: http://odoo:8069
  - service: http_status:404
```
(`dbfilter=^touriha$` trong `deploy/odoo.conf` để Host mà cloudflared gửi không làm sai `%d`.) Bật connector ở §3 (`--profile tunnel up -d cloudflared`).

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
# (a) BẮT BUỘC: ./data là bind-mount thuộc root, odoo image chạy uid 100 →
#     fix quyền filestore TRƯỚC khi cài, nếu không sẽ "PermissionError /var/lib/odoo/filestore".
docker compose -f docker-compose.vps.yml run --rm -T --user root odoo chown -R odoo:odoo /var/lib/odoo </dev/null

# (b) Tạo DB rỗng (tên chữ thường → không cần dấu nháy)
docker compose -f docker-compose.vps.yml exec -T db psql -U odoo -d postgres -c "CREATE DATABASE touriha OWNER odoo;" </dev/null

# (c) Cài module — DÙNG `run --rm` (KHÔNG `exec`): exec bỏ qua entrypoint nên thiếu db_password
#     (lỗi "fe_sendauth: no password supplied"). Cài ~vài phút.
docker compose -f docker-compose.vps.yml run --rm -T odoo odoo -d touriha \
  -i touriha_crm,touriha_costing --without-demo=True --stop-after-init --no-http </dev/null

# (d) Đóng băng URL + restart
docker compose -f docker-compose.vps.yml exec -T db psql -U odoo -d touriha \
  -c "UPDATE ir_config_parameter SET value='https://touriha.bsdinsights.com' WHERE key='web.base.url';" </dev/null
docker compose -f docker-compose.vps.yml restart odoo
```
> Bỏ `--without-demo=True` nếu muốn DB có sẵn dữ liệu mẫu. Cài lâu + qua SSH thì nên chạy
> detached (`setsid bash -c '... > install.log 2>&1' &`) để sống sót nếu SSH rớt.

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
- **`PermissionError: /var/lib/odoo/filestore`** (cả khi cài mới lẫn sau restore) → `./data` bind-mount thuộc root, odoo chạy **uid 100**. Fix: `docker compose -f docker-compose.vps.yml run --rm -T --user root odoo chown -R odoo:odoo /var/lib/odoo`.
- **`fe_sendauth: no password supplied`** khi cài → đừng dùng `exec`; dùng `docker compose run --rm` (đi qua entrypoint để dịch env `PASSWORD`→`db_password`).
- **Cài vỡ ở `base/.../res_lang_data.xml`** lạ lùng → thường KHÔNG phải code: tag rolling `odoo:19` từng kéo nightly regression. Đã pin `odoo:19.0`; trên VPS đảm bảo `odoo:19.0` là build đã verify.
- **OOM** → giảm `workers = 1` trong `deploy/odoo.conf`.

## Bảo mật
- `.env` trong `.gitignore` — không commit. Đổi `admin_passwd` (master) + password admin từng DB sang chuỗi mạnh.
- Firewall chỉ mở SSH; Cloudflare tunnel outbound, không cần mở cổng vào.
