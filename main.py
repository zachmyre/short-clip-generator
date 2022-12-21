# download video
# clip random part of the video
# add text on screen
# render video

#### ideas ####
# figure out how to find most viewed parts of a video


from bot import Bot

# video_name = f"{'PowerfulJRE'}-{random.randrange(0, 99999)}"


# def download_video():
#     '''Downloads a video from youtube'''

#     url = 'https://www.youtube.com/watch?v=Q9hrH-sZ0Vc&ab_channel=PowerfulJRE'

#     print_step(f"Downloading video source from {url}")


#     print_substep("")
#     print_substep("Video downloaded successfully! 🎉", style="bold green")

# def chop_background_video():
#     print_step("Finding a spot in the video to chop...✂️")
#     video = VideoFileClip(f"assets/videos/{video_name}.mp4")
#     audio = AudioFileClip(f"assets/audio/{video_name}.mp3")
#     temp = video.set_audio(audio)

#     print_markdown("Writing temp video file..")
#     temp.write_videofile(f"assets/temp/{video_name}.mp4")
#     final = VideoFileClip(f"assets/temp/{video_name}.mp4")

#     start_time = int(final.duration / 2.5)
#     end_time = int(start_time + 45)
#     print_substep("Start time: " + start_time)
#     print_substep("End time: " + end_time)

#     clip = final.subclip(start_time, end_time)
#     clip.write_videofile(f"assets/clips/final-{video_name}.mp4")

#     print_markdown("Removing downloaded audio and video from /videos and /audio")
#     os.remove(f"assets/videos/{video_name}.mp4")
#     os.remove(f"assets/audio/{video_name}.mp3")
#     os.remove(f"assets/temp/{video_name}.mp4")
#     video.close()
#     audio.close()
#     final.close()
if __name__ == '__main__':
    # download_video()
    # chop_background_video()
    bot = Bot()
