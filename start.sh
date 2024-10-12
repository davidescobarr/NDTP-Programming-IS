#!/bin/bash -x

# Define paths to your other bash scripts
SCRIPT1="./scripts/run_sc_server.sh"
SCRIPT2="./scripts/run_py_sc_server.sh"
SCRIPT3="./scripts/run_sc_web.sh"
SCRIPT4="./scripts/run_interface.sh"

chmod +x "$SCRIPT1"

chmod +x "$SCRIPT2"

chmod +x "$SCRIPT3"

chmod +x "$SCRIPT4"

cd "../"
source .venv/bin/activate
cd "/nika"

# Function to start a screen session and run a script
start_screen_session() {
    local session_name="$1"
    local script_path="$2"
    screen -dmS "$session_name" bash $script_path
}

# Start 4 screen sessions
start_screen_session "session1" "$SCRIPT1"
start_screen_session "session2" "$SCRIPT2"
start_screen_session "session3" "$SCRIPT3"
start_screen_session "session4" "$SCRIPT4"

echo "Screens launched and scripts are running."
