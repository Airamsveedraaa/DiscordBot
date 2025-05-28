import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTM3NzE3Nzg5NjA1Mjk4MTgxMA.GQoihH.4JjG7VR1Ai_yUqibl8q0aKSi-X3H6vjtsue9I4')
