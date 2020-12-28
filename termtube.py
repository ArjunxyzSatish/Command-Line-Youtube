#!/bin/env python

import uyts
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
     -f, --file             specify the file with the list of channels on it and it fetches the 3 most recent videos of these channels.
     -rss, --get-rss        specify the file with the list of channels on it and it fetches the RSS links of these channels and stores them in another file. It will ask you to name this new file.

    Query:
     This is what the script looks for on YouTube. Please enter it in quotes, eg. 'Messi vs Ronaldo'

    Channel List:
     This is the file containing the names of the channels whose videos you want in your feed. Make sure you have only one channel per line. The program prints the latest 3 videos for each channel. If this is used with the -rss or --get-rss option, it gets the RSS links of these channels and stores them in a new file in the same directory. It will ask you to name the new file containing the RSS links of these channels. 
""")

def getRSS(channelFile):
    RSSlinks = []
    with open(channelFile, 'r') as file:
        listOfChannels = file.readlines()
        for channel in listOfChannels:
            search = uyts.Search(channel)
            for res in search.results:
                if res.resultType == 'channel':
                    channelID = res.id
                    channelName = res.title
                    RSSlinks.append({"creator":channelName, "link":"https://www.youtube.com/feeds/videos.xml?channel_id="+channelID})
                    break
    return RSSlinks

def getVideos(channel):
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
    for i in range(3):
        videos.append({"title":entries[i].title.text, "url":entries[i].link.attrs["href"], "creator": channelName})


def playVideo(choice):
    chosenVideo = videos[int(choice) - 1]
    print("Playing: " + chosenVideo['title'])
    chosenVideoLink = chosenVideo['url']
    player.play(chosenVideoLink)
    player.wait_for_playback()


def displayVideos(videoList):
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
            getVideos(channel)

    displayVideos(videos)
    ch = input('Enter Choice: ')
    playVideo(ch)

elif sys.argv[1] == '-rss' or sys.argv[1] == '--get-rss':
    subfile = sys.argv[2]
    print("Getting RSS feed links for channels in '" + subfile + "' file..")
    RSSlinks = getRSS(subfile)
    RSSfile = input("Enter the name of the file you want to store the links in: ")
    with open(RSSfile, 'a') as file:
        for channel in RSSlinks:
            file.writelines(channel['creator'] + " : " + channel['link'] + "\n")


else:
    try:
        number = int(sys.argv[1])
        searchQuery = sys.argv[2]
    except:
        print("Number of results not provided. Defaulting to 5...")
        number = 5
        searchQuery = sys.argv[1]


    search = uyts.Search(searchQuery)
    for res in search.results:
        if res.resultType == 'video':
            videos.append({'title':res.title, 'url':'https://www.youtube.com/watch?v='+res.id, 'creator': res.author})
            if len(videos) == number:
                break

    displayVideos(videos)
    ch = input('Enter Choice: ')
    playVideo(ch)
