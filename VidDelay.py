import cv2, math
import cv2.cv as cv
import sys
import numpy as np
import time, datetime
from optparse import OptionParser
from Queue import Queue

parser = OptionParser()
parser.add_option("-o", "--output", dest="filename", default = "VD", help="video output prefix")
parser.add_option("-d", type="int", default = 150, help = "number of frames in delay queue", dest="delaysize")
parser.add_option("-s", type="int", default = 300, help = "number of frames in save queue", dest="savesize")

(options, args) = parser.parse_args()

delay = Queue()
save = Queue()

cap = cv2.VideoCapture(0)
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
fourcc = cv2.cv.CV_FOURCC(*'XVID')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    delay.put(frame)

    #Reads from delay queue
    if delay.qsize() > options.delaysize:
        f = delay.get()
        save.put(f)	
        cv2.imshow('frame', f)

    #Caps the size of the save queue
    if save.qsize() > options.savesize:
        save.get()

    #Read keypress
    k = cv2.waitKey(1)
    
    #Save Video when 's' is pressed
    if k & 0xFF == ord('s'):
        if save.qsize() > 10:
            print(str(save.qsize())+" frames to save...")
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            out = cv2.VideoWriter(options.filename+"_"+timestamp+".avi", fourcc, 20.0, (w,h))
            while save.qsize() > 0:
                s = save.get()
                out.write(s)
            out.release()
            print("Done Saving")

    #Quit when 'q' is pressed
    if k & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
