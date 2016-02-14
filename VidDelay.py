import cv2, math
import cv2.cv as cv
import sys
import numpy as np
import time, datetime
from optparse import OptionParser
from Queue import Queue
import webserver
import threading

parser = OptionParser()
parser.add_option("-o", "--output", dest="filename", default = "VD", help="video output prefix")
parser.add_option("-d", type="int", default = 150, help = "number of frames in delay queue", dest="delaysize")
parser.add_option("-s", type="int", default = 300, help = "number of frames in save queue", dest="savesize")

(options, args) = parser.parse_args()

delay = Queue()
save = Queue()

font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
fourcc = cv2.cv.CV_FOURCC(*'XVID')

thr = threading.Thread(target=webserver.run)
thr.start()

cv2.namedWindow("Instant Replay", cv2.WINDOW_NORMAL)

waittime = 1
lastsave = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    delay.put(frame)

    #Reads from delay queue
    if delay.qsize() > options.delaysize:
        f = delay.get()
        save.put(f)
        if time.time() - lastsave < 5:
            cv2.putText(f,'Video Saved',(10,h-10), font, 1,(255,255,255),3)
        cv2.imshow("Instant Replay", f)

    #Caps the size of the save queue
    if save.qsize() > options.savesize:
        save.get()

    #Read keypress
    k = cv2.waitKey(waittime)
    
    #Save Video when 's' is pressed
    #if k & 0xFF == ord('s'):
    if webserver.getstatus():
        if save.qsize() > 10:
            print(str(save.qsize())+" frames to save...")
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            out = cv2.VideoWriter(options.filename+"_"+timestamp+".avi", fourcc, 30.0, (w,h))
            while save.qsize() > 0:
                s = save.get()
                out.write(s)
            out.release()
            print("Done Saving")
            lastsave = time.time()

    if k & 0xFF == ord('f'):
        waittime = (waittime+1)%2

    #Quit when 'q' is pressed
    if k & 0xFF == ord('q'):
        break

# When everything done, release the capture
webserver.kill()
cap.release()
cv2.destroyAllWindows()
