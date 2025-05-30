const WS_URL = "wss://discordbot-jv7p.onrender.com/ws";
const statusElement = document.getElementById("bot-status");
let socket;

function updateStatus(status) {
    statusElement.textContent = status === "active" ? "🟢 Activo" : "🔴 Inactivo";
    statusElement.className = `status ${status === "active" ? "active" : "inactive"}`;
}

function connectWebSocket() {
    socket = new WebSocket(WS_URL);

    socket.onopen = () => {
        console.log("Conexión WebSocket establecida");
        socket.send("get_status");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateStatus(data.status);
    };

    socket.onclose = () => {
        updateStatus("inactive");
        console.log("Conexión cerrada. Reconectando en 5 segundos...");
        setTimeout(connectWebSocket, 5000);
    };

    socket.onerror = (error) => {
        console.error("Error en WebSocket:", error);
        updateStatus("inactive");
    };
}

window.onload = connectWebSocket;
