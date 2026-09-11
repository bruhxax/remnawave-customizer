from __future__ import annotations

import copy
import time

from . import cli_v2 as v2
from . import subpage, ui
from .config import load_config, save_config
from .palette import choose_color
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
from .utils import require_root

base = v2.base
_ORIGINAL_PANEL_APPLY = v2.apply_now


def _sub_name(config: dict, lang: str) -> str:
    data = subpage.ensure_config(config)
    if data.get('mode') == 'sync':
        return 'Как тема Panel' if lang == 'ru' else 'Synced with Panel'
    preset = preset_by_key(str(data.get('preset', '')))
    if preset:
        return preset.name_ru if lang == 'ru' else preset.name_en
    return 'Custom'


def _sub_status_card(config: dict, lang: str) -> None:
    ok, reason = subpage.local_status()
    data = subpage.ensure_config(config)
    enabled = bool(data.get('enabled'))
    mode = data.get('mode', 'custom')
    lines = [
        f"{ui.green('●') if ok else ui.red('●')} {'Локальный Sub Page' if lang == 'ru' else 'Local Sub Page':<20} "
        f"{('найден' if lang == 'ru' else 'detected') if ok else ('не найден' if lang == 'ru' else 'not found')}",
        f"{ui.green('●') if enabled else ui.dim('●')} {'Оформление' if lang == 'ru' else 'Appearance':<20} "
        f"{('активно' if lang == 'ru' else 'active') if enabled else ('стандартное' if lang == 'ru' else 'default')}",
        f"{ui.primary('◆')} {'Режим' if lang == 'ru' else 'Mode':<20} "
        f"{('синхронизация с Panel' if lang == 'ru' else 'sync with Panel') if mode == 'sync' else ('отдельная тема' if lang == 'ru' else 'independent theme')}",
        f"{ui.primary('◆')} {'Тема' if lang == 'ru' else 'Theme':<20} {_sub_name(config, lang)}",
    ]
    if not ok and reason:
        lines.append(f"{ui.yellow('!')} {'Причина' if lang == 'ru' else 'Reason':<20} {reason}")
    ui.card('Subscription Page', lines)


