import os
import discord
from discord.ext import commands
from aiohttp import web
import asyncio
from daytime import Daytime
import datetime as dt  # para importar libreria de fecha y hora
from database import init_db, get_experience, add_experience, get_user_exp, set_user_exp

# Declaración de día y fecha actual para posterior uso
current_date = dt.date.today()
current_date.strftime("%A")  # formato de salida de los días, para mostrar nombre completo 'Sabado'
current_date_time = dt.datetime.now()  # hora del dia actual

# Configuración del bot (usando discord.py oficial)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await init_db()
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        user_id = str(message.author.id)
        user_data = await get_user_exp(user_id)
        user_data["exp"] += 5

        exp_needed = user_data["level"] * 100
        if user_data["exp"] >= exp_needed:
            user_data["level"] += 1
            await message.channel.send(f"🎉 {message.author.mention} subió al nivel {user_data['level']}")

        await set_user_exp(user_id, user_data["exp"], user_data["level"])
        await bot.process_commands(message)
    except Exception as e:
        print(f"[on_message error] {e}")


# Sistema para detectar entradas/salidas del servidor
@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined the server!")

@bot.event
async def on_member_remove(member):
    print(f"{member.name} has left the server!")

# Comando !exp
@bot.command()
async def exp(ctx, amount: int = 10):
    user_id = str(ctx.author.id)
    await add_experience(user_id, amount)
    new_exp = await get_experience(user_id)
    await ctx.send(f"{ctx.author.mention} ahora tiene {new_exp} puntos de experiencia.")


# Comando !hola
@bot.command()
async def hola(ctx):
    await ctx.send(f"¡Hola, {ctx.author.mention}!")

# Comando !adiós
@bot.command()
async def adios(ctx):
    await ctx.send(f"Chao chao chao {ctx.author.mention}")

# Servidor web
async def handle(request):
    return web.Response(text="Bot is running")

async def handle_status(request):
    return web.json_response({"status": "active"}, headers={'Access-Control-Allow-Origin': '*'})

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == "get_status":
                await ws.send_str('{"status": "active"}')
    return ws

async def main():
    # Inicia servidor web
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/status', handle_status)
    app.router.add_get('/ws', websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()

    await init_db()  # Esto crea las tablas si no existen

    # Inicia bot
    await bot.start(os.getenv("DISCORD_TOKEN"))

    # Ciclo infinito para mantener el proceso activo (por si acaso)
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())