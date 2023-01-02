import threading
import datetime
import customtkinter
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from bot import Bot
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from youtube_transcript_api import YouTubeTranscriptApi


# Implement multithreading for the bot to process while tkinter continues to run

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


class GUI(customtkinter.CTk):
    WIDTH = 1100
    HEIGHT = 580
    FRAME_WIDTH = 350
    FRAME_HEIGHT = 250
    bot = Bot()

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Senjin Clip Generator")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # frame for video
        self.video_frame = customtkinter.CTkFrame(
            self, width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT, fg_color="red")
        self.video_frame.place(x=self.WIDTH-self.FRAME_WIDTH)

        # video player
        self.video_player = TkinterVideo(scaled=True, master=self.video_frame)
        self.video_player.place(x=self.WIDTH-self.FRAME_WIDTH)

        # video player gui
        self.load_btn = tk.Button(
            self.video_frame, text="Load", command=self.load_video)
        self.load_btn.pack()

        self.play_pause_btn = tk.Button(
            self.video_frame, text="Play", command=self.play_pause)
        self.play_pause_btn.pack()

        self.skip_plus_5sec = tk.Button(
            self.video_frame, text="Skip -5 sec", command=lambda: self.skip(-5))
        self.skip_plus_5sec.pack(side="left")

        self.start_time = tk.Label(
            self.video_frame, text=str(datetime.timedelta(seconds=0)))
        self.start_time.pack(side="left")

        self.progress_value = tk.IntVar(self.video_frame)

        self.progress_slider = tk.Scale(self.video_frame, variable=self.progress_value,
                                        from_=0, to=0, orient="horizontal", command=self.seek)
        # progress_slider.bind("<ButtonRelease-1>", seek)
        self.progress_slider.pack(side="left", fill="x", expand=True)

        self.end_time = tk.Label(
            self.video_frame, text=str(datetime.timedelta(seconds=0)))
        self.end_time.pack(side="left")

        self.video_player.bind("<<Duration>>", self.update_duration)
        self.video_player.bind("<<SecondChanged>>", self.update_scale)
        self.video_player.bind("<<Ended>>", self.video_ended)

        self.skip_plus_5sec = tk.Button(
            self.video_frame, text="Skip +5 sec", command=lambda: self.skip(5))
        self.skip_plus_5sec.pack(side="left")

        # youtube download frame
        self.youtube_download_frame = customtkinter.CTkFrame(
            self, width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT/2, fg_color="blue")
        self.youtube_download_frame.place(x=0, y=0)

        # youtube download widgets
        self.youtube_frame_label = customtkinter.CTkLabel(
            self.youtube_download_frame, text="Enter Youtube Link to Download Video", anchor="w")
        self.youtube_frame_label.place(x=30, y=self.FRAME_HEIGHT/4-25)

        self.youtube_url_textbox = customtkinter.CTkTextbox(
            self.youtube_download_frame, width=self.FRAME_WIDTH/2, height=25)
        self.youtube_url_textbox.place(
            x=30, y=self.FRAME_HEIGHT/4)

        self.youtube_video_download_btn = customtkinter.CTkButton(
            self.youtube_download_frame, text="Download Video", width=50, height=27, command=self.download_youtube_video_thread)
        self.youtube_video_download_btn.place(
            x=30+self.FRAME_WIDTH/2, y=self.FRAME_HEIGHT/4+3)

        self.youtube_frame_label = customtkinter.CTkLabel(
            self.youtube_download_frame, text='', text_color="red", anchor="w")
        self.youtube_frame_label.place(x=30, y=self.FRAME_HEIGHT/4-50)

    def download_youtube_video_thread(self):
        threading.Thread(target=self.download_youtube_video).start()

    def download_youtube_video(self):
        print("download youtube video method")
        self.youtube_url = self.youtube_url_textbox.get("0.0", "end").strip()
        print(self.youtube_url)
        self.youtube_id = self.get_youtube_id(self.youtube_url)
        print(str(self.youtube_id))
        if (self.youtube_id == None):
            self.update_label('youtube', "Error, invalid youtube link!", "red")
            return
        self.update_label('youtube', "Getting audio...", "yellow")
        self.get_transcribed_audio()
        self.update_label('youtube', "Downloading...", "yellow")
        self.bot.download_video(self.youtube_url)
        self.update_label(
            'youtube', "Download complete! /assets/temp", "yellow")

    def get_transcribed_audio(self):
        try:
            self.youtube_transcribed_audio = YouTubeTranscriptApi.get_transcript(
                self.youtube_id)
            print(self.youtube_transcribed_audio)
        except Exception as e:
            self.update_label(
                'youtube', "Error, cannot transcribe youtube link!", "red")
            print("transcribing error audio")
            print(e)

    def get_youtube_id(self, url, ignore_playlist=False):
        # Examples:
        # https://www.youtube.com/watch?v=yDPQfj4bZY8&ab_channel=NeuralNine
        # https://www.youtube.com/watch?v=BEWz4SXfyCQ&ab_channel=PowerfulJRE
        # - http://youtu.be/SA2iWivDJiE
        # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        # - http://www.youtube.com/embed/SA2iWivDJiE
        # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
            if not ignore_playlist:
                # use case: get playlist id not current video in playlist
                with suppress(KeyError):
                    return parse_qs(query.query)['list'][0]
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/watch/':
                return query.path.split('/')[1]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        return None

    def update_duration(self, event):
        """ updates the duration after finding the duration """
        self.duration = self.video_player.video_info()["duration"]
        self.end_time["text"] = str(datetime.timedelta(seconds=self.duration))
        self.progress_slider["to"] = self.duration

    def update_scale(self, event):
        """ updates the scale value """
        self.progress_value.set(self.video_player.current_duration())

    def load_video(self):
        """ loads the video """
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            self.video_player.load(self.file_path)

            self.progress_slider.config(to=0, from_=0)
            self.play_pause_btn["text"] = "Play"
            self.progress_value.set(0)

    def seek(self, value):
        """ used to seek a specific timeframe """
        self.video_player.seek(int(value))

    def skip(self, value: int):
        """ skip seconds """
        self.video_player.seek(int(self.progress_slider.get())+value)
        self.progress_value.set(self.progress_slider.get() + value)

    def play_pause(self):
        """ pauses and plays """
        if self.video_player.is_paused():
            self.video_player.play()
            self.play_pause_btn["text"] = "Pause"

        else:
            self.video_player.pause()
            self.play_pause_btn["text"] = "Play"

    def video_ended(self, event):
        """ handle video ended """
        self.progress_slider.set(self.progress_slider["to"])
        self.play_pause_btn["text"] = "Play"
        self.progress_slider.set(0)

    def update_label(self, type, text, text_color):
        match type:
            case 'youtube':
                self.youtube_frame_label.configure(
                    require_redraw=True, text=text, text_color=text_color)
            case _:
                return
