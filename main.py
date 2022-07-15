from config import *
from functions import *


client = discord.Client()
player = Audio()


@client.event
async def on_ready():

    print('logged as {}'.format(client.user))
    guild = client.get_guild(451295482988199938)
    for channel in guild.channels:

        if channel.name == 'music':
            await channel.send('Привет всем')


@client.event
async def on_message(message):
    print('message from {0.author}:{0.content}'.format(message))

    content = message.content
    print(message.channel)

    author = message.author

    if finder(content.lower(), 'привет') and message.author != client.user:
        await message.channel.send('Привет <@{0}>'.format(author.id))

    if message.author != client.user:
        if message.content[0] == '!':
            await player.main_player(message)

    if message.content.isnumeric():
        player.pos = int(message.content)

client.run(TOKEN)
