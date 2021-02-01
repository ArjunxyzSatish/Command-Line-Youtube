#!/bin/env python3

import os
import uyts
import youtube_dl
import requests
from bs4 import BeautifulSoup
import mpv
import sys

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)

videos = []

def help():
    print("""
    Usage: termtube [OPTIONS] [QUERY]/[Channel List]

    Options:
     -h, --help             prints this help message
      n                     where n is the number of video results you want displayed
     -l, --link             copies the link of the youtube video to your clipboard
     -f, --file             specify the file with the list of channels on it and it fetches the 3 most recent videos of these channels.
     -d, --download         This option gives you a list of 10 videos based on your query and lets you pick one to download.
     -p, --playlist         This option gives you a list of playlists based on your query and lets you pick one to download.
     -rss, --get-rss        specify the file with the list of channels on it and it fetches the RSS links of these channels and stores them in another file. It will ask you to name this new file.

    Query:
     This is what the script looks for on YouTube. Please enter it in quotes, eg. 'Messi vs Ronaldo'

    Channel List:
     This is the file containing the names of the channels whose videos you want in your feed. Make sure you have only one channel per line. The program prints the latest 3 videos for each channel. Comments can be added in this file with '#'.

     If this is used with the -rss or --get-rss option, it gets the RSS links of these channels and stores them in a new file in the same directory. It will ask you to name the new file containing the RSS links of these channels.

     Examples:
     termtube 3 'call me kevin'     This prints out 5 videos with the query 'call me kevin' and asks you which one you want to play. If the number isn't specified, it prints out 5 videos. The max is 18.

     termtube -f sublist            This prints out the latest 3 videos from the channels in the file 'subfile' and asks you which one you want to play.

     termtube -d 'call me kevin'    This prints out videos with the query 'call me kevin' adn asks you which one you want to download.

     termtube -p 'call me kevin'    This prints out playlists for you to download.

     termtube -rss sublist          This gets rss feed links for all the channels in the file 'subfile'
""")


def playlistSearch(query, num):
    search = uyts.Search(query)
    for res in search.results:
        if res.resultType == 'playlist':
            videos.append({'title':res.title, 'url':'https://www.youtube.com/playlist?list='+res.id, 'creator': res.author, "length":res.length, 'type':res.resultType})
            if len(videos) == num:
                break

def videoSearch(query, num):
    search = uyts.Search(query)
    for res in search.results:
        if res.resultType == 'video':
            videos.append({'title':res.title, 'url':'https://www.youtube.com/watch?v='+res.id, 'creator': res.author, "length":res.duration, "type":res.resultType})
            if len(videos) == num:
                break

def downloadVideo(choice):
    chosenVideo = videos[int(choice) - 1]
    url = chosenVideo['url']

    if chosenVideo['type'] == 'playlist':
        ydl_opts = {
        'format': 'best',
    }

    else:
        ydl_opts = {
        'format': 'best',
        'outtmpl': chosenVideo['title'],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)


def getRSS(channelFile):
    RSSlinks = []
    with open(channelFile, 'r') as file:
        listOfChannels = file.readlines()
        for channel in listOfChannels:
            if channel[0] != '#':
                search = uyts.Search(channel)
                for res in search.results:
                    if res.resultType == 'channel':
                        channelID = res.id
                        channelName = res.title
                        RSSlinks.append({"creator":channelName, "link":"https://www.youtube.com/feeds/videos.xml?channel_id="+channelID})
                    break
    return RSSlinks

def getVideosFromChannel(channel, num):
    search = uyts.Search(channel)
    for res in search.results:
        if res.resultType == 'channel':
            channelID = res.id
            channelName = res.title
            break

    url = "https://www.youtube.com/feeds/videos.xml?channel_id="+channelID
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    entries = soup.find_all("entry")
    number = int(num)
    for i in range(number):
        videos.append({"title":entries[i].title.text, "url":entries[i].link.attrs["href"], "creator": channelName})

