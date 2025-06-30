import os
import discord
from discord.ext import commands
from aiohttp import web
import asyncio
import datetime as dt
import yt_dlp
from dotenv import load_dotenv
from database import (
    init_db, get_user_exp, set_user_exp, get_full_ranking
)
import tempfile

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# 🎧 Función para obtener audio con yt_dlp usando cookies desde variable de entorno
def get_audio_url(url: str) -> (str, str):
    cookies_content = os.getenv("COOKIES_TXT_CONTENT")
    if not cookies_content:
        raise Exception("❌ No se encontró la variable de entorno COOKIES_TXT_CONTENT")

    # Crear un archivo temporal para las cookies
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_cookies:
        temp_cookies.write(cookies_content)
        temp_cookies.flush()
        temp_cookies_path = temp_cookies.name

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'cookiefile': temp_cookies_path,
        'noplaylist': True,
        'default_search': 'ytsearch',
        'extract_flat': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:  # si es búsqueda
                info = info['entries'][0]
            return info['url'], info['title']
    finally:
        # Borrar archivo temporal de cookies después de usarlo
        os.unlink(temp_cookies_path)

@bot.event
async def on_ready():
    await init_db()
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    username = str(message.author)
    avatar_url = message.author.display_avatar.url if hasattr(message.author, "display_avatar") else message.author.avatar_url

    user_data = await get_user_exp(user_id)
    exp = user_data["experience"] + 5
    level = user_data["level"]
    exp_needed = level * 100

    if exp >= exp_needed:
        level += 1
        exp -= exp_needed
        await message.channel.send(f"🎉 {message.author.mention} subió al nivel {level}")

    await set_user_exp(user_id, exp, level, username, avatar_url)
    await bot.process_commands(message)

@bot.command()
async def exp(ctx):
    user_id = str(ctx.author.id)
    user_data = await get_user_exp(user_id)
    exp_needed = user_data["level"] * 100
    await ctx.send(
        f"{ctx.author.mention}, eres nivel **{user_data['level']}** "
        f"(EXP: {user_data['experience']}/{exp_needed}). ¡Sigue así!"
    )

@bot.command()
async def rank(ctx):
    ranking = await get_full_ranking()
    if not ranking:
        await ctx.send("No hay usuarios en el ranking todavía.")
        return

    per_page = 10
    total_pages = (len(ranking) + per_page - 1) // per_page
    page = 0

    def get_page_msg(page):
        start = page * per_page
        end = start + per_page
        msg = f"**🏆 Ranking de experiencia (página {page+1}/{total_pages}):**\n"
        for i, user in enumerate(ranking[start:end], start + 1):
            user_mention = f"<@{user['user_id']}>"
            msg += f"{i}. {user_mention} — Nivel {user['level']} ({user['experience']} exp)\n"
        return msg

    message = await ctx.send(get_page_msg(page))

    if total_pages == 1:
        return

    await message.add_reaction("⏪")
    await message.add_reaction("⏩")

    def check(reaction, user):
        return (
            user == ctx.author
            and reaction.message.id == message.id
            and str(reaction.emoji) in ["⏪", "⏩"]
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            break

        if str(reaction.emoji) == "⏩" and page < total_pages - 1:
            page += 1
            await message.edit(content=get_page_msg(page))
            await message.remove_reaction(reaction, user)
        elif str(reaction.emoji) == "⏪" and page > 0:
            page -= 1
            await message.edit(content=get_page_msg(page))
            await message.remove_reaction(reaction, user)
        else:
            await message.remove_reaction(reaction, user)

@bot.command()
async def hola(ctx):
    await ctx.send(f"¡Hola, {ctx.author.mention}!")

@bot.command()
async def adios(ctx):
    await ctx.send(f"Chao chao chao {ctx.author.mention}")

# ✅ Comando !play usando yt_dlp y cookies desde variable de entorno
@bot.command()
async def play(ctx, *, url):
    if ctx.author.voice is None:
        await ctx.send("¡Debes estar en un canal de voz para reproducir música!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client
        if voice_client.channel != channel:
            await voice_client.move_to(channel)

    try:
        audio_url, title = get_audio_url(url)

        source = discord.FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        if not voice_client.is_playing():
            voice_client.play(source)
            await ctx.send(f"🎶 Reproduciendo: {title}")
        else:
            await ctx.send("Ya estoy reproduciendo música. Usa `!stop` para detenerla.")
    except Exception as e:
        await ctx.send(f"❌ Error al intentar reproducir el audio: {e}")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client

    if voice_client and voice_client.is_connected():
        if voice_client.is_playing():
            voice_client.stop()

        await voice_client.disconnect()
        await ctx.send("🔇 Me he desconectado del canal de voz.")
    else:
        await ctx.send("❌ No estoy conectado a ningún canal de voz.")

@bot.command()
async def ayuda(ctx):
    await ctx.send(f"Aquí tienes la lista de comandos disponibles {ctx.author.mention}: !exp \n !hola \n !adios \n !play \n !stop")

# Web API para Render
async def handle(request):
    return web.Response(text="Bot is running")

async def handle_status(request):
    if not bot.is_ready() or bot.is_closed():
        status = "inactive"
    else:
        status = "active"
    return web.json_response({"status": status}, headers={'Access-Control-Allow-Origin': '*'})

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == "get_status":
                await ws.send_str('{"status": "active"}')
    return ws

async def handle_ranking(request):
    try:
        page = int(request.query.get("page", 1))
        per_page = 10
        ranking = await get_full_ranking()
        total = len(ranking)
        start = (page - 1) * per_page
        end = start + per_page
        data = [
            {
                "user_id": row["user_id"],
                "username": row["username"],
                "avatar_url": row["avatar_url"],
                "experience": row["experience"],
                "level": row["level"]
            }
            for row in ranking[start:end]
        ]
        return web.json_response({
            "data": data,
            "total": total,
            "page": page,
            "per_page": per_page
        }, headers={'Access-Control-Allow-Origin': '*'})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_stats(request):
    num_guilds = len(bot.guilds)
    num_users = len(set(bot.get_all_members()))
    return web.json_response({
        "servers": num_guilds,
        "users": num_users
    }, headers={'Access-Control-Allow-Origin': '*'})

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/status', handle_status)
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/api/ranking', handle_ranking)
    app.router.add_get('/api/stats', handle_stats)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()

    await init_db()
    await bot.start(os.getenv("DISCORD_TOKEN"))

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
