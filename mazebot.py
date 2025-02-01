import discord, random, os, subprocess
from discord.ext import commands

# Discord bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Read bot token from file
with open(os.path.expanduser("~/bot_tokens/TilleyHelper_token"), 'r') as f:
    token = f.readline().strip()

def separate(input_string):
    return [word.strip() for word in input_string.split()]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "-mase" in message.content.lower():
        parts = separate(message.content.lower())
        if "help" in parts:
            help_message = (
                "Type `-maze <size>` to generate a maze of that size.\n"
                "If no size is provided, a random maze size will be generated.\n"
                "The maze starts at the red pixel and ends at the black one.\n"
                "Example: `-maze 41` generates a 41x41 maze.\n"
            )
            await message.channel.send(help_message)
            return

        # Determine maze size
        num = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else random.randint(20, 40) * 2 + 1
        num = num if num % 2 != 0 else num + 1  # Ensure odd size

        output_file = "maze.png"
        try:
            # Generate and send the maze
            subprocess.run(["./maze", str(num), output_file], check=True)

            # Send the maze image
            await message.channel.send(file=discord.File(output_file))
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            await message.channel.send(f"Error: {e}")
            if "Large" in str(e):
                await message.channel.send("This happened because you tried to generate a maze too big to be an image on Discord.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            await message.channel.send(f"Unexpected error: {e}")

    await bot.process_commands(message)

# Run the bot
bot.run(token)
