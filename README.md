# Envoy Gateway — Redis Logger Sidecar

Envoy Gateway with Lua-based request/response logging to Redis via a Python sidecar or Vector.

## Quick Start

```bash
git clone <repo-url>
cd <repo-name>

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f envoy

# Stop
docker compose down
```

## Routes

| URI | Upstream |
|-----|----------|
| `/mcp*` | `UPSTREAM_HOST:8000` |
| `/mcp-xdr*` | `UPSTREAM_HOST:8000` |
| `/test-api*` | `UPSTREAM_HOST:8000` |
| `/api*` | `UPSTREAM_HOST:8080` |
| `/sce*` | `UPSTREAM_HOST:8080` |
| `/scr*` | `UPSTREAM_HOST:8080` |

## Ports

| Port | Purpose |
|------|---------|
| `443` | HTTPS proxy |
| `9901` | Admin endpoint |
| `9001` | redis-logger sidecar |

## Logging to Redis

1. **Envoy** collects request/response body via Lua filter, writes JSON access_log to `/var/log/envoy_access.log`
2. **redis-logger** (Python/aiohttp) receives POST `/log` and writes to Redis `RPUSH log_proxy`

Log fields: `request_id`, `server_port`, `request_uri`, `request_method`, `http_version`, `remote_addr`, `remote_user`, `time_local`, `duration`, `status`, `body_bytes_sent`, `http_referer`, `http_x_forwarded_for`, `http_x_real_ip`, `http_host`, `http_user_agent`, `http_authorization`, `http_accept_language`, `http_accept_encoding`, `http_connection`, `http_cookie`, `request_body`, `response_body`.

## Structure

```
├── envoy/envoy.yaml        # Envoy configuration
├── redis-logger/           # Redis logging sidecar
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
├── docker-compose.yml
└── README.md
```
