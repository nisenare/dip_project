import tkinter as tk
import cv2
import model.video_analysis
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
        self.__after_id = None
        self.__video_analyzer = model.video_analysis.VideoAnalizer()

    def cap_release(self):
        if self.__cap is None:
            return
        self.__cap.release()

    def set_cam_index_first_time(self, index):
        if not self.__cap is None:
            return
        self.__cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.__cap.set(cv2.CAP_PROP_FPS, 30)
    
    def change_cam_index(self, new_index):
        if self.__after_id is None:
            return
        self.after_cancel(self.__after_id)
        self.__cap.release()
        self.__cap = cv2.VideoCapture(new_index, cv2.CAP_DSHOW)
        self.__cap.set(cv2.CAP_PROP_FPS, 30)
        self.play_cam_video()

    def play_cam_video(self):
        if self.__cap is None:
            return
        ret, frame = self.__cap.read()
        if ret == True:
            height = abs(int(self.master.winfo_height()))
            frame = self.__image_resize(frame, height = height)


            # analysis
            frame, x, y, w, h = self.__video_analyzer.analizeFrame(frame)


            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image = im)
            self.config(image = img)
            self.image = img
            self.__after_id = self.after(10, self.play_cam_video)
        else:
            self.image = ""
            self.__cap.release()

    def __image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation = inter)
        