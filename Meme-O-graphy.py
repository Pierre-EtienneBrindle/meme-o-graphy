import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk

formats = [".png",".gif",".jpeg",".bmp",".webp"]
class MemeOGraphy :
    def __init__(self,root):
        self.root = root
        self._buildLayouts()
        self._buildWidgets()
        self.root.mainloop()
    
    def _buildLayouts(self):
        self.imagesFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=5)
        self.imagesFrame.grid(row=1,column=1,padx=5,pady=5)

        self.dataFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=5)
        self.dataFrame.grid(row=1,column=0,padx=5,pady=5,sticky= "nw")

    def _buildWidgets(self):
        title = ctk.CTkLabel(self.root, text = "Meme-O-Graphy",font=("Arial",20))
        title.grid(row = 0,column = 0,columnspan = 2,sticky = "ew",padx = 5,pady = 5)

        self.imageSelection = ctk.CTkButton(self.imagesFrame,text = "Select image",command = self._selectImage)
        self.imageSelection.grid(row = 0,column=0,padx=5,pady=5,sticky= "n")

        self.image = ctk.CTkLabel(self.imagesFrame,text = "")
        self.image.grid(row=1,column = 0,padx = 5,pady = 5)

        self.inputCryption = ctk.CTkEntry(self.dataFrame, placeholder_text = "Enter message")
        self.inputCryption.grid(row = 0,column = 0,padx = 5,pady = 5)

        self.initCryption = ctk.CTkButton(self.dataFrame,text = "Encrypt message",command = self._initCryption)
        self.initCryption.grid(row = 0,column = 1,padx = 5,pady = 5)

        self.initDecryption = ctk.CTkButton(self.dataFrame,text = "Decrypt message",command = self._initDecryption)
        self.initDecryption.grid(row = 1,column = 1,padx = 5,pady = 5)

        #self.encryptionMethod = ctk.CTkOptionMenu()

    def _selectImage(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        #check extension
        extension = os.path.splitext(filepath)[1].lower()
        if extension not in formats:
            messagebox.showerror(f"Invalid format", f'Select a {format} file')
            return

        self.imageSelection.configure(text=os.path.basename(filepath))
        self._updateImage(filepath)
    
    def _updateImage(self,filepath):
        img_pil = Image.open(filepath)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image.configure(image = img_tk)

    def _initCryption(self) :
        self.initCryption.destroy()
        self.inputCryption.configure(state="disabled")
        entry = self.inputCryption.get()
        #pierreEtienneBrindle(entry)
        self.outputDecryption = ctk.CTkTextbox(self.dataFrame, width = 100, corner_radius = 0)
        self.outputDecryption.grid(row = 0, column = 3, sticky = "nsew")
        self.outputDecryption.insert("0.0", "Cryption started")
        self.outputDecryption.grid(row = 0,column = 3,padx = 5,pady = 5)
        
        
    def _initDecryption(self) :
        self.outputDecryption = ctk.CTkTextbox(self.dataFrame, width = 400, corner_radius = 0)
        self.outputDecryption.grid(row = 1, column = 3, sticky = "nsew")
        self.outputDecryption.insert("0.0", "We're no strangers to love You know the rules and so do IA full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching, but you're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it And if you ask me how I'm feeling Don't tell me you're too blind to see Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you (Ooh, give you up) (Ooh, give you up) Never gonna give, never gonna give (Give you up) Never gonna give, never gonna give (Give you up) We've known each other for so long Your heart's been aching, but you're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you")
        self.outputDecryption.grid(row = 1,column = 3,padx = 5,pady = 5)


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MemeOGraphy(root)