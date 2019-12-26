import cv2
import numpy as np
class Tracker:
    def __init__(self):
        self.lower_bound = [0,0,0]
        self.upper_bound = [359,255,255]
    def track(self):
        capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.isInLoop = True

        while self.isInLoop:
            ret,frame = capture.read()

            lower_value = np.array(self.lower_bound,np.uint8)
            upper_value = np.array(self.upper_bound,np.uint8)

            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv,lower_value,upper_value)

            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

            cv2.drawContours(frame,contours,-1, (0,255,0), 1)

            cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()
    def break_loop(self):
        self.isInLoop = False
    def update_bounds(self,lower,upper):
        self.lower_bound = lower
        self.upper_bound = upper
if __name__ == "__main__":
    tracker = Tracker()
    tracker.track()