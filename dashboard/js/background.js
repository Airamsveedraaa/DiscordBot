const canvas = document.getElementById("miCanvas");
const ctx = canvas.getContext("2d");

// Ajustar canvas al tamaño de la ventana
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Configuración de la cuadrícula
const tamañoCelda = 40; // Tamaño de cada cuadrado de la cuadrícula
const grosorLinea = 1; // Grosor de las líneas
const colorLinea = "rgba(255, 255, 255, 0.15)"; // Color blanco con transparencia (ajusta el alpha)
ctx.globalCompositeOperation = "lighter"; // Asegura que el fondo se dibuje correctamente
// Función para dibujar la cuadrícula
function dibujarCuadricula() {
  ctx.strokeStyle = colorLinea;
  ctx.lineWidth = grosorLinea;

  // Líneas verticales
  for (let x = 0.5; x < canvas.width; x += tamañoCelda) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }

  // Líneas horizontales
  for (let y = 0.5; y < canvas.height; y += tamañoCelda) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
}

// Animación sutil (opcional: desplazamiento lento)
let offset = 0;
function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Mover la cuadrícula (efecto de desplazamiento suave)
  offset += 0.2; // Ajusta la velocidad
  ctx.save();
  ctx.translate(offset % tamañoCelda, offset % tamañoCelda);
  
  dibujarCuadricula();
  ctx.restore();
  
  requestAnimationFrame(animar);
}

// Iniciar (elige una opción):
animar(); // Para animación sutil
// dibujarCuadricula(); // Para cuadrícula estática

// Redimensionar al cambiar el tamaño de la ventana
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  dibujarCuadricula();
});