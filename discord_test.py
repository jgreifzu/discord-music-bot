#Bot.py
import discord
import os
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from youtube_download import download_song
import time # To reproduce the error
import typing # For typehinting
import functools
import private

import asyncio
import nacl

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

song_queue = []


async def on_ready():
    print ("Ready")

async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await bot.loop.run_in_executor(None, func)

@bot.command(pass_context=True)
async def play(ctx):
    if (ctx.author.voice):
        song_title = await run_blocking(download_song, ctx.message.content)
        print("adding song to queue: " + song_title)
        song_queue.append(song_title)
        print(song_queue)
        if(not ctx.voice_client): #join voice channel if not already joined
            await ctx.send("joining voice channel")
            voiceChannel = discord.utils.get(ctx.guild.voice_channels)
            await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        file_found = False
        if not voice.is_playing():
            play_next_in_queue(ctx)
        
    else:
        await ctx.send("join a voice channel first")

@bot.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("leaving voice channel")
    else:
        await ctx.send("not in voice channel")

@bot.command(pass_context=True)
async def clear_songs(ctx):
    for filename in os.listdir('.'):
        if filename.endswith('.mp3'):
            print("removing: " + filename)
            os.remove(filename)

@bot.command(pass_context=True)
async def skip(ctx):
    print("skipping song")
    ctx.voice_client.stop()

def play_next_in_queue(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if len(song_queue) >= 1:
        song = song_queue[0]
        print("playing song: " + song)
        del song_queue[0]
        for filename in os.listdir('.'):  # youtube-dl gives it a weird name so do this so i can find the file
                if filename.startswith(song):
                    # if we find it then play it and queue up next song
                    voice.play(discord.FFmpegPCMAudio(filename),after=lambda e: play_next_in_queue(ctx))

@bot.command(pass_context=True)
async def current_queue(ctx):
    string = ''
    for i in song_queue:
        string += i + ', '
    await ctx.send(string)

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return

    if len(voice_state.channel.members) == 1:
        print("leaving due to inactivity")
        await voice_state.disconnect()




bot.run(private.discord_key)