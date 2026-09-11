from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

RGB = tuple[int, int, int]


@dataclass(frozen=True)
class ThemePreset:
    key: str
    name_ru: str
    name_en: str
    accent: RGB
    background: RGB
    surface: RGB
    radius: str


# Presets deliberately keep background/surface contrast restrained. Remnawave has
# a lot of nested cards, drawers and tables; very different surface colors make
# those layers visually noisy even when every selector is technically correct.
PRESETS: tuple[ThemePreset, ...] = (
    ThemePreset('remnawave', 'Remnawave+', 'Remnawave+', (6, 182, 212), (13, 17, 23), (22, 27, 34), 'medium'),
    ThemePreset('midnight', 'Midnight Blue', 'Midnight Blue', (36, 166, 255), (7, 11, 17), (16, 22, 30), 'medium'),
    ThemePreset('oled', 'OLED Black', 'OLED Black', (0, 210, 255), (0, 0, 0), (10, 11, 13), 'medium'),
    ThemePreset('graphite', 'Graphite', 'Graphite', (122, 162, 247), (14, 15, 18), (24, 26, 31), 'small'),
    ThemePreset('slate', 'Slate', 'Slate', (100, 160, 255), (13, 17, 23), (24, 30, 39), 'medium'),
    ThemePreset('nord', 'Nord', 'Nord', (136, 192, 208), (34, 39, 49), (45, 51, 63), 'medium'),
    ThemePreset('ocean', 'Deep Ocean', 'Deep Ocean', (34, 211, 238), (4, 13, 20), (10, 25, 35), 'medium'),
    ThemePreset('arctic', 'Arctic', 'Arctic', (125, 211, 252), (12, 20, 27), (23, 33, 42), 'large'),
    ThemePreset('emerald', 'Emerald', 'Emerald', (52, 211, 153), (6, 15, 13), (14, 28, 24), 'medium'),
    ThemePreset('forest', 'Forest', 'Forest', (74, 222, 128), (8, 14, 10), (18, 29, 21), 'small'),
    ThemePreset('purple', 'Purple Dark', 'Purple Dark', (168, 123, 255), (12, 9, 20), (25, 20, 36), 'large'),
    ThemePreset('violet', 'Violet', 'Violet', (139, 92, 246), (13, 11, 21), (25, 22, 37), 'medium'),
    ThemePreset('tokyo', 'Tokyo Night', 'Tokyo Night', (122, 162, 247), (10, 14, 24), (21, 27, 40), 'medium'),
    ThemePreset('rose', 'Rose Pine', 'Rose Pine', (235, 188, 186), (19, 17, 28), (31, 27, 42), 'large'),
    ThemePreset('mocha', 'Mocha', 'Mocha', (137, 180, 250), (17, 17, 27), (30, 30, 46), 'medium'),
    ThemePreset('crimson', 'Crimson', 'Crimson', (248, 113, 113), (18, 9, 11), (32, 18, 21), 'medium'),
    ThemePreset('amber', 'Amber', 'Amber', (245, 158, 11), (18, 13, 7), (32, 25, 16), 'small'),
    ThemePreset('sunset', 'Sunset', 'Sunset', (251, 113, 133), (20, 10, 15), (34, 20, 27), 'large'),
    ThemePreset('cyber', 'Cyber Purple', 'Cyber Purple', (217, 70, 239), (10, 7, 16), (23, 16, 31), 'medium'),
)

RADIUS_VALUES = {
    'none': 0,
    'small': 6,
    'medium': 10,
    'large': 14,
    'xl': 20,
}

RADIUS_LABELS = {
    'ru': {
        'none': 'Без скругления',
        'small': 'Небольшое',
        'medium': 'Среднее',
        'large': 'Большое',
        'xl': 'Максимальное',
    },
    'en': {
        'none': 'Square',
        'small': 'Small',
        'medium': 'Medium',
        'large': 'Large',
        'xl': 'Maximum',
    },
}

