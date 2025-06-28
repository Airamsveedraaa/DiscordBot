# Usa una imagen ligera de Python
FROM python:3.11-slim

# Instala ffmpeg y dependencias necesarias para audio, compilación y cifrado
RUN apt-get update && \# Usa una imagen ligera de Python
FROM python:3.11-slim

# Instala ffmpeg y dependencias necesarias para audio, compilación y cifrado
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev libnacl-dev libopus-dev && \
    apt-get clean

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias del bot
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto para aiohttp (Render lo necesita para salud)
EXPOSE 10000

# Comando para ejecutar el bot
CMD ["python", "main.py"]

    apt-get install -y ffmpeg gcc libffi-dev libnacl-dev libopus-dev && \
    apt-get clean

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias del bot
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto para aiohttp (Render lo necesita para salud)
EXPOSE 10000

# Comando para ejecutar el bot
CMD ["python", "main.py"]
