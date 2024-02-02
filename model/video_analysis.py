import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

class VideoAnalizer:

    def __init__(self, bottle_cascade_path = "./model/coke_500ml.xml"):
        # self.__bottle_cascade = cv2.CascadeClassifier(bottle_cascade_path)
        self.__last_frame_bottle_rect = 0

    def analizeFrame(self, frame):
        bbox, frame_with_roi = self.__detectBottle(frame)
        return frame_with_roi
        # self.__calculateVolume(frame_with_roi)
        # return frame_with_roi
    
    def __detectBottle(self, frame):
        bbox, label, conf = cv.detect_common_objects(frame, model="yolov3")
        frame = draw_bbox(frame, bbox, label, conf)
        return bbox, frame
        
    def __calculateVolume(self, frame_with_roi):
        if self.__last_frame_bottle_rect == 0:
            return

