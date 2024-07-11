import tkinter as tk
from tkinter import messagebox
import quality
import download


class MyGUI:
    def __init__(self):
        self.choice = 0
        self.format = 0
        self.link = str()
        self.quality_list = 0
        self.quality_choosen = str()
        self.path_user = 0

        self.window = tk.Tk()
        self.window.geometry("600x600")

        self.label = tk.Label(self.window, text="YouTube Downloader", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.myentry = tk.Entry(self.window, width=60, font=("Arial", 18))  # Create a box where the user can enter characters
        self.myentry.pack()

        self.check_state = tk.IntVar()  # 1 or 0
        self.check = tk.Checkbutton(self.window, text="Playlist", font=("Arial", 18), variable=self.check_state)
        self.check.pack(padx=10, pady=10)  # Checkbox

        self.check_state_mp3 = tk.IntVar()  # checker
        self.check = tk.Checkbutton(self.window, text="MP3", font=("Arial", 18), variable=self.check_state_mp3)
        self.check.pack(padx=10, pady=10)  # Checkbox mp3

        self.check_state_mp4 = tk.IntVar()  # checker
        self.check = tk.Checkbutton(self.window, text="MP4", font=("Arial", 18), variable=self.check_state_mp4)
        self.check.pack(padx=10, pady=10)  # Checkbox mp4

        self.button = tk.Button(self.window, text="Download", font=('Arial', 18), command=self.play_or_not)
        self.button.pack(padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def play_or_not(self):
        """
        Verify the user's entered values
        :return: None
        """
        if self.check_state_mp3.get() == 1 and self.check_state_mp4.get() == 1:  # Verify that mp3 and mp4 are not checked a the same time
            messagebox.showerror("Error", "You can't choose mp4 and mp3")
            return None
        elif self.check_state_mp3.get() == 0 and self.check_state_mp4.get() == 0:
            messagebox.showerror("Error", "You have to choose between mp4 and mp3")
            return None
        else:
            if self.check_state_mp3.get() == 1:  # The user choose mp3
                self.format = 1
            else:  # Mp4
                self.format = 2
            self.link = self.myentry.get()  # Gets the link from user
            if not len(self.link) in [43, 76, 91] and len(self.link) != 0:  # Verify the length of the link (not done)
                messagebox.showerror("Error", "Error, you entered a invalid link "
                         "(you maybe entered a link to a playlist instead of a single video).")
            elif len(self.link) == 0:
                messagebox.showerror("Error", "Error, you entered nothing in the link section. Try again")
            if self.check_state.get() == 1:  # Looks if the link is a playlist
                self.choice = 2
                self.path()
            else:
                self.choice = 1
                self.quality_list = quality.quality_check(self.link, self.format)
                self.ouvrir_dialogue()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):  # Text box yes/no when quitting
            self.window.destroy()

    def ouvrir_dialogue(self):
        self.dialogue = tk.Toplevel(self.window)
        self.dialogue.title("Quality of the video")
        label = tk.Label(self.dialogue, text="Choose the quality for the video/audio (ex: 48kbps/1080p): " + str(self.quality_list[1]))
        label.pack(pady=10)

        self.entry_qualite = tk.Entry(self.dialogue, width=50)
        self.entry_qualite.pack(pady=10)

        bouton_end = tk.Button(self.dialogue, text="Enter", command=self.verification_user_quality)
        bouton_end.pack(pady=10)

    def verification_user_quality(self):
        quality_choosen = self.entry_qualite.get()  # Check that the input is valid
        if quality_choosen not in self.quality_list[1]:
            if len(quality_choosen) < 4 or quality_choosen[2:] != "kbps" or quality_choosen[3:] != "kbps":
                messagebox.showerror("Error",
                                     "The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)")
                return
        self.check_quality()

    def check_quality(self):
        # Récupération de la valeur entrée par l'utilisateur
        self.quality_choosen = self.entry_qualite.get()
        messagebox.showinfo("Quality video", f"You choose : {self.quality_choosen}")
        self.dialogue.destroy()
        self.path()

    def path(self):
        dialogue = tk.Toplevel(self.window)
        dialogue.title("Path")

        label = tk.Label(dialogue, text="Enter the destination (leave blank for current directory): ")
        label.pack(pady=10)

        path_entry = tk.Entry(dialogue, width=50)
        path_entry.pack(pady=10)

        # Check and use the directory from the user
        def valider():
            self.path_user = path_entry.get()

            if not self.path_user:  # Takes the current directory
                self.path_user = "."

            if self.choice == 1:
                download.download(self.link, self.format, self.quality_list[0][self.quality_choosen], self.path_user)
            else:
                print('b')
                download.playlist(self.link, self.format, self.path_user)
            dialogue.destroy()

        bouton_valider = tk.Button(dialogue, text="Valider", command=valider)
        bouton_valider.pack(pady=10)

        dialogue.transient(self.window)
        dialogue.grab_set()
        self.window.wait_window(dialogue)


if __name__ == "__main__":
    tk = MyGUI()