from ultralytics import YOLO
# import os
# import torch

import cv2
import math
import numpy as np

# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
# torch.cuda.empty_cache()
# model = YOLO("yolov8.yaml")  # build a new model from scratch

# # Use the model
# results = model.train(
#    data = "/home/nisenare/Documents/dip_project/model/bottle/data.yaml",
#    epochs=30,
#    batch=2
# )

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

model = YOLO("/home/nisenare/Documents/dip_project/model/last.pt")
classes = [
    "Liquid_15"
]
scale_factor = 18.7 / 380 # cm / pixel

once = True

def calculate_volume(roi):
    volume = 0
    roi_orig = roi.copy()[:,int(roi.shape[1]/2):]
    roi = cv2.cvtColor(roi_orig, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    roi = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    ret, roi_bin = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(roi_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        roi_bin = cv2.cvtColor(roi_bin, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(roi_bin, contours, len(contours) - 1, (0, 255, 0), 1)
        for y in roi_bin:
            green = [0, 255, 0]
            green_pixels = np.where(np.all(y == green, axis = 1))[0]
            if len(green_pixels) > 1:
                volume += math.pi * math.pow(green_pixels.max() * scale_factor, 2) * scale_factor
    cv2.imshow("ROI", roi_bin)
    return volume

while True:
    ret, frame = cap.read()
    results = model(frame, stream = True, verbose = False)
    for r in results:
        boxes = r.boxes
        if boxes:
            box = boxes[0]
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            org_height = [x1 - 10, y1 - 15]
            font = cv2.FONT_HERSHEY_PLAIN
            fontScale = 1
            color = (0, 0, 0)
            thickness = 2
            height_cm = round((y2 - y1) * scale_factor, 2)
            width_cm = round((x2 - x1) * scale_factor, 2)
            volume = calculate_volume(frame[y1:y2 + 10, x1 - 10:x2 + 10])
            cv2.putText(frame, "(w, h) = (" + str(width_cm) + ", " + str(height_cm) + ") cm" , org_height, font, fontScale, color, thickness)
            cv2.putText(frame, "Volume = " + str(round(volume, 2)) + " ml", [x2, y2], font, fontScale, color, thickness)
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()