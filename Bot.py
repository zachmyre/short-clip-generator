
import random
import os
from pathlib import Path
from pytube import YouTube
from pytube.cli import on_progress
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


''' 
    ###############                         ############### 
    ###############      TO DO LIST         ############### 
    ###############                         ############### 

    1) Add method to download the video with audio and combine them, then remove the un-used files
    2) ??? Add a method to find the best spot to clip the video        
    3) Add a method to generate a clip from the video
    4) Add a method to download and generate subtitles (text to speech?)
             

'''


class Bot:
    error_count = 0

    url = ''
    audio_file_name = 'audio.mp3'
    video_file_name = 'video.mp4'
    temp_file_name = 'temp.mp4'

    '''  ########## Class Config ########## '''
    MAX_ERROR_COUNT = 5

    def __init__(self):
        print("""
         ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
         ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
         ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
        self.init_directories()
        self.initalize()

    def initalize(self):
        ''' Initialize method to kickstart the bot '''
        self.error_check()
        self.url = input("Type in a youtube link to generate clips:")

        if not self.validate_text("youtube.com", self.url):
            print_step("You must specifiy a youtube link!")
            self.error_count += 1
            self.initalize()
        self.download_video()

    def download_video(self):
        self.error_check()
        try:
            print_step("Downloading video...", "bold green")
            video_title = YouTube(self.url).title
            print_substep("Video Title: " + video_title, "yellow")
            # self.video_file_name =  video_title.replace(" ", "") + ".mp4"
            # self.audio_file_name = video_title.replace(" ", "") + ".mp3"
            youtube_video = YouTube(self.url, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
                "assets/videos", filename=self.video_file_name)
            youtube_audio = YouTube(self.url, on_progress_callback=on_progress).streams.filter(
                only_audio=True).first().download("assets/audio", filename=self.audio_file_name)
            video = VideoFileClip(f"assets/videos/{self.video_file_name}")
            audio = AudioFileClip(f"assets/audio/{self.audio_file_name}")
            temp = video.set_audio(audio)

            print_substep("Writing temp video file..", "yellow")
            temp.write_videofile(f"assets/temp/{self.temp_file_name}")
            os.remove(f"assets/videos/{self.video_file_name}")
            os.remove(f"assets/audio/{self.audio_file_name}")
            temp.close()
            audio.close()
            video.close()
        except Exception as e:
            print(e)
            print_step("Error downloading videos")
            self.error_count += 1
            self.download_video()

    def init_directories(self):
        ''' Creates directories for app'''
        Path('./assets/videos').mkdir(parents=True, exist_ok=True)
        Path('./assets/clips').mkdir(parents=True, exist_ok=True)
        Path('./assets/audio').mkdir(parents=True, exist_ok=True)
        Path('./assets/temp').mkdir(parents=True, exist_ok=True)

    def error_check(self):
        ''' Exits script if there are too many errors '''
        if self.error_count > self.MAX_ERROR_COUNT:
            print_step("Too many errors.. exiting")
            exit()

    def validate_text(self, text, comparison_text):
        ''' Validates text or a URL with the text parameter passed, returns true or false'''
        if text in comparison_text:
            return True
        return False


console = Console()


def print_step(text, style="bold red"):
    """Prints a rich info message."""
    panel = Panel(Text(text, justify="left"))
    console.print(panel, style=style)


def print_substep(text, style="green"):
    """Prints a rich info message without the panelling."""
    console.print(text, style=style)
