import cv2

class VideoAnalizer:

    def __init__(self, bottle_cascade_path = "./model/coke_500ml.xml"):
        self.__bottle_cascade = cv2.CascadeClassifier(bottle_cascade_path)
        self.__last_frame_bottle_rect = 0

    def analizeFrame(self, frame):
        frame_with_roi = self.__detectBottle(frame)
        self.__calculateVolume(frame_with_roi)
        return frame_with_roi
    
    def __detectBottle(self, frame):
        bottle = self.__bottle_cascade.detectMultiScale(frame, 1.01, 2)
        for (x, y, w, h) in bottle:
            if self.__last_frame_bottle_rect == 0:
                self.__last_frame_bottle_rect = [x, y, w, h]
            else:
                diff_x = abs(self.__last_frame_bottle_rect[0] - x)
                diff_w = abs(self.__last_frame_bottle_rect[2] - w)
                condition_1 = (x * 0.25) <= diff_x
                condition_2 = (w * 0.25) <= diff_w

                if w < 100:
                    w += 200

                if condition_1 and condition_2:
                    self.__last_frame_bottle_rect[0] = x
                    self.__last_frame_bottle_rect[2] = w
                    
            frame = cv2.rectangle(
                frame,
                (self.__last_frame_bottle_rect[0], 20),
                (self.__last_frame_bottle_rect[0] + self.__last_frame_bottle_rect[2], frame.shape[0] - 20),
                (255, 0, 0),
                2
            )
            return (frame, self.__last_frame_bottle_rect[0], 20, self.__last_frame_bottle_rect[2], frame.shape[0] - 20)
        self.__last_frame_bottle_rect = 0
        return (frame, 0, 0, 0, 0)
        
    def __calculateVolume(self, frame_with_roi):
        if self.__last_frame_bottle_rect == 0:
            return

