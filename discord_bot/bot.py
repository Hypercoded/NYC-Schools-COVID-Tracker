import discord
import dotenv
import os
from discord.ext import commands
from discord.ui import button
from discord import Option

dotenv.load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("bot is ready")

# import embeds.py
# message.send(embeds.all_time_stats(data, to, get, passed, in))
# TODO: calvin and williams can u guys create an embeds file where all the embeds can live, and the function
# TODO: will take in parameters for the values?
# what parameters do you want to use


@client.slash_command(guild_ids=[821868761329696769])
async def test(ctx):
    em1 = discord.Embed(title="Covid Stats", description="temp", color=discord.Color.teal())

    em1.add_field(
        name="Total Number of Positive Cases",
        value="temp, will set up when retrieving data is finished",
        inline=False,
    )
    em1.add_field(
        name="Total Number of Student Cases",
        value="temp",
        inline=False
    )
    em1.add_field(
        name="Total Number of Teacher Cases",
        value="temp",
        inline=False
    )
    #TODO: staff & teacher cases are combined into faculty cases
    em1.add_field(
        name="Total Number of Staff Cases",
        value="temp",
        inline=False
    )
    em1.add_field(
        name="New Cases in the Past Week",
        value="temp",
        inline=False
    )
    em1.add_field(
        name="Positivity Rate",
        value="temp",
        inline=False
    )
    em1.add_field(
        name="what else are we adding",
        value="temp",
        inline=False
    )
    await ctx.send(embed=em1)
client.run(os.environ.get('token'))
