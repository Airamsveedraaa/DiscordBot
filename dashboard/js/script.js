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

document.addEventListener("DOMContentLoaded", () => {
  connectWebSocket();

  const miBoton = document.getElementById('miBoton');
  if (miBoton) {
    miBoton.addEventListener('click', () => {
      alert('¡Botón clickeado!');
    });
  }

  const openGithubIssueBtn = document.getElementById('open-github-issue');
  if (openGithubIssueBtn) {
    openGithubIssueBtn.addEventListener('click', () => {
      const title = encodeURIComponent('Sugerencia de mejora para el bot');
      const body = encodeURIComponent(
        'Describe tu sugerencia aquí:\n\n- ¿Qué te gustaría que cambiara o añadiera?\n- ¿Por qué sería útil?'
      );

      const url = `https://github.com/Airamsveedraaa/DiscordBot/issues/new?title=${title}&body=${body}`;
      window.open(url, '_blank');
    });
  }
});
