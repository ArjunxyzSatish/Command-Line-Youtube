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
     -f

    Query:
     This is what the script looks for on YouTube. Please enter it in quotes, eg. 'Messi vs Ronaldo'

    Channel List:
     This is the file containing the names of the channels whose videos you want in your feed. Make sure you have only one channel per line. The program prints the latest 3 videos for each channel.
""")

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

    ch = input('Enter Choice: ')


if len(sys.argv) == 1:
    help()

elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
    help()

elif sys.argv[1] == '-f' or sys.argv[1] == '--file':
    subfile = sys.argv[2]
    with open(subfile, 'r') as file:
        listOfChannels = file.readlines()
        for channel in listOfChannels:
            getVideos(channel)
    for x, video in enumerate(videos):
        print(f'{x+1}. ' + videos[x]['title'] + ' : ' + videos[x]['creator'])

    ch = input('Enter Choice: ')
    playVideo(ch)


else:

    if sys.argv[1] != int:
        number = 5
        searchQuery = sys.argv[1]
    else:
        searchQuery = sys.argv[2]
        number = int(sys.argv[1])

    search = uyts.Search(searchQuery)
    for res in search.results:
        if res.resultType == 'video':
            videos.append({'title':res.title, 'url':'https://www.youtube.com/watch?v='+res.id, 'creator': res.author})
            if len(videos) == number:
                break

    displayVideos(videos)
    playVideo(ch)
