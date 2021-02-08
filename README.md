# Auto Twitch Drops

This program runs and controls a browser to automatically watch twitch drops.

## Setup  

To run the code, you must install the requirement

```bash
pip install -r requirements.txt
```

Enter your username, password in the `config.py` file

Inside of this `config.py` file, you need to modify the streamerURLs and AlreadyGot values to tell the program what to visit and if to skip certain streamers if you already have the drop

```
username = Enter your username here
password = Enter your password here

streamerURL = 'Streamer Channel link 1',
'Streamer Channel link 2',
'Streamer Channel link 3',
...,

AlreadyGot = [False, 	Tells the program that you do not have this drop and it should visit this streamer (link 1)
True,					Tells the program that you have this drop and do not visit this streamer (link 2)
False,					Tells the program that you do not have this drop and it should visit this streamer (link 3)
...,]					
```
__NOTE: AFTER EDITING CONFIG.PY, DO NOT COMMIT THE FILE__

__NOTE: This program does not upload or store your username/password anywhere else. I will never get any passwords from this program.

## Execute

To execute the bot, run the following in your terminal

You must provide a string of the game you want to look for. This is how the bot determines if the streamer is playing a specific game.

```
python3 autotwitch.py -g rust		This will tell the program to see if the streamer is playing rust

OR

autotwitch.py -g rust
```

 
