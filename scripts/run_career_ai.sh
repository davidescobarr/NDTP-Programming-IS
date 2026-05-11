#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd)"
APP_ROOT_PATH="$(cd "${SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
SERVICE_PATH="${APP_ROOT_PATH}/career-ai-service"
VENV_PATH="${SERVICE_PATH}/.venv"
REQUIREMENTS_PATH="${SERVICE_PATH}/requirements.txt"
REQUIREMENTS_MARKER="${VENV_PATH}/.requirements.sha256"
HOST="${CAREER_AI_HOST:-0.0.0.0}"
PORT="${CAREER_AI_PORT:-8010}"

if [ ! -d "${SERVICE_PATH}" ]; then
    echo "Career AI service directory not found: ${SERVICE_PATH}" >&2
    exit 1
fi

find_python() {
    if command -v python3 >/dev/null 2>&1; then
        command -v python3
        return
    fi

    if command -v python >/dev/null 2>&1; then
        command -v python
        return
    fi

    echo "python3 or python is required to run Career AI service" >&2
    exit 1
}

if [ ! -d "${VENV_PATH}" ]; then
    PYTHON_BIN="$(find_python)"
    "${PYTHON_BIN}" -m venv "${VENV_PATH}"
fi

if [ -x "${VENV_PATH}/bin/python" ]; then
    VENV_PYTHON="${VENV_PATH}/bin/python"
elif [ -x "${VENV_PATH}/Scripts/python.exe" ]; then
    VENV_PYTHON="${VENV_PATH}/Scripts/python.exe"
else
    echo "Python executable was not found in ${VENV_PATH}" >&2
    exit 1
fi

requirements_hash() {
    "${VENV_PYTHON}" - "$REQUIREMENTS_PATH" <<'PY'
import hashlib
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
}

REQ_HASH="$(requirements_hash)"
INSTALLED_HASH="$(cat "${REQUIREMENTS_MARKER}" 2>/dev/null || true)"

if [ "${REQ_HASH}" != "${INSTALLED_HASH}" ] || ! "${VENV_PYTHON}" -c "import fastapi, pydantic, uvicorn" >/dev/null 2>&1; then
    "${VENV_PYTHON}" -m pip install --upgrade pip
    "${VENV_PYTHON}" -m pip install -r "${REQUIREMENTS_PATH}"
    echo "${REQ_HASH}" > "${REQUIREMENTS_MARKER}"
fi

cd "${SERVICE_PATH}"
exec "${VENV_PYTHON}" -m uvicorn app.main:app --host "${HOST}" --port "${PORT}"
