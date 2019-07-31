import math
import cv2
import math
import numpy as np
from grid import Grid
class Tracker:
    def __init__(self):
        pass
    def track(self):
        capture = cv2.VideoCapture(0)
        width = capture.get(3)
        height = capture.get(4)
        grid = Grid([width,height],[5,5])

        while capture.isOpened:
            ret,frame = capture.read()
            
            #HSV values, 0-255
            lower_green = np.array([45,50,50],np.uint8)
            upper_green = np.array([90,255,255],np.uint8)

            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            kernelOpen=np.ones((5,5),dtype=np.uint8)
            kernelClose=np.ones((20,20),dtype=np.uint8)

            mask = cv2.inRange(hsv,lower_green,upper_green)

            #Close small holes in middle of contour
            maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
            maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

            contours, hierarchy = cv2.findContours(maskClose,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                if cv2.contourArea(cnt) > 300:
                    x,y = self._find_center(cnt)
                    gridX,gridY = grid.contains_in([x,y])
                    print(gridX,gridY)

            cv2.drawContours(frame,contours,-1, (0,255,0), 1)

            # Draw grid for display
            for i,x in enumerate(grid.grid[0]):
                cv2.line(img=frame, pt1=(grid.grid[0][i][0], 0), pt2=( grid.grid[0][i][0], int(height)), color=(255, 0, 0), thickness=1, lineType=1, shift=0)
            for i,y in enumerate(grid.grid):
                cv2.line(img=frame, pt1=(0, grid.grid[i][0][1]), pt2=( int(width), grid.grid[i][0][1]), color=(255, 0, 0), thickness=1, lineType=1, shift=0)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
              
        cv2.destroyAllWindows()

    def _find_center(self,cnt):
        M = cv2.moments(cnt)
        # If unable to find contour moments, return default value
        try:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return cx,cy
        except:
            return None
        
if __name__ == "__main__":
    tracker = Tracker()
    tracker.track()