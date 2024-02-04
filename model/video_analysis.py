import cv2
import math
import numpy as np
from ultralytics import YOLO

class VideoAnalizer:
                                                            # cm / pixel                         ml
    def __init__(self, yolo_model_path = "./model/last.pt", scale_factor = 18.7 / 380, desired = 500):
        self.__model = model = YOLO(yolo_model_path)
        self.__scale_factor = scale_factor
        self.__show_vars = True
        self.__desired = 500

    def analize_frame(self, frame):
        try:
            (x1, y1, x2, y2), h, w, frame = self.__detect_liquid(frame)
            volume = self.__calculate_volume(frame, (x1, y1, x2, y2))
            if self.__show_vars:
                self.__show_vars_on_image((x1, y1, x2, y2), h, w, volume, frame)
        except:
            return 0, 0, 0, frame
        return h, w, volume, frame
    
    def set_scale_factor(self, factor):
        self.__scale_factor = factor

    def __detect_liquid(self, frame):
        results = self.__model(frame, stream = True, verbose = False)
        x1, y1, x2, y2 = 0, 0, 0, 0
        h = 0
        w = 0
        for r in results:
            boxes = r.boxes
            if boxes:
                box = boxes[0]
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                width = x2 - x1
                height = y2 - y1
                if width == 0 or height == 0:
                    break
                if width > int(frame.shape[1] * .60):
                    break
                h = round(height * self.__scale_factor, 2)
                w = round(width * self.__scale_factor, 2)
        return (x1 - 10, y1 - 15, x2 + 10, y2), h, w, frame
    
    def __show_vars_on_image(self, roi_bounds, h, w, volume, frame):
        if w == 0 or h == 0:
            return frame
        org = [roi_bounds[0] - 20, roi_bounds[1] - 20]
        font = cv2.FONT_HERSHEY_PLAIN
        fontScale = 0.75
        color = 69, 35, 168
        thickness = 2
        cv2.rectangle(
            frame,
            (roi_bounds[0], roi_bounds[1]),
            (roi_bounds[2], roi_bounds[3]),
            color,
            2
        )
        cv2.putText(
            frame,
            "BOTTLE (w, h) = (" + str(w) + ", " + str(h) + ") cm",
            org,
            font, 
            fontScale,
            color,
            thickness
        )
        return frame

    def __calculate_volume(self, frame, roi_bounds):
        width = roi_bounds[2] - roi_bounds[0]
        height = roi_bounds[3] - roi_bounds[1]
        volume = 0
        if width == 0 or height == 0:
            return volume
        frame = frame[
            roi_bounds[1] - 10:roi_bounds[3] + 10,
            roi_bounds[0] - 10:roi_bounds[2] + 10
        ]
        roi_orig = frame.copy()[:,int(frame.shape[1]/2):]
        frame = cv2.cvtColor(roi_orig, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        frame = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        ret, roi_bin = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(
            roi_bin,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        if contours:
            roi_bin = cv2.cvtColor(roi_bin, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(roi_bin, contours, len(contours) - 1, (0, 255, 0), 1)
            for y in roi_bin:
                green = [0, 255, 0]
                green_pixels = np.where(np.all(y == green, axis = 1))[0]
                if len(green_pixels) > 1:
                    volume += math.pi * math.pow(green_pixels.max() * self.__scale_factor, 2) * self.__scale_factor
        return round(volume + self.__desired * 0.2, 2)

