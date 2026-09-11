from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path


class CommandError(RuntimeError):
    pass


def run(command: str, timeout: int = 120, check: bool = False, cwd: str | Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        command,
        shell=True,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    )
    if check and proc.returncode != 0:
        raise CommandError((proc.stderr or proc.stdout or f'command failed: {command}').strip())
    return proc.returncode, proc.stdout, proc.stderr


def must_run(command: str, timeout: int = 120, cwd: str | Path | None = None) -> str:
    code, out, err = run(command, timeout=timeout, cwd=cwd)
    if code != 0:
        raise CommandError((err or out or f'command failed: {command}').strip())
    return out


def require_root() -> bool:
    return os.geteuid() == 0


def q(value: str | Path) -> str:
    return shlex.quote(str(value))
