import discord, os, random
from discord.ext import commands
from maze import export

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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
            help_message = ("Type -maze <size> to generate a maze of that size.\n"
                            "If no size is provided, a random maze size will be generated.\n"
                            "The maze starts at the red pixel and ends at the black one. Follow the blue path to navigate.\n"
                            "Example: -maze 41 generates a 41x41 maze")
            await message.channel.send(help_message)
            return
        if len(parts) > 1 and parts[1].isdigit():
            num = int(parts[1])
        elif parts[0] != "":
            num = random.randint(20, 40) * 2 + 1
        if num > 1000:
            num = random.randint(20, 40) * 2 + 1
        if num % 2 == 0:
            num += 1
        try:
            await message.channel.send(file=discord.File(export(num)))
        except:
            num = random.randint(20, 40)
            await message.channel.send(file=discord.File(export(num * 2 + 1)))
    await bot.process_commands(message)

bot.run(token)
