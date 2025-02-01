import discord
from discord.ext import commands
import random
import os
from maze import export

# Discord bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Read bot token from file
with open("./bot_token", 'r') as f:
    token = f.readline().strip()

def separate(input_string):
    return [word.strip() for word in input_string.split(' ')]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "-maze" in message.content.lower():
        parts = separate(message.content.lower())
        if "help" in parts[1]:
            help_message = (
                "Type `-maze <size>` to generate a maze of that size.\n"
                "If no size is provided, a random maze size will be generated.\n"
                "The maze starts at the red pixel and ends at the black one.\n"
                "Example: `-maze 41` generates a 41x41 maze."
            )
            await message.channel.send(help_message)
            return

        # Determine maze size
        if len(parts) > 1 and parts[1].isdigit():
            num = int(parts[1])
        else:
            num = random.randint(20, 40) * 2 + 1  # Ensure odd size

        # Ensure maze size is odd
        if num % 2 == 0:
            num += 1

        try:
            # Generate and send the maze
            maze_file = export(num, False)
            await message.channel.send(file=discord.File(maze_file))
        except Exception as e:
            print(f"Error generating maze: {e}")
            await message.channel.send("tilly made skill issu.e")

    await bot.process_commands(message)

# Run the bot
bot.run(token)