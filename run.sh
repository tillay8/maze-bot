#!/bin/bash
gcc -o maze maze.c -lpng
if [ "$1" = "-n" ]; then
    nohup python3 mazebot.py &
elif ["$1" ="-k" ]; then
    pkill -f "python3 mazebot.py"
else
    python3 mazebot.py
fi
