const WS_URL = "wss://discordbot-jv7p.onrender.com/ws";
const statusElement = document.getElementById("bot-status");
let socket;

function updateStatus(status) {
  statusElement.textContent = status === "active" ? "🟢 Activo" : "🔴 Inactivo";
  statusElement.className = `status-minimal ${status === "active" ? "active" : "inactive"}`;
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

let currentPage = 1;
let totalPages = 1;

async function cargarRanking(page = 1) {
  const response = await fetch(`https://discordbot-jv7p.onrender.com/api/ranking?page=${page}`);
  const result = await response.json();
  const data = result.data;
  const tbody = document.querySelector("#ranking-section tbody");
  tbody.innerHTML = "";
  data.forEach((user, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${(page - 1) * result.per_page + i + 1}</td>
      <td>
        <img src="${user.avatar_url || ''}" alt="avatar" style="width:32px;height:32px;border-radius:50%;vertical-align:middle;margin-right:8px;">
        ${user.username || user.user_id}
      </td>
      <td>${user.experience}</td>
      <td>${user.level}</td>
    `;
    tbody.appendChild(tr);
  });

  // Actualiza paginación
  currentPage = result.page;
  totalPages = Math.ceil(result.total / result.per_page);
  document.getElementById("ranking-pagination").innerHTML = `
    <button ${currentPage === 1 ? "disabled" : ""} id="prev-page">Anterior</button>
    Página ${currentPage} de ${totalPages}
    <button ${currentPage === totalPages ? "disabled" : ""} id="next-page">Siguiente</button>
  `;

  document.getElementById("prev-page").onclick = () => cargarRanking(currentPage - 1);
  document.getElementById("next-page").onclick = () => cargarRanking(currentPage + 1);
}

document.addEventListener("DOMContentLoaded", () => {
  connectWebSocket();
  cargarRanking();
  const openGithubIssueBtn = document.getElementById('open-github-issue');
  if (openGithubIssueBtn) {

    openGithubIssueBtn.textContent = "¡Envía tu sugerencia de cambio/mejora aquí!"; // aseguramos que el botón tenga texto visible
    openGithubIssueBtn.addEventListener('click', () => {


    openGithubIssueBtn.classList.add('clicked'); // Agrega la clase al hacer clic

      openGithubIssueBtn.textContent = "¡Gracias por tu sugerencia :) !"; // Cambia el texto del botón
      openGithubIssueBtn.disabled = true; // Deshabilita el botón para evitar múltiples clics
      const title = encodeURIComponent('Sugerencia de mejora para el bot');
      const body = encodeURIComponent(
        'Describe tu sugerencia aquí:\n\n- ¿Qué te gustaría que cambiara o añadiera?\n- ¿Por qué sería útil?'
      );

      const url = `https://github.com/Airamsveedraaa/DiscordBot/issues/new?title=${title}&body=${body}`;
      window.open(url, '_blank'); // abrir en nueva pestaña
    });
  }
});
