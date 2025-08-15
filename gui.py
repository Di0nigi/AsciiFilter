import tkinter as tk
import numpy
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import zoom

import filters as f

class App:
    def __init__(self,r):

        self.filters = ["Basic Ascii", "Color Ascii"]
        self.toApply="Basic Ascii"
        self.currentFile=""
        self.currentImage = None
        self.currentFont = tk.StringVar()
        self.fileName="None"
        self.displayedIm = np.zeros(shape=(800,800,3),dtype=np.uint8)
        self.displayedIm[:, :] = [170, 170, 170]
        self.w = 1000
        self.h = 800
        self.r = r
        self.r.title("Ascii Converter")
        self.r.geometry(f"{self.w}x{self.h}")
        self.sideSetting= tk.Frame(self.r,bg="grey",height=self.h,width=self.w-self.h)
        self.sideSetting.place(x=0,y=0)
        self.sidePanel()
        self.imPanel = tk.Frame(self.r,bg="dark grey",height=self.h,width=self.h)
        self.imPanel.place(x=self.w-self.h,y=0)
        self.imagePanel()
        return
    def run(self):
        self.r.mainloop()
        return
    def sidePanel(self):
        self.nameFile = tk.Label(text=self.fileName, font=("TkDefaultFont",10),width=25,anchor="w")
        self.nameFile.place(x=0,y=0)
        self.fileBt=tk.Button(self.sideSetting, text="Choose file", command=self.importFile,width=28)
        self.fileBt.place(x=0,y=25)
        
        self.dwnSampleLabel = tk.Label(text="Downsampling size", font=("TkDefaultFont",10),width=25,anchor="w")
        self.dwnSampleLabel.place(x=0,y=55)
        self.dwnSampleField=tk.Entry(self.sideSetting,width=33)
        self.dwnSampleField.place(x=0,y=80)

        self.fontSizeLabel = tk.Label(text="Font size", font=("TkDefaultFont",10),width=25,anchor="w")
        self.fontSizeLabel.place(x=0,y=105)
        self.fontSizeField=tk.Entry(self.sideSetting,width=33)
        self.fontSizeField.place(x=0,y=125)

        self.filtersLabel = tk.Label(text="Pick effect", font=("TkDefaultFont",10),width=25,anchor="w")
        self.filtersLabel.place(x=0,y=145)
        var = tk.StringVar(value=self.filters[0]) 

        dropdown = tk.OptionMenu(self.sideSetting, var, *self.filters, command=self.onChange)
        dropdown.place(x=0,y=200)

        self.fileBt=tk.Button(self.sideSetting, text="Apply", command=self.applyFilter,width=28)
        self.fileBt.place(x=0,y=225)
        return
    
    def onChange(self,value):
        self.toApply=value

        print("You chose:", value)

    def applyFilter(self):
        return

    def imagePanel(self):
        self.imTkImage = ImageTk.PhotoImage(Image.fromarray(self.displayedIm))
        self.imDisplayer = tk.Label(self.imPanel, image=self.imTkImage, width=self.h-10, height=self.h-10)
        self.imDisplayer.place(x=0, y=0)   

        return
    def importFile(self):
        self.currentFile=filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png"),("Image files", "*.jpg"),("Image files", "*.JPEG")]
        
    )
        self.nameFile.config(text=self.currentFile.split("/")[-1])
        print(self.currentFile)

        self.currentImage = Image.open(self.currentFile)

        displayable = self.convertToSize(np.array(self.currentImage))

        self.imTkImage = ImageTk.PhotoImage(Image.fromarray(displayable))
        self.imDisplayer.config(image=self.imTkImage)
        self.imDisplayer.image = self.imTkImage
        return
    def onSelect(self,value):
        

        return
   
        ''' def convertToSize(self,im):
        w=self.imDisplayer.winfo_width()-1
        resized=resize(im,(computeRatio(w,1/1),w,3))

        return resized'''
    def convertToSize(self,im):
   
        w = self.imDisplayer.winfo_height() - 1
         
        ratio = im.shape[0]/im.shape[1]
        print(ratio)
        
        #im = im.astype(np.uint8)
        
        #pilImage = Image.fromarray(im)
        
        #resizedPil = pilImage.resize((w, h), Image.LANCZOS)
        
        #resizedArr = np.array(resizedPil)

        resized=self.resize(im,(w,self.computeRatio(w,ratio),3))
        
        return resized
    
    def resize(self,dataArr, size):    
        factors = [n / o for n, o in zip(size, dataArr.shape[:2])]  
        resized = zoom(dataArr, factors + [1], order=3) 
        return resized
    def computeRatio(self,dim,ratio):
    
        dim2 = dim / ratio
        #elif ori == "p":
        #   dim2= ratio * dim
        #print(dim2)
        return dim2



def main():
    root = tk.Tk()
    app = App(r=root)
    app.run()
    return
    

print(main())