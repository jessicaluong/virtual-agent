# Virtual Agent with Real-time Gesture Recognition

A real-time virtual agent that recognizes human gestures through webcam input and responds with character animations. The system analyzes user gestures through a Python backend and displays responses via a Unity-based 3D character frontend, connected through WebSocket communication.

[Include GIF/video demo of the agent responding to gestures]

## Gesture Recognition System

The agent recognizes and responds to the following gestures in real-time:

| User Gesture | Agent Animation Response |
| --- | --- |
| 👋 Raise hand | Pointing gesture |
| 👍 Thumbs up | Head nod with positive expression |
| 👎 Thumbs down | Head shake with negative expression |
| 🙌 Cheer | Excited animation with happy expression |
| Cross arms | Shrugging gesture |
| 👏 Clap | Clapping animation with happy expression |
| 😐 Idle (Neutral) | Idle animation |

## Technologies Used 

[![Tech](https://skillicons.dev/icons?i=py,unity,cs)](https://skillicons.dev)

### System Architecture 

<img width="1078" alt="system_architecture" src="https://github.com/user-attachments/assets/bb319ee6-fb17-4658-97e7-a1ad3cf7dde8" />

* **Backend**: Python-based gesture processing pipeline
   * MediaPipe Holistic for gesture detection
   * Custom-trained ML model for gesture classification
   * Real-time gesture recognition through webcam input

* **Communication**
   * WebSocket protocol for real-time data transfer
   * Server implementation in Python
   * Client implementation in C#/Unity

* **Frontend**: Unity-based character 
   * WebGL build for browser compatibility
   * Real-time character animation

## Personal Contribution 

This project is a refactored version of a group project originally developed for a Special Topics in AI course (https://github.com/jessicaluong/CMPT419-Project). 

In the original project, I was responsible for:

- 🛠️ Implementing TCP networking infrastructure
- 🐍 Developing the Python backend components
- 🎮 Writing Unity frontend scripts
- 🤖 Integrating the 3D character model and animations in Unity 

Key improvements in this version:

- 🔄 Migrated from TCP to WebSocket protocol for web compatibility
- 🌐 Added WebGL support for browser-based access
- 🍎 Implemented startup script for MacOS users
- ⚡ Enhanced real-time performance and reduced latency


### Project Structure

```
virtual-agent/
├── server/                       # Backend components
│   ├── main.py                   # Entry point
│   ├── websocket_server.py       # WebSocket server implementation
│   ├── live_stream_processing.py # Real-time gesture detection and classification
│   └── model.keras               # Trained ML model for gesture recognition
├── client/                       # WebGL build
└── Unity/                                    # Frontend components
    └── Assets/
        ├── Scripts/
        │   ├── RespondToSignals.cs           # Manages character animations and state changes
        │   └── WebSocketClient.cs            # WebSocket client implementation
        └── Jammo-Character/                  # 3D character model and animations
```

## Getting Started 

### Prerequisites 
- Python version requirements: 
  - Windows: Python 3.10.9
  - MacOS: Python 3.11
- Webcam 
- Web browser with WebGL support 

### ⚠️ Privacy Notice
The application requires webcam access for gesture detection. All processing happens locally, and no video/images are stored.

### Installation and Setup

#### 1. Clone the Repository
```
git clone https://github.com/jessicaluong/virtual-agent.git
cd virtual-agent
```

#### 2. Set up Python Environment 
```
python3 -m venv venv

source venv/bin/activate  # MacOS
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### 3. Start Application 

##### Option 1: Quick Start (MacOS only)
```
./start.sh    # Default webcam
# or 
./start.sh 1  # External webcam
```

##### Option 2: Manual Start (All platforms)

1. Start the backend server in first terminal:
```
python3 server/main.py               # Default webcam
# or 
python3 server/main.py --camera 1    # External webcam
```
2. Start the WebGL server in second terminal: 
```
python3 serve_webgl.py 8000
```

#### 4. View Application
Open http://localhost:8000 in your web browser
