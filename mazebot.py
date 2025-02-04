import discord, random, subprocess, os, time
from discord.ext import commands

# Read bot token from file
with open(os.path.expanduser("~/bot_tokens/SlashMaze_token"), 'r') as f:
    token = f.readline().strip()

insult_delay = 0.8

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def separate(input_string):
    return [word.strip() for word in input_string.split()]

async def generate_maze(ctx, size_input=None):
    # Determine maze size
    parts = separate(size_input) if size_input else []
    num = int(parts[0])
    num = num if num % 2 != 0 else num + 1  # Ensure odd size

    output_file = "maze.png"
    try:
        subprocess.run(["./maze", str(num), output_file], check=True)

        # Send the maze image
        file = discord.File(output_file)
        if isinstance(ctx, discord.Interaction):
            await ctx.response.send_message(file=file)
        else:
            await ctx.channel.send(file=file)

    except subprocess.CalledProcessError as e:
        error_msg = f"The maze generator had an error: {e}"
        print(error_msg)
        await send_response(ctx, error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        await send_response(ctx, error_msg)
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

async def send_response(ctx, message):
    if isinstance(ctx, discord.Interaction):
        await ctx.response.send_message(message)
    else:
        await ctx.channel.send(message)

@bot.tree.command(
    name="maze",
    description="Generate a maze"
)
async def slash_maze(interaction: discord.Interaction, size: str = None):
    await generate_maze(interaction, size)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('-maze'):
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
        # Extract size input from the message
        size_input = parts[1] if len(parts) > 1 else None
        try:
            await generate_maze(message, size_input)
        except Exception as e:
            await message.channel.send(e)

    # Replies to defend Sense's maze solver
    elif "Solution file" in message.content:
        time.sleep(insult_delay)
        await message.channel.send("skill issue <@1335044960898252830>")
        return
    elif "with a maze" in message.content:
        time.sleep(insult_delay)
        await message.channel.send("yeah, get it right")
        return
    elif "valid maze" in message.content:
        time.sleep(insult_delay)
        await message.channel.send("that maze is already solved you idiot")
        return
    elif "contain a maze" in message.content:
        time.sleep(insult_delay)
        await message.channel.send("bruh dont reply to random messages. they aint mazes")
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# Run the bot
bot.run(token)
