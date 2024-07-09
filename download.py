from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
def download(link, format, id, destination):
    """
    Downloads a video in mp4 or in mp3
    :param link: str
    :param id: int
    :return: None
    """
    print(YouTube(link).title)
    if format == 2:
        stream_video = YouTube(link).streams.get_by_itag(id)
        out_file = stream_video.download(output_path=destination)
        stream_audio = YouTube(link).streams.get_by_itag(id).download(destination)
        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.mp3")
        final_clip = video_clip.set_audio(audio_clip)
    else:
        stream_audio = YouTube(link).streams.get_by_itag(id).download(destination)

def playlist(link, format, destination):
    """
    Used to download a playlist
    :param link: str()
    :param format: str()
    :return: None
    """


    playl = Playlist(link)
    for url, vid in zip(playl.video_urls, playl.videos):  # Will loop though all the videos in the playlist
        download(url, format, vid.streams.first().itag, destination)