import numpy as np
import cv2 as cv
 
print('This is mirror.py')

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

first = True

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # calculate change in gray
    if first:
        prev_gray = gray
        first = False
    delta = cv.absdiff(gray, prev_gray).sum()

    # Display Text
    cv.putText(frame, str(delta), (50,300), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 4)

    cv.putText(frame, "Hello", (50,50), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 4)

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