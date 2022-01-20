# discord api
import discord
from discord.ext import commands
from discord.ui import button
from discord import Option

# .env configuration
from dotenv import load_dotenv
load_dotenv()
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("bot is ready")

@client.slash_command(guild_ids=[821868761329696769])
async def test(ctx):
    await ctx.respond("test")

@client.slash_command(guild_ids=[821868761329696769])
async def test2(ctx):
    em = discord.Embed(title="Covid Stats", description="temp", color=discord.Color.teal())
    em.add_field(
        name="Total Number of Positive Cases", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="Total Number of Student Cases", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="Total Number of Teacher Cases", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="Total Number of Staff Cases", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="New Cases in the Past Week", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="Positivity Rate", 
        value="temp",
        inline = False
    )
    em.add_field(
        name="temp", 
        value="temp",
        inline = False
    )
    await ctx.respond(embed=em)



client.run(os.getenv("TOKEN"))