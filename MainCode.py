# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:12:30 2023

@author: clara
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
import csv


"""For the two items following you should change the path to match where the files are for you, don't forget to change out to choose another video
to apply the code to and out to create a new result video instead of writing over the previous one"""
# Creates a VideoCapture object and read from input file
vid = cv2.VideoCapture(r'D:\OneDrive - ESEO\E4e\Stage\Finals\Vid1.mp4')
# Creates the object out which will sort the resulting video
out = cv2.VideoWriter(r'D:\OneDrive - ESEO\E4e\Stage\Finals\Out_1.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), 50, (1920,1080))
# Creates the csv file for the excel table, change the file name to not write over existing files, do not touch anything else
file = open(r'D:\OneDrive - ESEO\E4e\Stage\table1.csv', 'w', newline='')
writer = csv.writer(file,delimiter=";")


#Creates the background substractor object
backSub = cv2.createBackgroundSubtractorKNN(500,300.0,detectShadows = False)


# The transparency variable
alpha = 40
# The counter between adding transparency and reducing it
act = 0
# Variables to ensure the blinking is not too chaotic
a,b,c,e,f,g,h,j = 0,0,0,0,0,0,0,0
# Arrays for export to csv
transparency = []
timestamp=[]


# Function to create the court lines, takes both extremity points of the court line as entries
def lignes(xmin,ymin,xmax,ymax):
    cv2.line(lines,(xmin,ymin),(xmax,ymax),(255,255,255),4)
    cv2.line(lines,(xmin,ymin),(xmax,ymax),(255,255,255),6)
    cv2.line(lines,(xmin,ymin),(xmax,ymax),(255,255,255),8)
    cv2.line(lines,(xmin,ymin),(xmax,ymax),(0,0,0),2)


# This line is to grab the first frame of the video to always have the previous frame
ret, frame = vid.read()


# Main part of the code
while(vid.isOpened()):
    # Makes sure everything is the same size
    if(type(frame) == type(None)):
        pass
    else :
        frame = cv2.resize(frame, (1920, 1080))


    # Puts the frame back in the right position, if image appears upside down comment this line
    frame = cv2.flip(frame, -1)
    # Initialize the previous_frame variable and reads the new frame
    previous_frame = frame.copy()
    ret, frame = vid.read()


    # Makes sure everything is the same size again since we had copy and new frame read
    if(type(frame) == type(None)):
        pass
    else :
        frame = cv2.resize(frame, (1920, 1080))
    frame = cv2.flip(frame, -1)
   
    # Creates the "layer"/array that will contain the lines
    lines = np.empty_like(frame,dtype='uint8')


    # Creating the court lines on their separate layers thanks to the lignes function
    lignes(978,435,976,1033) #center court line
    lignes(538,439,428,502) #left court line up
    lignes(428,502,276,603) #left court line middle
    lignes(276,603,53,774) #left court line down
    lignes(1421,452,1527,519) #right court line top
    lignes(1527,519,1680,624) #right court line middle
    lignes(1680,624,1901,804) #right court line bottom
    lignes(538,439,978,435) #top court line left
    lignes(978,435,1421,452) #top court line right
    lignes(53,774,165,834) #bottom court line (first part)
    lignes(165,834,275,887) #bottom court line (second part)
    lignes(275,887,432,943) #bottom court line (third part)
    lignes(432,943,618,993) #bottom court line (fourth part)
    lignes(618,993,784,1022) #bottom court line (fifth part)
    lignes(784,1022,976,1033) #bottom court line (sixth part) half reached
    lignes(976,1033,1176,1027) #bottom court line (seventh part)
    lignes(1176,1027,1371,997) #bottom court line (eighth part)
    lignes(1371,997,1523,960) #bottom court line (ninth part)
    lignes(1523,960,1673,906) #bottom court line (tenth part)
    lignes(1673,906,1786,861) #bottom court line (eleventh part)
    lignes(1786,861,1901,804) #bottom court line (twelfth part)
   
    # While the video is being read sends back data, so goes on while the video is not finished
    if ret == True:
        # Makes a grayscale copy of the frames
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    


        # Calculates the difference between the previous frame and the current one
        frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)


        # Calculates the number of pixels that change between the frames and divides it up to a smaller number
        pix = cv2.countNonZero(frame_diff)
        pix = pix // 100
       
        # Gets rid of the non-moving parts of the image
        fgMask = backSub.apply(frame)
        dst = cv2.medianBlur(fgMask,5)
        res = cv2.bitwise_and(frame,frame, mask = dst)
        res = cv2.bitwise_not(res)
       
        # Adjusts the blinking speed/intensity according to the game speed. 20000 was the maximum amount of pixels varying between two frames
        # so I based the levels on percentages pof that number. As there were not a lot of times we were under 50% I didn't define more
        # intervals in the lower percentages. Then, as the percentage increases so does the number by which alpha increases and the act variable
        # which defines when we switch from adding transparency to decrasing it (and thus the "blinking speed")
        if act<40 :
            if (pix<(20000/100)*40) or a>=1:
                alpha+=5
                act+=1
                a+=1
                if (a==5):
                    a=0
            elif (pix<(20000/100)*50) or b>=1:
                alpha+=10
                act+=2
                b+=1
                if (b==5):
                    b=0
            elif (pix<(20000/100)*85) or c>=1:
                alpha+=15
                act+=3
                c+=1
                if (c==5):
                    c=0
            else :
                alpha+=20
                act+=5
                e+=1
            if alpha>80:
                alpha = 60
                act+=10
        else :
            if (pix<(20000/100)*40) or f>=1:
                alpha-=5
                act-=2
                f+=1
                if (f==5):
                    f=0
            elif (pix<(20000/100)*50) or g>=1:
                alpha-=10
                act-=2
                g+=1
                if (g==5):
                    g=0
            elif (pix<(20000/100)*85) or h>=1:
                alpha-=15
                act-=3
                h+=1
                if (h==5):
                    h=0
            else :
                alpha-=20
                act-=5
                j+=1
            if alpha<0:
                alpha = 40
                act+=10
        # Gets the timestamp of the video in milliseconds
        time = vid.get(cv2.CAP_PROP_POS_MSEC)
        if time%500 == 0:
            timestamp.append(time)
            transparency.append(alpha)
       
        # Puts the lines image's transparency at the corresponding transparency and turns it back into an array
        im_lines = Image.fromarray(lines)
        im_lines.putalpha(alpha)
        lines = np.asarray(im_lines).astype(np.uint8)
       
        res = cv2.cvtColor(res, cv2.COLOR_BGR2BGRA)
        # Adds the lines to the normal layer
        res = cv2.bitwise_and(res,lines)
       
        # Switches all the none completely white pixels to transparent on the layer
        img_alpha = cv2.cvtColor(res, cv2.COLOR_BGR2BGRA)
        img_alpha[np.where((res!=[255,255,255,255]).all(axis=-1))] = [0,0,0,0]
       
        # Changes the arrays to images to paste it on top of one another with transparency
        back = Image.fromarray(frame)
        fore = Image.fromarray(img_alpha)
       
        # Puts the images together as the end result  
        back.paste(fore, (0, 0), fore)
        end = np.asarray(back)
       
        # Shows the end result and writes it on the videowriter element
        cv2.imshow('Result', end)
        out.write(end)


        print(transparency)
        print(timestamp)
       
        # Allows to put an end to the program by pressing q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    else :
        break


print("a:", a ,", b:",b,", c:",c,", e:",e,", f:",f,", g:",g,", h:",h,", j:",j)
#for i in transparency :
writer.writerow(transparency)
writer.writerow(timestamp)
file.close()
# Cleans up the camera and closes any open windows
vid.release()
cv2.destroyAllWindows()
