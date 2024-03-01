import cv2
import numpy as np
import dlib
from imutils import face_utils
import threading
import time
import os
from scipy.spatial import distance as dist
from imutils.video import VideoStream


#datFile = "C:\Users\LENOVO\Desktop\TRIAL AND ERROR PROJECTS\miniproject\shape_predictor_68_face_landmarks.dat"

def alarm(message):
    global alarm1
    global alarm2
    global alarm3
    global saying
    global saying2

    while alarm1:
        print('Call For Sleep')
        x = 'espeak "'+message+'"'
        os.system(x)

    if alarm2:
        print('Call For Drowsy')
        saying = True
        x = 'espeak "' + message + '"'
        os.system(x)
        saying = False
        
    if alarm3:
        print('Call For noFaceDetected')
        saying2 = True
        x = 'espeak "' + message + '"'
        os.system(x)
        saying2 = False


camera = cv2.VideoCapture(0)

def set_resolution(width, height):
    camera.set(3, width)
    camera.set(4, height)

#Initializing the dlib facial detectors
FaceDetector = dlib.get_frontal_face_detector()
ConditionPredictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleepy = 0
drowsy = 0
awake = 0
NoFace = 0
display=""
color=(0,0,0)
alarm1 = False
alarm2 = False
alarm3 = False
saying = False
saying2 = False

def compute(X, Y):
    EucDist = np.linalg.norm(X - Y)
    return EucDist

def blinked(x,y,z,d,e,f):
    u = compute(y,d) + compute(z,e)
    d = compute(x,f)
    EAR = u/(2.0*d)

    #EAR ratio calculator
    if(EAR>0.22):
        return 2

    elif(EAR>0.165 and EAR<=0.22):
        return 1

    else:
        return 0




#changing the screen resolution
set_resolution(480, 480)

while True:
    ret, frame = camera.read()
    #a = bool(_)
    #print(a)
    grayscaledimage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = FaceDetector(grayscaledimage)
    b = bool(faces)
    print(b)
        
    if b == False:
        NoFace+=1
        if NoFace>50:
            print("No face detected")
            sentence = "No face detected"
            os.system('espeak"' + sentence + '"')
            NoFace = 0




 
    
#detecting all the faces in the faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        Facelandmarks = ConditionPredictor(grayscaledimage, face)
        Facelandmarks = face_utils.shape_to_np(Facelandmarks)
      

        
        lefteyeblink = blinked(Facelandmarks[36],Facelandmarks[37], 
            Facelandmarks[38], Facelandmarks[41], Facelandmarks[40], Facelandmarks[39])
        righteyeblink = blinked(Facelandmarks[42],Facelandmarks[43], 
            Facelandmarks[44], Facelandmarks[47], Facelandmarks[46], Facelandmarks[45])


        if(lefteyeblink==0 or righteyeblink==0):
            sleepy+=1
            drowsy=0
            awake=0
            yawn=0
            if(sleepy>6):
                display="Sleeping!"
                color = (255,0,0)
                if alarm1 == False:
                    alarm1 = True
                    t = threading.Thread(target=alarm, args=('wake up',))
                    t.deamon = True
                    t.start()
            else:
                alarm1 = False
                

        elif(lefteyeblink==1 or righteyeblink==1):
            sleepy=0
            awake=0
            drowsy+=1
            yawn=0
            if(drowsy>6):
                display="Drowsy!"
                color = (0,0,255)
                if alarm2 == False and saying == False:
                    alarm2 = True
                    t = threading.Thread(target=alarm, args=('take some fresh air',))
                    t.deamon = True
                    t.start()
            else:
                alarm2 = False


        else:
            drowsy=0
            sleepy=0
            awake+=1
            yawn=0
            if(awake>6):
                display="AWAKE AND ALRIGHT"
                color = (0,255,0)

        
        
        

       
            
        cv2.putText(frame, display, (50,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, color,2)

        for n in range(0, 68):
            (x,y) = Facelandmarks[n]
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Result of FaceDetector", frame)
    key = cv2.waitKey(1)
    if key == 27:
          break
