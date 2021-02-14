# Auto Twitch Drops

This program runs and controls a browser to automatically watch twitch drops.

## Setup  

To run the code, you must install the requirement. You must have pip downloaded on your pc

```bash
pip install -r requirements.txt
```

Enter your username, password in the `config.py` file

Inside of this `config.py` file, you need to modify the streamerURLs values to tell the program what to visit  
Modify the `status.txt` to tell the bot to skip certain streamers if you already have the drop

```
config.py
_____________________
username = Enter your username here
password = Enter your password here

streamerURL = 'Streamer Channel link 1',
'Streamer Channel link 2',
'Streamer Channel link 3',
...,

status.txt
_____________________

f f f f f f f f f		F = do not have the drop, T = do have the drop.

3rd F correlates with the 3rd streamer.


```
__NOTE: AFTER EDITING CONFIG.PY, DO NOT COMMIT THE FILE__

__NOTE: This program does not upload or store your username/password anywhere else. I will never get any passwords from this program.__

## Execute

To execute the bot, run the following in your terminal

You must provide a string of the game you want to look for. This is how the bot determines if the streamer is playing a specific game.

```
python3 autotwitch.py -g rust		This will tell the program to see if the streamer is playing rust

OR

autotwitch.py -g rust
```

### Parameters  

```
-h			Parameter Help
-g			Tells the bot what game to search for. example (Single Word Game) -g rust. (multi-word game) -g "Tom Clancy's Rainbow Six Siege"
-t			Tells the bot how long to watch a stream for.  DEFAULT WILL WATCH UNTIL THE PROGRAM CLOSES
-l 			Will override the break function and loop through streamers even if the drop has been reported as True
```

__NOTE:	YOU MUST PUT THE EXACT GAME NAME IN AS IS SHOWN ON THE STREAM.__

## Contact Information
Joseph D Cantrell
JosephCantrell@josephdcantrell.com
 
