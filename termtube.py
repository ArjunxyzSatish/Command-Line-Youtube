#!/bin/env python

from youtube_search import YoutubeSearch
import mpv
import json
import sys

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)

def help():
    print("""
    Usage: termtube [OPTIONS] [QUERY]

    Options:
     -h, --help             prints this help message
      n                     where n is the number of video results you want displayed

    Query:
     This is what the script looks for on YouTube. Please enter it in quotes, eg. 'Messi vs Ronaldo'
""")

if len(sys.argv) == 1:
    help()
    
elif sys.argv[1] == '-h' or sys.argv[1] == '--help': 
    help()

else:

    searchQuery = sys.argv[2]
    number = int(sys.argv[1])

    results = YoutubeSearch(searchQuery, max_results=number).to_json()
    data = json.loads(results)
    videos = data['videos']
    for x, video in enumerate(videos):
        print(f'{x+1}. ' + videos[x]['title'] + ' : ' + videos[x]['channel'])

    ch = input("Enter Choice: ")

    chosenVideo = videos[int(ch) - 1]
    print("Playing: " + chosenVideo['title'])
    chosenVideoLink = 'https://www.youtube.com/watch?v=' + chosenVideo['id']

    player.play(chosenVideoLink)
    player.wait_for_playback()