ACCENT_COLORS: tuple[RGB, ...] = (
    (255, 99, 132), (255, 82, 82), (255, 146, 43), (255, 199, 0), (198, 255, 0), (52, 211, 153), (0, 200, 160), (0, 210, 255),
    (0, 169, 255), (51, 136, 255), (91, 108, 255), (124, 92, 255), (168, 123, 255), (207, 95, 255), (245, 91, 200), (255, 105, 180),
    (255, 140, 105), (255, 176, 92), (250, 204, 21), (163, 230, 53), (34, 197, 94), (20, 184, 166), (6, 182, 212), (14, 165, 233),
    (59, 130, 246), (99, 102, 241), (139, 92, 246), (168, 85, 247), (217, 70, 239), (236, 72, 153), (244, 63, 94), (248, 113, 113),
    (251, 146, 60), (234, 179, 8), (132, 204, 22), (16, 185, 129), (13, 148, 136), (8, 145, 178), (2, 132, 199), (37, 99, 235),
    (79, 70, 229), (124, 58, 237), (147, 51, 234), (192, 38, 211), (219, 39, 119), (225, 29, 72), (220, 38, 38), (194, 65, 12),
)

BACKGROUND_COLORS: tuple[RGB, ...] = (
    (0, 0, 0), (5, 7, 10), (7, 12, 19), (9, 14, 22), (11, 16, 25), (13, 18, 28), (15, 20, 30), (17, 22, 32),
    (9, 10, 14), (12, 12, 18), (14, 13, 22), (13, 10, 22), (15, 12, 25), (12, 15, 26), (9, 17, 25), (8, 20, 24),
    (6, 16, 14), (8, 18, 16), (10, 20, 18), (12, 20, 16), (16, 19, 12), (20, 17, 12), (20, 14, 13), (21, 13, 18),
    (20, 20, 20), (24, 24, 24), (28, 28, 28), (22, 24, 28), (25, 27, 32), (28, 31, 36), (31, 34, 40), (36, 41, 51),
)

SURFACE_COLORS: tuple[RGB, ...] = (
    (8, 9, 11), (11, 14, 18), (13, 21, 31), (16, 24, 35), (19, 27, 38), (22, 30, 42), (25, 33, 46), (28, 36, 50),
    (15, 14, 20), (19, 17, 27), (22, 18, 32), (25, 19, 39), (29, 22, 44), (24, 27, 45), (18, 31, 43), (15, 34, 38),
    (13, 29, 25), (16, 33, 28), (19, 37, 31), (28, 37, 22), (37, 35, 22), (40, 31, 22), (40, 27, 25), (41, 24, 33),
    (30, 30, 30), (34, 34, 34), (38, 38, 38), (36, 39, 45), (40, 43, 50), (44, 48, 56), (46, 52, 64), (52, 58, 70),
)


def clamp(v: int) -> int:
    return max(0, min(255, int(v)))


def mix(a: RGB, b: RGB, t: float) -> RGB:
    return tuple(clamp(round(x + (y - x) * t)) for x, y in zip(a, b))  # type: ignore[return-value]


def lighten(c: RGB, amount: float) -> RGB:
    return mix(c, (255, 255, 255), amount)


def darken(c: RGB, amount: float) -> RGB:
    return mix(c, (0, 0, 0), amount)


def rgb(value: Iterable[int]) -> RGB:
    values = tuple(clamp(int(x)) for x in value)
    if len(values) != 3:
        raise ValueError('RGB must contain exactly 3 values')
    return values  # type: ignore[return-value]


def css_rgb(c: RGB) -> str:
    return f'rgb({c[0]} {c[1]} {c[2]})'


def css_rgb_csv(c: RGB) -> str:
    return f'{c[0]}, {c[1]}, {c[2]}'


def accent_scale(accent: RGB) -> list[RGB]:
    # Remnawave's primaryShade is 8. Keep shade 8 equal to the chosen color so
    # the palette shown in the CLI is the color users actually see in buttons.
    return [
        mix(accent, (255, 255, 255), 0.92),
        mix(accent, (255, 255, 255), 0.82),
        mix(accent, (255, 255, 255), 0.70),
        mix(accent, (255, 255, 255), 0.56),
        mix(accent, (255, 255, 255), 0.40),
        mix(accent, (255, 255, 255), 0.25),
        mix(accent, (255, 255, 255), 0.12),
        accent,
        accent,
        darken(accent, 0.14),
    ]


