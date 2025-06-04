const canvas = document.getElementById("miCanvas");
const ctx = canvas.getContext("2d");

const tamañoCelda = 40;
const grosorLinea = 0.5;
const colorLinea = "rgba(255, 255, 255, 1)";

function ajustarCanvas() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;
  canvas.style.width = window.innerWidth + "px";
  canvas.style.height = window.innerHeight + "px";
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(dpr, dpr);
}
ajustarCanvas();
window.addEventListener("resize", ajustarCanvas);

let offset = 0;

function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = colorLinea;
  ctx.lineWidth = grosorLinea;

  const width = window.innerWidth;
  const height = window.innerHeight;

  // Asegurarse de que offset sea un número entero para alinear
  const off = Math.floor(offset);

  // Verticales
  for (let x = -off % tamañoCelda; x < width; x += tamañoCelda) {
    ctx.beginPath();
    ctx.moveTo(Math.round(x) + 0.5, 0);
    ctx.lineTo(Math.round(x) + 0.5, height);
    ctx.stroke();
  }

  // Horizontales
  for (let y = -off % tamañoCelda; y < height; y += tamañoCelda) {
    ctx.beginPath();
    ctx.moveTo(0, Math.round(y) + 0.5);
    ctx.lineTo(width, Math.round(y) + 0.5);
    ctx.stroke();
  }

  offset += 0.15; // Movimiento lento pero controlado
  requestAnimationFrame(animar);
}

animar();
