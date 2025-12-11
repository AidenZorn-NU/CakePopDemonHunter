import numpy as np
import cv2 as cv
import random

print('This is mirror.py')

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

first = True
score = 0

prepare_demon_arrive_corner = True
prepare_demon_arrive_top = True
lose = False
demon_attack_corner = False
demon_attack_top = False
hunter_color = (0,255,255)
demon_color = (50,50,250)
demon_attack_corner_countdown = 300
demon_hunted = False

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

    # Display score
    cv.putText(frame, 'Score: '+str(score), (150,50), cv.FONT_HERSHEY_SIMPLEX, 2, hunter_color, 4)
    
    if not lose:
        ## determine demon activity

        # start countdown for corner attack
        if prepare_demon_arrive_corner:
            prepare_demon_arrive_corner = False
            demon_arrive_corner_timer = random.randint(60,200)
            demon_attack_corner_location = random.randint(1,4)

        if demon_arrive_corner_timer==0:
            demon_attack_corner = True
            if score<10:
                demon_attack_corner_countdown = 300
            if score<20:
                demon_attack_corner_countdown = 200
            else:
                demon_attack_corner_countdown = 150

        
        if demon_attack_corner and demon_attack_corner_countdown<=0:
            lose = True
        
        if prepare_demon_arrive_top:
            prepare_demon_arrive_top = False
            demon_arrive_top_timer = random.randint(1200,3600)
        
        if demon_arrive_top_timer==0:
            demon_attack_top = True
            demon_top_position = [-100,0,270,370]
        
        if demon_attack_top:
            demon_top_position = demon_top_position + [10,10,0,0]

        # demon countdowns/timers
        demon_arrive_corner_timer-=1
        demon_attack_corner_countdown-=1
        demon_arrive_top_timer-=1
        # calculate change in gray
        delta_1 = cv.absdiff(gray[0:100,0:100], prev_gray[0:100,0:100]).sum()
        delta_2 = cv.absdiff(gray[380:480,0:100], prev_gray[380:480,0:100]).sum()
        delta_3 = cv.absdiff(gray[0:100,540:640], prev_gray[0:100,540:640]).sum()
        delta_4 = cv.absdiff(gray[380:480,540:640], prev_gray[380:480,540:640]).sum()

        

        # color corner rectangles
        if delta_1>20000:
            defeat_1 = True
            color_1 = (255,0,0)
        else:
            defeat_1 = False
            color_1 = (100,100,100)
        
        if delta_2>20000:
            defeat_2 = True
            color_2 = (255,0,0)
        else:
            defeat_2 = False
            color_2 = (100,100,100)
        
        if delta_3>20000:
            defeat_3 = True
            color_3 = (255,0,0)
        else:
            defeat_3 = False
            color_3 = (100,100,100)

        if delta_4>20000:
            defeat_4 = True
            color_4 = (255,0,0)
        else:
            defeat_4 = False
            color_4 = (100,100,100)
        
        # draw corner rectangles
        cv.rectangle(frame, (0,0),(100,100), color_1,2)
        cv.rectangle(frame, (0,380),(100,480), color_2,2)
        cv.rectangle(frame, (540,0),(640,100), color_3,2)
        cv.rectangle(frame, (540,380),(640,480), color_4,2)

        # draw demon
        if demon_attack_corner:
            if demon_attack_corner_location==1:
                cv.circle(frame, (50,50),40, demon_color,-1)
                cv.putText(frame, str(demon_attack_corner_countdown), (0,130), cv.FONT_HERSHEY_SIMPLEX, 1, demon_color, 2)
                if defeat_1:
                    demon_hunted = True
            elif demon_attack_corner_location==2:
                cv.circle(frame, (50,430),40, demon_color,-1)
                cv.putText(frame, str(demon_attack_corner_countdown), (0,370), cv.FONT_HERSHEY_SIMPLEX, 1, demon_color, 2)
                if defeat_2:
                    demon_hunted = True
            elif demon_attack_corner_location==3:
                cv.circle(frame, (590,50),40, demon_color,-1)
                cv.putText(frame, str(demon_attack_corner_countdown), (540,130), cv.FONT_HERSHEY_SIMPLEX, 1, demon_color, 2)
                if defeat_3:
                    demon_hunted = True
            else:
                cv.circle(frame, (590,430),40, demon_color,-1)
                cv.putText(frame, str(demon_attack_corner_countdown), (540,370), cv.FONT_HERSHEY_SIMPLEX, 1, demon_color, 2)
                if defeat_4:
                    demon_hunted = True

        if demon_hunted:
            demon_hunted = False
            prepare_demon_arrive_corner = True
            demon_attack_corner = False
            score+=1

        # face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w,y+h), hunter_color, 2)

        # Display the resulting frame
        #cv.imshow('frame', gray)

        # save previous frame
        cv.imshow('frame',frame)
        prev_gray = gray

    else:
        cv.putText(frame, 'YOU LOSE', (10,300), cv.FONT_HERSHEY_SIMPLEX, 4, demon_color, 10)

        # save previous frame
        cv.imshow('frame',frame)
        prev_gray = gray
    
    
    
    # see if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
