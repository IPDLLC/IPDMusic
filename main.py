import discord
import random
import json
from random import choices
from discord.ext import commands
from discord.utils import get
import youtube_dl
import sys
import shutil
import os

tokenjson = json.load(open('token.json'))
TOKEN = tokenjson['token']

BOT_PREFIX = ')'

bot = commands.Bot(command_prefix=BOT_PREFIX)

bot.remove_command('help')


@bot.command(pass_context=True)
async def stoprun(ctx):
    if ctx.message.author.id == 408387953233100810 or ctx.message.author.id == 287885666941927424:
        await ctx.send("Yes master, I shall. ***Slices head off body***")
        sys.exit()
    else:
        await ctx.send(random.choice(['Haha you thought', "bruh are u actually", "u big dum", 'lol no', 'u stink bad', 'thot-begone!']))
    
    

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title = "IPD Music Bot Commands",
        description = "All commands for the IPD music bot",
        color = discord.Color.dark_purple()
    )

    embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/677606304918798367/c817706c900aeab37a451c2b31b26a1b.png?size=128')
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    embed.add_field(name = "Play", value = "Plays a song from a youtube url\n`Usage: )play <url>`", inline = True)
    embed.add_field(name = "Stop", value = "Stops all currently playing songs and resets the Queue\n`Usage: )stop`", inline = True)
    embed.add_field(name = "Join", value = "Makes the bot join your current voice channel\n`Usage: )join`", inline = True)
    embed.add_field(name = "Leave", value = "Makes the bot leave the current voice channel\n`Usage: )leave`", inline = True)
    embed.add_field(name = "Queue", value = "Queues a song to play after the current song is done.\n`Usage: )queue <url>`", inline = True)
    embed.add_field(name = "Skip", value = "Skips the current song that is playing\n`Usage: )skip`", inline = True)
    embed.add_field(name = "Pause", value = "Pauses the current song that is playing\n`Usage: )pause`", inline = True)
    embed.add_field(name = "Resume", value = "Resumes the current song if it is paused\n`Usage: )resume`", inline = True)
    await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        pass

@bot.command(pass_context=True, aliases=['p', 'P'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR) [0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next song in queue")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No songs were queued after ending of last song\n")




    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but its being played")
        await ctx.send('ERROR: Music playing')
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)

    except:
        print("No old Queue folder")



        
    await ctx.send('Getting everything ready now')
    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet' : False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3' ,
            'preferredquality': '192',

        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    try:
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
    except:
        await ctx.send("Playing song")
    print("Playing\n")

@bot.command(pass_context=True, aliases=['pa', 'pas'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing, Failed pause")
        await ctx.send("Music not playing, Failed pause")

@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed Music")
        voice.resume()
        await ctx.send("Music resumed")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@bot.command(pass_context=True, aliases=['s', 'st'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("Music not playing, Failed stop")
        await ctx.send("Music not playing, Failed")


@bot.command(pass_context=True, aliases=['next'])
async def skip(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)


    if voice and voice.is_playing():
        print("Playing next song")
        voice.stop()
        await ctx.send("Playing next song")
    else:
        print("Music not playing, Failed skip")
        await ctx.send("Music not playing, Failed")

queues = {}

@bot.command(pass_context=True, aliases=['q', 'qu'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num
    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet' : False,
        'outtmpl' : queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3' ,
            'preferredquality': '192',

        }],
    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    await ctx.send("Adding song " + str(q_num) + " to the queue")
    
    print("Song added to queue\n")



bot.run(TOKEN)
