from __future__ import annotations

import copy
import time

from . import cli as base
from . import ui
from .config import load_config, save_config
from .effects import EFFECT_KEYS
from .proxy import ensure_installed, restore_proxy, stop_injector
from .themes import PRESETS, RADIUS_LABELS, RADIUS_VALUES, rgb, theme_from_preset
from .utils import require_root


EFFECT_META = {
    'snow': ('❄', 'Падающие светящиеся точки', 'Falling glowing dots', 'снег', 'snow'),
    'particles': ('✦', 'Мерцающие частицы', 'Twinkling particles', 'частицы', 'particles'),
    'aurora': ('◌', 'Мягкая аура', 'Soft aurora', 'аура', 'aurora'),
    'orbs': ('●', 'Плавающие световые сферы', 'Floating glow orbs', 'сферы', 'orbs'),
    'sweep': ('╱', 'Мягкий световой блик', 'Soft light sweep', 'блик', 'sweep'),
}


def _rows(title: str, rows: list[str]) -> None:
    ui.card(title, rows)


def _state(value: bool, lang: str) -> str:
    if value:
        return ui.green('ВКЛ' if lang == 'ru' else 'ON')
    return ui.dim('ВЫКЛ' if lang == 'ru' else 'OFF')


def effects_summary(config: dict, lang: str) -> str:
    data = base._effects_data(config)
    active: list[str] = []
    for key in EFFECT_KEYS:
        if data.get(key):
            active.append(EFFECT_META[key][3 if lang == 'ru' else 4])
    return ' + '.join(active) if active else ('выключены' if lang == 'ru' else 'disabled')


