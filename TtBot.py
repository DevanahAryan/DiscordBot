import os
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions
from googlesearch import search
import discord.utils
import profile
import wikipedia
import random
import spotify
import asyncio
# from googleapiclient.discovery import build
import requests
# import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix='--', intents=intents)


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"{member.name}, WELCOME TO {member.guild}  HOPE YOU ENJOY YOUR STAY")


@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    await client.process_commands(message)


@client.command(name='totaluser', help="gives the total count of user in the srever")
async def totaluser(context):
    dtu_guild = context.guild
    await context.channel.send(f"```total member in this server::{dtu_guild.member_count}```")


@client.command(name='usercount', help="gives the count of online,offline,idle and dnd strength")
async def usercount(context):
    dtu_guild = context.guild
    online = 0
    idle = 0
    offline = 0
    dndd = 0

    for m in (dtu_guild.members):
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        elif (m.status) == discord.Status.idle:
            idle += 1
        elif (m.status) == discord.Status.dnd:
            dndd += 1

    embed = discord.Embed(
        title="Member Status",
        description=f"**Online:** {online}\n**Idle:** {idle}\n**Offline:** {offline}\n**Do Not Disturb:** {dndd}",
        colour=discord.Colour.random())
    await context.channel.send(embed=embed)


@client.command(name='google', help="helps to perform google serach commands :: --google <x> <query>")
async def google(context, x: int, query):
    query = query.strip()
    for i in search(query, lang='en', num=10, stop=x, pause=5):
        await context.channel.send(f'{i}')


@client.command(help="help you mute a member in a particular channel commands:: --mute <username>")
@commands.has_permissions(manage_channels=True)
@commands.has_guild_permissions(ban_members=True)
async def mute(ctx, member: discord.Member):
    channel = ctx.channel
    perms = channel.overwrites_for(member)
    perms.send_messages = False
    await channel.set_permissions(member, overwrite=perms, reason="Muted!")
    await ctx.send(f"{member} has been muted.")


@client.command(help="you can unmute a muted user in a particular channel commands:: --unmute <username>")
@commands.has_permissions(manage_channels=True)
@commands.has_guild_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member):
    channel = ctx.channel
    perms = channel.overwrites_for(member)
    perms.send_messages = True
    await channel.set_permissions(member, overwrite=perms, reason="unmute!")
    await ctx.send(f"{member} has been unmuted.")


@client.command()
@commands.has_permissions(manage_channels=True)
@commands.has_guild_permissions(ban_members=True)
async def lock(ctx, channel: discord.TextChannel, reason: str):
    my_list = channel.changed_roles

    if not channel and reason:
        await ctx.send("Channel mention & reason must be provided.")
    else:
        for i in my_list:
            await channel.set_permissions(i, send_messages=False, read_messages=True)
        await ctx.send(f"{channel.mention} has been locked.\nReason: {reason}.")


@client.command()
@commands.has_permissions(manage_channels=True)
@commands.has_guild_permissions(ban_members=True)
async def unlock(ctx, channel: discord.TextChannel, reason: str):

    my_list = channel.changed_roles

    if not channel and reason:
        await ctx.send("Channel mention & reason must be provided.")
    else:
        for i in my_list:
            await channel.set_permissions(i, send_messages=True, read_messages=True)
        await ctx.send(f"{channel.mention} has been unlocked.")


@client.command()
@commands.has_permissions()
async def profile(ctx, member: discord.Member):
    try:
        stat = member.status
        mobstat = member.mobile_status
        username = member.name
        my_list = member.roles
        embed = discord.Embed(
            title="member info",
            description=f"**NickName:    ** {member.display_name}\n**UserName:    **{username}\n**status:    ** {stat}\n**mobile status:    ** {mobstat}\n**list of role:    **{my_list}",
            colour=discord.Colour.random())

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("py\nplease try again")


@client.command()
async def define(ctx, *, query: str):

    defination = wikipedia.summary(
        query, sentences=5, auto_suggest=True, redirect=True)
    embed = discord.Embed(
        title="search result.............",
        description=f"{defination}",
        colour=discord.Colour.random())
    await ctx.send(embed=embed)


@client.command()
async def yt(ctx, *, search):
    with open(r"D:\python\discord_bot\apikey.txt", "r") as f:
        api_key = f.readlines()[0]
    yout = build('youtube', 'v3', developerKey=api_key)
    request = yout.search().list(part="snippet", q=search, maxResults=1)
    response = request.execute()
    ide = response['items'][0]['id']['videoId']
    await ctx.send("https://www.youtube.com/watch?v="+ide)


@client.command()
async def rd(ctx, i: int):
    for x in range(i):
        await ctx.send(f"{x+1} roll = {random.randint(1,6)}")


@client.command()
async def SP(ctx, member: discord.Member):
    try:
        for activity in member.activities:

            if isinstance(activity, discord.activity.Spotify):
                await ctx.send(f"```{member} is listening to {activity.title}\nby {activity.artist}\nduration {activity.duration}````")

    except Exception as e:
        await ctx.send("py\nplease try again")


@client.command()
@commands.has_permissions(ban_members=True)
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild
    #perms = discord.Permissions(send_messages=False, read_messages=True)
    role = await guild.create_role(name="Muted",)
    await member.add_roles(role)
    for channel in ctx.guild.channels:
        await channel.set_permissions(role, send_messages=False, read_messages=True)

    embed = discord.Embed(
        title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    embed.add_field(name="time left for the mute:",
                    value=f"{time}{d}", inline=False)
    await ctx.send(embed=embed)

    if d == "s":
        await asyncio.sleep(time)

    if d == "m":
        await asyncio.sleep(time*60)

    if d == "h":
        await asyncio.sleep(time*60*60)

    if d == "d":
        await asyncio.sleep(time*60*60*24)

    await member.remove_roles(role)

    embed = discord.Embed(title="unmute (temp) ",
                          description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)

    return


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


@client.command()
@commands.has_permissions(ban_members=True)
async def k(ctx, member: discord.Member, *, reason=None):
    try:
        mem = ctx.guild.get_member(member.id)
        await mem.kick()
        await ctx.send(f"```{member.name} was kicked from {ctx.guild.name}```")
    except Exception as e:
        await ctx.send("try again!!!!")


@client.command()
async def action(ctx,member: discord.Member, *, query):
    apikey = "PQZC768KUA6F"  
    r = requests.get(
        "https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (query, apikey, 10))
    t=0
    t=random.randint(0,9)
    print(t)
    gifs = json.loads(r.content)
    urls = gifs['results'][t]['url']
    
    await ctx.send(urls)

# @client.command#error


client.run("BOT TOKEN")
