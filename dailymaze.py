from selfbot import send_message, send_file
from datetime import datetime
import os, time, random

i = 1

def daily_maze(channel_id):
    global i
    size = random.randint(32,64)
    os.system(f"./maze {size} maze.png")
    send_message(channel_id, f"daily maze #{i}")
    send_file(channel_id, "./maze.png")
    i += 1

while True:
    now = datetime.now()
    if now.hour == 9 and now.minute == 22:
        daily_maze(754316521358098483)
        time.sleep(60)
    time.sleep(4)
