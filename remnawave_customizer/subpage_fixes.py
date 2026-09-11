from __future__ import annotations

"""Small visual compatibility fixes for the local Subscription Page.

The official Subscription Page still computes a few icon gradients inline from
its own color parser and keeps the active client glow in a CSS-module class.
Those values cannot be normalized by the regular token layer alone.  Keep the
fixes in a late stylesheet instead of touching official frontend files or JS.
"""

from . import subpage as _subpage

_ORIGINAL_RENDER_CSS = _subpage.render_css
_INSTALLED = False


EXTRA_CSS = r'''
/* RWC Subscription Page: finish hardcoded decorative glow normalization. */

/* Mantine Timeline uses cyan as its own line color. Keep the connector line in
   exactly the same accent as the selected Sub Page theme. */
.mantine-Timeline-root {
  --tl-color: var(--rwc-sub-accent) !important;
}

/* ThemeIconShared receives a generated inline gradient/box-shadow from
   getColorGradientSolid(). Override only the decorative cyan/blue/indigo/
   violet families. Semantic green/red/orange/yellow status icons stay stock. */
.mantine-ThemeIcon-root[style*="34, 211, 238"],
.mantine-ThemeIcon-root[style*="34,211,238"],
.mantine-ThemeIcon-root[style*="34, 139, 230"],
.mantine-ThemeIcon-root[style*="34,139,230"],
.mantine-ThemeIcon-root[style*="92, 124, 250"],
.mantine-ThemeIcon-root[style*="92,124,250"],
.mantine-ThemeIcon-root[style*="151, 117, 250"],
.mantine-ThemeIcon-root[style*="151,117,250"] {
  --ti-color: var(--rwc-sub-accent) !important;
  color: var(--rwc-sub-accent) !important;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--rwc-sub-surface) 90%, var(--rwc-sub-accent) 10%) 0%,
    color-mix(in srgb, var(--rwc-sub-surface) 96%, var(--rwc-sub-accent) 4%) 100%
  ) !important;
  border: 1px solid rgba(var(--rwc-sub-accent-rgb), 0.42) !important;
  box-shadow:
    inset 0 0 20px rgba(var(--rwc-sub-accent-rgb), 0.16),
    0 0 13px rgba(var(--rwc-sub-accent-rgb), 0.10) !important;
  filter: none !important;
}

.mantine-ThemeIcon-root[style*="34, 211, 238"] svg,
.mantine-ThemeIcon-root[style*="34,211,238"] svg,
.mantine-ThemeIcon-root[style*="34, 139, 230"] svg,
.mantine-ThemeIcon-root[style*="34,139,230"] svg,
.mantine-ThemeIcon-root[style*="92, 124, 250"] svg,
.mantine-ThemeIcon-root[style*="92,124,250"] svg,
.mantine-ThemeIcon-root[style*="151, 117, 250"] svg,
.mantine-ThemeIcon-root[style*="151,117,250"] svg {
  color: var(--rwc-sub-accent) !important;
  filter: drop-shadow(0 0 5px rgba(var(--rwc-sub-accent-rgb), 0.22)) !important;
}

/* Vite keeps the local CSS-module name inside the generated class.  Explicitly
   restore the active application/client treatment after the generic surface
   palette is applied, so selected Happ/INCY/etc. never looks flat. */
[class*="appButtonActive"] {
  background: linear-gradient(
    90deg,
    rgba(var(--rwc-sub-accent-rgb), 0.16) 0%,
    rgba(var(--rwc-sub-accent-rgb), 0.045) 100%
  ) !important;
  border-color: rgba(var(--rwc-sub-accent-rgb), 0.30) !important;
  border-left-color: var(--rwc-sub-accent) !important;
  box-shadow:
    inset 4px 0 14px -4px rgba(var(--rwc-sub-accent-rgb), 0.38),
    inset 0 0 22px rgba(var(--rwc-sub-accent-rgb), 0.07),
    0 0 13px rgba(var(--rwc-sub-accent-rgb), 0.09) !important;
}

[class*="appButtonActive"] [class*="appName"] {
  color: color-mix(in srgb, var(--rwc-sub-accent) 78%, white 22%) !important;
  text-shadow: 0 0 10px rgba(var(--rwc-sub-accent-rgb), 0.16) !important;
}

/* Keep the non-selected client quiet, but make hover use a very subtle theme
   tint rather than the original white/cyan mixture. */
[class*="appButton"]:not([class*="appButtonActive"]):hover {
  background: rgba(var(--rwc-sub-accent-rgb), 0.045) !important;
  border-left-color: rgba(var(--rwc-sub-accent-rgb), 0.28) !important;
}
'''


def _render_css(theme: dict) -> str:
    return _ORIGINAL_RENDER_CSS(theme).rstrip() + "\n\n" + EXTRA_CSS.strip() + "\n"


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _subpage.render_css = _render_css
    _INSTALLED = True
