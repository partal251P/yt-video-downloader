from pytube import YouTube, Playlist
import check
import mergesort


class Downloader():
    def searching_in_streams(self, response, format):
        """
        Will take a list with all the objects and will sort them
        :param response: str()
        :param format: str()
        :return: list(), list()
        """
        temp_list = {}
        if format == "2":
            stream = YouTube(response).streams.filter(file_extension="mp4")
        elif format == "1":
            stream = YouTube(response).streams.filter(only_audio=True)

        for element in stream:  # Creation of the dict with the quality : id
            if format == "1" and element.abr:
                temp_list[element.abr] = element.itag
            elif format == "2" and element.resolution:
                temp_list[element.resolution] = element.itag

        if format == "1":  # Will use the function fusion to sort the different ints (quality)
            a = [i[:-4] for i in temp_list.keys()]
            sorted_audio = [i + "kbps" for i in mergesort.fusion(a)]
            return temp_list, sorted_audio
        else:
            a = [i[:-1] for i in temp_list.keys()]
            sorted_audio = [i + "p" for i in mergesort.fusion(a)]
            return temp_list, sorted_audio

    def quality(self, response, format):
        """
        Sort the different quality available for the video in question by using the mergesort
        :param response: str()
        :param format: str()
        :return: list(), list()
        """
        if format == "2":
            sorted_resolutions = self.searching_in_streams(response, format)
            return sorted_resolutions

        elif format == "1":
            sorted_audio = self.searching_in_streams(response, format)
            return sorted_audio

    def download(self, link, format, id, destination):
        """
        Downloads a video in mp4 or in mp3
        :param link: str
        :param id: int
        :return: None
        """

        if format == "2":
            stream_video = YouTube(link).streams.get_by_itag(id)
            out_file = stream_video.download(output_path=destination)
        else:
            stream_audio = YouTube(link).streams.get_by_itag(id).download(destination)

    def playlist(self, link, format):
        """
        Used to download a playlist
        :param link: str()
        :param format: str()
        :return: None
        """
        destination = input("Enter the destination (leave blank for current directory):\n>>")
        playl = Playlist(link)
        for url, vid in zip(playl.video_urls, playl.videos):  # Will loop though all the videos in the playlist
            self.download(url, format, vid.streams.first().itag, destination)

    def main(self):
        """
        Main function that uses all the function
        :return: None
        """
        choice = input("Hi, this uses pytube to download youtube videos. Do you want to download:\n"
                       "(1) Playlist\n"
                       "(2) Single video\n>>")
        choice = check.check_choice(choice)
        if choice == "1":  # User chooses to download a playlist
            link = input("Enter the playlist link:\n>>")
            link = check.check_link(link)  # Will check the input for the link of the user
            format = input("Enter the format you want to download: \n(1) Mp3\n(2) Mp4\n>>")
            format = check.check_format(format)  # Will check the input for the format of the user
            self.playlist(link, format)

        else:  # A single video will be downloaded
            link = input("Enter the video link:\n>>")
            link = check.check_link(link)  # Will check the input for the link of the user
            format = input("Enter the format you want to download: \n(1) Mp3\n(2) Mp4\n>>")
            format = check.check_format(format)  # Will check the input for the format of the user
            option_quality = self.quality(link, format)
            quality_choosen = input(str(option_quality[1]) + " Choose the quality for the video/audio (ex: 48kbps/1080p)\n>>")

            while quality_choosen not in option_quality[1]:  # Check the input for the quality of the user
                if len(quality_choosen) == 6 and quality_choosen[2:] != "kbps" or len(quality_choosen) == 7 and quality_choosen[3:] != "kbps":
                    quality_choosen = input("The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)\n>>")
            destination = input("Enter the destination (leave blank for current directory):\n>>")
            self.download(link, format, option_quality[0][quality_choosen], destination)  # Will download the video with the quality choosen by the user


if __name__ == "__main__":
    down = Downloader().main()
