import discord
import dotenv
import os
from discord.ext import commands


#sheeesh
dotenv.load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("bot is ready")

@client.command()
async def test(ctx):
    await ctx.send("jordan is a dumbass")


client.run(os.environ.get('token'))