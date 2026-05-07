#!/usr/bin/env bash
set -eo pipefail

# Define paths to your other bash scripts
APP_ROOT_PATH="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd)"
SCRIPT1="${APP_ROOT_PATH}/scripts/run_sc_server.sh"
SCRIPT2="${APP_ROOT_PATH}/scripts/run_py_sc_server.sh"
SCRIPT3="${APP_ROOT_PATH}/scripts/run_sc_web.sh"
SCRIPT4="${APP_ROOT_PATH}/scripts/run_interface.sh"
SCRIPT5="${APP_ROOT_PATH}/scripts/run_career_ai.sh"
CAREER_AI_PORT="${CAREER_AI_PORT:-8010}"

chmod +x "$SCRIPT1"

chmod +x "$SCRIPT2"

chmod +x "$SCRIPT3"

chmod +x "$SCRIPT4"

chmod +x "$SCRIPT5"

PARENT_VENV="${APP_ROOT_PATH}/../.venv/bin/activate"
if [ -f "${PARENT_VENV}" ]; then
    source "${PARENT_VENV}"
fi

# Function to start a screen session and run a script
start_screen_session() {
    local session_name="$1"
    local script_path="$2"

    if screen -list | grep -q "[.]${session_name}[[:space:]]"; then
        echo "Screen session ${session_name} is already running."
        return
    fi

    screen -dmS "$session_name" bash "$script_path"
}

is_port_listening() {
    local port="$1"

    if command -v lsof >/dev/null 2>&1; then
        lsof -iTCP:"$port" -sTCP:LISTEN -P -n >/dev/null 2>&1
        return
    fi

    if command -v ss >/dev/null 2>&1; then
        ss -ltn | awk '{print $4}' | grep -Eq "[:.]${port}$"
        return
    fi

    if command -v netstat >/dev/null 2>&1; then
        netstat -ltn 2>/dev/null | awk '{print $4}' | grep -Eq "[:.]${port}$"
        return
    fi

    return 1
}

# Start screen sessions
start_screen_session "session1" "$SCRIPT1"
start_screen_session "session2" "$SCRIPT2"
start_screen_session "session3" "$SCRIPT3"
start_screen_session "session4" "$SCRIPT4"

if is_port_listening "${CAREER_AI_PORT}"; then
    echo "Career AI backend is already listening on port ${CAREER_AI_PORT}."
else
    start_screen_session "career-ai" "$SCRIPT5"
fi

echo "Screens launched and scripts are running."
