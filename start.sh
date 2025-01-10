#!/bin/bash
CAMERA=${1:-0}  
echo "Setting up Virtual Agent with camera $CAMERA..."

# Setup Python environment 
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt

# Function to cleanup processes on exit
cleanup() {
    echo "Shutting down servers..."
    kill $SERVER_PID $UNITY_PID 2>/dev/null
    exit 0
}

# Function to check if server is running on port 25001
check_server() {
    for i in {1..120}; do  # Try for 120 seconds
        if nc -z localhost 25001 > /dev/null 2>&1; then
            echo "Python server initialized successfully"
            return 0
        fi
        echo "Waiting for Python server to initialize... ($i/120)"
        sleep 1
    done
    echo "Error: Python server failed to initialize"
    cleanup
    exit 1
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Start Python server
echo "Starting Python server..."
{ python3 server/main.py --camera $CAMERA & } 2>/dev/null
SERVER_PID=$!

# Wait for server to initialize
check_server

# Start Unity WebGL server 
echo "Starting Unity WebGL server..."
cd client
python3 serve_webgl.py 8000 &
UNITY_PID=$!

# Open in default browser
sleep 2
open http://localhost:8000 2>/dev/null || echo "Please open http://localhost:8000 in your browser"

echo "Servers running. Press Ctrl+C to stop all servers."
wait