import customtkinter as ctk

class MemeOGraphy :
    def __init__(self,root):
        self.root = root
        self._buildWidgets()
        self.root.mainloop()
    
    def _buildWidgets(self):
        title = ctk.CTkLabel(self.root, text= "Meme-O-Graphy")
        title.grid(row=0,column=0,sticky = "ew",padx=5,pady=5)

        self.imageSelection = ctk.CTkButton(self.root,text="Select image",command=self._selectImage)
        self.imageSelection.grid(row = 1,column=0,padx=5,pady=5)
    
    def _selectImage(self):
        pass

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MemeOGraphy(root)