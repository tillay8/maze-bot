import discord, random, os
from discord.ext import commands
from discord import app_commands
from maze import export

with open("./mazebot_token", 'r') as f:
    token = f.readline().strip()

bot = commands.Bot("prefix", intents=discord.Intents.none())

def separate(input_string):
    return [word.strip() for word in input_string.split(' ')]

@bot.tree.command(
    name="maze",
    description="Generate a maze"
)
async def command(interaction: discord.Interaction, size: str = None):
    parts = separate(size if size else "")
    if len(parts) > 0 and parts[0].isdigit() and int(parts[0]) <= 256:
        num = int(parts[0])
    else:
        num = random.randint(40, 80)
    if num % 2 == 0:
        num += 1
    try:
        await interaction.response.send_message(file=discord.File(export(num)))
    except:
        await interaction.response.send_message("something really dumb just happenned")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(token)
