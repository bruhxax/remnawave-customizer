from __future__ import annotations

"""Runtime compatibility layer for Remnawave 3.x visual quirks.

The official frontend mixes theme tokens with several component-local cyan/blue
styles. Keeping these overrides here lets the Customizer stay reversible: no
Panel frontend files are modified and the whole layer can be removed at once.
"""

from . import proxy as _proxy
from . import themes as _themes
from .effects import render_effects_css

_ORIGINAL_RENDER_CSS = _themes.render_css
_ORIGINAL_RUNTIME_NGINX = _proxy.runtime_nginx
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


def _render_css(theme: dict) -> str:
    css = _ORIGINAL_RENDER_CSS(theme) + "\n" + EXTRA_CSS
    effects = render_effects_css(theme)
    if effects:
        css += "\n" + effects
    return css


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
    return text


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    _themes.render_css = _render_css
    _proxy.render_css = _render_css
    _proxy.runtime_nginx = _runtime_nginx
    _INSTALLED = True
