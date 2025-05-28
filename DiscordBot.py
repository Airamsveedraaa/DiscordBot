import os
from sys import prefix
import discord #importacion libreria de discord
from discord.ext import commands #importacion de funciones relacionadas con comandos#
from aiohttp import web
from aiohttp import WSMsgType
import asyncio

user_exp={}

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        #sumar la exp enviada en cada mensaje
        user_id=str(message.author.id)
        if user_id not in user_exp:
            user_exp[user_id]={"exp":0,"level":1}

        user_exp[user_id]["exp"]+=5 #+5 exp por cada mensaje enviado

        #Subir de nivel cuando se llega a la exp requerida
        exp_needed=user_exp[user_id]["level"]*100
        if user_exp[user_id]["exp"]>=exp_needed:
            user_exp[user_id]["level"]+=1 #si llega, sube de nivel
            await message.channel.send(f"🎉 {message.author.mention} subió al nivel {user_exp[user_id]['level']}") #mensaje de confirmacion

async def websocket_handler(request):
    ws=web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type==WSMsgType.TEXT:
         if msg.data=="get_status":
            await ws.send_str('{"status": "active"}')
#Configuracion del bot con Slash Commands
bot =commands.Bot(command_prefix="!",intents=discord.Intents.default())

@bot.slash_command(name="exp",description="Muestra tu nivel y EXP")
async def exp(ctx):
    user_id=str(ctx.author.id)
    if user_id not in user_exp:
        await ctx.respond(f"{ctx.author.mention},aun no tienes EXP, envíate algún mensajito pa conseguir home")
    else:
        exp_needed=user_exp[user_id]["level"]*100
        await ctx.respond(
            f"{ctx.author.mention},eres nivel **{user_exp['level']}**"
            f"(EXP:{user_exp[user_id]['exp']}/{exp_needed}). Vamos, tu puedes mostro"
        )
@bot.slash_command(name="hola",description="Saluda al bot") #comando /hola
async def hola(ctx):
    await ctx.respond(f"Hola, {ctx.author.mention}!")

@bot.slash_command(name="!exp",description="Pide experiencia conseguida escribiendo mensajes")
async def exp(ctx):
    await ctx.respond(f"{ctx.author.mention} eres nivel ", exp, "felicidades!")

async def handle(request):
    return web.Response(text="Bot is running")

async def handle_status(request):
    return web.json_response({"status": "active"}, headers={'Access-Control-Allow-Origin': '*'})

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/status', handle_status)
    app.router.add_get('/ws', websocket_handler)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    loop = asyncio.get_event_loop()
    loop.create_task(client.start(os.getenv("DISCORD_TOKEN")))
    loop.create_task(bot.start(os.getenv("DISCORD_TOKEN")))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())