# mazebot

### to compile:

install libpng package
```
sudo pacman -S libpng

sudo apt install libpng-dev
```
then compile the C code:
```
gcc -o maze maze.c -lpng
```
make to sure to install discord.py with
```
yay -S python-discord

sudo apt install python3-discord
```
### to run:
```
python3 mazebot.py 
```
or
```
./run.sh [-n]
```

mazebot is a discord bot that accepts dash and slash commands

keep tokens in ~/bot_tokens

thanks stigl for original idea and source code (which i converted into python and then into C)

https://github.com/stiglcz/maze-png

thanks semblanceofsense for solver code

https://github.com/SemblanceOfSense/mazesolver

originally meant for the salc1 discord but works by itself now
