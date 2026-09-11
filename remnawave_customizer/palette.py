from __future__ import annotations

import os
import select
import sys
import termios
import tty
from typing import Sequence

from . import ui
from .themes import RGB


def _read_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = os.read(fd, 1)
        if ch == b'\x1b':
            ready, _, _ = select.select([fd], [], [], 0.08)
            if not ready:
                return 'esc'
            seq = os.read(fd, 2)
            return {b'[A': 'up', b'[B': 'down', b'[C': 'right', b'[D': 'left'}.get(seq, 'esc')
        if ch in (b'\r', b'\n'):
            return 'enter'
        if ch in (b'q', b'Q'):
            return 'esc'
        return ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _nearest_index(colors: Sequence[RGB], current: RGB | None) -> int:
    if not current:
        return 0
    return min(range(len(colors)), key=lambda i: sum((colors[i][j] - current[j]) ** 2 for j in range(3)))


def choose_color(colors: Sequence[RGB], title: str, current: RGB | None = None, columns: int = 8) -> RGB | None:
    if not colors:
        return None
    index = _nearest_index(colors, current)
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return colors[index]

    while True:
        ui.clear()
        ui.header('🎨 Remnawave Customizer', title)
        print()
        for i, color in enumerate(colors):
            selected = i == index
            left = ui.primary('▶') if selected else ' '
            right = ui.primary('◀') if selected else ' '
            print(f'{left}{ui.swatch(color, 5)}{right}', end='  ')
            if (i + 1) % columns == 0:
                print('\n')
        if len(colors) % columns:
            print('\n')
        print(ui.dim('  ← → ↑ ↓  выбрать     Enter  подтвердить     Esc  назад'))
        key = _read_key()
        if key == 'enter':
            return colors[index]
        if key == 'esc':
            return None
        if key == 'left':
            index = index - 1 if index % columns else min(index + columns - 1, len(colors) - 1)
        elif key == 'right':
            index = index + 1 if (index + 1) % columns and index + 1 < len(colors) else index - (index % columns)
        elif key == 'up':
            index = index - columns if index - columns >= 0 else index
        elif key == 'down':
            index = index + columns if index + columns < len(colors) else index
