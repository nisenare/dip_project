import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
# python -m pip install pillow
# pytjon -m pip install imutils

class MainView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, *args)
        
        master.title("Validador de calidad por medio del volumen del líquido")
        master.geometry("800x450")
        master.minsize(750, 350)
        self.__cam_indexes = []

        # layout principal
        master.columnconfigure(0, weight = 3)
        master.columnconfigure(1, weight = 2)
        master.rowconfigure(1, weight = 1)

        self.__video_label = tk.Label(master, borderwidth = 1, relief = "solid", background = "black")
        self.__control_frame = tk.Frame(master)

        self.__video_label.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
        self.__control_frame.grid(row = 1, column = 1, sticky = "nsew")

        # layout control
        self.__control_frame.rowconfigure(0, weight = 1)
        self.__control_frame.rowconfigure(1, weight = 1)
        self.__control_frame.columnconfigure(0, weight = 1)

        self.__info_frame = tk.LabelFrame(self.__control_frame, text = "Información", borderwidth = 1, relief = "solid")
        self.__config_frame = tk.LabelFrame(self.__control_frame, text = "Configuración", borderwidth = 1, relief = "solid")

        self.__info_frame.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 10), pady = (0, 5))
        self.__config_frame.grid(row = 1, column = 0, sticky = "nsew", padx = (0, 10), pady = (5, 10))

        # config content
        self.__config_frame.columnconfigure(0, weight = 1)
        
        # configure source section
        self.__config_frame_source_section = tk.Frame(self.__config_frame, pady = 5)
        self.__config_frame_source_section.grid(row = 0, column = 0, sticky = "nsew")

        self.__config_frame_source_section.columnconfigure(0, weight = 1)
        self.__src_combo_box = ttk.Combobox(self.__config_frame_source_section, state = "readonly")
        self.__src_combo_box.grid(row = 0, column = 0, sticky = "nsew", padx = 5)

        # video content
        self.__get_cam_indexes()
        if len(self.__cam_indexes) > 0:
            indexes_copy = self.__cam_indexes.copy()
            for i in range(0, len(indexes_copy)):
                indexes_copy[i] = "Source " + str(indexes_copy[i])
            self.__src_combo_box["values"] = indexes_copy
            self.__src_combo_box.current(0)
            self.__cap = cv2.VideoCapture(self.__cam_indexes[0], cv2.CAP_DSHOW)
            self.__get_video()

        self.bind("<Destroy>", self.__on_destroy)
        self.__src_combo_box.bind("<<ComboboxSelected>>", self.__set_cam_index)

    def __get_cam_indexes(self):
        self.__cam_indexes = []
        for i in range(0, 10):
            this_cap = cv2.VideoCapture(i)
            if this_cap.isOpened():
                self.__cam_indexes.append(i)

    def __set_cam_index(self, event):
        selected_index = int(self.__src_combo_box.get().split(" ")[1])
        self.__video_label.after_cancel(self.__video_label_after_id)
        self.__cap.release()
        self.__cap = cv2.VideoCapture(selected_index, cv2.CAP_DSHOW)
        self.__get_video()

    def __get_video(self):
        if self.__cap is None:
            return
        ret, frame = self.__cap.read()
        if ret == True:
            h = abs(int(self.master.winfo_height()))
            frame = self.__image_resize(frame, height = h)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image = im)
            self.__video_label.config(image = img)
            self.__video_label.image = img
            self.__video_label_after_id = self.__video_label.after(10, self.__get_video)
        else:
            self.__video_label.image = ""
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
        resized = cv2.resize(image, dim, interpolation = inter)
        return resized
    
    def __on_destroy(self, event):
        self.__cap.release()