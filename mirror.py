import numpy as np
import cv2 as cv
 
print('This is mirror.py')

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

first = True
score = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    if first:
        prev_gray = gray
        first = False

    

    # calculate change in gray
    delta_1 = cv.absdiff(gray[0:100,0:100], prev_gray[0:100,0:100]).sum()
    delta_2 = cv.absdiff(gray[380:480,0:100], prev_gray[380:480,0:100]).sum()
    delta_3 = cv.absdiff(gray[0:100,540:640], prev_gray[0:100,540:640]).sum()
    delta_4 = cv.absdiff(gray[380:480,540:640], prev_gray[380:480,540:640]).sum()

    # Display Text
    # cv.putText(frame, str(delta_3), (50,300), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 4)
    cv.putText(frame, 'Score: '+str(score), (150,50), cv.FONT_HERSHEY_SIMPLEX, 2, (50,50,200), 4)

    # color corner rectangles
    if delta_1>20000:
        color_1 = (255,0,0)
    else:
        color_1 = (100,100,100)
    
    if delta_2>20000:
        color_2 = (255,0,0)
    else:
        color_2 = (100,100,100)
    
    if delta_3>20000:
        color_3 = (255,0,0)
    else:
        color_3 = (100,100,100)

    if delta_4>20000:
        color_4 = (255,0,0)
    else:
        color_4 = (100,100,100)
    
    # draw corner rectangles
    cv.rectangle(frame, (0,0),(100,100), color_1,2)
    cv.rectangle(frame, (0,380),(100,480), color_2,2)
    cv.rectangle(frame, (540,0),(640,100), color_3,2)
    cv.rectangle(frame, (540,380),(640,480), color_4,2)

    # face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x,y,w,h) in faces:
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 2)

    # Display the resulting frame
    #cv.imshow('frame', gray)

    # save previous frame
    cv.imshow('frame',frame)
    prev_gray = gray

    # see if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
