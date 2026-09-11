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


PRESETS: tuple[ThemePreset, ...] = (
    ThemePreset('midnight', 'Midnight Blue', 'Midnight Blue', (0, 169, 255), (7, 12, 19), (13, 21, 31), 'medium'),
    ThemePreset('oled', 'OLED Black', 'OLED Black', (0, 210, 255), (0, 0, 0), (9, 10, 12), 'medium'),
    ThemePreset('graphite', 'Graphite', 'Graphite', (122, 162, 247), (15, 17, 21), (25, 28, 34), 'small'),
    ThemePreset('nord', 'Nord', 'Nord', (136, 192, 208), (36, 41, 51), (46, 52, 64), 'medium'),
    ThemePreset('purple', 'Purple Dark', 'Purple Dark', (168, 123, 255), (13, 10, 22), (25, 19, 39), 'large'),
    ThemePreset('emerald', 'Emerald', 'Emerald', (52, 211, 153), (6, 16, 14), (13, 29, 25), 'medium'),
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


def accent_scale(accent: RGB) -> list[RGB]:
    # Mantine palettes are ordered light -> dark.
    return [
        mix(accent, (255, 255, 255), 0.90),
        mix(accent, (255, 255, 255), 0.78),
        mix(accent, (255, 255, 255), 0.62),
        mix(accent, (255, 255, 255), 0.42),
        mix(accent, (255, 255, 255), 0.20),
        accent,
        darken(accent, 0.10),
        darken(accent, 0.22),
        darken(accent, 0.34),
        darken(accent, 0.46),
    ]


def dark_scale(background: RGB, surface: RGB) -> list[RGB]:
    # Mantine dark palette is ordered light text-ish -> deepest dark.
    return [
        lighten(surface, 0.72),
        lighten(surface, 0.58),
        lighten(surface, 0.42),
        lighten(surface, 0.28),
        lighten(surface, 0.16),
        lighten(surface, 0.08),
        surface,
        mix(surface, background, 0.45),
        background,
        darken(background, 0.22),
    ]


def render_css(theme: dict) -> str:
    accent = rgb(theme['accent'])
    background = rgb(theme['background'])
    surface = rgb(theme['surface'])
    radius_key = str(theme.get('radius', 'medium'))
    radius = RADIUS_VALUES.get(radius_key, 10)
    accents = accent_scale(accent)
    darks = dark_scale(background, surface)
    border = lighten(surface, 0.13)
    surface_hover = lighten(surface, 0.07)

    lines = [
        '/* Generated by Remnawave Customizer. Do not edit manually. */',
        ':root {',
        f'  --rwc-background: {css_rgb(background)};',
        f'  --rwc-surface: {css_rgb(surface)};',
        f'  --rwc-surface-hover: {css_rgb(surface_hover)};',
        f'  --rwc-border: {css_rgb(border)};',
        f'  --rwc-accent: {css_rgb(accent)};',
        f'  --mantine-color-body: {css_rgb(background)} !important;',
    ]
    for i, value in enumerate(accents):
        lines.append(f'  --mantine-color-cyan-{i}: {css_rgb(value)} !important;')
    for i, value in enumerate(darks):
        lines.append(f'  --mantine-color-dark-{i}: {css_rgb(value)} !important;')
    lines += [
        f'  --mantine-primary-color-filled: {css_rgb(accents[6])} !important;',
        f'  --mantine-primary-color-filled-hover: {css_rgb(accents[7])} !important;',
        f'  --mantine-primary-color-light: color-mix(in srgb, {css_rgb(accent)} 16%, transparent) !important;',
        f'  --mantine-primary-color-light-hover: color-mix(in srgb, {css_rgb(accent)} 23%, transparent) !important;',
        f'  --mantine-primary-color-light-color: {css_rgb(accents[3])} !important;',
        f'  --mantine-radius-xs: {max(0, radius - 6)}px !important;',
        f'  --mantine-radius-sm: {max(0, radius - 3)}px !important;',
        f'  --mantine-radius-md: {radius}px !important;',
        f'  --mantine-radius-lg: {radius + 4}px !important;',
        f'  --mantine-radius-xl: {radius + 8}px !important;',
        f'  --mantine-radius-default: {radius}px !important;',
        '}',
        '',
        'html, body, #root { background-color: var(--rwc-background) !important; }',
        '.mantine-AppShell-main { background-color: var(--rwc-background) !important; }',
        '.mantine-Paper-root, .mantine-Card-root, .mantine-Modal-content, .mantine-Drawer-content,',
        '.mantine-Popover-dropdown, .mantine-Menu-dropdown, .mantine-Combobox-dropdown {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-Input-input, .mantine-Textarea-input, .mantine-Select-input, .mantine-MultiSelect-input {',
        '  background-color: color-mix(in srgb, var(--rwc-surface) 88%, black) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-Table-tr:hover, .mantine-Menu-item:hover, .mantine-Combobox-option:hover {',
        '  background-color: var(--rwc-surface-hover) !important;',
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
