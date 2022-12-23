import customtkinter
from bot import Bot
from urllib.parse import urlparse, parse_qs
from contextlib import suppress

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

        # youtube download frame
        self.youtube_download_frame = customtkinter.CTkFrame(
            self, width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT/2, fg_color="blue")
        self.youtube_download_frame.place(x=0, y=0)

        # youtube download widgets
        self.youtube_frame_label = customtkinter.CTkLabel(
            self.youtube_download_frame, text="Enter Youtube Link to Download Video", anchor="w")
        self.youtube_frame_label.place(x=20, y=self.FRAME_HEIGHT/4-25)

        self.youtube_url_textbox = customtkinter.CTkTextbox(
            self.youtube_download_frame, width=self.FRAME_WIDTH/2, height=25)
        self.youtube_url_textbox.place(
            x=25, y=self.FRAME_HEIGHT/4)

        self.youtube_video_download_btn = customtkinter.CTkButton(
            self.youtube_download_frame, text="Download Video", width=50, height=27, command=self.download_youtube_video)
        self.youtube_video_download_btn.place(
            x=30+self.FRAME_WIDTH/2, y=self.FRAME_HEIGHT/4+3)

    def download_youtube_video(self):
        try:
            self.youtube_frame_error.destroy()
        except:
            print('no error currently')
        print("download youtube video method")
        self.youtube_url = self.youtube_url_textbox.get("0.0", "end").strip()
        print(self.youtube_url)
        self.youtube_id = self.get_youtube_id(self.youtube_url)
        print(str(self.youtube_id))
        if(self.youtube_id == None):
            self.youtube_frame_error = customtkinter.CTkLabel(self.youtube_download_frame, text="Error, invalid youtube link!", text_color="red", anchor="w")
            self.youtube_frame_error.place(x=20, y=self.FRAME_HEIGHT/4-50)
            print(type(self.youtube_frame_error))
            return

    def get_youtube_id(self, url, ignore_playlist=False):
        # Examples:
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
