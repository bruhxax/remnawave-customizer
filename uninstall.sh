#!/usr/bin/env bash
set -euo pipefail

PURGE=0
if [[ "${1:-}" == "--purge" ]]; then
  PURGE=1
fi

if [[ ${EUID} -ne 0 ]]; then
  echo "Run as root: sudo ./uninstall.sh"
  exit 1
fi

APP="/opt/remnawave-customizer/app"

# Restore the original reverse-proxy route BEFORE removing any files. This is
# intentionally non-interactive so uninstall can never leave Panel pointing at
# a deleted Customizer container.
if [[ -d "$APP/remnawave_customizer" ]]; then
  PYTHONPATH="$APP${PYTHONPATH:+:$PYTHONPATH}" python3 - <<'PY'
from remnawave_customizer.config import load_config
from remnawave_customizer.proxy import restore_proxy, stop_injector

config = load_config()
restore_proxy(config)
stop_injector(remove=True)
PY
else
  if [[ -d /opt/remnawave-customizer-runtime ]]; then
    (cd /opt/remnawave-customizer-runtime && docker compose down --remove-orphans) || true
  fi
fi

rm -f /usr/local/bin/customizer
rm -rf /opt/remnawave-customizer/app
rm -rf /opt/remnawave-customizer-runtime

if [[ $PURGE -eq 1 ]]; then
  rm -rf /etc/remnawave-customizer
  echo "Remnawave Customizer fully removed, including settings and backups."
else
  echo "Remnawave Customizer removed."
  echo "Settings/backups kept in /etc/remnawave-customizer."
  echo "For a full purge use: sudo ./uninstall.sh --purge"
fi