def apply_now(config: dict, lang: str) -> bool:
    text = 'Применяю изменения...' if lang == 'ru' else 'Applying changes...'
    spinner = ui.Spinner(text).start()
    try:
        if bool(config.get('theme', {}).get('enabled', True)):
            info = ensure_installed(config)
            config['configured'] = True
            config.setdefault('proxy', {})['name'] = info.name
            save_config(config)
        else:
            # A disabled theme means truly stock Remnawave: bypass the Customizer
            # completely so none of our CSS rewriting can alter default colors.
            restore_proxy(config)
            stop_injector(remove=True)
            save_config(config)
        spinner.stop(True, base.tr(lang, 'applied'))
        time.sleep(.65)
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def choose_preset(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    rows = []
    for index, preset in enumerate(PRESETS, 1):
        name = preset.name_ru if lang == 'ru' else preset.name_en
        rows.append(f"{ui.primary(f'{index:>2}')}  {ui.swatch(preset.accent, 3)}  {name}")
    rows.append(f"{ui.primary(' 0')}  ←  {base.tr(lang, 'back')}")
    _rows(base.tr(lang, 'select_theme'), rows)
    allowed = ['0'] + [str(i) for i in range(1, len(PRESETS) + 1)]
    choice = ui.choose(base.tr(lang, 'choose'), allowed, '0')
    if choice == '0':
        return

    previous_theme = copy.deepcopy(config['theme'])
    previous_effects = copy.deepcopy(base._effects_data(config))
    config['theme'] = theme_from_preset(PRESETS[int(choice) - 1])
    config['theme']['effects'] = previous_effects
    save_config(config)
    if not apply_now(config, lang):
        base._restore_theme(config, previous_theme, lang)


def choose_radius(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    keys = list(RADIUS_VALUES)
    rows = [f"{ui.primary(str(i))}  {RADIUS_LABELS[lang][key]}" for i, key in enumerate(keys, 1)]
    rows.append(f"{ui.primary('0')}  ←  {base.tr(lang, 'back')}")
    _rows(base.tr(lang, 'radius_title'), rows)
    current = str(config['theme'].get('radius', 'medium'))
    default = str(keys.index(current) + 1) if current in keys else '3'
    choice = ui.choose(base.tr(lang, 'choose'), ['0'] + [str(i) for i in range(1, len(keys) + 1)], default)
    if choice == '0':
        return
    previous = copy.deepcopy(config['theme'])
    base._set_custom(config, 'radius', keys[int(choice) - 1])
    if not apply_now(config, lang):
        base._restore_theme(config, previous, lang)


def choose_effects(config: dict, lang: str) -> None:
    while True:
        data = base._effects_data(config)
        ui.clear(); base.header(lang)
        intro = (
            'Все эффекты полупрозрачные, не кликабельные и автоматически используют цвет текущей темы.'
            if lang == 'ru' else
            'All effects are translucent, click-through and automatically use the current theme accent.'
        )
        ui.info(intro)
        rows: list[str] = []
        for index, key in enumerate(EFFECT_KEYS, 1):
            icon, ru, en, _, _ = EFFECT_META[key]
            rows.append(f"{ui.primary(str(index))}  {icon}  {ru if lang == 'ru' else en:<31} [{_state(bool(data.get(key)), lang)}]")
        all_index = len(EFFECT_KEYS) + 1
        none_index = len(EFFECT_KEYS) + 2
        rows += [
            f"{ui.primary(str(all_index))}  ✨  {'Включить всё' if lang == 'ru' else 'Enable all'}",
            f"{ui.primary(str(none_index))}  ○   {'Выключить всё' if lang == 'ru' else 'Disable all'}",
            f"{ui.primary('0')}  ←   {base.tr(lang, 'back')}",
        ]
        _rows(base.tr(lang, 'effects_title'), rows)
        allowed = ['0'] + [str(i) for i in range(1, none_index + 1)]
        choice = ui.choose(base.tr(lang, 'choose'), allowed, '0')
        if choice == '0':
            return

        previous = copy.deepcopy(config['theme'])
        data = base._effects_data(config)
        selected = int(choice)
        if 1 <= selected <= len(EFFECT_KEYS):
            key = EFFECT_KEYS[selected - 1]
            data[key] = not bool(data.get(key))
        elif selected == all_index:
            for key in EFFECT_KEYS:
                data[key] = True
        else:
            for key in EFFECT_KEYS:
                data[key] = False
        config['theme']['enabled'] = True
        save_config(config)
        if not apply_now(config, lang):
            base._restore_theme(config, previous, lang)


def _reset_stock(config: dict, lang: str) -> bool:
    spinner = ui.Spinner('Возвращаю оригинальный Remnawave...' if lang == 'ru' else 'Restoring original Remnawave...').start()
    try:
        # Critical: do not leave the proxy in front of Panel. Even an empty
        # theme.css would still let CSS sub_filter rules repaint stock styles.
        restore_proxy(config)
        stop_injector(remove=True)
        config['theme']['preset'] = 'default'
        config['theme']['enabled'] = False
        config['theme']['effects'] = {key: False for key in EFFECT_KEYS}
        save_config(config)
        spinner.stop(True, base.tr(lang, 'reset_done'))
        return True
    except Exception as exc:
        spinner.stop(False, str(exc))
        return False


def reset_default(config: dict, lang: str) -> None:
    ui.clear(); base.header(lang)
    ui.warn('Будет восстановлен именно оригинальный внешний вид Remnawave.' if lang == 'ru' else 'This restores the original Remnawave appearance exactly.')
    if not ui.confirm(base.tr(lang, 'reset_confirm'), default=False):
        return
    _reset_stock(config, lang)
    ui.pause(base.tr(lang, 'press_enter'))


def settings(config: dict, lang: str) -> str:
    while True:
        ui.clear(); base.header(lang)
        rows = [
            f"{ui.primary('1')}  🌐  {base.tr(lang, 'change_language')}",
            f"{ui.primary('2')}  🛠  {base.tr(lang, 'repair')}",
            f"{ui.primary('0')}  ←   {base.tr(lang, 'back')}",
        ]
        _rows(base.tr(lang, 'settings_title'), rows)
        choice = ui.choose(base.tr(lang, 'choose'), ['0', '1', '2'], '0')
        if choice == '0':
            return lang
        if choice == '1':
            lang = base.select_language(lang)
            config['language'] = lang
            save_config(config)
            continue
        if bool(config.get('theme', {}).get('enabled', True)):
            apply_now(config, lang)
        else:
            # In stock mode, "repair" means keeping the direct Panel route.
            _reset_stock(config, lang)
        ui.pause(base.tr(lang, 'press_enter'))


def interactive(config: dict) -> None:
    lang = config.get('language', 'ru')
    while True:
        ui.clear(); base.header(lang); base._status_card(config, lang)
        rows = [
            f"{ui.primary('1')}  🎨  {base.tr(lang, 'presets')}",
            f"{ui.primary('2')}  ◉   {base.tr(lang, 'accent')}",
            f"{ui.primary('3')}  ▰   {base.tr(lang, 'background')}",
            f"{ui.primary('4')}  ▣   {base.tr(lang, 'surface')}",
            f"{ui.primary('5')}  ◯   {base.tr(lang, 'radius')}",
            f"{ui.primary('6')}  ✨  {base.tr(lang, 'effects')}",
            f"{ui.primary('7')}  👁   {base.tr(lang, 'preview')}",
            f"{ui.primary('8')}  ↻   {base.tr(lang, 'apply')}",
            f"{ui.primary('9')}  ↩   {base.tr(lang, 'reset')}",
            f"{ui.primary('10')} ⚙   {base.tr(lang, 'settings')}",
            f"{ui.primary('0')}  ⏻   {base.tr(lang, 'exit')}",
        ]
        _rows(base.tr(lang, 'menu'), rows)
        choice = ui.choose(base.tr(lang, 'choose'), [str(i) for i in range(0, 11)], '0')
        if choice == '0':
            ui.clear(); return
        if choice == '1': choose_preset(config, lang)
        elif choice == '2': base.choose_palette_field(config, lang, 'accent')
        elif choice == '3': base.choose_palette_field(config, lang, 'background')
        elif choice == '4': base.choose_palette_field(config, lang, 'surface')
        elif choice == '5': choose_radius(config, lang)
        elif choice == '6': choose_effects(config, lang)
        elif choice == '7': base.preview(config, lang)
        elif choice == '8': base.apply_current(config, lang)
        elif choice == '9': reset_default(config, lang)
        elif choice == '10': lang = settings(config, lang)


def install_overrides() -> None:
    base._effects_summary = effects_summary
    base._apply_now = apply_now
    base.choose_preset = choose_preset
    base.choose_radius = choose_radius
    base.choose_effects = choose_effects
    base.reset_default = reset_default
    base.settings = settings
    base.interactive = interactive


def main() -> int:
    install_overrides()
    args = base.build_parser().parse_args()
    if not require_root():
        ui.error('Запустите через sudo / Run as root.')
        return 1

    config = load_config()
    if args.command == 'setup' or not config.get('configured'):
        config = base.setup(config)
        if args.command == 'setup':
            return 0

    lang = config.get('language', 'ru')
    if args.command == 'apply':
        return 0 if apply_now(config, lang) else 1
    if args.command == 'reset':
        return 0 if _reset_stock(config, lang) else 1
    if args.command == 'status':
        return base.status(config, lang)
    if args.command == 'disconnect':
        return base.uninstall_integration(config, lang)

    interactive(config)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
