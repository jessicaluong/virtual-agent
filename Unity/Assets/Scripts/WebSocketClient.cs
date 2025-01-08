using UnityEngine;
using NativeWebSocket;

public class WebSocketClient : MonoBehaviour
{
    private WebSocket websocket;
    public string host = "localhost";
    public int port = 25001;
    public RespondToSignals signalResponder;

    private void Awake()
    {
        var dispatcher = UnityMainThreadDispatcher.Instance;
    }

    // Start is called before the first frame update
    private void Start()
    {
        ConnectToServer();
    }

    private async void ConnectToServer()
    {
        string url = $"ws://{host}:{port}";
        websocket = new WebSocket(url);

        websocket.OnOpen += () => Debug.Log("Connected to server");
        websocket.OnError += (e) => Debug.LogError($"WebSocket Error: {e}");
        websocket.OnClose += (e) => Debug.Log("Disconnected from server");
        websocket.OnMessage += GetSignal;

        await websocket.Connect();
    }

    private void GetSignal(byte[] data)
    {
        var signal = System.Text.Encoding.UTF8.GetString(data);
        Debug.Log($"Received data: {signal}");

        UnityMainThreadDispatcher.Instance.Enqueue(() => signalResponder.ReceiveSignal(signal));
    }

    // Update is called once per frame
    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
            websocket?.DispatchMessageQueue();
        #endif
    }

    private async void OnApplicationQuit()
    {
        if (websocket != null &&
            websocket.State == WebSocketState.Open)
        {
            await websocket.Close();
        }
    }
}
