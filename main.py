from bot import Bot
from gui import GUI
from youtube_transcript_api import YouTubeTranscriptApi


# Create gui that can download a video from youtube then display it in the GUI
# You will go through the video and figure out the best time frames(s) to clip from
# You will type the start / end time into a text box and the bot will clip that part of the video then add subtitles.
# Could also make it to where you can clip multiple parts of the video by adding more text boxes ^^.
# Once the video files are clipped, you can view them in the gui.


if __name__ == '__main__':
    # bot = Bot()
    gui = GUI()
    gui.mainloop()
    # print(YouTubeTranscriptApi.get_transcript("7MNv4_rTkfU"))
