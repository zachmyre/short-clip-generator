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
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

video_name = f"{'PowerfulJRE'}-{random.randrange(0, 99999)}.mp4"


def download_video():
    '''Downloads a video from youtube'''
    Path('./assets/videos').mkdir(parents=True, exist_ok=True)
    Path('./assets/clips').mkdir(parents=True, exist_ok=True)
    url = 'https://www.youtube.com/watch?v=qwogNykaAH8&ab_channel=PowerfulJRE'

    print_step(f"Downloading video source from {url}")
    YouTube(url, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
        "assets/videos", filename=video_name
    )
    print_substep("")
    print_substep("Background video downloaded successfully! 🎉", style="bold green")

def chop_background_video():
    print_step("Finding a spot in the video to chop...✂️")
    background = VideoFileClip(f"assets/videos/{video_name}", audio=True)
    print(background.duration)
    start_time = int(background.duration / 2.5)
    end_time = int(start_time + 45)
    print_substep(start_time)
    print_substep(end_time)
    clip = background.subclip(start_time, end_time)
    clip.write_videofile(f"assets/clips/0{video_name}", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    # try:
    #     with VideoFileClip(f"assets/videos/{video_name}") as video:
    #         new = video.subclip(start_time, end_time)
    #         new.write_videofile(f"assets/clips/0{video_name}", temp_audiofile="temp-audio.mp3", remove_temp=True, codec="libx264", audio_codec="aac")
    # except (OSError, IOError):  # ffmpeg issue see #348
    #     print_substep("FFMPEG issue. Trying again...")
    #     with VideoFileClip(f"assets/videos/{video_name}") as video:
    #         new = video.subclip(start_time, end_time)
    #         new.write_videofile(f"assets/clips/1{video_name}", temp_audiofile="temp-audio.mp3", remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == '__main__':
    print("""
     ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
     ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
     ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
    
    download_video()
    chop_background_video()