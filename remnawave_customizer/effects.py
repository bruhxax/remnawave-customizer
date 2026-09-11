from __future__ import annotations

"""Lightweight theme-aware visual effects for Remnawave Customizer.

Effects render inside a dedicated fixed overlay injected by the Customizer proxy.
That makes them visible above opaque Panel surfaces without touching the official
frontend. Every effect is CSS-only, pointer-events:none and uses the current
accent color.
"""

EFFECT_KEYS = ('snow', 'particles', 'aurora', 'orbs', 'sweep')


def effect_state(theme: dict, key: str) -> bool:
    data = theme.get('effects')
    return bool(data.get(key, False)) if isinstance(data, dict) else False


def render_effects_css(theme: dict) -> str:
    enabled = {key: effect_state(theme, key) for key in EFFECT_KEYS}
    if not any(enabled.values()):
        return ''

    blocks: list[str] = [r'''
/* Remnawave Customizer: dedicated compositor-friendly visual effects layer. */
:root { --rwc-fx-accent: var(--rwc-accent-rgb); }
#rwc-effects {
  position: fixed;
  inset: 0;
  z-index: 4;
  overflow: hidden;
  pointer-events: none;
  user-select: none;
  contain: strict;
}
#rwc-effects > .rwc-fx {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
''']

    if enabled['particles']:
        blocks.append(r'''
/* Tiny ambient stars. Kept intentionally dim. */
.rwc-fx-particles::before,
.rwc-fx-particles::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 2px;
  height: 2px;
  border-radius: 50%;
  background: rgba(var(--rwc-fx-accent), 0.22);
  box-shadow:
    5vw 11vh 4px rgba(var(--rwc-fx-accent), .24), 12vw 36vh 3px rgba(var(--rwc-fx-accent), .16),
    18vw 68vh 5px rgba(var(--rwc-fx-accent), .18), 25vw 22vh 3px rgba(var(--rwc-fx-accent), .21),
    31vw 52vh 4px rgba(var(--rwc-fx-accent), .15), 38vw 14vh 4px rgba(var(--rwc-fx-accent), .20),
    45vw 76vh 3px rgba(var(--rwc-fx-accent), .18), 52vw 42vh 5px rgba(var(--rwc-fx-accent), .17),
    59vw 19vh 3px rgba(var(--rwc-fx-accent), .22), 66vw 61vh 4px rgba(var(--rwc-fx-accent), .15),
    73vw 31vh 3px rgba(var(--rwc-fx-accent), .21), 80vw 83vh 5px rgba(var(--rwc-fx-accent), .14),
    87vw 47vh 3px rgba(var(--rwc-fx-accent), .19), 94vw 16vh 4px rgba(var(--rwc-fx-accent), .23),
    9vw 88vh 3px rgba(var(--rwc-fx-accent), .14), 22vw 92vh 4px rgba(var(--rwc-fx-accent), .15),
    41vw 90vh 3px rgba(var(--rwc-fx-accent), .17), 62vw 8vh 4px rgba(var(--rwc-fx-accent), .19),
    78vw 6vh 3px rgba(var(--rwc-fx-accent), .20), 91vw 71vh 4px rgba(var(--rwc-fx-accent), .16);
  opacity: .45;
  animation: rwc-ambient-particles 6.8s ease-in-out infinite alternate;
}
.rwc-fx-particles::after {
  transform: translate3d(3vw, 2vh, 0) scale(.72);
  opacity: .24;
  animation-duration: 9.7s;
  animation-delay: -2.4s;
}
@keyframes rwc-ambient-particles {
  0%   { opacity: .18; transform: translate3d(0, 0, 0); }
  45%  { opacity: .52; }
  100% { opacity: .25; transform: translate3d(.8vw, -1.1vh, 0); }
}
''')

    if enabled['snow']:
        blocks.append(r'''
/* Falling glowing dots: drift down only to around half the viewport and fade. */
.rwc-fx-snow::before,
.rwc-fx-snow::after {
  content: '';
  position: absolute;
  left: 0;
  top: -8vh;
  width: 2px;
  height: 2px;
  border-radius: 50%;
  background: rgba(var(--rwc-fx-accent), .30);
  box-shadow:
    3vw 2vh 3px rgba(var(--rwc-fx-accent), .34), 8vw 13vh 4px rgba(var(--rwc-fx-accent), .22),
    14vw 5vh 3px rgba(var(--rwc-fx-accent), .30), 20vw 18vh 5px rgba(var(--rwc-fx-accent), .19),
    27vw 9vh 3px rgba(var(--rwc-fx-accent), .28), 33vw 1vh 4px rgba(var(--rwc-fx-accent), .22),
    39vw 16vh 3px rgba(var(--rwc-fx-accent), .31), 46vw 7vh 5px rgba(var(--rwc-fx-accent), .20),
    52vw 20vh 3px rgba(var(--rwc-fx-accent), .27), 58vw 4vh 4px rgba(var(--rwc-fx-accent), .24),
    65vw 14vh 3px rgba(var(--rwc-fx-accent), .32), 71vw 8vh 5px rgba(var(--rwc-fx-accent), .18),
    77vw 19vh 3px rgba(var(--rwc-fx-accent), .27), 83vw 3vh 4px rgba(var(--rwc-fx-accent), .23),
    89vw 12vh 3px rgba(var(--rwc-fx-accent), .30), 95vw 17vh 5px rgba(var(--rwc-fx-accent), .18);
  opacity: 0;
  animation: rwc-soft-snow 13.5s linear infinite;
}
.rwc-fx-snow::after {
  left: 4vw;
  top: -19vh;
  transform: scale(.72);
  animation-duration: 17.2s;
  animation-delay: -6.1s;
  opacity: .72;
}
@keyframes rwc-soft-snow {
  0%   { opacity: 0; transform: translate3d(-1.5vw, -6vh, 0); }
  8%   { opacity: .72; }
  55%  { opacity: .56; transform: translate3d(.8vw, 22vh, 0); }
  78%  { opacity: .30; transform: translate3d(2.3vw, 38vh, 0); }
  100% { opacity: 0; transform: translate3d(3.6vw, 52vh, 0); }
}
''')

    if enabled['aurora']:
        blocks.append(r'''
/* Large soft accent haze. No blur filter: gradients stay cheap to render. */
.rwc-fx-aurora {
  opacity: .34;
  background:
    radial-gradient(55vw 38vh at 12% 8%, rgba(var(--rwc-fx-accent), .15), rgba(var(--rwc-fx-accent), .045) 38%, transparent 72%),
    radial-gradient(48vw 34vh at 88% 18%, rgba(var(--rwc-fx-accent), .11), rgba(var(--rwc-fx-accent), .03) 42%, transparent 74%);
  animation: rwc-soft-aurora 18s ease-in-out infinite alternate;
}
@keyframes rwc-soft-aurora {
  0%   { opacity: .22; transform: translate3d(-1.2vw, -.5vh, 0) scale(1.01); }
  50%  { opacity: .38; }
  100% { opacity: .25; transform: translate3d(1.8vw, 1.2vh, 0) scale(1.045); }
}
''')

    if enabled['orbs']:
        blocks.append(r'''
/* Floating soft circles around the edges. */
.rwc-fx-orbs {
  opacity: .30;
  background:
    radial-gradient(circle 85px at 8% 28%, rgba(var(--rwc-fx-accent), .12) 0 18%, rgba(var(--rwc-fx-accent), .045) 42%, transparent 72%),
    radial-gradient(circle 120px at 92% 68%, rgba(var(--rwc-fx-accent), .10) 0 17%, rgba(var(--rwc-fx-accent), .035) 45%, transparent 74%),
    radial-gradient(circle 70px at 72% 12%, rgba(var(--rwc-fx-accent), .09) 0 20%, transparent 70%);
  animation: rwc-floating-orbs 15s ease-in-out infinite alternate;
}
@keyframes rwc-floating-orbs {
  0%   { transform: translate3d(-.8vw, 1vh, 0) scale(.99); opacity: .20; }
  50%  { opacity: .34; }
  100% { transform: translate3d(1.2vw, -1.5vh, 0) scale(1.035); opacity: .24; }
}
''')

    if enabled['sweep']:
        blocks.append(r'''
/* Rare diagonal light sweep, subtle enough not to distract from tables/forms. */
.rwc-fx-sweep::before {
  content: '';
  position: absolute;
  top: -35vh;
  left: -36vw;
  width: 24vw;
  height: 170vh;
  opacity: 0;
  transform: rotate(18deg) translate3d(0, 0, 0);
  background: linear-gradient(90deg, transparent, rgba(var(--rwc-fx-accent), .055), rgba(var(--rwc-fx-accent), .12), rgba(var(--rwc-fx-accent), .055), transparent);
  animation: rwc-soft-sweep 14s ease-in-out infinite;
}
@keyframes rwc-soft-sweep {
  0%, 38%  { opacity: 0; transform: rotate(18deg) translate3d(0, 0, 0); }
  45%      { opacity: .42; }
  68%      { opacity: .22; }
  76%,100% { opacity: 0; transform: rotate(18deg) translate3d(175vw, 0, 0); }
}
''')

    blocks.append(r'''
@media (prefers-reduced-motion: reduce) {
  #rwc-effects .rwc-fx,
  #rwc-effects .rwc-fx::before,
  #rwc-effects .rwc-fx::after {
    animation: none !important;
  }
  .rwc-fx-snow, .rwc-fx-sweep { display: none !important; }
}
''')
    return '\n'.join(blocks).strip() + '\n'
