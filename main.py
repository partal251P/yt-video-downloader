from pytube import YouTube, Playlist


class Downloader():
    def fusion(self, list):
        """
        A simple Mergesort
        :param list: list()
        :return: list()
        """
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
            sorted_audio = [i + "kbps" for i in self.fusion(a)]
            return temp_list, sorted_audio
        else:
            a = [i[:-1] for i in temp_list.keys()]
            sorted_audio = [i + "p" for i in self.fusion(a)]
            return temp_list, sorted_audio

    def quality(self, response, format):
        if format == "2":
            sorted_resolutions = self.searching_in_streams(response, format)
            return sorted_resolutions

        elif format == "1":
            sorted_audio = self.searching_in_streams(response, format)
            return sorted_audio

    def download(self, link, format, id, destination):
        """
        Downloads
        :param link: str
        :param id: int
        :return: None
        """

        if format == "2":
            stream_video = YouTube(link).streams.get_by_itag(id)
            out_file = stream_video.download(output_path=destination)
        else:
            stream_audio = YouTube(link).streams.get_by_itag(id).download(destination)

    def playlist(self, link,format):
        destination = input("Enter the destination (leave blank for current directory):\n>>")
        playl = Playlist(link)
        for url, vid in zip(playl.video_urls, playl.videos):
            print(vid.streams.first().itag)
            self.download(url, format, vid.streams.first().itag, destination)

    def main(self):
        choice = input("Hi, this uses pytube to download youtube videos. Do you want to download:"
                       "(1) Playlist "
                       "(2) Single video\n>>")
        if choice == "1":
            link = input("Enter the playlist link:\n>>")
            print(Playlist("https://www.youtube.com/watch?v=FQxSwhee8KM&list=PLMyw82_22zVxokspEoncAuvOgp-SxnyjT"))
            format = input("Enter the format you want to download: \n(1) Mp3\n(2) Mp4\n>>")
            self.playlist(link, format)

        else:
            link = input("Enter the video link:\n>>")
            format = input("Enter the format you want to download: \n(1) Mp3\n(2) Mp4\n>>")

            while not len(link) in [90, 43, 99, 95] or format not in ["1", "2"]:
                link = input("Error, you entered a invalid link or format. Enter the link:\n>>")
                format = input("Enter the format you want to download: \n(1) Mp3\n(2) Mp4\n>>")

            option_quality = self.quality(link, format)
            quality_choosen = input(str(option_quality[1]) + " Choose the quality for the video/audio (ex: 48kbps/1080p)\n>>")
            while quality_choosen not in option_quality[1]:  # Vérifie

                if len(quality_choosen) == 6 and quality_choosen[2:] != "kbps" or len(quality_choosen) == 7 and quality_choosen[3:] != "kbps":
                    quality_choosen = input("The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)\n>>")
            destination = input("Enter the destination (leave blank for current directory):\n>>")
            self.download(link, format, option_quality[0][quality_choosen], destination)



down = Downloader().main()
