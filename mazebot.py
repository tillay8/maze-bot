import discord, subprocess, os, time
from datetime import datetime
from discord.ext import commands

with open(os.path.expanduser("~/bot_tokens/SlashMaze_token"), 'r') as f:
    token = f.readline().strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

output_file = "maze.png"

async def try_to_send(operation, message=None, file=None):
    if isinstance(operation, discord.Interaction):
        if not operation.response.is_done():
            if file:
                await operation.response.send_message(file=discord.File(file))
            else:
                await operation.response.send_message(message)
        else:
            if file:
                await operation.followup.send(file=discord.File(file))
            else:
                await operation.followup.send(message)
    else:
        if file:
            await operation.reply(file=discord.File(file))
        else:
            await operation.reply(message)

def separate(input_string):
    return input_string.split()

def log(message):
    with open("./mazebot.log", "a") as f:
        f.write(f"\n{message}")

async def generate_maze(operation, size_input=None):
    if not size_input or not size_input[0].lstrip('f').isnumeric():
        await try_to_send(operation, "Please enter an integer for size!")
        log(f"\033[31mUser did not input an integer for size: \033[34m{size_input}\033[0m")
        return

    force = size_input[0].startswith('f')
    if force: log("\033[32mUser is forcing maze generation\033[0m")
    num = int(size_input[0].lstrip('f'))
    num = num if num % 2 != 0 else num + 1

    if force or num <= 7800:
        try:
            if isinstance(operation, discord.Interaction) and num > 800 and not operation.response.is_done():
                if force:
                    await try_to_send(operation, "You're bypassing the filesize limit. If you cause an error thats ur fault")
                else:
                    await try_to_send(operation, "You put in big maze size. It will take a bit")
                log("\033[33mSent wait message.\033[0m")

            start_time = time.time()
            subprocess.run(["./maze", str(num), output_file], check=True)
            generation_time = time.time() - start_time

            maze_size = os.path.getsize(output_file) / (1024 * 1024)
            log(f"Maze size: \033[31m{maze_size:.2f}\033[0m MB")
            log(f"Time to generate: \033[95m{generation_time:.2f}\033[0m seconds")
            if maze_size > 10:
                await try_to_send(operation, f"Maze was generated successfully but is too large to send ({round(maze_size)} MB)")
            else:
                await try_to_send(operation, file=output_file)
                log("Successfully sent maze image!")
                log(f"Time to send: \033[96m{round(10 * (time.time() - start_time)) / 10}\033[0m seconds")
        except subprocess.CalledProcessError as e:
            await try_to_send(operation, "Number was wayyyy too big. told ya so")
        except Exception as e:
            log(f"\033[91mShit went down in the \033[93mPython\033[91m program: {e}")
            await try_to_send(operation, "Too many requests! Try in a few seconds.")
    else:
        await try_to_send(operation, "You know full well that that size is too big.")
        log(f"\033[31muser number was too big\033[0m")

@bot.tree.command(name="maze", description="Generate a maze")
async def slash_maze(interaction: discord.Interaction, size: str = None):
    log(f"\n\033[96m{datetime.now().strftime("%-m/%-d/%y %H:%M:%S")}\033[0m")
    log(f"\n\033[92mslash\033[0m maze request received from \033[94m{interaction.user}\033[0m")
    await generate_maze(interaction, separate(size))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('-maze'):
        log(f"\n\033[96m{datetime.now().strftime("%-m/%-d/%y %H:%M:%S")}\033[0m")
        log(f"\033[93mdash\033[0m maze request received from \033[94m{message.author}\033[0m")
        await generate_maze(message, separate(message.content.lower())[1:])

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.tree.sync()

bot.run(token)
