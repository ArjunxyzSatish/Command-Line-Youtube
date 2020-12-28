# TermTube

Clone the directory and run `./termtube.py -h` from the TermTube directory to get instructions on how to use the script.

This is a script that lets you watch Youtube videos on the command line! 

This script now also gives you a personalised feed of youtube videos. It reads the channel names from a list that you pass as a variable and prints out the 3 latest videos of each channel. Use the `-f 'channel-list'` option to use this option. Make sure that the 'channel-list' file exists in the directory you're running the script from.

You can also get RSS links for your favourite channels using the `-rss` option.

It uses the `python-mpv` library to do this. There is also an option in the script that lets you use the already installed `mpv` in your system which has been commented out. It also uses the `youtube-search` library. Take a look at the script to know what you need to have installed before you can run it. 

