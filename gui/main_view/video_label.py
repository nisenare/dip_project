import tkinter as tk
import cv2
import model.video_analysis
import threading
import time
import numpy as np
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
        self.__cap = ThreadedVideoCapture(index = index, api_preference = cv2.CAP_DSHOW)
        self.__cap.start()

    def change_cam_index(self, new_index):
        self.__cap.set_new_src(new_index)

    def toggle_resize(self):
        self.__should_resize = not self.__should_resize

    def __update_frame(self):
        ret, frame = self.__cap.get_frame()
        if ret:
            if self.__should_resize:
                frame = self.__image_resize(frame, height = self.__resize_height)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image = im)
            self.config(image = img)
            self.image = img
            
        if self.__running:
            self.after(self.__delay, self.__update_frame)

    def __image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        # if width is None and height is None:
        #     return image
        # if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
        # else:
        #     r = width / float(w)
        #     dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation = inter)
    
    def __on_destroy(self, event):
        self.__cap.release()
    
    def __on_resize(self, event):
        self.__resize_height = self.winfo_height()

class ThreadedVideoCapture:

    def __init__(self, api_preference, index = 0):
        self.__cap = cv2.VideoCapture(index, api_preference)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.__video_source = index
        self.__video_analyzer = model.video_analysis.VideoAnalizer()
        #threading
        self.__thread = threading.Thread(target = self.__process)
        self.__video_stop = threading.Event()
        self.ret = False
        self.frame = None

    def set_new_src(self, index):
        self.__video_stop.set()
        self.__thread.join()
        self.__cap.release()
        self.__cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.__video_stop.clear()
        self.__thread = threading.Thread(target = self.__process)
        self.__thread.start()

    def start(self):
        self.__thread.start()

    def get_frame(self):
        return self.ret, self.frame


    def __process(self):
        while not self.__video_stop.is_set():
            ret, frame = self.__cap.read()
            
            if ret:

                #TODO: Analysis here

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print('[MyVideoCapture] stream end: ', self.__video_source)
                self.__video_stop.set()
                break
                
            self.ret = ret
            self.frame = cv2.resize(frame, (640, 480))
            
            time.sleep(1/30)

    def release(self):
        if not self.__video_stop.is_set():
            self.__video_stop.set()
            self.__thread.join()
        if self.__cap.isOpened():
            self.__cap.release()
