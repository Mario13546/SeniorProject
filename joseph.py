# Created by Alex Pereira

import numpy as np
import cv2 as cv
import serial
import time

arduino = serial.Serial('COM3', 9600)
 
def main():
 
    # Create a VideoCapture object
    cap = cv.VideoCapture(0)

    # Larger video capture
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv.CAP_PROP_FRAME_WIDTH,  1920)
 
    # Create the background subtractor object
    # Use the last 200 video frames to build the background
    back_sub = cv.createBackgroundSubtractorMOG2(history = 250, varThreshold = 25, detectShadows = True)
 
    # Create kernel for morphological operation
    # You can tweak the dimensions of the kernel
    # e.g. instead of 20,20 you can try 30,30.
    kernel = np.ones((30,30),np.uint8)
 
    while(True):
        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        ret, frame = cap.read()
 
        # Use every frame to calculate the foreground mask and update
        # the background
        fg_mask = back_sub.apply(frame)
 
        # Close dark gaps in foreground object using closing
        fg_mask = cv.morphologyEx(fg_mask, cv.MORPH_CLOSE, kernel)
 
        # Remove salt and pepper noise with a median filter
        fg_mask = cv.medianBlur(fg_mask, 5)
         
        # Threshold the image to make it either black or white
        _, fg_mask = cv.threshold(fg_mask,127,255,cv.THRESH_BINARY)
 
        # Find the index of the largest contour and draw bounding box
        fg_mask_bb = fg_mask
        contours, hierarchy = cv.findContours(fg_mask_bb,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv.contourArea(c) for c in contours]
 
        # If there are no countours
        if len(areas) < 1:
 
            # Display the resulting frame
            cv.imshow('frame',frame)
            #pos=(str(310*(78/620))) #returns a degree measure (39 degrees)
            #arduino.write(pos.encode())
            reset=str(91)
            arduino.write(reset.encode())
            times=0
 
            # If "q" is pressed on the keyboard, exit this loop
            if cv.waitKey(1) == ord('q'):
                cap.release()
                break
 
            # Go to the top of the while loop
            continue
 
        else:
            # Find the largest moving object in the image
            max_index = np.argmax(areas)
 
        # Draw the bounding box
        cnt = contours[max_index]
        x,y,w,h = cv.boundingRect(cnt)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
 
        # Draw circle in the center of the bounding box
        x2 = x + int(w/2)
        y2 = y + int(h/2)
        cv.circle(frame,(x2,y2),4,(0,255,0),-1)
 
        # Print the centroid coordinates (we'll use the center of the
        # bounding box) on the image
        text = "x: " + str(x2) + ", y: " + str(y2)
        cv.putText(frame, text, (x2 - 10, y2 - 10),
            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        pos=(str(x2*(78/620))) #returns a degree measure (0-78 degrees which is the FOV)
        arduino.write(pos.encode())
        #print(pos)
        time.sleep(0.01)
        #STRING='on'
        #arduino.write(STRING.encode())

        # Display the resulting frame
        cv.imshow('frame', frame)
 
        # If "q" is pressed on the keyboard,
        # exit this loop
        if cv.waitKey(1) == ord('q'):
            cap.release()
            break
 
    # Close down the video stream
    cap.release()
    cv.destroyAllWindows()
 
if __name__ == '__main__':
    print(__doc__)
    main()