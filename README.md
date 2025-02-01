# mazebot

### to compile:

install libpng package
```
sudo pacman -S libpng

sudo apt install libpng-dev
```
then compile it:
```
gcc -o maze maze.c -lpng
```
### to run:
```
python3 mazebot.py 
```
or
```
python3 slashbot.py
```

mazebot is a server discord bot that accepts dash commands

slashbot accepts slash commands (is a user application)

keep tokens in ~/bot_tokens

thanks stigl for original idea and source code (which i converted into python)

https://github.com/stiglcz/maze-png

thanks semblanceofsense for solver code

https://github.com/SemblanceOfSense/mazesolver
