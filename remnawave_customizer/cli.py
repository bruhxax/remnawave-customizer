from __future__ import annotations

import argparse
import copy
import shutil
import sys
import time
from pathlib import Path

from . import __version__
from . import ui
from .config import CONFIG_FILE, RUNTIME_DIR, load_config, save_config
from .palette import choose_color
from .proxy import (
    CUSTOM_TARGET,
    PANEL_TARGET,
    apply_theme,
    detect_proxy,
    ensure_installed,
    injector_status,
    panel_is_here,
    proxy_from_config,
    restore_proxy,
    start_injector,
    stop_injector,
    write_empty_theme,
)
from .themes import (
    ACCENT_COLORS,
    BACKGROUND_COLORS,
    PRESETS,
    RADIUS_LABELS,
    RADIUS_VALUES,
    SURFACE_COLORS,
    preset_by_key,
    rgb,
    theme_from_preset,
)
from .utils import CommandError, require_root, run

TEXT = {
    'ru': {
        'subtitle': 'Темы и внешний вид Remnawave Panel  ·  by bruhxax',
        'menu': 'Главное меню',
        'presets': 'Готовые темы',
        'accent': 'Цвет акцента',
        'background': 'Цвет фона',
        'surface': 'Цвет карточек и поверхностей',
        'radius': 'Скругление элементов',
        'preview': 'Предпросмотр',
        'apply': 'Применить изменения',
        'reset': 'Вернуть стандартный вид',
        'settings': 'Настройки',
        'exit': 'Выход',
        'choose': 'Выберите пункт',
        'status': 'Система',
        'panel': 'Panel',
        'proxy': 'Reverse proxy',
        'injector': 'Customizer',
        'theme': 'Тема',
        'online': 'активен',
        'offline': 'не активен',
        'detected': 'найдена',
        'not_found': 'не найдена',
        'custom': 'Custom',
        'saved': 'Выбрано. Нажмите «Применить изменения», чтобы обновить Panel.',
        'applied': 'Тема применена. Обновите страницу Panel в браузере.',
        'reset_done': 'Стандартный вид восстановлен. Обновите страницу Panel.',
        'setup_title': 'Первоначальная настройка',
        'setup_only_panel': 'Customizer должен устанавливаться исключительно на сервере, где находится Remnawave Panel.',
        'setup_proxy': 'Найден reverse proxy: {name}',
        'setup_safe': 'Panel, база данных и официальный frontend не изменяются. Customizer работает отдельным CSS-слоем перед Panel.',
        'setup_confirm': 'Подключить Customizer к Panel?',
        'setup_done': 'Настройка завершена',
        'unsupported': 'Не найден поддерживаемый reverse proxy. Поддерживаются официальные Nginx, Caddy, Angie и Traefik.',
        'language': 'Язык',
        'back': 'Назад',
        'press_enter': 'Нажмите Enter, чтобы продолжить',
        'radius_title': 'Выберите скругление',
        'preview_title': 'Предпросмотр темы',
        'current': 'Текущие настройки',
        'select_theme': 'Выберите тему',
        'apply_confirm': 'Применить эту тему?',
        'reset_confirm': 'Вернуть стандартный внешний вид Remnawave?',
        'settings_title': 'Настройки',
        'change_language': 'Изменить язык',
        'repair': 'Проверить / восстановить подключение Customizer',
        'repair_done': 'Подключение Customizer проверено',
    },
    'en': {
        'subtitle': 'Themes and appearance for Remnawave Panel  ·  by bruhxax',
        'menu': 'Main menu',
        'presets': 'Theme presets',
        'accent': 'Accent color',
        'background': 'Background color',
        'surface': 'Cards and surfaces color',
        'radius': 'Element rounding',
        'preview': 'Preview',
        'apply': 'Apply changes',
        'reset': 'Restore default look',
        'settings': 'Settings',
        'exit': 'Exit',
        'choose': 'Choose an option',
        'status': 'System',
        'panel': 'Panel',
        'proxy': 'Reverse proxy',
        'injector': 'Customizer',
        'theme': 'Theme',
        'online': 'active',
        'offline': 'inactive',
        'detected': 'detected',
        'not_found': 'not found',
        'custom': 'Custom',
        'saved': 'Selected. Choose “Apply changes” to update Panel appearance.',
        'applied': 'Theme applied. Refresh the Panel page in your browser.',
        'reset_done': 'Default appearance restored. Refresh the Panel page.',
        'setup_title': 'Initial setup',
        'setup_only_panel': 'Customizer must be installed only on the server where Remnawave Panel is installed.',
        'setup_proxy': 'Reverse proxy detected: {name}',
        'setup_safe': 'Panel, database and the official frontend are not modified. Customizer works as a separate CSS layer in front of Panel.',
        'setup_confirm': 'Connect Customizer to Panel?',
        'setup_done': 'Setup complete',
        'unsupported': 'Supported reverse proxy was not found. Official Nginx, Caddy, Angie and Traefik layouts are supported.',
        'language': 'Language',
        'back': 'Back',
        'press_enter': 'Press Enter to continue',
        'radius_title': 'Choose element rounding',
        'preview_title': 'Theme preview',
        'current': 'Current settings',
        'select_theme': 'Choose a theme',
        'apply_confirm': 'Apply this theme?',
        'reset_confirm': 'Restore the default Remnawave appearance?',
        'settings_title': 'Settings',
        'change_language': 'Change language',
        'repair': 'Check / repair Customizer connection',
        'repair_done': 'Customizer connection checked',
    },
}


