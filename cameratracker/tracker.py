import math
import cv2

class Tracker:
    def __init__(self):
        self.display = False
        self.position = (0,0)
    def track_video(self):
        capture = cv2.VideoCapture(0)
        wi,hi = capture.set(3,1920),capture.set(4,1080)
        xPoint = 0 
        yPoint = 0
        while capture.isOpened():
            ret,self.frame = capture.read()
            grayScale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
            
            # Unsure of gaus blur, more testing Required
            ##gaus = cv2.GaussianBlur(grayScale,(5,5),0)
            edge = cv2.Canny(grayScale,35,125)

            #convert to hsv to get black and white values
            hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
            baw = cv2.inRange(hsv,(0,0,0),(255, 255,30))

            # Use either thresh, or thresh2 inside contours
            # More testing required
            
            ret, thresh = cv2.threshold(baw,127,255,0)
            ret, thresh2 = cv2.threshold(grayScale,15,255,0)
            img, contours, hierarchy = cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            
            self.contList = []
            for contour  in contours:
                # Use if you have a lot of reflection on object
                ##cont = cv2.convexHull(contour)

                # Find area to get rid of big contours
                # Use cont variable if uncommented
                area = cv2.contourArea(contour)
                
                if area > 500:
                    # find circumfrence and circularity to determine if it is circular enough
                    circ = cv2.arcLength(contour,True)
                    circle = circ ** 2 / (4 * math.pi * area)        
                    # Use appxLen if detecting something other than circle.
                    # Appx num is number of line changes positionally
                    appxLen = cv2.approxPolyDP(contour, 0.03 * circ, True)

                    if circle > .85 and circle < 1.25:
                        self.contList.append(contour)
                        cx,cy = self._find_center(contour)
                        # point = self.master.findLocationOnScreen(center)
                        # self.set_point_position(point)
                        xPoint = int(cx)
                        yPoint = int(cy)
                        print(xPoint,yPoint)
                        # Check if object is outside of center axis
                        if xPoint < 930:
                            print("left")
                        elif xPoint > 990:
                            print("right")
                        if yPoint < 500:
                            print("up")
                        elif yPoint > 580:
                            print("down")
        
            cv2.drawContours(self.frame,self.contList,-1, (0,255,0), 1)

            if self.display == True:
                cv2.imshow('edges only',edge)
                cv2.imshow('frame with contours',self.frame)
            else:
                cv2.destroyAllWindows()
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
        cv2.destroyAllWindows()

    def toggle_video(self):
        if self.display == False:
            self.display = True
        else:
            self.display = False

    def set_point_position(self,pos):
        self.position = pos

    def _find_center(self,cnt):
        M = cv2.moments(cnt)
        # If unable to find contour moments, return a default value
        try:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return cx,cy
        except:
            return None
        