from pytube import YouTube
import os
from moviepy.editor import AudioClip, VideoClip

class Downloader():
    def __init__(self):
        self.list_res = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

    def fusion(self, list):
        if len(list) > 1:
            left = list[:len(list) // 2]
            right = list[len(list) // 2:]

            self.fusion(left)
            self.fusion(right)

            i, j, k = 0, 0, 0
            while i < len(left) and j < len(right):
                if int(left[i]) < int(right[j]):
                    list[k] = left[i]
                    i += 1
                else:
                    list[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                list[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                list[k] = right[j]
                j += 1
                k += 1
        return list

    def searching_in_streams(self, response, format):
        temp_list = {}
        if format == "mp4":
            stream = YouTube(response).streams.filter(file_extension="mp4")
        elif format == "mp3":
            stream = YouTube(response).streams.filter(only_audio=True)

        for element in stream:
            if format == "mp3" and element.abr:
                temp_list[element.abr] = element.itag
            elif format == "mp4" and element.resolution:
                temp_list[element.resolution] = element.itag

        if format == "mp3":
            a = [i[:-4] for i in temp_list.keys()]
            sorted_audio = [i + "kbps" for i in self.fusion(a)]
            return temp_list, sorted_audio
        else:
            a = [i[:-1] for i in temp_list.keys()]
            sorted_audio = [i + "p" for i in self.fusion(a)]
            return temp_list, sorted_audio

    def quality(self, response, format):
        if format == "mp4":
            sorted_resolutions = self.searching_in_streams(response, format)
            return sorted_resolutions

        elif format == "mp3":
            sorted_audio = self.searching_in_streams(response, format)
            return sorted_audio
    """
    def download(self, link, id):
        stream_video = YouTube(link).streams.get_by_itag(id)
        stream_audio = YouTube(link).streams.filter(only_audio=True).first()

        stream_video.download(os.path.join(os.path.expanduser("~"), "Downloads"))
        stream_audio.download(os.path.join(os.path.expanduser("~"), "Downloads"))

        video_path = os.path.join(os.path.expanduser("~"), "Downloads", stream_video.title)
        audio_filepath = os.path.join(os.path.expanduser("~"), "Downloads", stream_audio.title)

        os.rename(video_path,"video.mp4")
        os.rename(audio_filepath, "audio.webm")

        input_video = VideoClip("video.mp4")
        input_audio = AudioClip("audio.webm")
        
        final = input_video.set_audio(input_audio).write_videofile("output.mp4")
        os.remove("video.mp4")
        os.remove("audio.webm")"""
    def download(self, link, id):
        stream_video = YouTube(link).streams.get_by_itag(id)
        stream_audio = YouTube(link).streams.filter(mime_type="audio/webm", only_audio=True).first()

        stream_video.download(os.path.join(os.path.expanduser("~"), "Downloads"))
        stream_audio.download(os.path.join(os.path.expanduser("~"), "Downloads"))






    def main(self):
        link = input("Hi, this uses pytube to download youtube videos. Enter the video link: ")
        format = input("Enter the format you want to download (mp4/mp3): ")

        while not len(link) in [90, 43, 99] or format not in ["mp4", "mp3"]:
            link = input("Error, you entered a invalid link or format. Enter the link: ")
            format = input("Enter the format you want to download (mp4/mp3): ")
        option_quality = self.quality(link, format)

        quality_choosen = input(str(option_quality[1]) + "   Choose the quality for the video/audio (ex: 48kbps/1080p)\n")
        while quality_choosen not in option_quality[1]:

            if len(quality_choosen) == 6 and quality_choosen[2:] != "kbps" or len(quality_choosen) == 7 and quality_choosen[3:] != "kbps":
                quality_choosen = input("The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)\n")
        self.download(link, option_quality[0][quality_choosen])


down = Downloader().main()
