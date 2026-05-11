#!/bin/bash
# DF-PMS-Protel-Adapter Mac LaunchAgent Runner [CRUX-MK]
# Welle-36

set -euo pipefail

LOCK_DIR="/tmp/df-pms-protel-adapter.lock"
LOCK_AGE_LIMIT_S=21600

if [ -d "$LOCK_DIR" ]; then
  LOCK_MTIME=$(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0)
  LOCK_AGE_S=$(( $(date +%s) - LOCK_MTIME ))
  if [ "$LOCK_AGE_S" -gt "$LOCK_AGE_LIMIT_S" ]; then
    rm -rf "$LOCK_DIR"
  fi
fi

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "[df-pms-protel-adapter] K16 lock held, exiting (ok)" >&2
  exit 3
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT INT TERM

cd "$(dirname "$0")/.."
PYTHONPATH="$(pwd):${PYTHONPATH:-}" python3 -c "
import sys
sys.path.insert(0, '.')
from src.adapter_orchestrator import ProtelAdapterOrchestrator

orch = ProtelAdapterOrchestrator()
report = orch.run()
print(f'[df-pms-protel-adapter] loop_id={report.loop_id} status={report.final_status} sandbox={report.sandbox_mode}')
sys.exit(0 if report.final_status in ('complete', 'partial') else 1)
"
