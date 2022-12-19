#download video
#clip random part of the video
#add text on screen
#render video

import random
from pathlib import Path
from pytube import YouTube
from pytube.cli import on_progress
from utils.console import *
from pytube import YouTube
from pytube.cli import on_progress

def download_video():
    '''Downloads a video from youtube'''
    Path('./assets/videos').mkdir(parents=True, exist_ok=True)
    url = 'https://www.youtube.com/watch?v=qwogNykaAH8&ab_channel=PowerfulJRE'

    print_step(f"Downloading video source from {url}")
    YouTube(url, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
        "assets/videos", filename=f"{'PowerfulJRE'}-{random.randrange(0, 99999)}"
    )
    print_substep("")
    print_substep("Background video downloaded successfully! 🎉", style="bold green")














if __name__ == '__main__':
    print("""
     ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
     ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
     ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
    
    download_video()