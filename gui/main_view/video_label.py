import tkinter as tk
import cv2
import model.video_analysis
import threading
import time
import numpy as np
import platform
from PIL import Image
from PIL import ImageTk

class VideoLabel(tk.Label):

    def __init__(self, master: tk.Tk):
        super().__init__(master,
            borderwidth = 1,
            relief = "solid",
            background = "black")
        self.grid(row = 1,
            column = 0,
            sticky = "nsew",
            padx = 10,
            pady = 10)
        self.__cap = None
        self.__should_resize = False
        self.__resize_height = 0
        self.__delay = int(1000 / 30)
        self.__running = False
        self.bind('<Destroy>', self.__on_destroy)
        master.bind('<Configure>', self.__on_resize)

    def start_video_play(self):
        if not self.__running:
            self.__running = True
            self.__update_frame()

    def set_cam_index_first_time(self, index):
        if not self.__cap is None:
            return
        if platform.system() == "Windows":
            self.__cap = ThreadedVideoCapture(index = index, api_preference = cv2.CAP_DSHOW)
        elif platform.system() == "Linux":
            self.__cap = ThreadedVideoCapture(index = index, api_preference = None)
        self.__cap.start()

    def change_cam_index(self, new_index):
        self.__cap.set_new_src(new_index)

    def toggle_resize(self):
        self.__should_resize = not self.__should_resize

    def set_info_frame(self, info_frame):
        self.__info_frame = info_frame

    def change_scale_factor(self, scale_factor):
        self.__cap.set_scale_factor(scale_factor)

    def __update_frame(self):
        ret, frame = self.__cap.get_frame()
        if ret:
            self.__info_frame.update_altura_bottle(self.__cap.get_height())
            self.__info_frame.update_ancho_bottle(self.__cap.get_width())
            self.__info_frame.update_volumen_bottle(self.__cap.get_volume())
            if self.__should_resize:
                frame = self.__image_resize(frame, height = self.__resize_height)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image = im)
            self.config(image = img)
            self.image = img
        if self.__running:
            self.after(self.__delay, self.__update_frame)

    def __image_resize(self, image, height):
        dim = None
        (h, w) = image.shape[:2]
        r = height / float(h)
        dim = (int(w * r), height)
        return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    def __on_destroy(self, event):
        self.__cap.release()

    def __on_resize(self, event):
        self.__resize_height = self.winfo_height()


class ThreadedVideoCapture:

    def __init__(self, api_preference, index = 0):
        self.__api_preference = api_preference
        self.__cap = cv2.VideoCapture(index, self.__api_preference)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.__video_source = index
        self.__video_analyzer = model.video_analysis.VideoAnalizer()
        self.__thread = threading.Thread(target = self.__process)
        self.__video_stop = threading.Event()
        self.ret = False
        self.frame = None
        self.__volume = 0
        self.__height = 0
        self.__width = 0

    def set_new_src(self, index):
        self.__video_stop.set()
        self.__thread.join()
        self.__cap.release()
        self.__cap = cv2.VideoCapture(index, self.__api_preference)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.__video_stop.clear()
        self.__thread = threading.Thread(target = self.__process)
        self.__thread.start()

    def set_scale_factor(self, scale_factor):
        self.__video_analyzer.set_scale_factor(scale_factor)

    def start(self):
        self.__thread.start()

    def get_frame(self):
        return self.ret, self.frame
    
    def get_volume(self):
        return self.__volume
    
    def get_height(self):
        return self.__height
    
    def get_width(self):
        return self.__width

    def __process(self):
        while not self.__video_stop.is_set():
            ret, frame = self.__cap.read() 
            volume = 0
            if ret:
                h, w, volume, frame = self.__video_analyzer.analize_frame(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print('[ThreadedVideoCapture] stream end: ', self.__video_source)
                self.__video_stop.set()
                break
            self.ret = ret
            self.__volume = volume
            self.__height = h
            self.__width = w
            self.frame = cv2.resize(frame, (640, 480))
            time.sleep(1/30)

    def release(self):
        if not self.__video_stop.is_set():
            self.__video_stop.set()
            self.__thread.join()
        if self.__cap.isOpened():
            self.__cap.release()
