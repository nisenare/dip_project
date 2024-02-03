import cv2
from ultralytics import YOLO

class VideoAnalizer:

                                                            # cm / pixel
    def __init__(self, yolo_model_path = "./model/last.pt", scale_factor = 18.7 / 380):
        self.__model = model = YOLO(yolo_model_path)
        self.__scale_factor = scale_factor

    def analize_frame(self, frame):
        (x1, y1, x2, y2), frame = self.__detect_liquid(frame)
        return frame
        # self.__calculateVolume(frame_with_roi)
        # return frame_with_roi
    
    def set_scale_factor(self, factor):
        self.__scale_factor = factor

    def __detect_liquid(self, frame):
        results = self.__model(frame, stream = True, verbose = False)
        x1, y1, x2, y2 = 0, 0, 0, 0
        for r in results:
            boxes = r.boxes
            if boxes:
                box = boxes[0]
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1) - 10, int(x2), int(y2) # convert to int values
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                fontScale = 1
                color = (255, 255, 0)
                thickness = 2
                cv2.putText(frame, "Liquido", org, font, fontScale, color, thickness)
        return (x1, y1, x2, y2), frame

    def __calculate_volume(self, frame_with_roi):
        if self.__last_frame_bottle_rect == 0:
            return

