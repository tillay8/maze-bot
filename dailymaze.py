from selfbot import send_message, send_file
from datetime import datetime
import os, time, random, sys

if len(sys.argv) != 5:
    print("python3 dailymaze.py hour min channel_id, start_num")
    sys.exit(0)
    
hour = int(sys.argv[1])
minute = int(sys.argv[2])
channel = sys.argv[3]
i = int(sys.argv[4])

def daily_maze(channel_id):
    global i
    size = random.randint(32,64)
    os.system(f"./maze {size} maze.png")
    send_message(channel_id, f"daily maze #{i}")
    time.sleep(2)
    send_file(channel_id, "./maze.png")
    i += 1

while True:
    now = datetime.now()
    if now.hour == hour and now.minute == minute:
        daily_maze(channel)
        time.sleep(60)
    time.sleep(4)
