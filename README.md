# mazebot

### to use:
mazebot is both a server and user application. 

- If added to a server, any user in that server can use slash commands to make the maze, or dash commands. an example dash command is `-maze 64`

- If added to a user, the user may use slash commands (application commands) anywhere to make a maze. If they have the external application permission in that server, it will render to all users.

Discord has a maze size limit of around 7550. (Which corresponds to about 10 megabyte file). It will still attempt to generate the maze if it is larger, but it will not be sent. 

If you try to generate a stupidly large maze you will just instantly segfault it but it has good error correction so it wont cause any problems. 


### to compile (only needed if you want to host this bot yourself):

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

keep tokens in ~/bot_tokens



### dailymaze
dailymaze is used for making a daily maze in a server where the bot cannot be added using a self bot (against discord tos)

because it is against discord tos, it uses my **private** self-bot library to send messages. contact me on discord to get it. 

### credits

thanks stigl for original idea and source code (which i converted into python and then into C)

https://github.com/stiglcz/maze-png

thanks semblanceofsense for solver code

https://github.com/SemblanceOfSense/mazesolver

thanks sce for compiling it into an exe for windows
