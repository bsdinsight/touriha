# Cloudflare Tunnel — demo Touriha

Đưa Odoo local (`localhost:8169`) ra `https://turiha.bsdinsights.com` mà không mở port.

> ⚠️ Hostname: bạn ghi **`turiha.bsdinsights.com`** — có **'s'** trong *bsdinsight**s***, và **turiha** (thiếu *o*) khác với sản phẩm *touriha.com*. Xác nhận đúng chính tả trước khi route DNS.

## Một lần
```bash
brew install cloudflared
cloudflared tunnel login                 # chọn zone bsdinsights.com
cloudflared tunnel create touriha-demo   # tạo UUID + file credentials .json
cloudflared tunnel route dns touriha-demo turiha.bsdinsights.com
```

## Cấu hình
```bash
cp cloudflare/config.example.yml ~/.cloudflared/config.yml
# điền <TUNNEL_UUID> + đường dẫn credentials .json
```
Trong `config/odoo.conf` đã bật `proxy_mode = True` (bắt buộc khi chạy sau tunnel).

## Chạy
```bash
docker compose up -d            # Odoo ở 8169
cloudflared tunnel run touriha-demo
```
Tùy chọn chạy nền: `cloudflared service install` (macOS launchd).

File `*.json` (credentials) đã được .gitignore — KHÔNG commit.
