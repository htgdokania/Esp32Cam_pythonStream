# urllib.urlopen works only in python 2 and not python3
#this code is used to stream from any url
#here we are streaming a video directly from  an esp32cam module
#Replace the url with your required link to get the desired stream
import cv2
import urllib
import numpy as np

#load cascade xml files
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

stream=urllib.urlopen('http://192.168.31.117:81/stream')
stream_bytes = ''

while True:
    try:    
        stream_bytes += stream.read(1024)
        first = stream_bytes.find(b'\xff\xd8')
        last = stream_bytes.find(b'\xff\xd9')
        if first != -1 and last != -1:
            jpg = stream_bytes[first:last + 2]
            stream_bytes = stream_bytes[last + 2:]
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#convert current frame to gray 

            #detect face coordinates x,y,w,h
            faces=face_cascade.detectMultiScale(gray,1.3,5)
            for(x,y,w,h) in faces:
                image=cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),6)
        
            cv2.imshow('image', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    except:     #important block try except
        continue# this  is required to deal with error due to blank frames received 
print("here")
