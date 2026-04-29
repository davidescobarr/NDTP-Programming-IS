# Function to start a screen session and run a script
stop_screen_session() {
	local session_name="$1"
    screen -X -S "$session_name" kill
}

# Start 4 screen sessions
stop_screen_session "session1"
stop_screen_session "session2"
stop_screen_session "session3"
stop_screen_session "session4"

echo "Screens stopped"