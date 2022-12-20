#download video
#clip random part of the video
#add text on screen
#render video

#### ideas ####
# figure out how to find most viewed parts of a video

import random
import os
from pathlib import Path
from pytube import YouTube
from pytube.cli import on_progress
from utils.console import *
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

video_name = f"{'PowerfulJRE'}-{random.randrange(0, 99999)}"


def download_video():
    '''Downloads a video from youtube'''
    Path('./assets/videos').mkdir(parents=True, exist_ok=True)
    Path('./assets/clips').mkdir(parents=True, exist_ok=True)
    Path('./assets/audio').mkdir(parents=True, exist_ok=True)
    Path('./assets/temp').mkdir(parents=True, exist_ok=True)
    url = 'https://www.youtube.com/watch?v=Q9hrH-sZ0Vc&ab_channel=PowerfulJRE'

    print_step(f"Downloading video source from {url}")
    youtube_video = YouTube(url, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
        "assets/videos", filename=video_name+".mp4"
    )
    youtube_audio = YouTube(url, on_progress_callback=on_progress).streams.filter(only_audio=True).first().download("assets/audio", filename=video_name+".mp3")

    print_substep("")
    print_substep("Video downloaded successfully! 🎉", style="bold green")

def chop_background_video():
    print_step("Finding a spot in the video to chop...✂️")
    video = VideoFileClip(f"assets/videos/{video_name}.mp4")
    audio = AudioFileClip(f"assets/audio/{video_name}.mp3")
    temp = video.set_audio(audio)

    print_markdown("Writing temp video file..")
    temp.write_videofile(f"assets/temp/{video_name}.mp4")
    final = VideoFileClip(f"assets/temp/{video_name}.mp4")

    start_time = int(final.duration / 2.5)
    end_time = int(start_time + 45)
    print_substep("Start time: " + start_time)
    print_substep("End time: " + end_time)

    clip = final.subclip(start_time, end_time)
    clip.write_videofile(f"assets/clips/final-{video_name}.mp4")

    print_markdown("Removing downloaded audio and video from /videos and /audio")
    os.remove(f"assets/videos/{video_name}.mp4")
    os.remove(f"assets/audio/{video_name}.mp3")
    os.remove(f"assets/temp/{video_name}.mp4")
    video.close()
    audio.close()
    final.close()
if __name__ == '__main__':
    print("""
     ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
     ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
     ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
    
    # download_video()
    chop_background_video()