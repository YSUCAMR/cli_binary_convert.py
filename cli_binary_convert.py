from collections import deque
import sys
import struct
import numpy as np
import time
from matplotlib import pyplot as plt
import datetime
import re
import cv2
import math
import datetime
import itertools 

scale = 0.5
fileinput =  sys.argv[1]
bytes_read = open(fileinput, "rb").read()
poly_line_index = 0

height = int(1000 * scale)
width = int(1800 * scale)
frame = np.ones((height,width,3), np.uint8)
output_size = (width, height)

codec = cv2.VideoWriter_fourcc('M','J','P','G')
fps = 15
videof = cv2.VideoWriter()
success = videof.open('cli.avi',codec,fps,output_size,True) 

ASCII = True
Binary = False

dq1 = deque(['.','.','H','E','A','D','E','R','E','N','D'])
dq2 = deque(['$','$','H','E','A','D','E','R','E','N','D'])

l = []
l1 = []
poly_lines = []
directions = []

iterator = iter(bytes_read)

try:
    b = iterator.next()
    while True:
        if(Binary):   
            intb = int(b.encode('hex_codec'), 16) 
            #            print b.encode('hex_codec')
            b = iterator.next()
            nextb = int(b.encode('hex_codec'), 16) 
            if((intb == 127) and (nextb == 0)):
                z1 = iterator.next()
                z2 = iterator.next()
                z3 = iterator.next()
                z4 = iterator.next()
                zheight = z4 + z3 + z2 + z1 
                zheight = struct.unpack('>f',zheight)[0] * 0.01   # CLI file is in 0.01 mm increments
                frame = np.ones((height,width,3), np.uint8)
                if (len(poly_lines) and len(directions)):
                    for l1, d1 in itertools.izip(poly_lines, directions):
                   	 #print "Direction=" +str(d1) 
                   	 #print l1
                   	 if d1 == 1:
                            cv2.fillPoly(frame,[l1],(255,255,255))
                   	 if d1 == 0: 
                            cv2.fillPoly(frame,[l1],(0,0,0))
                directions = []
                text_string1 = "Youngstown State University"
                text_string2 = "Z Height=" + str(float(zheight))
                text_string3 = "CLI Cracker"
                cv2.putText(frame, text_string1, (230, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.putText(frame, text_string3, (400, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.putText(frame, text_string2, (635, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.imshow("window",frame)
                videof.write(frame)
                poly_lines = []
                #print "0x7F new layer long found at z height = " + str(zheight) 

            if((intb == 130) and (nextb == 0)):
                z1 = iterator.next()
                z2 = iterator.next()
                z3 = iterator.next()
                z4 = iterator.next()
                idx = z4 + z3 + z2 + z1
                idx = struct.unpack('>L',idx)[0]
                z1 = iterator.next()
                z2 = iterator.next()
                z3 = iterator.next()
                z4 = iterator.next()
                direction = z4 + z3 + z2 + z1
                direction = struct.unpack('>L',direction)[0]
		#print direction
		directions.append(direction)
                z1 = iterator.next()
                z2 = iterator.next()
                z3 = iterator.next()
                z4 = iterator.next()
                npts = z4 + z3 + z2 + z1
                npts = struct.unpack('>L',npts)[0]
                poly_line = []
                while (npts > 0):
                    x1 = iterator.next()
                    x2 = iterator.next()
                    x3 = iterator.next()
                    x4 = iterator.next()
                    x = x4 + x3 + x2 + x1 
                    x = struct.unpack('>f',x)[0]  
                    x = int(x*scale/100)
                    y1 = iterator.next()
                    y2 = iterator.next()
                    y3 = iterator.next()
                    y4 = iterator.next()
                    y = y4 + y3 + y2 + y1 
                    y = struct.unpack('>f',y)[0]  
                    y = int(y*scale/100)
                    npts = npts - 1
                    poly_line.append((x,y))
                poly_line = np.array( poly_line, dtype=np.int32 )
                poly_lines.append(poly_line)  
		b = iterator.next()
		

        if(ASCII):   
            dq1.append(b)
            dq1.popleft()
            b = iterator.next()
            if(dq1 == dq2):
                print "found the end of ASCII"
                ASCII = False
                Binary = True
except StopIteration:
        pass