def dark_scale(background: RGB, surface: RGB) -> list[RGB]:
    # dark.0..3 remain neutral text colors. dark.4..9 are surfaces/borders.
    # Borders are intentionally subtle: aggressive contrast creates bright
    # outlines around cards/forms that are almost invisible in stock Remnawave.
    border = lighten(surface, 0.09)
    border_soft = lighten(surface, 0.045)
    return [
        (232, 236, 242),
        (204, 210, 219),
        (168, 176, 188),
        (126, 136, 150),
        border,
        border_soft,
        surface,
        mix(surface, background, 0.42),
        background,
        darken(background, 0.16),
    ]


def render_css(theme: dict) -> str:
    accent = rgb(theme['accent'])
    background = rgb(theme['background'])
    surface = rgb(theme['surface'])
    radius_key = str(theme.get('radius', 'medium'))
    radius = RADIUS_VALUES.get(radius_key, 10)

    accents = accent_scale(accent)
    darks = dark_scale(background, surface)
    text = (238, 241, 245)
    dimmed = (157, 166, 179)
    muted = (112, 122, 137)
    surface_hover = lighten(surface, 0.04)
    border = darks[4]

    lines = [
        '/* Generated by Remnawave Customizer. Token-first compatibility layer. */',
        ':root, [data-mantine-color-scheme="dark"] {',
        f'  --rwc-background: {css_rgb(background)};',
        f'  --rwc-surface: {css_rgb(surface)};',
        f'  --rwc-surface-deep: {css_rgb(darks[7])};',
        f'  --rwc-surface-hover: {css_rgb(surface_hover)};',
        f'  --rwc-border: {css_rgb(border)};',
        f'  --rwc-accent: {css_rgb(accent)};',
        f'  --rwc-accent-rgb: {css_rgb_csv(accent)};',
        f'  --rwc-text: {css_rgb(text)};',
        f'  --rwc-dimmed: {css_rgb(dimmed)};',
        f'  --rwc-muted: {css_rgb(muted)};',
        f'  --mantine-color-body: {css_rgb(background)} !important;',
        f'  --mantine-color-text: {css_rgb(text)} !important;',
        f'  --mantine-color-dimmed: {css_rgb(dimmed)} !important;',
        f'  --mantine-color-bright: {css_rgb(text)} !important;',
        f'  --mantine-color-placeholder: {css_rgb(muted)} !important;',
        '  --mantine-color-default: var(--mantine-color-dark-6) !important;',
        '  --mantine-color-default-hover: var(--rwc-surface-hover) !important;',
        '  --mantine-color-default-color: var(--rwc-text) !important;',
        '  --mantine-color-default-border: var(--mantine-color-dark-4) !important;',
        '  --mantine-color-anchor: var(--rwc-accent) !important;',
        '  --mantine-color-gray-outline-hover: var(--rwc-surface-hover) !important;',
        '  --mantine-color-cyan-outline: var(--rwc-accent) !important;',
    ]

    # Remnawave's decorative accent is not consistently named: some components
    # use cyan, some blue and some indigo. Bridge those three palettes to the
    # selected accent while leaving semantic red/green/orange/teal colors alone.
    for palette in ('cyan', 'blue', 'indigo'):
        for i, value in enumerate(accents):
            lines.append(f'  --mantine-color-{palette}-{i}: {css_rgb(value)} !important;')

    for i, value in enumerate(darks):
        lines.append(f'  --mantine-color-dark-{i}: {css_rgb(value)} !important;')

    lines += [
        '  --mantine-primary-color-filled: var(--mantine-color-cyan-8) !important;',
        '  --mantine-primary-color-filled-hover: var(--mantine-color-cyan-9) !important;',
        '  --mantine-primary-color-light: rgba(var(--rwc-accent-rgb), 0.14) !important;',
        '  --mantine-primary-color-light-hover: rgba(var(--rwc-accent-rgb), 0.20) !important;',
        '  --mantine-primary-color-light-color: var(--mantine-color-cyan-4) !important;',
        f'  --mantine-radius-xs: {max(0, radius - 6)}px !important;',
        f'  --mantine-radius-sm: {max(0, radius - 3)}px !important;',
        f'  --mantine-radius-md: {radius}px !important;',
        f'  --mantine-radius-lg: {radius + 4}px !important;',
        f'  --mantine-radius-xl: {radius + 8}px !important;',
        f'  --mantine-radius-default: {radius}px !important;',
        '}',
        '',
        '/* Page canvas. Remove top-level outlines/shadows that become visible on',
        '   strongly tinted themes even though stock Remnawave hides them. */',
        'html, body, #root, .mantine-AppShell-root, .mantine-AppShell-main {',
        '  background-color: var(--rwc-background) !important;',
        '  border: 0 !important;',
        '  outline: 0 !important;',
        '}',
        '.mantine-AppShell-root { box-shadow: none !important; }',
        '.mantine-AppShell-header { border-top: 0 !important; }',
        '',
        '/* Sidebar ambient glow follows the selected accent instead of the stock',
        '   hard-coded cyan/indigo glow. Keep it subtle to avoid a colored fog. */',
        '.mantine-AppShell-navbar::before {',
        '  background: radial-gradient(circle at 20% 20%, rgba(var(--rwc-accent-rgb), 0.065) 0%, transparent 52%) !important;',
        '}',
        '',
        '/* Mantine NavigationProgress shares Progress track styles. With a custom',
        '   dark palette its transparent top track can become visible as a 2-3px',
        '   line. Force only the navigation progress track itself transparent. */',
        '.mantine-Progress-root[style*="--nprogress-z-index"] {',
        '  background: transparent !important;',
        '  border: 0 !important;',
        '  box-shadow: none !important;',
        '}',
        '.mantine-Progress-root[style*="--nprogress-z-index"]:not([data-mounted]) {',
        '  opacity: 0 !important;',
        '}',
        '.mantine-Progress-root[style*="--nprogress-z-index"] .mantine-Progress-section::before {',
        '  box-shadow: 0 0 8px rgba(var(--rwc-accent-rgb), 0.42), 0 0 4px rgba(var(--rwc-accent-rgb), 0.24) !important;',
        '}',
        '',
        '/* Inline legacy surfaces from a handful of React components. */',
        '[style*="#1b1f26" i], [style*="rgb(27, 31, 38)" i] {',
        '  background-color: var(--rwc-surface) !important;',
        '}',
        '[style*="#161b23" i], [style*="rgb(22, 27, 35)" i] {',
        '  background-color: var(--rwc-surface-deep) !important;',
        '}',
        '',
        '/* Some Remnawave components hard-code indigo/cyan decoration in inline',
        '   styles instead of theme variables. Normalize only background/border',
        '   properties; text/status colors are intentionally left semantic. */',
        '[style*="background: rgba(99, 102, 241"], [style*="background-color: rgba(99, 102, 241"],',
        '[style*="background: rgba(6, 182, 212"], [style*="background-color: rgba(6, 182, 212"] {',
        '  background-color: rgba(var(--rwc-accent-rgb), 0.08) !important;',
        '}',
        '[style*="border: 1px solid rgba(99, 102, 241"], [style*="border-color: rgba(99, 102, 241"],',
        '[style*="border: 1px solid rgba(6, 182, 212"], [style*="border-color: rgba(6, 182, 212"] {',
        '  border-color: rgba(var(--rwc-accent-rgb), 0.20) !important;',
        '}',
        '',
        '/* Scrollbars should not keep Remnawave cyan/teal when another accent is selected. */',
        '::-webkit-scrollbar-track, ::-webkit-scrollbar-corner {',
        '  background: var(--rwc-background) !important;',
        '}',
        '::-webkit-scrollbar-thumb {',
        '  background: var(--rwc-accent) !important;',
        '  border-color: var(--rwc-background) !important;',
        '}',
        '* { scrollbar-color: var(--rwc-accent) var(--rwc-background); }',
        '::selection {',
        '  background: rgba(var(--rwc-accent-rgb), 0.24) !important;',
        '  color: var(--rwc-text) !important;',
        '}',
        '',
    ]
    return '\n'.join(lines)


def preset_by_key(key: str) -> ThemePreset | None:
    return next((p for p in PRESETS if p.key == key), None)


def theme_from_preset(preset: ThemePreset) -> dict:
    return {
        'preset': preset.key,
        'enabled': True,
        'accent': list(preset.accent),
        'background': list(preset.background),
        'surface': list(preset.surface),
        'radius': preset.radius,
    }
