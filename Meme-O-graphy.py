import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import os
from PIL import Image, ImageTk


formats = [".png",".gif",".jpg",".bmp",".webp"]
encryptionMethods = ["RSA","autres"]

class MemeOGraphy :
    def __init__(self,root):
        self.root = root
        self.menubar = tk.Menu(self.root)
        self.currentImageFilepath = None
        self._setBackground(self.root,"bg.png")
        self._buildMenu()
        self._buildLayouts()
        self._buildWidgets()
        self.root.mainloop()
    
    def _buildMenu(self):
        self.menu = tk.Menu(self.menubar,tearoff=0,font=("Inter",12))
        self.menu.add_command(label="Create Key",command=lambda: self._changeLayout(0))
        self.menu.add_separator()
        self.menu.add_command(label="Encryption",command=lambda: self._changeLayout(1))
        self.menu.add_separator()
        self.menu.add_command(label="Decryption",command=lambda : self._changeLayout(2))
        self.menubar.add_cascade(label="Pages", menu=self.menu,font=("Inter",14))
        self.root.config(menu=self.menubar)

    def _buildLayouts(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.imagesFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=2)
        self.imagesFrame.grid(row=1,column=1,padx=5,pady=5,sticky = "")
        self.imagesFrame.grid_remove()

        self.dataFrame = ctk.CTkFrame(self.root,border_color="grey",border_width=2,corner_radius=2)
        self.dataFrame.grid(row=1,column=0,padx=5,pady=5,sticky= "")

        self.encryptionFrame = ctk.CTkFrame(self.dataFrame,border_color="grey",border_width=2,corner_radius=2)
        self.encryptionFrame.grid(row=1,column=0,padx=5,pady=5)
        self.encryptionFrame.grid_remove()

        self.decryptionFrame = ctk.CTkFrame(self.dataFrame,border_color="grey",border_width=2,corner_radius=2)
        self.decryptionFrame.grid(row=1,column=0,padx=5,pady=5)
        self.decryptionFrame.grid_remove()

        self.outputFrame = ctk.CTkFrame(self.dataFrame,border_color="grey",border_width=2,corner_radius=2)
        self.outputFrame.grid(row=0,column=1,padx=5,pady=5,rowspan=2)

        self.keyCreationFrame = ctk.CTkFrame(self.dataFrame,border_color="grey",border_width=2,corner_radius=2)
        self.keyCreationFrame.grid(row=1,column=0,padx=5,pady=5)

    def _buildWidgets(self):
        box = ctk.CTkFrame(self.root,border_width =2,corner_radius =2,border_color="red")
        box.grid(row=0,column=0,columnspan=2,sticky="n",padx=5,pady=5)
        title = ctk.CTkLabel(box, text = "Meme-O-Graphy",font=("Comic Sans MS",40),corner_radius=5)
        title.grid(row = 0,column = 0)
    
        #method
        self.encryptionMethod = ctk.CTkOptionMenu(self.dataFrame,values=encryptionMethods)
        self.encryptionMethod.grid(row=0,column=0,padx=5,pady=5)

        #image box
        self.imageSelection = ctk.CTkButton(self.imagesFrame,text = "Select image",command = self._selectImage)
        self.imageSelection.grid(row = 0,column=0,columnspan = 2,padx=5,pady=5)
        self.image = ctk.CTkLabel(self.imagesFrame,text = "")
        self.image.grid(row=1,column = 0,columnspan=2,padx = 5,pady = 5)

        #key creation
        self.createKey = ctk.CTkButton(self.keyCreationFrame,text = "Generate key",command=self._generateKey)
        self.createKey.grid(row=0,column=0,padx=5,pady=5)

        #encryption
        self.inputCryption = ctk.CTkEntry(self.encryptionFrame, placeholder_text = "Enter message")
        self.inputCryption.grid(row = 2,column = 0,padx = 5,pady = 5,sticky ="nw")
        self.initCryption = ctk.CTkButton(self.encryptionFrame,text = "Encrypt message",command = self._initCryption)
        self.initCryption.grid(row = 1,column = 0,padx = 5,pady = 5)
        
        #decryption
        self.initDecryption = ctk.CTkButton(self.decryptionFrame,text = "Decrypt message",command = self._initDecryption)
        self.initDecryption.grid(row = 2,column = 0,padx = 5,pady = 5)

        #output
        self.outputDecryption = ctk.CTkTextbox(self.outputFrame, width = 200, corner_radius = 5)
        self.outputDecryption.grid(row = 0, column = 0, padx=5,pady=5,sticky="nsew")
        self.outputDecryption.configure(state="disabled")

    def _generateKey(self):
        self._updateOutput("Generating key")
        algo = self.encryptionMethod.get()
        #call code PE

    def _changeLayout(self,layoutNb):
        #most bs way to do this 
        match layoutNb:
            case 0:
                self.imagesFrame.grid_remove()
                self.decryptionFrame.grid_remove()
                self.encryptionFrame.grid_remove()
                self.keyCreationFrame.grid()
            case 1:
                self.imagesFrame.grid()
                self.decryptionFrame.grid_remove()
                self.keyCreationFrame.grid_remove()
                self.encryptionFrame.grid()
            case 2:
                self.imagesFrame.grid()
                self.encryptionFrame.grid_remove()
                self.keyCreationFrame.grid_remove()
                self.decryptionFrame.grid()

    def _selectImage(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        #check extension
        extension = os.path.splitext(filepath)[1].lower()
        if extension not in formats:
            messagebox.showerror(f"Invalid format", f'Select a {format} file')
            return
        self.currentImageFilepath = filepath
        self.imageSelection.configure(text=os.path.basename(filepath))
        self._updateImage(filepath)
    
    def _updateImage(self,filepath):
        self.imagesFrame.configure(border_color = "grey")
        
        img_pil = Image.open(filepath)

        frame_w = self.root.winfo_width()/2 or 1
        frame_h = self.root.winfo_height()/2 or 1

        ratio = min(frame_w / img_pil.width, frame_h / img_pil.height)
        new_w = int(img_pil.width * ratio)
        new_h = int(img_pil.height * ratio)

        img_pil = img_pil.resize((new_w, new_h), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        self.image.configure(image=img_tk)
        self.image.image = img_tk
    def _updateOutput(self,msg):
        self.outputDecryption.configure(state ="normal")
        self.outputDecryption.insert("0.0",msg)
        self.outputDecryption.configure(state="disabled")
    def _verifyImage(self):
        if  not self.image.cget("image"):
            self._updateOutput("no image\n")
            self.imagesFrame.configure(border_color = "red")
            return False
        else :
            self.imagesFrame.configure(border_color = "grey")
            return True
    def _initCryption(self) :
        input = True
        #clear output
        self.outputDecryption.configure(state ="normal")
        self.outputDecryption.delete("1.0","end")

        #make sur an image is selected
        image = self._verifyImage()
        #make sure you input a message
        if self.inputCryption.get() == "":
            self._updateOutput("No message\n")
            self.inputCryption.configure(border_color="red")
            input =False
        else : 
             self.inputCryption.configure(border_color = "grey")
        if not input or not image : return 
        
        self.initCryption.configure(state="disabled")
        self.inputCryption.configure(state="disabled")
        self._updateOutput("Cryption started")
        
        msg = self.inputCryption.get()
        algo = self.encryptionMethod.get()
        imgPath = self.currentImageFilepath
        #call code PE

        self.initCryption.configure(state="normal")
        self.inputCryption.configure(state="normal")
    def _initDecryption(self) :
        self.outputDecryption.configure(state ="normal")
        self.outputDecryption.delete("1.0","end")
        if not self._verifyImage() : return

        self._updateOutput("We're no strangers to love You know the rules and so do I A full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching, but you're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it And if you ask me how I'm feeling Don't tell me you're too blind to see Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you (Ooh, give you up) (Ooh, give you up) Never gonna give, never gonna give (Give you up) Never gonna give, never gonna give (Give you up) We've known each other for so long Your heart's been aching, but you're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you")

    def _setBackground(self,container, image_path, keep_aspect=True):

        container.update_idletasks()
        W = max(1, container.winfo_width())
        H = max(1, container.winfo_height())

        pil = Image.open(image_path).convert("RGB")

        def _fit_size(img, w, h):
            if not keep_aspect:
                return (w, h)
            iw, ih = img.size
            s = min(w/iw, h/ih) if iw and ih else 1
            return (max(1, int(iw*s)), max(1, int(ih*s)))

        size = _fit_size(pil, W, H)
        bg_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=size)
        bg_lbl = ctk.CTkLabel(container, text="", image=bg_img)
        bg_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_lbl.lower()
        container._bg_pil = pil
        container._bg_img = bg_img
        container._bg_lbl = bg_lbl
        def _on_resize(_=None):
            w = max(1, container.winfo_width())
            h = max(1, container.winfo_height())
            new_size = _fit_size(container._bg_pil, w, h)
            container._bg_img.configure(size=new_size)

        container.bind("<Configure>", _on_resize)
        return bg_lbl
    

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MemeOGraphy(root)