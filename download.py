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
    if format == 2:
        yt = YouTube(link)
        title_video = yt.title
        stream_video = yt.streams.get_by_itag(id)

        # Téléchargement de la vidéo
        out_file_video = stream_video.download(output_path=destination)
        video_path = os.path.join(destination, os.path.basename(out_file_video))

        # Renommer le fichier vidéo pour éviter les conflits
        new_video_path = os.path.join(destination, f"{title_video}_video.mp4")
        os.rename(video_path, new_video_path)

        # Téléchargement de l'audio
        stream_audio = yt.streams.filter(only_audio=True).first()
        out_file_audio = stream_audio.download(output_path=destination)
        audio_path = os.path.join(destination, os.path.basename(out_file_audio))

        # Renommer le fichier audio pour éviter les conflits
        new_audio_path = os.path.join(destination, f"{title_video}_audio.mp3")
        os.rename(audio_path, new_audio_path)

        # Chargement des clips vidéo et audio
        video_clip = VideoFileClip(new_video_path)
        audio_clip = AudioFileClip(new_audio_path)

        # Finalisation du clip avec l'audio
        final_clip = video_clip.set_audio(audio_clip)

        # Chemin du fichier final
        final_path = os.path.join(destination, f"{title_video}_final.mp4")
        final_clip.write_videofile(final_path, codec='libx264')

        # Nettoyage des fichiers intermédiaires
        os.remove(new_video_path)
        os.remove(new_audio_path)

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