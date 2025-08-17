import tkinter as tk
import numpy as np
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
from scipy.ndimage import zoom
import cv2

import filters as f

class App:

    def __init__(self,r):

        self.alphaVal=1
        self.betaVal=0
        self.gammaVal=0.0

        self.clarityVal=0.0
        self.lastClarity=0.0


        self.lastG=0.0
        self.lastA=1.0

        


        self.filters = ["None","Basic Ascii", "Color Ascii"]
        self.bckg=(0,0,0)
        self.fgC=(255,255,255)
        self.fontSize=5
        self.toApply=self.filters[0]
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
        self.fontSizeField.insert(0, "5")
        self.fontSizeField.place(x=0,y=125)

        self.filtersLabel = tk.Label(text="Pick effect", font=("TkDefaultFont",10),width=25,anchor="w")
        self.filtersLabel.place(x=0,y=145)
        var = tk.StringVar(value=self.filters[0]) 

        dropdown = tk.OptionMenu(self.sideSetting, var, *self.filters, command=self.onChange)
        dropdown.place(x=0,y=200)

        self.colorBtn1 = tk.Button(self.sideSetting, text="Background color", command=self.pickColorBkg)
        self.colorBtn1.place(x=0,y=225)

        self.colorLabel1 = tk.Label(self.sideSetting,  width=20, height=2)
        self.colorLabel1.config(bg="#000000")
        self.colorLabel1.place(x=0,y=250)

        self.colorBtn2 = tk.Button(self.sideSetting, text="Foreground color", command=self.pickColorFg)
        self.colorBtn2.place(x=0,y=275)

        self.colorLabel2 = tk.Label(self.sideSetting, width=20, height=2)
        self.colorLabel2.config(bg="#FFFFFF")
        self.colorLabel2.place(x=0,y=300)

        self.fileBt=tk.Button(self.sideSetting, text="Apply", command=self.applyFilter,width=28)
        self.fileBt.place(x=0,y=330)

        self.fileBt=tk.Button(self.sideSetting, text="Save", command=self.saveFile,width=28)
        self.fileBt.place(x=0,y=350)

        self.contrastLabel = tk.Label(text="Contrast", font=("TkDefaultFont",10),width=25,anchor="w")
        self.contrastLabel.place(x=0,y=380)
        self.sliderContrast = tk.Scale(self.sideSetting, from_=0,to=2,resolution=0.00001, orient='horizontal',command=self.updateContrast)
        self.sliderContrast.set(1)
        self.sliderContrast.place(x=0,y=400)


        self.expLabel = tk.Label(text="Exposure", font=("TkDefaultFont",10),width=25,anchor="w")
        self.expLabel.place(x=0,y=440)

        self.sliderExp = tk.Scale(self.sideSetting, from_=-4, to=4,resolution=0.001, orient='horizontal',command=self.updateExp)
        self.sliderExp.place(x=0,y=490)

        self.expLabel = tk.Label(text="Clarity", font=("TkDefaultFont",10),width=25,anchor="w")
        self.expLabel.place(x=0,y=550)

        self.sliderExp = tk.Scale(self.sideSetting, from_=-5, to=5,resolution=0.01, orient='horizontal',command=self.updateClarity)
        self.sliderExp.place(x=0,y=580)

        return
    
    def updateClarity(self,val):
        self.clarityVal=float(val)
        
        return

    def updateExp(self,val):
        #self.gammaVal = float(val)
        
        gamma = 2.0 ** (float(val))
        self.gammaVal = 1.0 / gamma
        return
    def updateContrast(self,val):
        
        self.alphaVal = float(val)
        return
    
    def pickColorBkg(self):
        
        colorCode = colorchooser.askcolor(title="Choose a color")
        # color_code is a tuple: ((R, G, B), "#rrggbb")
        if colorCode[1]:  # if user didn’t cancel
            
            self.colorLabel1.config(text=colorCode[1], bg=colorCode[1])
            self.bckg=colorCode[0]

    def pickColorFg(self):
        
        colorCode = colorchooser.askcolor(title="Choose a color")
        # color_code is a tuple: ((R, G, B), "#rrggbb")
        if colorCode[1]:  # if user didn’t cancel
            
            self.colorLabel2.config(text=colorCode[1], bg=colorCode[1])
            self.fgC=colorCode[0]

    
    def onChange(self,value):
        self.toApply=value

        #print("You chose:", value)

    def saveFile(self):
        if self.currentImage:
            self.currentImage.save(f"out\\{self.fileName}_Ascii.png")
        return

    def applyFilter(self):
        if self.currentImage:
            self.currentImage=np.array(self.currentImage)

            if self.gammaVal!=self.lastG:
                
                self.lastG=self.gammaVal
                table = np.array([((i / 255.0) ** self.gammaVal) * 255 for i in range(256)]).astype("uint8")
                self.currentImage = cv2.LUT(self.currentImage, table)
                print(self.gammaVal)
                print(self.lastG)

            if self.alphaVal!=self.lastA:
                self.lastA=self.alphaVal
                self.currentImage = cv2.convertScaleAbs(self.currentImage, alpha=self.alphaVal, beta=0)

            if self.clarityVal!=self.lastClarity:
                self.lastClarity=self.clarityVal
                self.currentImage = f.clarityEffect(self.currentImage,self.clarityVal)



            if self.fontSizeField.get()!="":
                self.fontSize=int(self.fontSizeField.get())
            self.currentImage=Image.fromarray(self.currentImage)
            
            if self.toApply == "None":
                out=self.currentImage
            elif self.toApply == "Basic Ascii":
                im=f.preprocess(self.currentImage,dwnSamp=int(self.dwnSampleField.get()))
                out = f.applyBasic(im,bg=self.bckg,fg=self.fgC,fontSz=self.fontSize)
            elif self.toApply=="Color Ascii":
                im=f.preprocess(self.currentImage,dwnSamp=int(self.dwnSampleField.get()))
                out = f.basicColor(im,bg=self.bckg,fontSz=self.fontSize)
            self.currentImage=out
            self.displayPrev()
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

        self.fileName= self.currentFile.split("/")[-1]
        #print(self.currentFile)

        self.currentImage = Image.open(self.currentFile)

        self.displayPrev()

        return
  
    def onSelect(self,value):
        
        return
   
    def convertToSize(self,im):
    
        w = self.imDisplayer.winfo_height() - 1
         
        ratio = im.shape[0]/im.shape[1]
        #print(ratio)
        
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
        
        return dim2
    
    def displayPrev(self):

        if self.currentImage:

            displayable = self.convertToSize(np.array(self.currentImage))
            self.imTkImage = ImageTk.PhotoImage(Image.fromarray(displayable))
            self.imDisplayer.config(image=self.imTkImage)
            self.imDisplayer.image = self.imTkImage

        return



def main():
    root = tk.Tk()
    app = App(r=root)
    app.run()
    return
    

print(main())