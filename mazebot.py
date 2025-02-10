import discord
import subprocess
import os
import time
from discord.ext import commands

# Read bot token from file
with open(os.path.expanduser("~/bot_tokens/SlashMaze_token"), 'r') as f:
    token = f.readline().strip()

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

wait_message = "matte kudasai! >.<"
def separate(input_string):
    return input_string.split()

async def generate_maze(operation, size_input=None):
    if not size_input or not size_input[0].isnumeric():
        message = "Please enter an integer for size!"
        # Send the initial response to the interaction
        if isinstance(operation, discord.Interaction):
            # Ensure we only send one response
            if not operation.response.is_done():
                await operation.response.send_message(message)
        else:
            await operation.channel.send(message)
        print("\033[31mUser did not input an integer for size\033[0m")
        return

    num = int(size_input[0])
    num = num if num % 2 != 0 else num + 1

    output_file = "maze.png"
    try:
        # Only send the wait message if the maze width is greater than 512
        if isinstance(operation, discord.Interaction) and num > 800 and not operation.response.is_done():
            await operation.response.send_message(wait_message)
            print("\033[33mSent wait message.\033[0m")

        start_time = time.time()
        subprocess.run(["./maze", str(num), output_file], check=True)
        generation_time = time.time() - start_time

        maze_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        print(f"Maze size: \033[31m{maze_size:.2f}\033[0m MB" if maze_size > 10 else f"Maze size: \033[92m{maze_size:.2f}\033[0m MB")
        print(f"Time to generate: \033[95m{generation_time:.2f}\033[0m seconds")

        if maze_size > 10:
            size_warning = f"Maze was generated successfully but is too large to send ({round(maze_size)} MB)"
            if isinstance(operation, discord.Interaction):
                # If the interaction was already responded to, we can only use followup
                if not operation.response.is_done():
                    await operation.response.send_message(size_warning)
                else:
                    await operation.followup.send(size_warning)
            else:
                await operation.reply(size_warning)
            return

        # Send the maze image after successful generation
        start_time = time.time()
        if isinstance(operation, discord.Interaction):
            if not operation.response.is_done():
                await operation.response.send_message(file=discord.File(output_file))  # Send initial message
            else:
                await operation.followup.send(file=discord.File(output_file))  # Send follow-up if initial response is done
        else:
            await operation.reply(file=discord.File(output_file))  # For non-interaction messages

        print("Successfully sent maze image!")
        print(f"Time to send: \033[96m{round(10*(time.time() - start_time))/10}\033[0m seconds")
    except subprocess.CalledProcessError as e:
        error_msg = f"shit went down in the C program: {e}"
        print(error_msg)
        if isinstance(operation, discord.Interaction):
            if not operation.response.is_done():
                await operation.response.send_message(error_msg)
            else:
                await operation.followup.send(error_msg)
        else:
            await operation.reply(error_msg)
    except Exception as e:
        error_msg = f"shit went down in the Python program: {e}"
        print(error_msg)
        if isinstance(operation, discord.Interaction):
            if not operation.response.is_done():
                await operation.response.send_message(error_msg)
            else:
                await operation.followup.send(error_msg)
        else:
            await operation.channel.send(error_msg)


@bot.tree.command(name="maze", description="Generate a maze")
async def slash_maze(interaction: discord.Interaction, size: str = None):
    print(f"\n\033[92mslash\033[0m maze request received from \033[94m{interaction.user}\033[0m")
    await generate_maze(interaction, separate(size))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('-maze'):
        print(f"\n\033[93mdash\033[0m maze request received from \033[94m{message.author}\033[0m")
        await generate_maze(message, separate(message.content.lower())[1:])

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.tree.sync()

# Run the bot
bot.run(token)
