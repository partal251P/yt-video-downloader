from pytube import YouTube, Playlist
import check
import mergesort
import tk_test

class Downloader():








    def main(self):
        """
        Main function that uses all the function
        :return: None
        """
        tk = tk_test.MyGUI()
        choice, link, format = tk.choice, tk.link, tk.format
        print(choice, link, format)


        choice = check.check_choice(choice)


        if choice == "1":  # User chooses to download a playlist
            self.playlist(link, format)

        else:  # A single video will be downloaded
            while quality_choosen not in option_quality[1]:  # Check the input for the quality of the user
                if len(quality_choosen) == 6 and quality_choosen[2:] != "kbps" or len(quality_choosen) == 7 and quality_choosen[3:] != "kbps":
                    quality_choosen = input("The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)\n>>")
            destination = input("Enter the destination (leave blank for current directory):\n>>")
            self.download(link, format, option_quality[0][quality_choosen], destination)  # Will download the video with the quality choosen by the user


if __name__ == "__main__":
    down = Downloader().main()

#https://www.youtube.com/watch?v=uu565buON1U