def tr(lang: str, key: str, **kwargs) -> str:
    value = TEXT.get(lang, TEXT['en']).get(key, key)
    return value.format(**kwargs) if kwargs else value


def header(lang: str) -> None:
    ui.header('🎨 Remnawave Customizer', tr(lang, 'subtitle'), badge=f'v{__version__}')


def select_language(current: str | None = None) -> str:
    ui.clear()
    ui.header('Language / Язык', 'Remnawave Customizer  ·  by bruhxax')
    ui.menu(['🇷🇺 Русский', '🇬🇧 English'])
    default = '2' if current == 'en' else '1'
    return 'en' if ui.choose('>', ['1', '2'], default) == '2' else 'ru'


def _theme_name(config: dict, lang: str) -> str:
    if not bool(config.get('theme', {}).get('enabled', True)):
        return 'Default'
    preset = preset_by_key(str(config.get('theme', {}).get('preset', '')))
    if preset:
        return preset.name_ru if lang == 'ru' else preset.name_en
    return tr(lang, 'custom')


def _status_card(config: dict, lang: str) -> None:
    panel_ok, _ = panel_is_here()
    proxy = proxy_from_config(config) or detect_proxy()
    injector = injector_status()
    lines = [
        f"{ui.green('●') if panel_ok else ui.red('●')} {tr(lang, 'panel'):<15} {tr(lang, 'detected') if panel_ok else tr(lang, 'not_found')}",
        f"{ui.green('●') if proxy else ui.red('●')} {tr(lang, 'proxy'):<15} {proxy.name if proxy else tr(lang, 'not_found')}",
        f"{ui.green('●') if injector else ui.yellow('●')} {tr(lang, 'injector'):<15} {tr(lang, 'online') if injector else tr(lang, 'offline')}",
        f"{ui.primary('◆')} {tr(lang, 'theme'):<15} {_theme_name(config, lang)}",
    ]
    ui.card(tr(lang, 'status'), lines)


def _set_custom(config: dict, field: str, value) -> None:
    config['theme'][field] = list(value) if isinstance(value, tuple) else value
    config['theme']['preset'] = 'custom'
    config['theme']['enabled'] = True
    save_config(config)


def choose_preset(config: dict, lang: str) -> None:
    ui.clear(); header(lang); ui.heading(tr(lang, 'select_theme'))
    labels = [p.name_ru if lang == 'ru' else p.name_en for p in PRESETS] + [tr(lang, 'back')]
    ui.menu(labels)
    choice = ui.choose(tr(lang, 'choose'), [str(i) for i in range(1, len(labels) + 1)], '1')
    if int(choice) == len(labels):
        return
    preset = PRESETS[int(choice) - 1]
    config['theme'] = theme_from_preset(preset)
    save_config(config)
    ui.ok(tr(lang, 'saved'))
    time.sleep(0.7)


def choose_palette_field(config: dict, lang: str, field: str) -> None:
    if field == 'accent':
        colors, title = ACCENT_COLORS, tr(lang, 'accent')
    elif field == 'background':
        colors, title = BACKGROUND_COLORS, tr(lang, 'background')
    else:
        colors, title = SURFACE_COLORS, tr(lang, 'surface')
    current = rgb(config['theme'][field])
    selected = choose_color(colors, title, current=current, columns=8)
    if selected is not None:
        _set_custom(config, field, selected)
        ui.ok(tr(lang, 'saved'))
        time.sleep(0.6)


