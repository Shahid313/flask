import cv2
import random
import os
import glob
from PIL import Image
import shutil
import cv2


from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
import datetime
from PIL import Image, ImageFilter
from reportlab.lib.colors import HexColor


import string
import random
import shutil




#Create folder
def checkcreatefolder(name):
    shutil.rmtree(name, ignore_errors=True)
    try:
        # creating a folder named data
        if not os.path.exists(name):
            os.makedirs(name)
    except OSError:
        print ('Error: Creating directory of'+ name)

def cropped2(im):  
    (w,h) = im.size

    width = int((4/3)*h)

    cutw = (w-width)//2

    left = cutw
    top = 0
    right = cutw+width
    bottom = h

    if width<w:

        im = im.crop((left, top, right, bottom))
    else:
        im1 = im.resize((width,h))
        boxImage = im1.filter(ImageFilter.GaussianBlur(10))
        
        boxImage.paste(im,(-cutw,0 ))
        (w,h) = boxImage.size

        width = int((4/3)*h)

        cutw = (w-width)//2

        left = cutw
        top = 0
        right = cutw+width
        bottom = h
        im = boxImage.crop((left, top, right, bottom))
    return im

fol = ''.join(random.choices(string.ascii_uppercase, k = 5))



def getpdff(vid,color):
    time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fol = ''.join(random.choices(string.ascii_uppercase, k = 5))

    checkcreatefolder(fol)
    checkcreatefolder('output')
    
    
    data = os.path.join(fol, 'data')
    comb = os.path.join(fol, 'combined')
    
    checkcreatefolder(data)
    checkcreatefolder(comb)
    
    #Getting Image from Video
    cap= cv2.VideoCapture(vid)
    
    

    #Get total duration of video
    fps = cap.get(cv2.CAP_PROP_FPS)
    totalNoFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT);
    durationInSeconds = int((float(totalNoFrames) / float(fps))*1000)
    divider = durationInSeconds//24

    j=0
    for sec in range(durationInSeconds+1):
        if sec%divider==0:
            cap.set(cv2.CAP_PROP_POS_MSEC, sec)
            ret, frame = cap.read()
            if ret == False:
                break
            if j>=10:
                name=str(j)
            else:
                name='0'+str(j)

            cv2.imwrite(data+'/'+name+'.jpg',frame)
            j+=1

    cap.release()
    cv2.destroyAllWindows() 
    
    
    #cropping data
    print("resizing images")
    for filename in (glob.glob(data+ '\\*')):
        img = Image.open(filename)
        im = cropped2(img)
        im.save(filename , 'JPEG', quality=100)

        #GIF

        # filepaths
        fp_in = data
        
        #Change
        fp_out = "output/"+time+"_data.gif"

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in+ '\\*'))]
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                 save_all=True,optimize=True, duration=100, loop=0)


    #Get images
    print("Combining Images")

    imgfiles = (glob.glob(data+ '\\*'))
    totfiles = len(imgfiles)

    for i in range(totfiles):
        topimg = Image.open(imgfiles[i])
        try:
    #         img = Image.open(imgfiles[i+1]).crop((0, 300, 800, 600))
            img = Image.open(imgfiles[i+1])
            btmimg = img.crop((0,img.size[1]//2, img.size[0],img.size[1]))
        except:
    #         btmimg = Image.open(imgfiles[0]).crop((0, 300, 800, 600))
            img = Image.open(imgfiles[0])
            btmimg = img.crop((0,img.size[1]//2, img.size[0],img.size[1]))

        topimg.paste(btmimg, (0,img.size[1]//2))
        if i>=10:
            name=str(i)
        else:
            name='0'+str(i)

        filename = comb+'/comb'+name+'.jpg'

        topimg.save(filename, 'JPEG')

        
    #get PDF
    #change
    imgforpdf = (glob.glob(comb+ '\\*'))
    totimg = len(imgforpdf)

    pagesize = (297 * mm, 210 * mm)
    pdfname = "output/"+time+"_imgreport.pdf"
    c = canvas.Canvas(pdfname)
    c.setPageSize(pagesize)


    datetim = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")

    sheets=len(list(range(0,totimg,4)))
    shno=1    
    print("Generating Pdf")
    for i in list(range(0,totimg,4)):

        c.setFont('Helvetica',8)

        #Adding Image to pdf.
        c.drawImage(imgforpdf[i], 11*mm, 105*mm, 135*mm, 102*mm)      
        c.drawImage(imgforpdf[i+1], 151*mm, 105*mm, 135*mm, 102*mm)  
        c.drawImage(imgforpdf[i+2], 11*mm, 3*mm, 135*mm, 102*mm)
        c.drawImage(imgforpdf[i+3], 151*mm, 3*mm, 135*mm, 102*mm)

        #Adding page Number
        c.drawString(146.5*mm, 204*mm,str(i+1))
        c.drawString(287*mm, 204*mm,str(i+2)) 
        c.drawString(146.5*mm, 4*mm,str(i+3))
        c.drawString(287*mm, 4*mm,str(i+4))

            #Setting number on image     
        c.setFillColor(HexColor(color))
        c.drawString(78.5*mm, 204*mm,str(i+1))
        c.drawString(218.5*mm, 204*mm,str(i+2))
        c.drawString(78.5*mm, 102*mm,str(i+3))
        c.drawString(218.5*mm, 102*mm,str(i+4))


        #Extra Text
        c.setFillColor(HexColor('#000'))
        c.rotate(270)
        c.setFont('Courier',12)
        c.drawString(-170*mm, 290*mm,"The German Kurbelkiste | Create something WUNDERVOLL")
        c.drawString(-150*mm, 4*mm,"www.german-kurbelkiste.de")
        c.setFont('Courier',9)
        c.drawString(-200*mm, 4*mm,"Bilder "+str(i+1)+'-'+str(i+4)+'/'+str(totimg))
        c.drawString(-70*mm, 4*mm, datetim)
        c.drawRightString(-11*mm, 4*mm,"S. "+str(shno)+'/'+str(sheets))

        shno=shno+1
        c.showPage()

    c.save()
    shutil.rmtree(fol)


    return pdfname

