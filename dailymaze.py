from selfbot import send_message, send_file
from datetime import datetime
import os, time, random

hour = int(input("Hour to send at: "))
min = int(input("Min to send at: "))
channel = inpit("Channel ID to send in: "))
i = int(input("Number to start at: "))

def daily_maze(channel_id):
    global i
    size = random.randint(32,64)
    os.system(f"./maze {size} maze.png")
    send_message(channel_id, f"daily maze #{i}")
    send_file(channel_id, "./maze.png")
    i += 1

while True:
    now = datetime.now()
    if now.hour == hour and now.minute == min:
        daily_maze(channel)
        time.sleep(60)
    time.sleep(4)