def playVideo(choice):
    chosenVideo = videos[int(choice) - 1]
    print("Playing: " + chosenVideo['title'])
    chosenVideoLink = chosenVideo['url']
    player.play(chosenVideoLink)
    player.wait_for_playback()

def getLink(choice):
    chosenVideo = videos[int(choice) - 1]
    chosenVideoLink = chosenVideo['url']
    if sys.platform == 'linux':
        cmd = "echo "+chosenVideoLink+" | xclip -sel clip"
        os.system(cmd)

    elif sys.platform == 'darwin':
        cmd = "echo "+chosenVideoLink+" | pbcopy -sel clip"
        os.system(cmd)

    elif sys.platform == 'win32':
        cmd = "echo "+chosenVideoLink+" | clip"
        os.system(cmd)

    print("The chosen video's link has been copied to the system clipboard")

def display(videoList):
    for x, video in enumerate(videos):
        print(f'{x+1}. ' + videos[x]['title'] + ' : ' + videos[x]['creator'] + " (" + videos[x]['length'] + ")")

def displayScraped(videoList):
    for x, video in enumerate(videos):
        print(f'{x+1}. ' + videos[x]['title'] + ' : ' + videos[x]['creator'])


if len(sys.argv) == 1:
    help()

elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
    help()

elif sys.argv[1] == '-f' or sys.argv[1] == '--file':
    subfile = sys.argv[2]
    print("Looking for videos from channels in '" + subfile + "' file..")
    with open(subfile, 'r') as file:
        listOfChannels = file.readlines()
        for channel in listOfChannels:
            if channel[0] != '#':
                getVideosFromChannel(channel, 3)

    displayScraped(videos)
    ch = input('Enter Choice: ')
    try:
        getLink(ch)
    except:
        print("Couldn't copy the link to clipboard. Make sure you have the right command line tools installed. You can check what tools this script uses for your OS in the help menu.")
    playVideo(ch)

elif sys.argv[1] == '-rss' or sys.argv[1] == '--get-rss':
    subfile = sys.argv[2]
    print("Getting RSS feed links for channels in '" + subfile + "' file..")
    RSSlinks = getRSS(subfile)
    RSSfile = input("Enter the name of the file you want to store the links in: ")
    with open(RSSfile, 'a') as file:
        for channel in RSSlinks:
            file.writelines(channel['creator'] + " : " + channel['link'] + "\n")

elif sys.argv[1] == '-d' or sys.argv[1] == '--download':

    searchQuery = sys.argv[2]
    number = input("Enter the number of videos you want to get back (max: 18): ")

    videoSearch(searchQuery, number)

    display(videos)
    ch = input('Enter Choice: ')
    downloadVideo(ch)

elif sys.argv[1] == '-p' or sys.argv[1] == '--playlist':

    searchQuery = sys.argv[2]
    number = input("Enter the number of playlists you want to get back (max: 15): ")

    playlistSearch(searchQuery, number)

    display(videos)
    ch = input('Enter Choice: ')
    downloadVideo(ch)

elif sys.argv[1] == '-c' or sys.argv[1] == '--channel':
    searchQuery = sys.argv[2]
    number = input("Enter the number of videos you want to get back (max: 15): ")
    getVideosFromChannel(searchQuery, number)

    displayScraped(videos)
    ch = input("Enter choice: ")
    playVideo(ch)

elif sys.argv[1] == '-l' or sys.argv[1] == '--link':

    searchQuery = sys.argv[2]
    number = input("Enter the number of videos you want to get back (max: 15): ")

    videoSearch(searchQuery, number)

    display(videos)
    ch = input('Enter Choice: ')
    try:
        getLink(ch)
    except:
        print("Couldn't copy the link to clipboard. Make sure you have the right command line tools installed. You can check what tools this script uses for your OS in the help menu.")

else:
    try:
        number = int(sys.argv[1])
        searchQuery = sys.argv[2]
    except:
        print("Number of results not provided. Defaulting to 5...")
        number = 5
        searchQuery = sys.argv[1]

    videoSearch(searchQuery, number)

    display(videos)
    ch = input('Enter Choice: ')
    playVideo(ch)
