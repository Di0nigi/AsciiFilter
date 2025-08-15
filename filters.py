import numpy as np
from PIL import Image,ImageFont,ImageDraw
import cv2


#chars= ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/*#MW&8%B@$'
chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
#chars= ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

def pixelTochar(l):
    charL=[]
    colors=[]
    for x,y in enumerate(l):
        row=""
        rowCol=[]
        for i,j in enumerate(y):
            colVal=(int(j[0]),int(j[1]),int(j[2]))
            pixB=(int(j[0])+int(j[1])+int(j[2]))/3
            ind=(pixB/255)*len(chars)
            charvalue= chars[int(ind)-1]
            row+=charvalue
            row+=charvalue
            rowCol.append(colVal)
            rowCol.append(colVal)
        colors.append(rowCol)
        charL.append(row)
    
    return charL,colors

def determineSize(font, rowSpace,lettSpace,numChar,numLines,text):
    charW = font.getbbox(text)[0]
    charH = font.getbbox(text)[1]
    rowSpace = rowSpace-charH
    width  = (charW + lettSpace) * numChar - lettSpace
    height = (charH + rowSpace) * numLines - rowSpace


    return (height,width,3)

def drawText(img,charList,font,color):

    #font = ImageFont.truetype("D:\dionigi\Documents\Python scripts\AsciiFilter\\assets\\fonts\COURE.FON", size)

    
    
    draw = ImageDraw.Draw(img)
    
    #draw.text(position, text, font=font, fill=color)
    y=0
    for ind,char in enumerate(charList):
        #print(len(char))
        x=0
        i=0

        
        
        for c in char:

            draw.text((x,y), c, font=font, fill=tuple(color[ind][i]))
            x+=3
            i+=1

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

### FILTERS

def applyBasic(img):

    font = ImageFont.truetype("arial.ttf", 5)

    chars,cols = pixelTochar(img)

    cols = np.clip(np.array(cols)+255,a_min=0,a_max=255)
    cols=cols.tolist()
    #print(cols)

    sz = determineSize(font=font,rowSpace=6,lettSpace=3,numChar=len(chars[0]),numLines=len(chars),text=chars[0][0])

    canvas = np.zeros(shape=sz,dtype=np.uint8)
    
    #img = np.mean(img,axis=2)

    canvas = Image.fromarray(canvas)

    ret = drawText(img=canvas,charList=chars,font=font,color=cols)
    #ret = toTextFile("prova.txt",chars)

    ret = Image.fromarray(ret)

    return ret

def basicColor(img):
    font = ImageFont.truetype("arial.ttf", 5)

    chars,cols = pixelTochar(img)

    sz = determineSize(font=font,rowSpace=6,lettSpace=3,numChar=len(chars[0]),numLines=len(chars),text=chars[0][0])

    canvas = np.zeros(shape=sz,dtype=np.uint8)
    
    #img = np.mean(img,axis=2)

    canvas = Image.fromarray(canvas)

    ret = drawText(img=canvas,charList=chars,font=font,color=cols)
    #ret = toTextFile("prova.txt",chars)

    ret = Image.fromarray(ret)
    return ret



def main():
    imgTitle = "D:\dionigi\Desktop\\x100 prov\edchives\\templateinstahg35.jpg"
    img = Image.open(imgTitle)
    width, height = img.size

    dwnSamp=2

    newSize = (width //dwnSamp , height // dwnSamp)

    print(newSize)

    img = img.resize(newSize, Image.Resampling.LANCZOS)

    #img.show()

    img= np.array(img)
    out = applyBasic(img)

    out.show()
    out.save("prova.png")

    return "done"

print(main())