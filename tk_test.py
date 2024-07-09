import tkinter as tk
from tkinter import messagebox
import quality
import download

from pytube import YouTube
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

        self.myentry = tk.Entry(self.window, width=60, font=("Arial", 18))  # utilisé pour les mdp par ex
        self.myentry.pack()




        self.check_state = tk.IntVar()  #checker
        self.check = tk.Checkbutton(self.window, text="Playlist", font=("Arial", 18), variable=self.check_state)
        self.check.pack(padx=10, pady=10)  #checkbox



        self.check_state_mp3 = tk.IntVar()  # checker
        self.check = tk.Checkbutton(self.window, text="MP3", font=("Arial", 18), variable=self.check_state_mp3)
        self.check.pack(padx=10, pady=10)  # checkbox mp3



        self.check_state_mp4 = tk.IntVar()  # checker
        self.check = tk.Checkbutton(self.window, text="MP4", font=("Arial", 18), variable=self.check_state_mp4)
        self.check.pack(padx=10, pady=10)  # checkbox mp4




        self.button = tk.Button(self.window, text="Download", font=('Arial', 18), command=self.play_or_not)
        self.button.pack(padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def message_dynamic(self, message):
        self.label = tk.Label(self.window, text=message, font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

    def play_or_not(self):
        """
        Permet de vérifier les valeurs mises
        :return:
        """
        #est ce que checkbox est checker?
        if self.check_state_mp3.get() == 1 and self.check_state_mp4.get() == 1:  # Vérifie que mp3 et  mp4  ne sont pas choisi en meme temps
            messagebox.showerror("Error", "You can't choose mp4 and mp3")
            return None
        elif self.check_state_mp3.get() == 0 and self.check_state_mp4.get() == 0:
            messagebox.showerror("Error", "You have to choose between mp4 and mp3")
            return None
        else:
            if self.check_state_mp3.get() == 1:  # Check ce que l'user a choisi mp3/4
                self.format = 1
            else:
                self.format = 2
            self.link = self.myentry.get()  # update le link
            if not len(self.link) in [43, 76, 91] and len(self.link) != 0:  #vérifie le link
                messagebox.showerror("Error", "Error, you entered a invalid link "
                         "(you maybe entered a link to a playlist instead of a single video).")
            elif len(self.link) == 0:
                messagebox.showerror("Error", "Error, you entered nothing in the link section. Try again")
            if self.check_state.get() == 1: #obtient le state du checkbox (0 ou 1)
                #c'est une playlist
                self.choice = 2
                self.path()
            else:
                self.choice = 1
                self.quality_list = quality.quality_check(self.link, self.format)
                self.ouvrir_dialogue()






    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):  #text box yes/no
            self.window.destroy()

    def ouvrir_dialogue(self):
        # Création de la fenêtre de dialogue
        self.dialogue = tk.Toplevel(self.window)
        self.dialogue.title("Qualité Vidéo")
        # Ajout d'un label et d'un champ de saisie
        label = tk.Label(self.dialogue, text="Choisissez la qualité pour la vidéo/audio (ex: 48kbps/1080p): " + str(self.quality_list[1]))
        label.pack(pady=10)

        self.entry_qualite = tk.Entry(self.dialogue, width=50)
        self.entry_qualite.pack(pady=10)

        # Bouton pour valider
        bouton_valider = tk.Button(self.dialogue, text="Valider", command=self.verification_user_quality)
        bouton_valider.pack(pady=10)



    def verification_user_quality(self):
        quality_choosen = self.entry_qualite.get()  #vérife que l'input est correct
        if quality_choosen not in self.quality_list[1]:
            if len(quality_choosen) < 4 or quality_choosen[2:] != "kbps" or quality_choosen[3:] != "kbps":
                messagebox.showerror("Error",
                                     "The input is not in the list of the available quality. Try again (ex: 48kbps/1080p)")

                return
        self.valider_qualite()
    def valider_qualite(self):
        # Récupération de la valeur entrée par l'utilisateur
        self.quality_choosen = self.entry_qualite.get()
        messagebox.showinfo("Qualité Vidéo", f"Vous avez choisi : {self.quality_choosen}")
        self.dialogue.destroy()
        self.path()

    def path(self):
        # Création de la fenêtre de dialogue
        dialogue = tk.Toplevel(self.window)
        dialogue.title("Path")

        # Ajout d'un label et d'un champ de saisie
        label = tk.Label(dialogue, text="Enter the destination (leave blank for current directory): ")
        label.pack(pady=10)

        path_entry = tk.Entry(dialogue, width=50)
        path_entry.pack(pady=10)

        # Fonction pour valider et récupérer la saisie de l'utilisateur
        def valider():
            self.path_user = path_entry.get()

            if not self.path_user:  # Si le champ est vide, utiliser le répertoire courant
                self.path_user = "."

            if self.choice == 1:
                print('a')
                download.download(self.link, self.format, self.quality_list[0][self.quality_choosen], self.path_user)
            else:
                print('b')
                download.playlist(self.link, self.format, self.path_user)
            dialogue.destroy()

        # Bouton pour valider
        bouton_valider = tk.Button(dialogue, text="Valider", command=valider)
        bouton_valider.pack(pady=10)

        dialogue.transient(self.window)  # Pour que la fenêtre de dialogue soit modale
        dialogue.grab_set()  # Pour capturer tous les événements
        self.window.wait_window(dialogue)  # Pour attendre la fermeture de la fenêtre de dialogue
