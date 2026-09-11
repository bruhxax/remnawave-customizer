from __future__ import annotations

"""Lightweight, theme-aware visual effects for Remnawave Customizer.

The effects are CSS-only and use a handful of compositor-friendly layers.  They
never touch the official frontend, never load remote assets and deliberately
keep opacity low so the dashboard stays readable.
"""

EFFECT_KEYS = ('snow', 'particles', 'aurora')


def effect_state(theme: dict, key: str) -> bool:
    data = theme.get('effects')
    return bool(data.get(key, False)) if isinstance(data, dict) else False


def render_effects_css(theme: dict) -> str:
    snow = effect_state(theme, 'snow')
    particles = effect_state(theme, 'particles')
    aurora = effect_state(theme, 'aurora')
    if not (snow or particles or aurora):
        return ''

    blocks: list[str] = [
        '/* Remnawave Customizer: lightweight visual effects. */',
        ':root { --rwc-fx-accent: var(--rwc-accent-rgb); }',
    ]

    if particles:
        blocks.append(r'''
/* Tiny ambient points. One rasterized layer, animated only with transform and opacity. */
#root::before {
  content: '';
  position: fixed;
  left: 0;
  top: 0;
  width: 1px;
  height: 1px;
  pointer-events: none;
  z-index: 1;
  border-radius: 999px;
  box-shadow:
    4vw 9vh 4px 0 rgba(var(--rwc-fx-accent), 0.14),
    11vw 27vh 3px 0 rgba(var(--rwc-fx-accent), 0.10),
    18vw 16vh 5px 0 rgba(var(--rwc-fx-accent), 0.12),
    26vw 42vh 4px 0 rgba(var(--rwc-fx-accent), 0.09),
    34vw 12vh 3px 0 rgba(var(--rwc-fx-accent), 0.13),
    42vw 33vh 5px 0 rgba(var(--rwc-fx-accent), 0.08),
    49vw 7vh 4px 0 rgba(var(--rwc-fx-accent), 0.12),
    57vw 23vh 3px 0 rgba(var(--rwc-fx-accent), 0.10),
    64vw 46vh 5px 0 rgba(var(--rwc-fx-accent), 0.08),
    71vw 14vh 4px 0 rgba(var(--rwc-fx-accent), 0.13),
    79vw 35vh 3px 0 rgba(var(--rwc-fx-accent), 0.10),
    86vw 8vh 5px 0 rgba(var(--rwc-fx-accent), 0.11),
    93vw 28vh 4px 0 rgba(var(--rwc-fx-accent), 0.09),
    7vw 58vh 3px 0 rgba(var(--rwc-fx-accent), 0.08),
    22vw 67vh 5px 0 rgba(var(--rwc-fx-accent), 0.07),
    39vw 61vh 3px 0 rgba(var(--rwc-fx-accent), 0.09),
    56vw 72vh 4px 0 rgba(var(--rwc-fx-accent), 0.07),
    74vw 63vh 5px 0 rgba(var(--rwc-fx-accent), 0.08),
    91vw 76vh 3px 0 rgba(var(--rwc-fx-accent), 0.07);
  opacity: 0.58;
  transform: translate3d(0, 0, 0) scale(1);
  transform-origin: 50vw 45vh;
  animation: rwc-ambient-particles 6.8s ease-in-out infinite alternate;
}

@keyframes rwc-ambient-particles {
  0%   { opacity: 0.40; transform: translate3d(-0.35vw, 0.25vh, 0) scale(0.99); }
  52%  { opacity: 0.66; }
  100% { opacity: 0.48; transform: translate3d(0.55vw, -0.35vh, 0) scale(1.02); }
}
''')

    if snow:
        blocks.append(r'''
/* Soft glowing "snow" dots. They fall only through the upper half of the viewport,
   drift sideways and dissolve before reaching the bottom. */
#root::after {
  content: '';
  position: fixed;
  left: 0;
  top: -8vh;
  width: 2px;
  height: 2px;
  pointer-events: none;
  z-index: 2;
  border-radius: 50%;
  background: transparent;
  box-shadow:
    3vw 2vh 3px 0 rgba(var(--rwc-fx-accent), 0.34),
    8vw 13vh 4px 0 rgba(var(--rwc-fx-accent), 0.22),
    14vw 5vh 3px 0 rgba(var(--rwc-fx-accent), 0.30),
    20vw 18vh 5px 0 rgba(var(--rwc-fx-accent), 0.19),
    27vw 9vh 3px 0 rgba(var(--rwc-fx-accent), 0.28),
    33vw 1vh 4px 0 rgba(var(--rwc-fx-accent), 0.22),
    39vw 16vh 3px 0 rgba(var(--rwc-fx-accent), 0.31),
    46vw 7vh 5px 0 rgba(var(--rwc-fx-accent), 0.20),
    52vw 20vh 3px 0 rgba(var(--rwc-fx-accent), 0.27),
    58vw 4vh 4px 0 rgba(var(--rwc-fx-accent), 0.24),
    65vw 14vh 3px 0 rgba(var(--rwc-fx-accent), 0.32),
    71vw 8vh 5px 0 rgba(var(--rwc-fx-accent), 0.18),
    77vw 19vh 3px 0 rgba(var(--rwc-fx-accent), 0.27),
    83vw 3vh 4px 0 rgba(var(--rwc-fx-accent), 0.23),
    89vw 12vh 3px 0 rgba(var(--rwc-fx-accent), 0.30),
    95vw 17vh 5px 0 rgba(var(--rwc-fx-accent), 0.18),
    17vw 24vh 4px 0 rgba(var(--rwc-fx-accent), 0.20),
    43vw 25vh 3px 0 rgba(var(--rwc-fx-accent), 0.22),
    69vw 23vh 4px 0 rgba(var(--rwc-fx-accent), 0.19),
    92vw 26vh 3px 0 rgba(var(--rwc-fx-accent), 0.21);
  opacity: 0;
  transform: translate3d(-1.5vw, -6vh, 0);
  animation: rwc-soft-snow 13.5s linear infinite;
}

@keyframes rwc-soft-snow {
  0%   { opacity: 0;    transform: translate3d(-1.5vw, -6vh, 0); }
  8%   { opacity: 0.72; }
  55%  { opacity: 0.56; transform: translate3d(0.8vw, 22vh, 0); }
  78%  { opacity: 0.30; transform: translate3d(2.3vw, 38vh, 0); }
  100% { opacity: 0;    transform: translate3d(3.6vw, 52vh, 0); }
}
''')

    if aurora:
        blocks.append(r'''
/* Very soft moving accent haze behind the page content. */
.mantine-AppShell-main {
  position: relative;
  isolation: isolate;
}

.mantine-AppShell-main::before {
  content: '';
  position: fixed;
  inset: -18vh -12vw auto 12vw;
  height: 68vh;
  pointer-events: none;
  z-index: 0;
  opacity: 0.28;
  background:
    radial-gradient(ellipse at 18% 16%, rgba(var(--rwc-fx-accent), 0.13) 0%, rgba(var(--rwc-fx-accent), 0.045) 24%, transparent 57%),
    radial-gradient(ellipse at 76% 12%, rgba(var(--rwc-fx-accent), 0.09) 0%, rgba(var(--rwc-fx-accent), 0.03) 28%, transparent 61%);
  transform: translate3d(-1.5vw, 0, 0) scale(1.02);
  transform-origin: 50% 20%;
  animation: rwc-soft-aurora 18s ease-in-out infinite alternate;
}

@keyframes rwc-soft-aurora {
  0%   { opacity: 0.20; transform: translate3d(-1.5vw, -0.5vh, 0) scale(1.01); }
  48%  { opacity: 0.31; }
  100% { opacity: 0.23; transform: translate3d(2vw, 1.2vh, 0) scale(1.05); }
}
''')

    blocks.append(r'''
/* Respect OS/browser reduced-motion preferences. */
@media (prefers-reduced-motion: reduce) {
  #root::before,
  #root::after,
  .mantine-AppShell-main::before {
    animation: none !important;
  }
  #root::after { display: none !important; }
}
''')
    return '\n'.join(blocks).strip() + '\n'
