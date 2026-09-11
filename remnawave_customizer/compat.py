from __future__ import annotations

"""Runtime compatibility layer for Remnawave visual quirks.

The official Panel and Subscription Page mix theme tokens with several local
cyan/blue styles. Keeping overrides in the proxy makes the Customizer fully
reversible: official frontend files and Docker images are never modified.
"""

from . import proxy as _proxy
from . import themes as _themes
from .config import RUNTIME_DIR
from .effects import render_effects_css

_ORIGINAL_RENDER_CSS = _themes.render_css
_ORIGINAL_RUNTIME_NGINX = _proxy.runtime_nginx
_ORIGINAL_RUNTIME_COMPOSE = _proxy.runtime_compose
_ORIGINAL_WRITE_RUNTIME = _proxy.write_runtime
_INSTALLED = False


EXTRA_CSS = r'''
/* Remnawave Customizer: decorative accent compatibility. */
.mantine-ActionIcon-root[style*="mantine-color-cyan"],
.mantine-ActionIcon-root[style*="mantine-color-blue"],
.mantine-ActionIcon-root[style*="mantine-color-indigo"] {
  --ai-color: var(--rwc-accent) !important;
  --ai-hover-color: var(--rwc-accent) !important;
  --ai-bd: 1px solid rgba(var(--rwc-accent-rgb), 0.42) !important;
}

.mantine-ActionIcon-root[data-variant="light"][style*="mantine-color-cyan"],
.mantine-ActionIcon-root[data-variant="light"][style*="mantine-color-blue"],
.mantine-ActionIcon-root[data-variant="light"][style*="mantine-color-indigo"],
.mantine-ActionIcon-root[data-variant="soft"][style*="mantine-color-cyan"],
.mantine-ActionIcon-root[data-variant="soft"][style*="mantine-color-blue"],
.mantine-ActionIcon-root[data-variant="soft"][style*="mantine-color-indigo"] {
  --ai-bg: rgba(var(--rwc-accent-rgb), 0.10) !important;
  --ai-hover: rgba(var(--rwc-accent-rgb), 0.18) !important;
}

.mantine-ActionIcon-root[data-variant="outline"][style*="mantine-color-cyan"],
.mantine-ActionIcon-root[data-variant="outline"][style*="mantine-color-blue"],
.mantine-ActionIcon-root[data-variant="outline"][style*="mantine-color-indigo"] {
  --ai-bg: transparent !important;
  --ai-hover: rgba(var(--rwc-accent-rgb), 0.10) !important;
}

.mantine-ThemeIcon-root[style*="mantine-color-cyan"],
.mantine-ThemeIcon-root[style*="mantine-color-blue"],
.mantine-ThemeIcon-root[style*="mantine-color-indigo"] {
  --ti-color: var(--rwc-accent) !important;
  --ti-bg: rgba(var(--rwc-accent-rgb), 0.09) !important;
  --ti-bd: 1px solid rgba(var(--rwc-accent-rgb), 0.36) !important;
}

.mantine-AppShell-navbar a:hover svg,
.mantine-AppShell-navbar button:hover svg,
.mantine-AppShell-navbar [data-active="true"] svg {
  filter: drop-shadow(0 2px 4px rgba(var(--rwc-accent-rgb), 0.28)) !important;
}

.mantine-AppShell-navbar a:hover::before,
.mantine-AppShell-navbar button:hover::before,
.mantine-AppShell-navbar [data-active="true"]::before {
  background: linear-gradient(135deg, transparent 0%, rgba(var(--rwc-accent-rgb), 0.08) 50%, transparent 100%) !important;
}

.mantine-AppShell-navbar [data-active="true"] {
  border-color: var(--rwc-accent) !important;
  box-shadow: inset 0 0 0 1px rgba(var(--rwc-accent-rgb), 0.05), 0 0 14px rgba(var(--rwc-accent-rgb), 0.04) !important;
}

.mantine-AppShell-navbar [data-active="true"]::after {
  background: var(--rwc-accent) !important;
  box-shadow: 0 0 8px rgba(var(--rwc-accent-rgb), 0.42) !important;
}
'''

EFFECTS_HTML = (
    '<div id="rwc-effects" aria-hidden="true">'
    '<div class="rwc-fx rwc-fx-particles"></div>'
    '<div class="rwc-fx rwc-fx-aurora"></div>'
    '<div class="rwc-fx rwc-fx-orbs"></div>'
    '<div class="rwc-fx rwc-fx-sweep"></div>'
    '<div class="rwc-fx rwc-fx-snow"></div>'
    '</div>'
)

