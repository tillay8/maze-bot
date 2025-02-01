import discord
from discord.ext import commands
import random
import os
import subprocess

# Discord bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Read bot token from file
with open("os.path.expanduser(~/bot_tokens/TilleyHelper_token", 'r') as f:
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

    if "-mase" in message.content.lower():
        parts = separate(message.content.lower())
        verbose = "-v" in parts

        if "help" in parts[1]:
            help_message = (
                "Type `-maze <size>` to generate a maze of that size.\n"
                "If no size is provided, a random maze size will be generated.\n"
                "The maze starts at the red pixel and ends at the black one.\n"
                "Example: `-maze 41` generates a 41x41 maze.\n"
                "Add `-v` for verbose output."
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
            output_file = "maze.png"
            if verbose:
                # Start the C program with verbose mode
                process = subprocess.Popen(
                    ["./maze", str(num), output_file, "-v"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Stream output line by line
                for line in process.stdout:
                    await message.channel.send(line.strip())

                # Wait for the process to finish
                process.wait()

                # Check for errors
                if process.returncode != 0:
                    error_output = process.stderr.read()
                    await message.channel.send(f"Error: {error_output}")
            else:
                subprocess.run(["./maze", str(num), output_file], check=True)

            # Send the maze image
            await message.channel.send(file=discord.File(output_file))
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send(f"Error: {e}")

    await bot.process_commands(message)

# Run the bot
bot.run(token)
