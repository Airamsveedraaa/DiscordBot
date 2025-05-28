import os
import discord
from aiohttp import web
import asyncio

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f'Message from {message.author}: {message.content}')
        if message.content.lower()=="hola":
            await message.channel.send(f"¡Hola,{message.author.display_name}!")
        else:
            if message.content.lower()=="Callate":
                await message.channel.send(f"Callate tu {message.author.display_name}, maricon")

async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    # Iniciar el bot de Discord
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(os.getenv("DISCORD_TOKEN")))

    # Iniciar el servidor web
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()

    # Mantener el proceso en ejecución
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
