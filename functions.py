import discord
import asyncio

from config import SLEEP_TIME
from YouTube import *


def finder(phrase, word, phrase_pointer=0, word_pointer=0):
    if len(phrase) < len(word):
        return

    if type(phrase) == str:
        phrase = list(phrase)

    if type(word) == str:
        word = list(word)

    if word[word_pointer] == phrase[phrase_pointer]:
        word_pointer += 1
        if word_pointer == len(word):
            return True
    else:
        word_pointer = 0

    if phrase_pointer == len(phrase)-1:
        return False

    phrase_pointer += 1
    result = finder(phrase, word, phrase_pointer, word_pointer)

    return result


async def connect(message):

    guild = message.guild

    member = await guild.fetch_member(message.author.id)

    channel = member.voice.channel

    voice_client = await channel.connect()

    return voice_client


class Audio:

    def __init__(self):
        self.normal_url = []
        self.voice_client = None
        self.queue = []
        self.source = None
        self.message = None
        self.pos = None
        self.loop_flag = False
        self.skip_flag = True

    async def connect(self, message):

        guild = message.guild

        member = await guild.fetch_member(message.author.id)

        channel = member.voice.channel

        self.voice_client = await channel.connect()

    async def player(self, channel):

        if self.source is not None:
            self.source.cleanup()

        self.source = discord.FFmpegPCMAudio(self.queue[0], executable='C:/FFmpeg/bin/ffmpeg')

        self.voice_client.play(self.source)

        info = get_info(self.normal_url[0])

        embed = discord.Embed()
        embed.title = 'Сейчас играет:'
        embed.description = '{0} \r{1}'.format(*info)
        embed.url = self.normal_url[0]
        embed.set_image(url=info[2])
        red = discord.Colour.red()
        embed.colour = red
        await channel.send(embed=embed)

    async def pause(self):
        self.voice_client.pause()

    async def resume(self):
        self.voice_client.resume()

    async def skip(self):
        self.voice_client.stop()
        self.queue.pop(0)
        self.normal_url.pop(0)
        self.source.cleanup()

    async def main_player(self, message):

        if self.voice_client is None:
            await self.connect(message)

        if not self.voice_client.is_connected():
            await self.connect(message)

        if finder(message.content, '!play'):

            new_song = message.content[6::]
            results_of_search = get_list_(new_song)

            string_of_variables = ''
            for pos, info in zip(range(10), results_of_search):
                string_of_variables += '{}. {} \r  {}'.format(pos, info['title'], info['channel'])
                string_of_variables += '\n'

            embed = discord.Embed()
            embed.description = string_of_variables
            await message.channel.send(embed=embed)

            while self.pos is None:
                await asyncio.sleep(3)

            self.normal_url.append(results_of_search[self.pos]['url'])
            self.queue.append(get_url(results_of_search[self.pos]['url']))
            self.pos = None

            if not self.voice_client.is_playing():

                while len(self.queue) > 0:

                    if not self.voice_client.is_playing() and not self.voice_client.is_paused():

                        await self.player(message.channel)

                        while self.voice_client.is_playing() or self.voice_client.is_paused():
                            await asyncio.sleep(SLEEP_TIME)

                        if not self.loop_flag and self.skip_flag:
                            await self.skip()

                        self.skip_flag = True

                    else:
                        await asyncio.sleep(SLEEP_TIME)

        if message.content == '!skip':
            await self.skip()
            self.skip_flag = False

        if message.content == '!pause':
            await self.pause()

        if message.content == '!resume':
            await self.resume()

        if message.content == '!loop':
            self.loop_flag = True if self.loop_flag is False else False

        if finder(message.content, '!download'):

            url = message.content[11::]
            url = get_download(url)

            embed = discord.Embed()
            embed.url = url

            embed.title = 'Your download link'
            await message.channel.send(embed=embed)
