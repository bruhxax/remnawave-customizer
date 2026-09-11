from __future__ import annotations

import datetime as dt
import hashlib
import os
import time
from dataclasses import dataclass
from pathlib import Path

from .config import BACKUP_DIR, RUNTIME_DIR, save_config
from .themes import render_css
from .utils import CommandError, must_run, run

CUSTOM_TARGET = 'remnawave-customizer-proxy:3100'
PANEL_TARGET = 'remnawave:3000'


@dataclass(frozen=True)
class ProxyInfo:
    kind: str
    name: str
    config_path: Path
    compose_dir: Path
    service: str


CANDIDATES: tuple[ProxyInfo, ...] = (
    ProxyInfo('nginx', 'Nginx', Path('/opt/remnawave/nginx/nginx.conf'), Path('/opt/remnawave/nginx'), 'remnawave-nginx'),
    ProxyInfo('caddy', 'Caddy', Path('/opt/remnawave/caddy/Caddyfile'), Path('/opt/remnawave/caddy'), 'caddy'),
    ProxyInfo('angie', 'Angie', Path('/opt/remnawave/angie/angie.conf'), Path('/opt/remnawave/angie'), 'remnawave-angie'),
    ProxyInfo('traefik', 'Traefik', Path('/opt/remnawave/traefik/config/remnawave.yml'), Path('/opt/remnawave/traefik'), 'traefik'),
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def panel_is_here() -> tuple[bool, str]:
    compose = Path('/opt/remnawave/docker-compose.yml')
    if not compose.exists():
        return False, '/opt/remnawave/docker-compose.yml not found'
    code, out, _ = run("docker inspect -f '{{.Name}}' remnawave", timeout=15)
    if code != 0 or out.strip().lstrip('/') != 'remnawave':
        return False, 'Remnawave Panel container not found'
    return True, ''


def detect_proxy() -> ProxyInfo | None:
    for item in CANDIDATES:
        if not item.config_path.exists():
            continue
        try:
            text = item.config_path.read_text(encoding='utf-8')
        except Exception:
            continue
        if CUSTOM_TARGET in text:
            return item
    for item in CANDIDATES:
        if not item.config_path.exists():
            continue
        try:
            text = item.config_path.read_text(encoding='utf-8')
        except Exception:
            continue
        if PANEL_TARGET in text:
            return item
    return None


def runtime_compose() -> str:
    return '''services:
  remnawave-customizer-proxy:
    image: nginx:alpine
    container_name: remnawave-customizer-proxy
    hostname: remnawave-customizer-proxy
    restart: always
    networks:
      - remnawave-network
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./theme.css:/usr/share/nginx/html/theme.css:ro
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "wget -q -O /dev/null http://127.0.0.1:3100/__remnawave_customizer/theme.css || exit 1"]
      interval: 20s
      timeout: 3s
      retries: 3
      start_period: 5s
networks:
  remnawave-network:
    name: remnawave-network
    external: true
'''


def runtime_nginx() -> str:
    # Important performance rule: JS/API/images keep their original compression.
    # Only HTML (for one <link> injection) and CSS (for known legacy design
    # tokens) are decoded. Nginx compresses transformed responses again.
    return r'''map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

map $http_x_real_ip $rwc_real_ip {
    default $http_x_real_ip;
    ''      $remote_addr;
}

map $http_x_forwarded_proto $rwc_forwarded_proto {
    default $http_x_forwarded_proto;
    ''      $scheme;
}

server {
    listen 3100;
    server_name _;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 5;
    gzip_types text/css application/json application/javascript image/svg+xml;

    location = /__remnawave_customizer/theme.css {
        alias /usr/share/nginx/html/theme.css;
        default_type text/css;
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0" always;
        add_header Pragma "no-cache" always;
        add_header X-Content-Type-Options "nosniff" always;
    }

    # API and sockets are a pure pass-through. No decompression, no filtering.
    location ^~ /api {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $remnawave_upstream http://remnawave:3000;
        proxy_http_version 1.1;
        proxy_pass $remnawave_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    location ^~ /socket.io/ {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $remnawave_upstream http://remnawave:3000;
        proxy_http_version 1.1;
        proxy_pass $remnawave_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Transform CSS only. This is intentionally limited to known Remnawave 3.x
    # legacy tokens so the browser still does the normal layout/painting work.
    location ~* \.css$ {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $remnawave_upstream http://remnawave:3000;
        proxy_http_version 1.1;
        proxy_pass $remnawave_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Accept-Encoding "";
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        sub_filter_types text/css;
        sub_filter_once off;

        # Legacy structural surfaces.
        sub_filter '#1b1f26' 'var(--rwc-surface)';
        sub_filter '#1B1F26' 'var(--rwc-surface)';
        sub_filter '#161b23' 'var(--rwc-surface-deep)';
        sub_filter '#161B23' 'var(--rwc-surface-deep)';

        # Stock cyan effects.
        sub_filter 'rgba(6,182,212,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(6, 182, 212,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(6,182,212,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(6, 182, 212,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(34,211,238,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(34, 211, 238,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(34,211,238,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(34, 211, 238,' 'rgba(var(--rwc-accent-rgb),';

        # Remnawave also mixes indigo/blue into the same decorative gradients.
        # Normalize those glows so a pink/green/etc theme never keeps blue fog.
        sub_filter 'rgba(99,102,241,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(99, 102, 241,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(99,102,241,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgb(99, 102, 241,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(59,130,246,' 'rgba(var(--rwc-accent-rgb),';
        sub_filter 'rgba(59, 130, 246,' 'rgba(var(--rwc-accent-rgb),';

        # Fixed cyan/teal hex accents used by scrollbars and decorative chrome.
        sub_filter '#06b6d4' 'var(--rwc-accent)';
        sub_filter '#06B6D4' 'var(--rwc-accent)';
        sub_filter '#22d3ee' 'var(--mantine-color-cyan-4)';
        sub_filter '#22D3EE' 'var(--mantine-color-cyan-4)';
        sub_filter '#0d9488' 'var(--mantine-color-cyan-8)';
        sub_filter '#0D9488' 'var(--mantine-color-cyan-8)';
        sub_filter '#14b8a6' 'var(--mantine-color-cyan-7)';
        sub_filter '#14B8A6' 'var(--mantine-color-cyan-7)';
    }

    # Heavy static files are untouched and keep upstream compression/caching.
    location ~* \.(?:js|mjs|map|json|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|wasm|lottie)$ {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $remnawave_upstream http://remnawave:3000;
        proxy_http_version 1.1;
        proxy_pass $remnawave_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # SPA routes return the small index HTML. Decode only that response, append
    # theme.css after official styles, then gzip it again for the client.
    location / {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $remnawave_upstream http://remnawave:3000;
        proxy_http_version 1.1;
        proxy_pass $remnawave_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Accept-Encoding "";
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        sub_filter_once on;
        sub_filter '</head>' '<link rel="stylesheet" href="/__remnawave_customizer/theme.css"></head>';
    }
}
'''


def write_runtime(theme: dict) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    (RUNTIME_DIR / 'docker-compose.yml').write_text(runtime_compose(), encoding='utf-8')
    (RUNTIME_DIR / 'nginx.conf').write_text(runtime_nginx(), encoding='utf-8')
    (RUNTIME_DIR / 'theme.css').write_text(render_css(theme), encoding='utf-8')
    os.chmod(RUNTIME_DIR / 'docker-compose.yml', 0o644)
    os.chmod(RUNTIME_DIR / 'nginx.conf', 0o644)
    os.chmod(RUNTIME_DIR / 'theme.css', 0o644)


def write_empty_theme() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    (RUNTIME_DIR / 'theme.css').write_text('/* Remnawave Customizer disabled: default Panel theme */\n', encoding='utf-8')


def _wait_injector_running(timeout: float = 35.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        code, out, _ = run("docker inspect -f '{{.State.Running}}' remnawave-customizer-proxy", timeout=10)
        if code == 0 and out.strip().lower() == 'true':
            return
        time.sleep(0.5)
    raise CommandError('Customizer proxy did not start')


def start_injector() -> None:
    code, _, _ = run('docker network inspect remnawave-network', timeout=15)
    if code != 0:
        raise CommandError('Docker network remnawave-network not found')

    must_run('docker compose up -d', timeout=240, cwd=RUNTIME_DIR)
    _wait_injector_running()

    # Bind-mounted config changes do not recreate the container. Validate and
    # reload explicitly so upgrades take effect immediately.
    must_run('docker exec remnawave-customizer-proxy nginx -t', timeout=30)
    must_run('docker exec remnawave-customizer-proxy nginx -s reload', timeout=30)

    deadline = time.monotonic() + 35
    last = 'starting'
    while time.monotonic() < deadline:
        code, out, _ = run(
            "docker inspect -f '{{.State.Running}} {{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' remnawave-customizer-proxy",
            timeout=10,
        )
        if code == 0:
            parts = out.strip().lower().split()
            running = bool(parts and parts[0] == 'true')
            health = parts[1] if len(parts) > 1 else 'none'
            last = health
            if running and health in {'healthy', 'none'}:
                return
        time.sleep(1)
    raise CommandError(f'Customizer proxy did not become healthy ({last})')


def injector_status() -> bool:
    code, out, _ = run("docker inspect -f '{{.State.Running}}' remnawave-customizer-proxy", timeout=15)
    return code == 0 and out.strip().lower() == 'true'


def stop_injector(remove: bool = False) -> None:
    if not RUNTIME_DIR.exists():
        return
    command = 'docker compose down' + (' --remove-orphans' if remove else '')
    run(command, timeout=120, cwd=RUNTIME_DIR)


def _backup_proxy(info: ProxyInfo, text: str) -> Path:
    stamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    folder = BACKUP_DIR / info.kind
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{stamp}-{info.config_path.name}.bak'
    path.write_text(text, encoding='utf-8')
    os.chmod(path, 0o600)
    return path


def _container_running(name: str) -> bool:
    code, out, _ = run(f"docker inspect -f '{{{{.State.Running}}}}' {name}", timeout=15)
    return code == 0 and out.strip().lower() == 'true'


def _validate_proxy(info: ProxyInfo) -> None:
    if not _container_running(info.service):
        raise CommandError(f'{info.name} container is not running: {info.service}')
    if info.kind == 'nginx':
        must_run(f'docker exec {info.service} nginx -t', timeout=30)
    elif info.kind == 'angie':
        must_run(f'docker exec {info.service} angie -t', timeout=30)
    elif info.kind == 'caddy':
        must_run(f'docker exec {info.service} caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile', timeout=30)


def _reload_proxy(info: ProxyInfo) -> None:
    if info.kind == 'nginx':
        must_run(f'docker exec {info.service} nginx -s reload', timeout=30)
    elif info.kind == 'angie':
        must_run(f'docker exec {info.service} angie -s reload', timeout=30)
    elif info.kind == 'caddy':
        must_run(f'docker exec {info.service} caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile', timeout=30)
    elif info.kind == 'traefik':
        time.sleep(1.0)
    if not _container_running(info.service):
        raise CommandError(f'{info.name} stopped after applying the route')


def _apply_proxy_text(info: ProxyInfo, text: str) -> None:
    info.config_path.write_text(text, encoding='utf-8')
    _validate_proxy(info)
    _reload_proxy(info)


def patch_proxy(config: dict, info: ProxyInfo) -> None:
    text = info.config_path.read_text(encoding='utf-8')
    if CUSTOM_TARGET in text:
        config['proxy'] = {
            'kind': info.kind,
            'name': info.name,
            'config_path': str(info.config_path),
            'compose_dir': str(info.compose_dir),
            'service': info.service,
            'patched': True,
            'applied_hash': _sha(text),
        }
        save_config(config)
        return
    if PANEL_TARGET not in text:
        raise CommandError(f'{PANEL_TARGET} was not found in {info.config_path}')

    backup = _backup_proxy(info, text)
    patched = text.replace(PANEL_TARGET, CUSTOM_TARGET)
    try:
        _apply_proxy_text(info, patched)
    except Exception as exc:
        try:
            _apply_proxy_text(info, text)
        except Exception as rollback_exc:
            raise CommandError(f'{exc}; rollback also failed: {rollback_exc}') from rollback_exc
        raise

    config['proxy'] = {
        'kind': info.kind,
        'name': info.name,
        'config_path': str(info.config_path),
        'compose_dir': str(info.compose_dir),
        'service': info.service,
        'patched': True,
        'backup': str(backup),
        'original_hash': _sha(text),
        'applied_hash': _sha(patched),
    }
    save_config(config)


def proxy_from_config(config: dict) -> ProxyInfo | None:
    data = config.get('proxy') or {}
    if data.get('config_path'):
        return ProxyInfo(
            str(data.get('kind') or 'unknown'),
            str(data.get('name') or 'Proxy'),
            Path(str(data['config_path'])),
            Path(str(data.get('compose_dir') or Path(str(data['config_path'])).parent)),
            str(data.get('service') or ''),
        )
    return detect_proxy()


def restore_proxy(config: dict) -> bool:
    info = proxy_from_config(config)
    if not info or not info.config_path.exists():
        return False
    text = info.config_path.read_text(encoding='utf-8')
    if CUSTOM_TARGET not in text:
        config['proxy'] = {}
        save_config(config)
        return False

    restored = text.replace(CUSTOM_TARGET, PANEL_TARGET)
    try:
        _apply_proxy_text(info, restored)
    except Exception:
        try:
            _apply_proxy_text(info, text)
        except Exception:
            pass
        raise
    config['proxy'] = {}
    save_config(config)
    return True


def apply_theme(config: dict) -> None:
    if bool(config.get('theme', {}).get('enabled', True)):
        write_runtime(config['theme'])
    else:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        (RUNTIME_DIR / 'docker-compose.yml').write_text(runtime_compose(), encoding='utf-8')
        (RUNTIME_DIR / 'nginx.conf').write_text(runtime_nginx(), encoding='utf-8')
        write_empty_theme()
    start_injector()


def ensure_installed(config: dict) -> ProxyInfo:
    ok, reason = panel_is_here()
    if not ok:
        raise CommandError(reason)
    info = proxy_from_config(config) or detect_proxy()
    if not info:
        raise CommandError('Supported reverse proxy not found. Supported official layouts: Nginx, Caddy, Angie, Traefik.')

    if bool(config.get('theme', {}).get('enabled', True)):
        write_runtime(config['theme'])
    else:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        (RUNTIME_DIR / 'docker-compose.yml').write_text(runtime_compose(), encoding='utf-8')
        (RUNTIME_DIR / 'nginx.conf').write_text(runtime_nginx(), encoding='utf-8')
        write_empty_theme()
    start_injector()
    patch_proxy(config, info)
    return info
