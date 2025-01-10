import argparse
import asyncio
import threading
import queue
import signal
from live_stream_processing import capture_and_process_webcam
from websocket_server import start_server

def main(camera_number=0, dev_mode=False):
    """
    Main function to initialize the application based on provided arguments.

    This function handles the setup of threading events and queues, initiates server communication if
    not in Development mode, and starts webcam processing. 

    Parameters:
        camera_number (int): Specifies the camera index to use for video capture.
        dev_mode (bool): If True, enables development mode which does not start a WebSocket server. 
    """
    # Threading event to signal server thread to stop
    shutdown_event = threading.Event()
    # Thread-safe queue is shared between webcam processing and server communication
    signal_queue = queue.Queue()

    def signal_handler(sig, frame):
        print("\nSignal received, initiating shutdown...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    if not dev_mode:
        # Create and start the server in a separate thread
        def run_server_thread(): 
            asyncio.run(start_server("localhost", 25001, shutdown_event, signal_queue))

        server_thread = threading.Thread(target=run_server_thread)
        server_thread.start()
        print("WebSocket server started. Waiting for Unity client...")

        try:     
            capture_and_process_webcam(camera_number, shutdown_event, signal_queue, dev_mode)
        finally: 
            server_thread.join()
            print("Unity connection closed.")
    else: 
        capture_and_process_webcam(camera_number, shutdown_event, signal_queue, dev_mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process webcam feed and optionally communicate with Unity.")
    parser.add_argument('--camera', type=int, default=0, help='Camera number to use for capturing video.')
    parser.add_argument('--dev_mode', action='store_true', help='Displays landmarks and predictions to the screen.')

    args = parser.parse_args()

    main(camera_number=args.camera, dev_mode=args.dev_mode)

