import glob
import os
import cv2
import time
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

# defining a function to clean the folder
def clean_folder():
    print("Clean folder has started")
    images = glob.glob("Images/*.png")
    for image in images:
        os.remove(image)
    print("Clean folder has ended")


while True:
    status = 0

#start the camera
    check , frame = video.read()

#convert frame to gray colour
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21),0,None)

#storing each gray frame in a list
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

#apply colour vAriation technique to seperate image from background images
    thres_frame = cv2.threshold(delta_frame,45, 255,
                                cv2.THRESH_BINARY)[1]
    dil_frame=cv2.dilate(thres_frame,None,iterations=2)

# noting area of interest to image detection
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
#adding conditioning to image detection based
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w,h = cv2.boundingRect(contour)
#Using the dimension to generate an rectangle to indicate object in the frame
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"Images/{count}.png", frame)
            count = count + 1
            AllImages = glob.glob("Images/*png")
            index = int(len(AllImages)/2)
            image_with_obj = AllImages[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:

# Threading to ensure both functions work concurrentky with video lagging
        email_thread =  Thread(target=send_email,args=(image_with_obj, ))
        email_thread.daemon =True
        clean_thread =  Thread(target=clean_folder)
        clean_thread.daemon =True
        email_thread.start()



    cv2.imshow("Video",frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()

clean_thread.start()





