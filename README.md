# TermTube

Clone the directory and run `./termtube.py -h` from the TermTube directory to get instructions on how to use the script.

This is a script that lets you watch Youtube videos on the command line!

This script now also gives you a personalised feed of youtube videos. It reads the channel names from a list that you pass as a variable and prints out the 3 latest videos of each channel. Use the `-f 'channel-list'` option to use this option. Make sure that the 'channel-list' file exists in the directory you're running the script from.

To download videos with this script, use the `-d` option. Check the help menu for more details.

Playlists can be downloaded using the `-p` option. Check the help menu for more details.

To get RSS links for your favourite channels, use the `-rss` option.

It uses the `python-mpv` library to do this. There is also an option in the script that lets you use the already installed `mpv` in your system which has been commented out. It also uses the `youtube-search` library. Take a look at the script to know what you need to have installed before you can run it.

More features will be added soon!

# Examples:

`termtube 3 'call me kevin'`     This prints out 5 videos with the query 'call me kevin' and asks you which one you want to play. If the number isn't specified, it prints out 5 videos. The max is 18.

`termtube -f sublist`           This prints out the latest 3 videos from the channels in the file 'subfile' and asks you which one you want to play.

`termtube -d 'call me kevin'`    This prints out videos with the query 'call me kevin' adn asks you which one you want to download.

`termtube -p 'call me kevin'`    This prints out playlists for you to download.

`termtube -rss sublist`          This gets rss feed links for all the channels in the file 'subfile'

# Donations
Consider Donating if you're feeling generous :)
[![PayPal Donation Link](blue.svg "PayPal Donation Link")](https://www.paypal.me/feedmeplsthx)
