import discord, random, subprocess, os
from discord.ext import commands

# Read bot token from file
with open(os.path.expanduser("~/bot_tokens/MazeSlash_token"), 'r') as f:
    token = f.readline().strip()

# Bot setup
bot = commands.Bot("prefix", intents=discord.Intents.none())

@bot.tree.command(
    name="maze",
    description="Generate a maze"
)
async def command(interaction: discord.Interaction, size: str = None):
    # Determine maze size
    parts = size.split() if size else []
    num = int(parts[0]) if parts and parts[0].isdigit() else random.randint(20, 40) * 2 + 1
    num = num if num % 2 != 0 else num + 1  # Ensure odd size

    output_file = "maze.png"
    try:
        # Generate the maze 
        subprocess.run(["./maze", str(num), output_file], check=True)

        # Send the maze image
        await interaction.response.send_message(file=discord.File(output_file))
    except:
        print("image size was probably too big")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# Run the bot
bot.run(token)
