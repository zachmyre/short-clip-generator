import os
from pathlib import Path
from pytube import YouTube
from pytube.cli import on_progress
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import *
import speech_recognition as sr
from helpers import console


''' 
    ###############                         ############### 
    ###############      TO DO LIST         ############### 
    ###############                         ############### 

    1) Add method to download the video with audio and combine them, then remove the un-used files
    2) ??? Add a method to find the best spot to clip the video        
    3) Add a method to generate a clip from the video
    4) Add a method to download and generate subtitles (text to speech?)
             

'''


# https://www.youtube.com/watch?v=7MNv4_rTkfU&ab_channel=PowerfulJRE

class Bot:
    error_count = 0

    url = ''
    test_temp = "assets/temp/test_clip.mp4"
    audio_file_name = 'audio.wav'
    video_file_name = 'video.mp4'
    temp_file_name = 'temp.mp4'
    start_time = 0
    end_time = 0

    step_style = "bold green"
    substep_style = "yellow"

    '''  ########## Class Config ########## '''
    MAX_ERROR_COUNT = 5

    def __init__(self):
        print("""
         ░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░▀█▀░█▀█░█▀▀░░░█▀▄░█▀█░▀█▀░░░░░░░░░░░░
         ░▀▀█░░█░░█▀█░█▀▄░░█░░░█░░█░█░█░█░░░█▀▄░█░█░░█░░░░░░░░░░░░░
         ░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░▀░░▀░░▀░░▀░
         """)
        self.init_directories()
        # self.initalize()
        # self.main()

    def download_video(self, url):
        self.url = url
        self.error_check()
        try:
            console.print_step("Downloading video...")
            video_title = YouTube(self.url).title
            console.print_substep(
                "Video Title: " + video_title)
            youtube_video = YouTube(self.url, on_progress_callback=on_progress).streams.filter(res="1080p").first().download(
                "assets/videos", filename=self.video_file_name)
            youtube_audio = YouTube(self.url, on_progress_callback=on_progress).streams.filter(
                only_audio=True).first().download("assets/audio", filename=self.audio_file_name)
            video = VideoFileClip(f"assets/videos/{self.video_file_name}")
            audio = AudioFileClip(f"assets/audio/{self.audio_file_name}")
            temp = video.set_audio(audio)

            console.print_substep(
                "Writing temp video file..")
            temp.write_videofile(f"assets/temp/{self.temp_file_name}")
            os.remove(f"assets/videos/{self.video_file_name}")
            os.remove(f"assets/audio/{self.audio_file_name}")
            temp.close()
            audio.close()
            video.close()
        except Exception as e:
            print(e)
            console.print_step("Error downloading videos")
            self.error_count += 1
            self.download_video(self.url)

    def clip_video(self):
        ''' Generates a clip from the start / end time '''
        console.print_step("Clipping video!")
        temp_clip = VideoFileClip(self.test_temp)
        print(temp_clip.duration)
        start_time = int(temp_clip.duration / 2.5)
        end_time = int(start_time + 45)
        console.print_substep("Start time: " + str(start_time))
        console.print_substep("End time: " + str(end_time))

        console.print_substep("Writing clip file.")
        clip = temp_clip.subclip(start_time, end_time)
        clip.write_videofile(f"assets/clips/final-{self.video_file_name}")
        temp_clip.close()
        clip.close()

    def extract_audio(self):
        console.print_step("Extracting audio!")
        temp_clip = VideoFileClip(f"assets/clips/final-{self.video_file_name}")
        temp_clip.audio.write_audiofile(f"assets/audio/{self.audio_file_name}")
        temp_clip.close()

    def extract_text_from_audio(self):
        console.print_step("Extracting text from audio!")
        r = sr.Recognizer()
        with sr.AudioFile(f"assets/audio/{self.audio_file_name}") as source:
            audio = r.record(source)  # read the entire audio file
            script = r.recognize_google(audio, show_all=True)
        for transcript in script['alternative']:
            print(transcript['transcript'])

    def init_directories(self):
        ''' Creates directories for app'''
        console.print_step("Creating directories if not already created..")
        Path('./assets/videos').mkdir(parents=True, exist_ok=True)
        Path('./assets/clips').mkdir(parents=True, exist_ok=True)
        Path('./assets/audio').mkdir(parents=True, exist_ok=True)
        Path('./assets/temp').mkdir(parents=True, exist_ok=True)

    def error_check(self):
        ''' Exits script if there are too many errors '''
        if self.error_count > self.MAX_ERROR_COUNT:
            console.print_step("Too many errors.. exiting")
            exit()

    def validate_text(self, text, comparison_text):
        ''' Validates text or a URL with the text parameter passed, returns true or false'''
        if text in comparison_text:
            return True
        return False
