const canvas = document.getElementById("miCanvas");
const ctx = canvas.getContext("2d");

// Ajustar canvas al tamaño de la ventana
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Configuración de los cuadrados
const cuadrados = [];
const tamanoCuadrado = 20;
const velocidad = 2;
const colores = ["#E0F2FE", "#BAE6FD", "#7DD3FC", "#38BDF8"]; // Tonos azules claros (puedes cambiarlos)

// Crear cuadrados iniciales
function inicializarCuadrados() {
  for (let i = 0; i < 30; i++) {
    cuadrados.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height - canvas.height, // Empiezan arriba de la pantalla
      color: colores[Math.floor(Math.random() * colores.length)],
      velocidadX: velocidad * (Math.random() * 0.5 + 0.5), // Diagonal variable
      velocidadY: velocidad * (Math.random() * 0.5 + 0.5),
    });
  }
}

// Función para animar
function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Dibujar y mover cuadrados
  cuadrados.forEach((cuadrado, index) => {
    ctx.fillStyle = cuadrado.color;
    ctx.fillRect(cuadrado.x, cuadrado.y, tamanoCuadrado, tamanoCuadrado);

    // Mover en diagonal
    cuadrado.x += cuadrado.velocidadX;
    cuadrado.y += cuadrado.velocidadY;

    // Reiniciar posición si sale de la pantalla
    if (
      cuadrado.y > canvas.height ||
      cuadrado.x > canvas.width ||
      cuadrado.x < -tamanoCuadrado
    ) {
      cuadrados[index] = {
        x: Math.random() * canvas.width,
        y: -tamanoCuadrado,
        color: colores[Math.floor(Math.random() * colores.length)],
        velocidadX: velocidad * (Math.random() * 0.5 + 0.5),
        velocidadY: velocidad * (Math.random() * 0.5 + 0.5),
      };
    }
  });

  requestAnimationFrame(animar);
}

// Iniciar
inicializarCuadrados();
animar();

// Redimensionar canvas si cambia el tamaño de la ventana
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});