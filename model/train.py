from ultralytics import YOLO
# import os
# import torch

import cv2
import math

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
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

model = YOLO("/home/nisenare/Documents/dip_project/model/last.pt")
classes = [
    "Liquid_15"
]
scale_factor = 18.7 / 380 # cm / pixel

while True:
    ret, frame = cap.read()
    results = model(frame, stream = True, verbose = False)

    for r in results:
        boxes = r.boxes

        if boxes:
            box = boxes[0]
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
            # put box in cam
            cv2.rectangle(frame, (x1 - 10, y1 - 10), (x2 + 10, y2), (0, 255, 0), 3)
            org_height = [x1 - 10, y1 - 15]
            font = cv2.FONT_HERSHEY_PLAIN
            fontScale = 1
            color = (0, 0, 0)
            thickness = 2
            height_cm = round((y2 - y1) * scale_factor, 2)
            width_cm = round((x2 - x1) * scale_factor, 2)
            cv2.putText(frame, "(w, h) = (" + str(width_cm) + ", " + str(height_cm) + ") cm" , org_height, font, fontScale, color, thickness)
        
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()