SUBPAGE_SERVER = r'''

# Local Subscription Page customizer. This listener is used only when the
# official remnawave-subscription-page container is on the same server/network.
server {
    listen 3101;
    server_name _;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 5;
    gzip_types text/css application/json application/javascript image/svg+xml;

    location = /__remnawave_customizer/subpage.css {
        alias /usr/share/nginx/html/subpage.css;
        default_type text/css;
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0" always;
        add_header Pragma "no-cache" always;
        add_header X-Content-Type-Options "nosniff" always;
    }

    # API stays untouched and keeps normal upstream compression.
    location ^~ /api {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $subpage_upstream http://remnawave-subscription-page:3010;
        proxy_http_version 1.1;
        proxy_pass $subpage_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Rewrite only known visual constants from the official Subscription Page.
    location ~* \.css$ {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $subpage_upstream http://remnawave-subscription-page:3010;
        proxy_http_version 1.1;
        proxy_pass $subpage_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Accept-Encoding "";

        sub_filter_types text/css;
        sub_filter_once off;

        # Stock dark surfaces.
        sub_filter '#161b23' 'var(--rwc-sub-background)';
        sub_filter '#161B23' 'var(--rwc-sub-background)';
        sub_filter '#161b22' 'var(--rwc-sub-background)';
        sub_filter '#161B22' 'var(--rwc-sub-background)';
        sub_filter '#21262d' 'var(--rwc-sub-surface)';
        sub_filter '#21262D' 'var(--rwc-sub-surface)';
        sub_filter '#30363d' 'var(--rwc-sub-border)';
        sub_filter '#30363D' 'var(--rwc-sub-border)';

        # Primary cyan and decorative blue/violet families. Semantic
        # green/red/orange/yellow states intentionally stay stock.
        sub_filter 'rgba(34,211,238,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(34, 211, 238,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(6,182,212,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(6, 182, 212,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(34,139,230,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(34, 139, 230,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(151,117,250,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(151, 117, 250,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(132,94,247,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter 'rgba(132, 94, 247,' 'rgba(var(--rwc-sub-accent-rgb),';
        sub_filter '#22d3ee' 'var(--rwc-sub-accent)';
        sub_filter '#22D3EE' 'var(--rwc-sub-accent)';
        sub_filter '#06b6d4' 'var(--rwc-sub-accent)';
        sub_filter '#06B6D4' 'var(--rwc-sub-accent)';
        sub_filter '#228be6' 'var(--rwc-sub-accent)';
        sub_filter '#228BE6' 'var(--rwc-sub-accent)';
        sub_filter '#9775fa' 'var(--rwc-sub-accent)';
        sub_filter '#9775FA' 'var(--rwc-sub-accent)';
        sub_filter '#845ef7' 'var(--rwc-sub-accent)';
        sub_filter '#845EF7' 'var(--rwc-sub-accent)';

        proxy_hide_header Cache-Control;
        proxy_hide_header Expires;
        add_header Cache-Control "no-cache, must-revalidate" always;
    }

    # Large/static assets are a pure pass-through.
    location ~* \.(?:js|mjs|map|json|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|wasm|lottie)$ {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $subpage_upstream http://remnawave-subscription-page:3010;
        proxy_http_version 1.1;
        proxy_pass $subpage_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # SPA HTML receives one extra stylesheet; official files stay untouched.
    location / {
        resolver 127.0.0.11 valid=5s ipv6=off;
        set $subpage_upstream http://remnawave-subscription-page:3010;
        proxy_http_version 1.1;
        proxy_pass $subpage_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $rwc_real_ip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $rwc_forwarded_proto;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Accept-Encoding "";

        sub_filter_once on;
        sub_filter '</head>' '<link rel="stylesheet" href="/__remnawave_customizer/subpage.css"></head>';
    }
}
'''


def _render_css(theme: dict) -> str:
    css = _ORIGINAL_RENDER_CSS(theme) + "\n" + EXTRA_CSS
    effects = render_effects_css(theme)
    if effects:
        css += "\n" + effects
    return css


def _runtime_compose() -> str:
    text = _ORIGINAL_RUNTIME_COMPOSE()
    mount = '      - ./theme.css:/usr/share/nginx/html/theme.css:ro\n'
    extra = '      - ./subpage.css:/usr/share/nginx/html/subpage.css:ro\n'
    if extra not in text and mount in text:
        text = text.replace(mount, mount + extra, 1)
    return text


def _runtime_nginx() -> str:
    text = _ORIGINAL_RUNTIME_NGINX()

    marker = "        sub_filter_once off;\n"
    addition = (
        "\n"
        "        # RWC: transformed CSS must not stay immutable across Customizer updates.\n"
        "        proxy_hide_header Cache-Control;\n"
        "        proxy_hide_header Expires;\n"
        "        add_header Cache-Control \"no-cache, must-revalidate\" always;\n"
    )
    if "RWC: transformed CSS must not stay immutable" not in text and marker in text:
        text = text.replace(marker, marker + addition, 1)

    head_line = "        sub_filter '</head>' '<link rel=\"stylesheet\" href=\"/__remnawave_customizer/theme.css\"></head>';\n"
    body_line = f"        sub_filter '</body>' '{EFFECTS_HTML}</body>';\n"
    if body_line not in text and head_line in text:
        text = text.replace(head_line, head_line + body_line, 1)

    if 'listen 3101;' not in text:
        text = text.rstrip() + SUBPAGE_SERVER + '\n'
    return text


def _write_runtime(theme: dict) -> None:
    _ORIGINAL_WRITE_RUNTIME(theme)
    path = RUNTIME_DIR / 'subpage.css'
    if not path.exists():
        path.write_text('/* Subscription Page Customizer disabled */\n', encoding='utf-8')
        path.chmod(0o644)


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    _themes.render_css = _render_css
    _proxy.render_css = _render_css
    _proxy.runtime_compose = _runtime_compose
    _proxy.runtime_nginx = _runtime_nginx
    _proxy.write_runtime = _write_runtime
    _INSTALLED = True
