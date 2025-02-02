import discord, random, subprocess, os
from discord.ext import commands

# Read bot token from file
with open(os.path.expanduser("~/bot_tokens/SlashMaze_token"), 'r') as f:
    token = f.readline().strip()

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def separate(input_string):
    return [word.strip() for word in input_string.split()]

async def generate_maze(interaction_or_message, size_input=None):
    # Determine maze size
    parts = separate(size_input) if size_input else []
    num = int(parts[0]) if parts and parts[0].isdigit() else random.randint(20, 40) * 2 + 1
    num = num if num % 2 != 0 else num + 1  # Ensure odd size

    output_file = "maze.png"
    try:
        subprocess.run(["./maze", str(num), output_file], check=True)

        # Send the maze image
        if isinstance(interaction_or_message, discord.Interaction):
            await interaction_or_message.response.send_message(file=discord.File(output_file))
        else:
            await interaction_or_message.channel.send(file=discord.File(output_file))
    except subprocess.CalledProcessError as e:
        error_msg = f"The maze generator had an error: {e}"
        print(error_msg)
        if isinstance(interaction_or_message, discord.Interaction):
            await interaction_or_message.response.send_message(error_msg)
        else:
            await interaction_or_message.channel.send(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        if isinstance(interaction_or_message, discord.Interaction):
            await interaction_or_message.response.send_message(error_msg)
        else:
            await interaction_or_message.channel.send(error_msg)
        if "Large" in str(e):
            size_error_msg = "This happened because you tried to generate a maze too big to be an image on Discord."
            if isinstance(interaction_or_message, discord.Interaction):
                await interaction_or_message.response.send_message(size_error_msg)
            else:
                await interaction_or_message.channel.send(size_error_msg)

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
                "Type `!maze <size>` to generate a maze of that size.\n"
                "If no size is provided, a random maze size will be generated.\n"
                "The maze starts at the red pixel and ends at the black one.\n"
                "Example: `!maze 41` generates a 41x41 maze.\n"
            )
            await message.channel.send(help_message)
            return

        # Extract size input from the message
        size_input = parts[1] if len(parts) > 1 else None
        await generate_maze(message, size_input)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# Run the bot
bot.run(token)
