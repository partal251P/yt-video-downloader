from pytube import YouTube


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
                temp_list[element.abr] = element.itag
        return dict(sorted(temp_list.items()))

    def quality(self, response, format):
        if format == "mp4":
            sorted_resolutions = self.searching_in_streams(response, format)

        elif format == "mp3":
            sorted_audio = self.searching_in_streams(response, format)

        return sorted_audio

    def main(self):
        link = input("Hi, this uses pytube to download youtube videos. Enter the video link: ")
        format = input("Enter the format you want to download (mp4/mp3): ")

        while not len(link) in [90, 43, 99] or format not in ["mp4", "mp3"]:
            link = input("Error, you entered a invalid link or format. Enter the link: ")
            format = input("Enter the format you want to download (mp4/mp3): ")
        quality_choosen = input(str(self.quality(link, format)) + " Choose the quality for the video/audio: ")



down = Downloader().main()
