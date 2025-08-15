import numpy as np
from PIL import Image,ImageFont,ImageDraw
import cv2


#chars= ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/*#MW&8%B@$'
chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
#chars= ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

def pixelTochar(l):
    charL=[]
    for x,y in enumerate(l):
        row=""
        for i,j in enumerate(y):
            pixB=(int(j[0])+int(j[1])+int(j[2]))/3
            ind=(pixB/255)*len(chars)
            charvalue= chars[int(ind)-1]
            row+=charvalue
            row+=charvalue
        charL.append(row)
    
    return charL

def drawText(img,charList,size,color):

    #font = ImageFont.truetype("D:\dionigi\Documents\Python scripts\AsciiFilter\\assets\\fonts\COURE.FON", size)

    font = ImageFont.truetype("arial.ttf", size)
    
    draw = ImageDraw.Draw(img)
    
    #draw.text(position, text, font=font, fill=color)
    y=0
    for ind,char in enumerate(charList):
        #print(len(char))
        x=0
        
        
        for c in char:
            draw.text((x,y), c, font=font, fill=color)
            x+=3

        y+=6

    
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    return image

def toTextFile(fileName,charlist):

    with open (fileName,mode="w",encoding="utf-8") as f:
        for line in charlist:
            f.write(line)
            f.write("\n")
        f.close()
    return



def applyBasic(img,sz=(2000,2000,3)):

    

    if not sz:
        sz = img.shape

    canvas = np.zeros(shape=sz,dtype=np.uint8)
    

    #img = np.mean(img,axis=2)

    chars = pixelTochar(img)


    canvas = Image.fromarray(canvas)

    ret = drawText(img=canvas,charList=chars,size=5,color=(255,255,255))
    #ret = toTextFile("prova.txt",chars)

    ret = Image.fromarray(ret)





    return ret




def main():
    imgTitle = "D:\dionigi\Desktop\\x100 prov\edchives\\templateinstahg35.jpg"
    img = Image.open(imgTitle)
    width, height = img.size

    newSize = (width //15 , height // 15)

    print(newSize)

    img = img.resize(newSize, Image.Resampling.LANCZOS)

    #img.show()

    img= np.array(img)
    out = applyBasic(img)

    out.show()

    return "done"

print(main())