def choose_radius(config: dict, lang: str) -> None:
    ui.clear(); header(lang); ui.heading(tr(lang, 'radius_title'))
    keys = list(RADIUS_VALUES)
    labels = [RADIUS_LABELS[lang][key] for key in keys] + [tr(lang, 'back')]
    ui.menu(labels)
    current = str(config['theme'].get('radius', 'medium'))
    default = str(keys.index(current) + 1) if current in keys else '3'
    choice = ui.choose(tr(lang, 'choose'), [str(i) for i in range(1, len(labels) + 1)], default)
    if int(choice) == len(labels):
        return
    _set_custom(config, 'radius', keys[int(choice) - 1])
    ui.ok(tr(lang, 'saved'))
    time.sleep(0.6)


def preview(config: dict, lang: str) -> None:
    ui.clear(); header(lang); ui.heading(tr(lang, 'preview_title'))
    theme = config['theme']
    accent = rgb(theme['accent']); bg = rgb(theme['background']); surface = rgb(theme['surface'])
    radius_label = RADIUS_LABELS[lang].get(str(theme.get('radius')), str(theme.get('radius')))
    ui.card(tr(lang, 'current'), [
        f"{tr(lang, 'theme')}: {_theme_name(config, lang)}",
        f"{tr(lang, 'accent')}:      {ui.swatch(accent, 8)}",
        f"{tr(lang, 'background')}:  {ui.swatch(bg, 8)}",
        f"{tr(lang, 'surface')}:     {ui.swatch(surface, 8)}",
        f"{tr(lang, 'radius')}:      {radius_label}",
    ])
    print()
    # Terminal-only visual sample.
    bar = ui.swatch(accent, 18)
    card = ui.swatch(surface, 18)
    background = ui.swatch(bg, 18)
    print(f"  {background}  background")
    print(f"  {card}  cards")
    print(f"  {bar}  accent")
    ui.pause(tr(lang, 'press_enter'))


def apply_current(config: dict, lang: str) -> None:
    ui.clear(); header(lang); preview_inline(config, lang)
    if not ui.confirm(tr(lang, 'apply_confirm'), default=True):
        return
    spinner = ui.Spinner('Применяю тему...' if lang == 'ru' else 'Applying theme...').start()
    try:
        apply_theme(config)
        spinner.stop(True, tr(lang, 'applied'))
    except Exception as exc:
        spinner.stop(False, str(exc))
    ui.pause(tr(lang, 'press_enter'))


def preview_inline(config: dict, lang: str) -> None:
    theme = config['theme']
    ui.card(tr(lang, 'current'), [
        f"{tr(lang, 'theme')}: {_theme_name(config, lang)}",
        f"{tr(lang, 'accent')}:     {ui.swatch(rgb(theme['accent']), 7)}",
        f"{tr(lang, 'background')}: {ui.swatch(rgb(theme['background']), 7)}",
        f"{tr(lang, 'surface')}:    {ui.swatch(rgb(theme['surface']), 7)}",
        f"{tr(lang, 'radius')}:     {RADIUS_LABELS[lang].get(str(theme.get('radius')), '')}",
    ])


def reset_default(config: dict, lang: str) -> None:
    ui.clear(); header(lang); ui.heading(tr(lang, 'reset'))
    if not ui.confirm(tr(lang, 'reset_confirm'), default=False):
        return
    try:
        write_empty_theme()
        if not injector_status():
            start_injector()
        config['theme']['preset'] = 'default'
        config['theme']['enabled'] = False
        save_config(config)
        ui.ok(tr(lang, 'reset_done'))
    except Exception as exc:
        ui.error(str(exc))
    ui.pause(tr(lang, 'press_enter'))


def setup(config: dict | None = None) -> dict:
    config = config or load_config()
    lang = select_language(config.get('language'))
    config['language'] = lang
    save_config(config)
    ui.clear(); header(lang); ui.heading(tr(lang, 'setup_title'))
    ui.warn(tr(lang, 'setup_only_panel'))
    ok, reason = panel_is_here()
    if not ok:
        ui.error(reason)
        raise SystemExit(1)
    proxy = detect_proxy()
    if not proxy:
        ui.error(tr(lang, 'unsupported'))
        raise SystemExit(1)
    ui.ok(tr(lang, 'setup_proxy', name=proxy.name))
    ui.info(tr(lang, 'setup_safe'))
    if not ui.confirm(tr(lang, 'setup_confirm'), default=True):
        raise SystemExit(0)
    spinner = ui.Spinner('Подключаю Customizer...' if lang == 'ru' else 'Connecting Customizer...').start()
    try:
        info = ensure_installed(config)
        config['configured'] = True
        config['proxy']['name'] = info.name
        save_config(config)
        spinner.stop(True, tr(lang, 'setup_done'))
    except Exception as exc:
        spinner.stop(False, str(exc))
        raise SystemExit(1)
    time.sleep(0.7)
    return config


