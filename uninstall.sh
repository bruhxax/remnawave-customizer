#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run as root: sudo ./uninstall.sh"
  exit 1
fi

if command -v customizer >/dev/null 2>&1; then
  customizer disconnect || true
fi

rm -f /usr/local/bin/customizer
rm -rf /opt/remnawave-customizer/app
rm -rf /opt/remnawave-customizer-runtime

echo "Remnawave Customizer removed."
echo "Backups and settings in /etc/remnawave-customizer were kept intentionally."
