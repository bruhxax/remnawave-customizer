#!/usr/bin/env bash
set -euo pipefail

APP_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DST="/opt/remnawave-customizer/app"
BIN="/usr/local/bin/customizer"
CONFIG="/etc/remnawave-customizer/config.json"
NO_SETUP=0

if [[ "${1:-}" == "--no-setup" ]]; then
  NO_SETUP=1
fi

if [[ ${EUID} -ne 0 ]]; then
  echo "Run as root: sudo ./install.sh"
  exit 1
fi

echo "[1/3] Checking requirements..."
for cmd in python3 docker; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "  ✗ $cmd not found"
    exit 1
  fi
  echo "  ✓ $cmd"
done
if ! docker compose version >/dev/null 2>&1; then
  echo "  ✗ docker compose plugin not found"
  exit 1
fi
echo "  ✓ docker compose"

if [[ ! -f /opt/remnawave/docker-compose.yml ]]; then
  echo
  echo "✗ Remnawave Panel not found in /opt/remnawave"
  echo "  Remnawave Customizer must be installed ONLY on the server where Panel is installed."
  exit 1
fi
if ! docker inspect remnawave >/dev/null 2>&1; then
  echo
  echo "✗ Container 'remnawave' not found"
  echo "  Start Remnawave Panel first, then run the installer again."
  exit 1
fi

echo "[2/3] Installing Remnawave Customizer..."
mkdir -p "$APP_DST" /etc/remnawave-customizer
rm -rf "$APP_DST/remnawave_customizer"
cp -a "$APP_SRC/remnawave_customizer" "$APP_DST/remnawave_customizer"

cat > "$BIN" <<'EOF'
#!/usr/bin/env bash
export PYTHONPATH="/opt/remnawave-customizer/app${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m remnawave_customizer.cli "$@"
EOF
chmod 755 "$BIN"

echo "[3/3] Done."
echo "  ✓ No apt update"
echo "  ✓ No pip install"
echo "  ✓ Panel files are not replaced"

if [[ $NO_SETUP -eq 1 ]]; then
  exit 0
fi

if [[ -f "$CONFIG" ]] && python3 - <<PY >/dev/null 2>&1
import json
p='$CONFIG'
try:
    d=json.load(open(p))
    raise SystemExit(0 if d.get('configured') else 1)
except Exception:
    raise SystemExit(1)
PY
then
  echo
  echo "Existing configuration found."
  echo "Run: customizer"
  exit 0
fi

echo
exec customizer setup
