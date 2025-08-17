import numpy as np
from PIL import Image,ImageFont,ImageDraw
import cv2


#chars = ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/*#MW&8%B@$'
chars = ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
#chars = ' .\'`^",:;Il!i><~+_-?][}{\\1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

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

def drawText(img,charList,font,color,spacingDims):

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
            x+=spacingDims[0]
            i+=1

        y+=spacingDims[1]

    
    #image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB)
    image = np.array(img)

    return image

def toTextFile(fileName,charlist):

    with open (fileName,mode="w",encoding="utf-8") as f:
        for line in charlist:
            f.write(line)
            f.write("\n")
        f.close()
    return

### FILTERS

def applyBasic(img,bg,fg,fontSz):

    
    font = ImageFont.truetype("arial.ttf", fontSz)

    chars,cols = pixelTochar(img)

    dim1=(fontSz//2)+1
    dim2=fontSz+1

    #print((dim1,dim2))

  

    cols = np.zeros_like(cols)
    cols=np.clip(np.array(cols)+fg,a_min=0,a_max=255)


    cols=cols.tolist()

    sz = determineSize(font=font,rowSpace=dim2,lettSpace=dim1,numChar=len(chars[0]),numLines=len(chars),text=chars[0][0])

    
    print(sz)

   #sz = determineSize(font=font,rowSpace=6,lettSpace=3,numChar=len(chars[0]),numLines=len(chars),text=chars[0][0])

    canvas = np.zeros(shape=sz,dtype=np.uint8)
    canvas = np.clip(canvas+bg,a_min=0,a_max=255)
    canvas= canvas.astype(np.uint8)
    
    #img = np.mean(img,axis=2)

    canvas = Image.fromarray(canvas)

    ret = drawText(img=canvas,charList=chars,font=font,color=cols,spacingDims=(dim1,dim2))
    #ret = toTextFile("prova.txt",chars)

    ret = Image.fromarray(ret)

    return ret

def basicColor(img,bg,fontSz):
    font = ImageFont.truetype("arial.ttf", fontSz)

    chars,cols = pixelTochar(img)

    dim1=(fontSz//2)+1
    dim2=fontSz+1

    

    sz = determineSize(font=font,rowSpace=dim2,lettSpace=dim1,numChar=len(chars[0]),numLines=len(chars),text=chars[0][0])


    canvas = np.zeros(shape=sz,dtype=np.uint8)
    canvas = np.clip(canvas+bg,a_min=0,a_max=255)
    canvas= canvas.astype(np.uint8)
    
    #img = np.mean(img,axis=2)

    canvas = Image.fromarray(canvas)

    ret = drawText(img=canvas,charList=chars,font=font,color=cols,spacingDims=(dim1,dim2))
    #ret = toTextFile("prova.txt",chars)

    ret = Image.fromarray(ret)
    return ret

def clarityEffect(img, strength=0.5):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    blur = cv2.GaussianBlur(l, (0, 0), sigmaX=3, sigmaY=3)
    details = cv2.subtract(l, blur)
    if strength >= 0:
        lNew = cv2.addWeighted(l, 1.0, details, strength, 0)
    else:
        lNew = cv2.addWeighted(l, 1.0, details, strength, 0)
    lNew = np.clip(lNew, 0, 255).astype(np.uint8)
    labNew = cv2.merge([lNew, a, b])
    result = cv2.cvtColor(labNew, cv2.COLOR_LAB2BGR)
    return result

def preprocess(img,dwnSamp):

    width, height = img.size


    newSize = (width //dwnSamp , height // dwnSamp)

    #print(newSize)

    img = img.resize(newSize, Image.Resampling.LANCZOS)

    img= np.array(img)

    return img



def main():
    imgTitle = "D:\dionigi\Desktop\\x100 prov\edchives\\templateinstahg35.jpg"
    img = Image.open(imgTitle)

    img = preprocess(img,10)
    

    #img.show()

    #img= np.array(img)0
    out = applyBasic(img,bg=(0,0,50),fg=(255,0,0))
    #out = basicColor(img,bg=(100,100,100))

    out.show()
    out.save("prova.png")

    return "done"

#print(main())