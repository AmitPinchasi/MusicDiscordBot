import os
import discord
from discord.ext import commands
import youtube_dl
import os
import datetime
import schedule
import time

#מתכנת: עמית פנחסי

now = datetime.datetime.now()
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="מעירה אנשים ב12"))
    channel = client.get_channel(777209009266098176)
    await channel.send('צופה בך')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'היי {member.name}, ברוכים הבאים לשרת שלנו! אני הביגבן ואני אשמח להעיר אותך בשרת'
    )
"""
@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
            return
  if '<@!873126822563434528>' in msg or '<@873126822563434528>' in msg:
            await message.channel.send(
                message.author.mention + ' שלום! אני הביגבן רוצה שהעיר אותך? * לוחש לול * ')
"""
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("תחכה שהשיר יגמר או שכתוב את הפקודה !stop")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='גאנג דייט')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("הבוט לא מחובר לחדר.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("אין כרגע קטע שמע לעשות לו פאוז.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("הקטע שמע לא על פאוז מטומטם")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def bigben(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='גאנג דייט')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("bigben.mp3"))


schedule.every().day.at("00:00").do(bigben)
schedule.every().day.at("12:00").do(bigben)

token = os.environ['token']
print(token)
client.run(token)
