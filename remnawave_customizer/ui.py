from __future__ import annotations

import os
import re
import shutil
import sys
import threading
from contextlib import contextmanager
from typing import Iterable, Iterator

_USE_COLOR = sys.stdout.isatty() and os.environ.get('NO_COLOR') is None
RESET = '\033[0m' if _USE_COLOR else ''
BOLD = '\033[1m' if _USE_COLOR else ''
DIM = '\033[2m' if _USE_COLOR else ''
PRIMARY = '\033[38;5;39m' if _USE_COLOR else ''
GREEN = '\033[38;5;82m' if _USE_COLOR else ''
YELLOW = '\033[38;5;220m' if _USE_COLOR else ''
RED = '\033[38;5;203m' if _USE_COLOR else ''
WHITE = '\033[97m' if _USE_COLOR else ''
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def color(text: str, code: str) -> str:
    return f'{code}{text}{RESET}' if code else text


def bold(text: str) -> str: return color(text, BOLD)
def dim(text: str) -> str: return color(text, DIM)
def primary(text: str) -> str: return color(text, PRIMARY)
def green(text: str) -> str: return color(text, GREEN)
def yellow(text: str) -> str: return color(text, YELLOW)
def red(text: str) -> str: return color(text, RED)
def white(text: str) -> str: return color(text, WHITE)


def _plain(value: str) -> str:
    return _ANSI_RE.sub('', value)


def clear() -> None:
    if sys.stdout.isatty():
        print('\033[2J\033[H', end='', flush=True)


def terminal_width() -> int:
    return max(62, min(100, shutil.get_terminal_size((84, 24)).columns))


def header(title: str, subtitle: str = '', badge: str | None = None) -> None:
    width = terminal_width() - 2
    inner = width - 2
    print(primary('╭' + '─' * inner + '╮'))
    title_text = f'  {title}'
    if badge:
        badge_text = f'  {badge}  '
        spaces = max(1, inner - len(_plain(title_text)) - len(_plain(badge_text)))
        line = title_text + ' ' * spaces + badge_text
    else:
        line = title_text
    print(primary('│') + bold(line) + ' ' * max(0, inner - len(_plain(line))) + primary('│'))
    if subtitle:
        sub = f'  {subtitle}'
        print(primary('│') + dim(sub) + ' ' * max(0, inner - len(_plain(sub))) + primary('│'))
    print(primary('╰' + '─' * inner + '╯'))


def heading(text: str) -> None:
    width = min(terminal_width() - 2, max(24, len(_plain(text)) + 4))
    print(f'\n{primary("─" * width)}')
    print(f'{primary("◆")} {bold(text)}')


def menu(items: list[str]) -> None:
    width = terminal_width() - 2
    inner = width - 2
    print(primary('╭' + '─' * inner + '╮'))
    for index, item in enumerate(items, 1):
        number = primary(f'{index:>2}')
        line = f'  {number}  {item}'
        print(primary('│') + line + ' ' * max(0, inner - len(_plain(line))) + primary('│'))
    print(primary('╰' + '─' * inner + '╯'))


def card(title: str, lines: list[str]) -> None:
    width = terminal_width() - 2
    inner = width - 2
    print(primary('╭' + '─' * inner + '╮'))
    title_line = f'  {title}'
    print(primary('│') + bold(title_line) + ' ' * max(0, inner - len(_plain(title_line))) + primary('│'))
    print(primary('├' + '─' * inner + '┤'))
    for line in lines:
        rendered = f'  {line}'
        print(primary('│') + rendered + ' ' * max(0, inner - len(_plain(rendered))) + primary('│'))
    print(primary('╰' + '─' * inner + '╯'))


def prompt(text: str, default: str | None = None) -> str:
    suffix = f' [{default}]' if default not in (None, '') else ''
    while True:
        try:
            value = input(f'{primary("›")} {text}{suffix}: ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit(130)
        if value:
            return value
        if default is not None:
            return default


def choose(text: str, allowed: Iterable[str], default: str | None = None) -> str:
    values = set(allowed)
    while True:
        value = prompt(text, default)
        if value in values:
            return value
        print(dim('  ' + ', '.join(sorted(values))))


def confirm(text: str, default: bool = True) -> bool:
    yes = {'y', 'yes', 'д', 'да', '1', '+', 'н'}  # н is y on RU layout
    no = {'n', 'no', 'нет', '0', '-', 'т'}       # т is n on RU layout
    suffix = ' [Y/n]' if default else ' [y/N]'
    while True:
        try:
            value = input(f'{primary("›")} {text}{suffix}: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit(130)
        if not value:
            return default
        if value in yes:
            return True
        if value in no:
            return False
        print(dim('  Y / N'))


def pause(text: str) -> None:
    try:
        input(f'\n{dim(text)}')
    except (EOFError, KeyboardInterrupt):
        print()


def ok(text: str) -> None: print(f'{green("●")} {text}')
def warn(text: str) -> None: print(f'{yellow("●")} {text}')
def error(text: str) -> None: print(f'{red("●")} {text}')
def info(text: str) -> None: print(f'{primary("›")} {text}')


def swatch(rgb: tuple[int, int, int], width: int = 3) -> str:
    if not _USE_COLOR:
        return '■' * width
    r, g, b = rgb
    return f'\033[48;2;{r};{g};{b}m' + (' ' * width) + RESET


class Spinner:
    frames = ('⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏')

    def __init__(self, text: str):
        self.text = text
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._active = False

    def _run(self) -> None:
        i = 0
        while not self._stop.is_set():
            print(f'\r\033[2K{primary(self.frames[i % len(self.frames)])} {self.text}', end='', flush=True)
            i += 1
            self._stop.wait(0.08)

    def start(self) -> 'Spinner':
        self._active = True
        if sys.stdout.isatty():
            print('\033[?25l', end='', flush=True)
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        else:
            info(self.text)
        return self

    def update(self, text: str) -> None:
        self.text = text

    def stop(self, ok_state: bool = True, final_text: str | None = None) -> None:
        if not self._active:
            return
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=0.3)
        if sys.stdout.isatty():
            print('\r\033[2K\033[?25h', end='', flush=True)
        text = final_text or self.text
        print(f'{green("✓") if ok_state else red("×")} {text}')
        self._active = False


@contextmanager
def spinner(text: str) -> Iterator[Spinner]:
    item = Spinner(text).start()
    try:
        yield item
    except Exception:
        item.stop(False)
        raise
    else:
        item.stop(True)
