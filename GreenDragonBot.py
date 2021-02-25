import asyncio
import shutil
import os
from discord.utils import get
from discord.ext import commands
import discord
import random
import youtube_dl
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

players = {}

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def pie(ctx):
    await ctx.send('https://imgur.com/5gwzUe0')

@client.command()
async def ping(ctx):
    await ctx.send(f'bot ping: {round(client.latency * 1000)}ms')

@client.command(aliases =['8ball'])
async def _8Ball(ctx, *,question):
    responses=['no' ,'yes','most defintely']
    await ctx.send(f'{random.choice(responses)}')
    
@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voices.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")
    
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel;
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("cy@")

@client.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length -1
            try :
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued songs\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(_file_))
            song_path = os.path.abspatch(os.path.realpath("Queue")+"\\"+first_file)
            if length!=0:
                print("song done")
                print(f"queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                voice.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e:check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.25
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("no songs queued")
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("removed old song")
    except PermissionError:
        await ctx.send("Music currently playing")
        return
    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("NO OLD FOLDER")

    await ctx.send("working...")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("downloading audio")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file,"song.mp3")
    await ctx.send("Now playing ")
    voice.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e:check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.25

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing")
                      
@client.command(pass_context=True)
async def pause(ctx):
    voice = get(client.voice_clients,guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("paused")
    else:
        await ctx.send("nothing playing")

@client.command(pass_context=True)        
async def resume(ctx):
    voice = get(client.voice_clients,guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("resuming")
        
@client.command(pass_context=True)
async def skip(ctx):
    voice = get(client.voice_clients,guild=ctx.guild)
    queues.clear()
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("skipping")
queues = {}

@client.command(pass_context =True, aliases=['q'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num +=1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num +=1
        else:
            add_queue = False
            queues[q_num] = q_num
    queue_path = os.path.abspath(os.path.realpath("Queue")+f"\song(q_num).%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        ydl.download([url])
    await ctx.send("adding song" +str(q_num) + "to the queue")
client.run('*********************************************')
