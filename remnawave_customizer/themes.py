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


def css_rgb_csv(c: RGB) -> str:
    return f'{c[0]}, {c[1]}, {c[2]}'


def accent_scale(accent: RGB) -> list[RGB]:
    # Remnawave uses cyan shades directly in many components, therefore the
    # whole cyan scale follows the selected accent instead of just buttons.
    return [
        mix(accent, (255, 255, 255), 0.92),
        mix(accent, (255, 255, 255), 0.82),
        mix(accent, (255, 255, 255), 0.68),
        mix(accent, (255, 255, 255), 0.50),
        mix(accent, (255, 255, 255), 0.30),
        mix(accent, (255, 255, 255), 0.14),
        accent,
        darken(accent, 0.10),
        darken(accent, 0.20),
        darken(accent, 0.32),
    ]


def dark_scale(background: RGB, surface: RGB) -> list[RGB]:
    # dark.0..4 are frequently used for text and borders, while dark.5..9 are
    # structural surfaces. Keeping the text side neutral prevents a selected
    # green/purple card color from tinting every label in the Panel.
    border = lighten(surface, 0.18)
    border_soft = lighten(surface, 0.10)
    return [
        (235, 238, 243),
        (205, 210, 218),
        (169, 176, 187),
        (132, 140, 152),
        border,
        border_soft,
        surface,
        mix(surface, background, 0.46),
        background,
        darken(background, 0.20),
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
    dimmed = (160, 168, 180)
    muted = (116, 126, 140)
    surface_deep = mix(surface, background, 0.48)
    surface_raised = lighten(surface, 0.035)
    surface_hover = lighten(surface, 0.075)
    surface_active = mix(surface, accent, 0.10)
    input_bg = mix(surface, background, 0.30)
    border = lighten(surface, 0.16)
    border_strong = lighten(surface, 0.24)

    lines = [
        '/* Generated by Remnawave Customizer. Do not edit manually. */',
        ':root, [data-mantine-color-scheme="dark"] {',
        f'  --rwc-background: {css_rgb(background)};',
        f'  --rwc-surface: {css_rgb(surface)};',
        f'  --rwc-surface-deep: {css_rgb(surface_deep)};',
        f'  --rwc-surface-raised: {css_rgb(surface_raised)};',
        f'  --rwc-surface-hover: {css_rgb(surface_hover)};',
        f'  --rwc-surface-active: {css_rgb(surface_active)};',
        f'  --rwc-input: {css_rgb(input_bg)};',
        f'  --rwc-border: {css_rgb(border)};',
        f'  --rwc-border-strong: {css_rgb(border_strong)};',
        f'  --rwc-accent: {css_rgb(accent)};',
        f'  --rwc-accent-rgb: {css_rgb_csv(accent)};',
        f'  --rwc-accent-soft-rgb: {css_rgb_csv(accents[4])};',
        f'  --rwc-text: {css_rgb(text)};',
        f'  --rwc-dimmed: {css_rgb(dimmed)};',
        f'  --rwc-muted: {css_rgb(muted)};',
        f'  --mantine-color-body: {css_rgb(background)} !important;',
        f'  --mantine-color-text: {css_rgb(text)} !important;',
        f'  --mantine-color-dimmed: {css_rgb(dimmed)} !important;',
        f'  --mantine-color-bright: {css_rgb(text)} !important;',
        f'  --mantine-color-placeholder: {css_rgb(muted)} !important;',
        '  --mantine-color-default: var(--rwc-surface) !important;',
        '  --mantine-color-default-hover: var(--rwc-surface-hover) !important;',
        '  --mantine-color-default-color: var(--rwc-text) !important;',
        '  --mantine-color-default-border: var(--rwc-border) !important;',
        '  --mantine-color-anchor: var(--rwc-accent) !important;',
    ]

    for i, value in enumerate(accents):
        lines.append(f'  --mantine-color-cyan-{i}: {css_rgb(value)} !important;')
    for i, value in enumerate(darks):
        lines.append(f'  --mantine-color-dark-{i}: {css_rgb(value)} !important;')

    lines += [
        '  --mantine-primary-color-filled: var(--mantine-color-cyan-8) !important;',
        '  --mantine-primary-color-filled-hover: var(--mantine-color-cyan-9) !important;',
        '  --mantine-primary-color-light: rgba(var(--rwc-accent-rgb), 0.16) !important;',
        '  --mantine-primary-color-light-hover: rgba(var(--rwc-accent-rgb), 0.23) !important;',
        '  --mantine-primary-color-light-color: var(--mantine-color-cyan-3) !important;',
        f'  --mantine-radius-xs: {max(0, radius - 6)}px !important;',
        f'  --mantine-radius-sm: {max(0, radius - 3)}px !important;',
        f'  --mantine-radius-md: {radius}px !important;',
        f'  --mantine-radius-lg: {radius + 4}px !important;',
        f'  --mantine-radius-xl: {radius + 8}px !important;',
        f'  --mantine-radius-default: {radius}px !important;',
        '}',
        '',
        'html, body, #root, .mantine-AppShell-root, .mantine-AppShell-main {',
        '  background-color: var(--rwc-background) !important;',
        '  color: var(--rwc-text) !important;',
        '}',
        '',
        '/* App chrome */',
        '.mantine-AppShell-navbar, .mantine-AppShell-header {',
        '  background-color: var(--rwc-surface-deep) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '',
        '/* Cards: explicit semantic backgrounds from Remnawave are preserved. */',
        '.mantine-Card-root:not([style*="background" i]) {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-Paper-root[data-with-border]:not([style*="background" i]) {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '',
        '/* Modals and drawers must not keep the original navy surface. */',
        '.mantine-Modal-content, .mantine-Drawer-content {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-Modal-header, .mantine-Drawer-header {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-Modal-body, .mantine-Drawer-body {',
        '  background-color: var(--rwc-surface) !important;',
        '}',
        '',
        '/* Floating surfaces */',
        '.mantine-Popover-dropdown, .mantine-Menu-dropdown, .mantine-Combobox-dropdown,',
        '.mantine-Select-dropdown, .mantine-MultiSelect-dropdown, .mantine-Autocomplete-dropdown,',
        '.mantine-DatePicker-dropdown {',
        '  background-color: var(--rwc-surface-raised) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '',
        '/* Form controls */',
        ':where(.mantine-Input-input, .mantine-Textarea-input, .mantine-Select-input,',
        '.mantine-MultiSelect-input, .mantine-NumberInput-input, .mantine-DateInput-input,',
        '.mantine-PillsInput-input, .mantine-PasswordInput-innerInput) {',
        '  background-color: var(--rwc-input) !important;',
        '  border-color: var(--rwc-border) !important;',
        '  color: var(--rwc-text) !important;',
        '}',
        ':where(.mantine-Input-input, .mantine-Textarea-input, .mantine-Select-input,',
        '.mantine-MultiSelect-input, .mantine-NumberInput-input, .mantine-DateInput-input,',
        '.mantine-PillsInput-input):focus,',
        ':where(.mantine-Input-input, .mantine-Textarea-input, .mantine-Select-input,',
        '.mantine-MultiSelect-input, .mantine-NumberInput-input, .mantine-DateInput-input,',
        '.mantine-PillsInput-input):focus-within {',
        '  border-color: var(--rwc-accent) !important;',
        '  box-shadow: 0 0 0 1px rgba(var(--rwc-accent-rgb), 0.20) !important;',
        '}',
        '.mantine-Fieldset-root {',
        '  background-color: var(--rwc-surface) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '',
        '/* Common interactive surfaces */',
        '.mantine-SegmentedControl-root {',
        '  background-color: var(--rwc-input) !important;',
        '  border-color: var(--rwc-border) !important;',
        '}',
        '.mantine-SegmentedControl-indicator { background-color: var(--rwc-surface-hover) !important; }',
        '.mantine-Accordion-item { border-color: var(--rwc-border) !important; }',
        '.mantine-Tabs-list { border-color: var(--rwc-border) !important; }',
        '.mantine-Table-table { --table-border-color: var(--rwc-border) !important; }',
        '.mantine-Table-tr:hover, .mantine-Menu-item:hover, .mantine-Combobox-option:hover {',
        '  background-color: var(--rwc-surface-hover) !important;',
        '}',
        '',
        '/* Remnawave has a few inline legacy surface colors. */',
        '[style*="#1b1f26" i], [style*="rgb(27, 31, 38)" i] {',
        '  background-color: var(--rwc-surface) !important;',
        '}',
        '[style*="#161b23" i], [style*="rgb(22, 27, 35)" i] {',
        '  background-color: var(--rwc-surface-deep) !important;',
        '}',
        '',
        '::-webkit-scrollbar-thumb {',
        '  background: linear-gradient(180deg, var(--mantine-color-cyan-7), var(--rwc-accent)) !important;',
        '  border-color: var(--rwc-surface-deep) !important;',
        '}',
        '::selection {',
        '  background: rgba(var(--rwc-accent-rgb), 0.28) !important;',
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