def settings(config: dict, lang: str) -> str:
    while True:
        ui.clear(); header(lang); ui.heading(tr(lang, 'settings_title'))
        ui.menu([tr(lang, 'change_language'), tr(lang, 'repair'), tr(lang, 'back')])
        choice = ui.choose(tr(lang, 'choose'), ['1', '2', '3'], '3')
        if choice == '1':
            lang = select_language(lang)
            config['language'] = lang
            save_config(config)
        elif choice == '2':
            spinner = ui.Spinner('Проверяю...' if lang == 'ru' else 'Checking...').start()
            try:
                ensure_installed(config)
                config['configured'] = True
                save_config(config)
                spinner.stop(True, tr(lang, 'repair_done'))
            except Exception as exc:
                spinner.stop(False, str(exc))
            ui.pause(tr(lang, 'press_enter'))
        else:
            return lang


def interactive(config: dict) -> None:
    lang = config.get('language', 'ru')
    while True:
        ui.clear(); header(lang); _status_card(config, lang); ui.heading(tr(lang, 'menu'))
        options = [
            tr(lang, 'presets'), tr(lang, 'accent'), tr(lang, 'background'), tr(lang, 'surface'),
            tr(lang, 'radius'), tr(lang, 'preview'), tr(lang, 'apply'), tr(lang, 'reset'),
            tr(lang, 'settings'), tr(lang, 'exit'),
        ]
        ui.menu(options)
        choice = ui.choose(tr(lang, 'choose'), [str(i) for i in range(1, 11)], '10')
        if choice == '1': choose_preset(config, lang)
        elif choice == '2': choose_palette_field(config, lang, 'accent')
        elif choice == '3': choose_palette_field(config, lang, 'background')
        elif choice == '4': choose_palette_field(config, lang, 'surface')
        elif choice == '5': choose_radius(config, lang)
        elif choice == '6': preview(config, lang)
        elif choice == '7': apply_current(config, lang)
        elif choice == '8': reset_default(config, lang)
        elif choice == '9':
            lang = settings(config, lang)
        else:
            ui.clear(); return


def status(config: dict, lang: str) -> int:
    ui.clear(); header(lang); _status_card(config, lang)
    proxy = proxy_from_config(config)
    if proxy and proxy.config_path.exists():
        text = proxy.config_path.read_text(encoding='utf-8', errors='replace')
        target_ok = CUSTOM_TARGET in text
        print()
        (ui.ok if target_ok else ui.warn)(f"Route: {'Customizer' if target_ok else 'Panel direct'}")
    return 0


def uninstall_integration(config: dict, lang: str) -> int:
    ui.clear(); header(lang)
    if not ui.confirm('Отключить Customizer от reverse proxy?' if lang == 'ru' else 'Disconnect Customizer from reverse proxy?', default=False):
        return 0
    try:
        restore_proxy(config)
        stop_injector(remove=True)
        config['configured'] = False
        save_config(config)
        ui.ok('Customizer отключен' if lang == 'ru' else 'Customizer disconnected')
        return 0
    except Exception as exc:
        ui.error(str(exc)); return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='customizer', description='Theme customizer for Remnawave Panel')
    p.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    sub = p.add_subparsers(dest='command')
    sub.add_parser('setup')
    sub.add_parser('apply')
    sub.add_parser('reset')
    sub.add_parser('status')
    sub.add_parser('disconnect')
    return p


def main() -> int:
    args = build_parser().parse_args()
    if not require_root():
        ui.error('Запустите через sudo / Run as root.')
        return 1
    config = load_config()
    if args.command == 'setup' or not config.get('configured'):
        config = setup(config)
        if args.command == 'setup':
            return 0
    lang = config.get('language', 'ru')
    if args.command == 'apply':
        try:
            apply_theme(config); ui.ok(tr(lang, 'applied')); return 0
        except Exception as exc:
            ui.error(str(exc)); return 1
    if args.command == 'reset':
        config['theme']['preset'] = 'default'
        config['theme']['enabled'] = False
        save_config(config)
        write_empty_theme(); ui.ok(tr(lang, 'reset_done')); return 0
    if args.command == 'status':
        return status(config, lang)
    if args.command == 'disconnect':
        return uninstall_integration(config, lang)
    interactive(config)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
