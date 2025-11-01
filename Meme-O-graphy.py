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
        self.imagesFrame.grid(row=1,column=0,padx=5,pady=5)

        self.dataFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=5)
        self.dataFrame.grid(row=1,column=1,padx=5,pady=5)

    def _buildWidgets(self):
        title = ctk.CTkLabel(self.root, text= "Meme-O-Graphy",font=("Arial",20))
        title.grid(row=0,column=0,columnspan = 2,sticky = "ew",padx=5,pady=5)

        self.imageSelection = ctk.CTkButton(self.imagesFrame,text="Select image",command=self._selectImage)
        self.imageSelection.grid(row = 0,column=0,padx=5,pady=5,sticky= "n")

        self.image = ctk.CTkLabel(self.imagesFrame,text = "")
        self.image.grid(row=1,column=0,padx=5,pady=5)
    
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

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MemeOGraphy(root)