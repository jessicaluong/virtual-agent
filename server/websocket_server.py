import asyncio
import websockets

async def handle_client(websocket, shutdown_event, signal_queue):
    print(f"Unity client connected: {websocket.remote_address}")

    try:
        while not shutdown_event.is_set():
            if not signal_queue.empty():
                signal = signal_queue.get()
                await websocket.send(signal)
            else:
                await asyncio.sleep(0.01) # Prevent busy waiting if the queue is empty
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected with error: {e}")
    finally:
        await websocket.close()
        print("Client connection closed.")

async def wait_for_shutdown(shutdown_event): 
    while not shutdown_event.is_set(): 
        await asyncio.sleep(0.1)

async def start_server(host, port, shutdown_event, signal_queue): 
    async def handler(websocket):
        await handle_client(websocket, shutdown_event, signal_queue)
    
    async with websockets.serve(handler, host, port): 
        print(f"WebSocket server listening on ws://{host}:{port}")
        await wait_for_shutdown(shutdown_event)
