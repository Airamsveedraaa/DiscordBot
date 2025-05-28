import os
import discord
from discord.ext import commands
from aiohttp import web
import asyncio

user_exp = {}

# Configuración del bot (usando solo commands.Bot)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sistema de EXP
    user_id = str(message.author.id)
    if user_id not in user_exp:
        user_exp[user_id] = {"exp": 0, "level": 1}

    user_exp[user_id]["exp"] += 5

    exp_needed = user_exp[user_id]["level"] * 100
    if user_exp[user_id]["exp"] >= exp_needed:
        user_exp[user_id]["level"] += 1
        await message.channel.send(f"🎉 {message.author.mention} subió al nivel {user_exp[user_id]['level']}")

    await bot.process_commands(message)  # Importante para procesar comandos

# Slash Commands
@bot.slash_command(
    name="exp",
    description="Muestra tu nivel y EXP",
    guild_ids=[1282445725166342308]  # Reemplaza con tu ID de servidor
)
async def exp(ctx):
    user_id = str(ctx.author.id)
    if user_id not in user_exp:
        await ctx.respond(f"{ctx.author.mention}, aún no tienes EXP. ¡Envía mensajes para ganar!")
    else:
        exp_needed = user_exp[user_id]["level"] * 100
        await ctx.respond(
            f"{ctx.author.mention}, eres nivel **{user_exp[user_id]['level']}** "
            f"(EXP: {user_exp[user_id]['exp']}/{exp_needed}). ¡Sigue así!"
        )

@bot.slash_command(
    name="hola",
    description="Saluda al bot",
    guild_ids=[1282445725166342308]  # Reemplaza con tu ID de servidor
)
async def hola(ctx):
    await ctx.respond(f"¡Hola, {ctx.author.mention}!")

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
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/status', handle_status)
    app.router.add_get('/ws', websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()

    await bot.start(os.getenv("DISCORD_TOKEN"))

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())