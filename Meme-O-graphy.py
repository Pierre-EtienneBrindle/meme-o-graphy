import customtkinter as ctk
from tkinter import filedialog

class MemeOGraphy :
    def __init__(self,root):
        self.root = root
        self._buildLayouts()
        self._buildWidgets()
        self.root.mainloop()
    
    def _buildLayouts(self):
        self.imagesFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=2)
        self.imagesFrame.grid(row=1,column=0,padx=5,pady=5)

        self.dataFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=2)
        self.dataFrame.grid(row=2,column=0,padx=5,pady=5)

    def _buildWidgets(self):
        title = ctk.CTkLabel(self.root, text= "Meme-O-Graphy")
        title.grid(row=0,column=0,sticky = "ew",padx=5,pady=5)

        self.imageSelection = ctk.CTkButton(self.imagesFrame,text="Select image",command=self._selectImage)
        self.imageSelection.grid(row = 1,column=0,padx=5,pady=5)
    
    def _selectImage(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MemeOGraphy(root)