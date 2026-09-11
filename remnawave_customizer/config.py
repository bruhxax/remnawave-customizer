from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path('/etc/remnawave-customizer')
CONFIG_FILE = CONFIG_DIR / 'config.json'
BACKUP_DIR = CONFIG_DIR / 'backups'
RUNTIME_DIR = Path('/opt/remnawave-customizer-runtime')
APP_DIR = Path('/opt/remnawave-customizer/app')

DEFAULT_CONFIG: dict[str, Any] = {
    'language': 'ru',
    'configured': False,
    'theme': {
        'preset': 'midnight',
        'enabled': True,
        'accent': [0, 169, 255],
        'background': [7, 12, 19],
        'surface': [13, 21, 31],
        'radius': 'medium',
    },
    'proxy': {},
}


def _merge(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
        return _merge(DEFAULT_CONFIG, data if isinstance(data, dict) else {})
    except Exception:
        return copy.deepcopy(DEFAULT_CONFIG)


def save_config(config: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.chmod(tmp, 0o600)
    tmp.replace(CONFIG_FILE)
    os.chmod(CONFIG_FILE, 0o600)