def _sub_apply(config: dict, lang: str) -> bool:
    spinner = ui.Spinner('Применяю оформление Sub Page...' if lang == 'ru' else 'Applying Sub Page appearance...').start()
    try:
        subpage.apply(config)
        spinner.stop(True, 'Sub Page обновлён' if lang == 'ru' else 'Sub Page updated')
        time.sleep(.55)
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def _sub_sync(config: dict, lang: str) -> bool:
    spinner = ui.Spinner('Синхронизирую с темой Panel...' if lang == 'ru' else 'Syncing with Panel theme...').start()
    try:
        subpage.sync_with_panel(config)
        panel_enabled = bool(config.get('theme', {}).get('enabled', True))
        if panel_enabled:
            text = 'Sub Page синхронизирован с Panel' if lang == 'ru' else 'Sub Page synced with Panel'
        else:
            text = 'Panel в стандартном виде — Sub Page тоже сброшен' if lang == 'ru' else 'Panel is stock — Sub Page restored to stock too'
        spinner.stop(True, text)
        time.sleep(.55)
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def _sub_reset(config: dict, lang: str) -> bool:
    spinner = ui.Spinner('Возвращаю стандартный Sub Page...' if lang == 'ru' else 'Restoring stock Sub Page...').start()
    try:
        subpage.reset(config)
        spinner.stop(True, 'Оригинальный Sub Page восстановлен' if lang == 'ru' else 'Original Sub Page restored')
        time.sleep(.55)
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def _sub_choose_preset(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    rows = []
    for index, preset in enumerate(PRESETS, 1):
        name = preset.name_ru if lang == 'ru' else preset.name_en
        rows.append(f"{ui.primary(f'{index:>2}')}  {ui.swatch(preset.accent, 3)}  {name}")
    rows.append(f"{ui.primary(' 0')}  ←  {base.tr(lang, 'back')}")
    ui.card('Готовые темы Sub Page' if lang == 'ru' else 'Sub Page presets', rows)
    choice = ui.choose(base.tr(lang, 'choose'), ['0'] + [str(i) for i in range(1, len(PRESETS) + 1)], '0')
    if choice == '0':
        return

    previous = copy.deepcopy(subpage.ensure_config(config))
    route = copy.deepcopy(previous.get('route') or {})
    selected = theme_from_preset(PRESETS[int(choice) - 1])
    data = subpage.ensure_config(config)
    data.update({
        'enabled': True,
        'mode': 'custom',
        'preset': selected['preset'],
        'accent': selected['accent'],
        'background': selected['background'],
        'surface': selected['surface'],
        'radius': selected['radius'],
        'route': route,
    })
    save_config(config)
    if not _sub_apply(config, lang):
        config['subpage'] = previous
        save_config(config)


def _sub_choose_color(config: dict, lang: str, field: str) -> None:
    if field == 'accent':
        colors = ACCENT_COLORS
        title = 'Акцент Sub Page' if lang == 'ru' else 'Sub Page accent'
    elif field == 'background':
        colors = BACKGROUND_COLORS
        title = 'Фон Sub Page' if lang == 'ru' else 'Sub Page background'
    else:
        colors = SURFACE_COLORS
        title = 'Карточки Sub Page' if lang == 'ru' else 'Sub Page surfaces'

    data = subpage.ensure_config(config)
    selected = choose_color(colors, title, current=rgb(data[field]), columns=8)
    if selected is None:
        return
    previous = copy.deepcopy(data)
    subpage.set_custom(config, field, selected)
    if not _sub_apply(config, lang):
        config['subpage'] = previous
        save_config(config)


def _sub_choose_radius(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    data = subpage.ensure_config(config)
    keys = list(RADIUS_VALUES)
    rows = [f"{ui.primary(str(i))}  {RADIUS_LABELS[lang][key]}" for i, key in enumerate(keys, 1)]
    rows.append(f"{ui.primary('0')}  ←  {base.tr(lang, 'back')}")
    ui.card('Скругление Sub Page' if lang == 'ru' else 'Sub Page rounding', rows)
    current = str(data.get('radius', 'medium'))
    default = str(keys.index(current) + 1) if current in keys else '3'
    choice = ui.choose(base.tr(lang, 'choose'), ['0'] + [str(i) for i in range(1, len(keys) + 1)], default)
    if choice == '0':
        return
    previous = copy.deepcopy(data)
    subpage.set_custom(config, 'radius', keys[int(choice) - 1])
    if not _sub_apply(config, lang):
        config['subpage'] = previous
        save_config(config)


def subpage_menu(config: dict, lang: str) -> None:
    while True:
        ui.clear(); base.header(lang); _sub_status_card(config, lang)
        ok, _ = subpage.local_status()
        if not ok:
            ui.warn(
                'Оформление Sub Page работает только когда Subscription Page запущен на этом же сервере, что и Panel.'
                if lang == 'ru' else
                'Sub Page appearance works only when Subscription Page is running on the same server as Panel.'
            )
            ui.card('Меню' if lang == 'ru' else 'Menu', [f"{ui.primary('0')}  ←  {base.tr(lang, 'back')}"])
            ui.choose(base.tr(lang, 'choose'), ['0'], '0')
            return

        rows = [
            f"{ui.primary('1')}  ⇄   {'Синхронизировать с темой Panel' if lang == 'ru' else 'Sync with Panel theme'}",
            f"{ui.primary('2')}  🎨  {'Готовые темы' if lang == 'ru' else 'Theme presets'}",
            f"{ui.primary('3')}  ◉   {'Цвет акцента' if lang == 'ru' else 'Accent color'}",
            f"{ui.primary('4')}  ▰   {'Цвет фона' if lang == 'ru' else 'Background color'}",
            f"{ui.primary('5')}  ▣   {'Цвет карточек и поверхностей' if lang == 'ru' else 'Cards and surfaces color'}",
            f"{ui.primary('6')}  ◯   {'Скругление элементов' if lang == 'ru' else 'Element rounding'}",
            f"{ui.primary('7')}  ↻   {'Применить оформление повторно' if lang == 'ru' else 'Reapply appearance'}",
            f"{ui.primary('8')}  ↩   {'Вернуть стандартный Sub Page' if lang == 'ru' else 'Restore stock Sub Page'}",
            f"{ui.primary('0')}  ←   {base.tr(lang, 'back')}",
        ]
        ui.card('Оформление Sub Page' if lang == 'ru' else 'Sub Page appearance', rows)
        choice = ui.choose(base.tr(lang, 'choose'), [str(i) for i in range(0, 9)], '0')
        if choice == '0':
            return
        if choice == '1':
            _sub_sync(config, lang)
        elif choice == '2':
            _sub_choose_preset(config, lang)
        elif choice == '3':
            _sub_choose_color(config, lang, 'accent')
        elif choice == '4':
            _sub_choose_color(config, lang, 'background')
        elif choice == '5':
            _sub_choose_color(config, lang, 'surface')
        elif choice == '6':
            _sub_choose_radius(config, lang)
        elif choice == '7':
            _sub_apply(config, lang)
        elif choice == '8':
            ui.clear(); base.header(lang)
            warning = (
                'Будет возвращён именно оригинальный внешний вид Subscription Page.'
                if lang == 'ru' else
                'This restores the exact original Subscription Page appearance.'
            )
            ui.warn(warning)
            if ui.confirm('Продолжить?' if lang == 'ru' else 'Continue?', default=False):
                _sub_reset(config, lang)


def apply_now(config: dict, lang: str) -> bool:
    ok = _ORIGINAL_PANEL_APPLY(config, lang)
    if not ok:
        return False
    data = subpage.ensure_config(config)
    if data.get('mode') == 'sync':
        try:
            subpage.sync_if_needed(config)
            if subpage.is_local():
                ui.info('Sub Page синхронизирован автоматически.' if lang == 'ru' else 'Sub Page synced automatically.')
        except Exception as exc:
            ui.warn(('Не удалось синхронизировать Sub Page: ' if lang == 'ru' else 'Could not sync Sub Page: ') + str(exc))
    return True


def _reset_panel(config: dict, lang: str) -> bool:
    spinner = ui.Spinner('Возвращаю оригинальный Remnawave...' if lang == 'ru' else 'Restoring original Remnawave...').start()
    try:
        from . import proxy

        proxy.restore_proxy(config)
        config['theme']['preset'] = 'default'
        config['theme']['enabled'] = False
        for key in v2.EFFECT_META:
            config['theme'].setdefault('effects', {})[key] = False
        save_config(config)

        data = subpage.ensure_config(config)
        if data.get('mode') == 'sync':
            subpage.reset(config, keep_sync=True)
        elif data.get('enabled'):
            # Custom Sub Page can keep using port 3101 while Panel itself goes
            # directly back to the original Remnawave container.
            proxy.write_empty_theme()
        else:
            proxy.stop_injector(remove=True)
        save_config(config)
        spinner.stop(True, base.tr(lang, 'reset_done'))
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def reset_panel(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    ui.warn('Будет восстановлен именно оригинальный внешний вид Remnawave Panel.' if lang == 'ru' else 'This restores the exact original Remnawave Panel appearance.')
    if ui.confirm(base.tr(lang, 'reset_confirm'), default=False):
        _reset_panel(config, lang)
        ui.pause(base.tr(lang, 'press_enter'))


def disconnect_all(config: dict, lang: str) -> int:
    ui.clear(); base.header(lang)
    prompt = 'Отключить Customizer от Panel и локального Sub Page?' if lang == 'ru' else 'Disconnect Customizer from Panel and local Sub Page?'
    if not ui.confirm(prompt, default=False):
        return 0
    try:
        from . import proxy

        subpage.restore_route(config)
        proxy.restore_proxy(config)
        proxy.stop_injector(remove=True)
        config['configured'] = False
        subpage.ensure_config(config)['enabled'] = False
        save_config(config)
        ui.ok('Customizer отключен' if lang == 'ru' else 'Customizer disconnected')
        return 0
    except Exception as exc:
        ui.error(str(exc))
        return 1


def interactive(config: dict) -> None:
    lang = config.get('language', 'ru')
    while True:
        ui.clear(); base.header(lang); base._status_card(config, lang)
        local, _ = subpage.local_status()
        sub_state = ('локальный найден' if lang == 'ru' else 'local detected') if local else ('не найден' if lang == 'ru' else 'not found')
        ui.info(f"Subscription Page: {sub_state}")
        rows = [
            f"{ui.primary('1')}  🎨  {base.tr(lang, 'presets')}",
            f"{ui.primary('2')}  ◉   {base.tr(lang, 'accent')}",
            f"{ui.primary('3')}  ▰   {base.tr(lang, 'background')}",
            f"{ui.primary('4')}  ▣   {base.tr(lang, 'surface')}",
            f"{ui.primary('5')}  ◯   {base.tr(lang, 'radius')}",
            f"{ui.primary('6')}  ✨  {base.tr(lang, 'effects')}",
            f"{ui.primary('7')}  ◈   {'Оформление Sub Page' if lang == 'ru' else 'Sub Page appearance'}",
            f"{ui.primary('8')}  👁   {base.tr(lang, 'preview')}",
            f"{ui.primary('9')}  ↻   {base.tr(lang, 'apply')}",
            f"{ui.primary('10')} ↩   {base.tr(lang, 'reset')}",
            f"{ui.primary('11')} ⚙   {base.tr(lang, 'settings')}",
            f"{ui.primary('0')}  ⏻   {base.tr(lang, 'exit')}",
        ]
        ui.card(base.tr(lang, 'menu'), rows)
        choice = ui.choose(base.tr(lang, 'choose'), [str(i) for i in range(0, 12)], '0')
        if choice == '0':
            ui.clear(); return
        if choice == '1': v2.choose_preset(config, lang)
        elif choice == '2': base.choose_palette_field(config, lang, 'accent')
        elif choice == '3': base.choose_palette_field(config, lang, 'background')
        elif choice == '4': base.choose_palette_field(config, lang, 'surface')
        elif choice == '5': v2.choose_radius(config, lang)
        elif choice == '6': v2.choose_effects(config, lang)
        elif choice == '7': subpage_menu(config, lang)
        elif choice == '8': base.preview(config, lang)
        elif choice == '9': base.apply_current(config, lang)
        elif choice == '10': reset_panel(config, lang)
        elif choice == '11': lang = v2.settings(config, lang)


def install_overrides() -> None:
    v2.install_overrides()
    v2.apply_now = apply_now
    base._apply_now = apply_now
    base.reset_default = reset_panel
    base.interactive = interactive


def main() -> int:
    install_overrides()
    args = base.build_parser().parse_args()
    if not require_root():
        ui.error('Запустите через sudo / Run as root.')
        return 1

    config = load_config()
    subpage.ensure_config(config)
    if args.command == 'setup' or not config.get('configured'):
        config = base.setup(config)
        if args.command == 'setup':
            return 0

    lang = config.get('language', 'ru')
    if args.command == 'apply':
        return 0 if apply_now(config, lang) else 1
    if args.command == 'reset':
        return 0 if _reset_panel(config, lang) else 1
    if args.command == 'status':
        result = base.status(config, lang)
        print()
        _sub_status_card(config, lang)
        return result
    if args.command == 'disconnect':
        return disconnect_all(config, lang)

    interactive(config)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
