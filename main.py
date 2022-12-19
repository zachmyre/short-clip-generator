#download video
#clip random part of the video
#add text on screen
#render video

from pathlib import Path
from pytube import YouTube
from pytube.cli import on_progress
from utils.console import *

def download_video():
    '''Downloads a video from youtube'''
    Path('./assets/videos').mkdir(parents=True, exist_ok=True)




if __name__ == '__main__':
    print("""
     ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
     ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
     ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
    
    download_video()