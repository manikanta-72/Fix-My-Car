import vlc
from pytube import YouTube
import time


def stream_youtube_video(url, start_time, end_time):
    # Get the YouTube video
    yt = YouTube(url)

    # Get the highest resolution stream available
    video_stream = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )

    # Play using VLC
    player = vlc.MediaPlayer(video_stream.url)

    # Set start position (VLC uses values from 0.0 to 1.0, so you need to calculate the ratio)
    start_ratio = start_time / yt.length
    player.set_position(start_ratio)
    player.play()

    # Sleep till the end time is reached and then stop the video
    play_duration = end_time - start_time
    time.sleep(play_duration)
    player.stop()


if __name__ == "__main__":
    video_url = input("Enter the YouTube video link: ")
    start_time = int(input("Enter the start time in seconds: "))
    end_time = int(input("Enter the end time in seconds: "))
    stream_youtube_video(video_url, start_time, end_time)
