import tkinter as tk
import cv2
from tkinter import ttk
from gui.main_view.video_label import VideoLabel

class ControlFrame(tk.Frame):

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.grid(row = 1, column = 1, sticky = "nsew")
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.__info_frame = InfoFrame(self)
        self.__config_frame = ConfigFrame(self)

    def set_video_label(self, video_label: VideoLabel):
        self.__info_frame.set_video_label(video_label)
        self.__config_frame.set_video_label(video_label)

class InfoFrame(tk.LabelFrame):

    def __init__(self, master: tk.Tk):
        super().__init__(master,
            text = "Información",
            borderwidth = 1,
            relief = "solid"
        )
        self.__video_label = None
        self.grid(row = 0,
            column = 0,
            sticky = "nsew",
            padx = (0, 10),
            pady = (0, 5)
        )

    def set_video_label(self, video_label: VideoLabel):
        if not self.__video_label is None:
            return
        self.__video_label = video_label
        
class ConfigFrame(tk.LabelFrame):

    def __init__(self, master: tk.Tk):
        super().__init__(master,
            text = "Configuración",
            borderwidth = 1,
            relief = "solid"
        )
        self.__cam_indexes = []
        self.__video_label = None
        self.grid(row = 1,
            column = 0,
            sticky = "nsew",
            padx = (0, 10),
            pady = (5, 10)
        )
        self.columnconfigure(0, weight = 1)
        self.__source_section = tk.Frame(self, pady = 5)
        self.__source_section.grid(row = 0, column = 0, sticky = "nsew")
        self.__source_section.columnconfigure(0, weight = 1)
        self.__src_combo_box = ttk.Combobox(self.__source_section, state = "readonly")
        self.__src_combo_box.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
        self.__src_combo_box.bind("<<ComboboxSelected>>", self.__set_cam_index)

    def __set_cam_index(self, event):
        selected_index = int(self.__src_combo_box.get().split(" ")[1])
        self.__video_label.change_cam_index(selected_index)

    def __get_cam_indexes(self):
        self.__cam_indexes = []
        for i in range(0, 10):
            this_cap = cv2.VideoCapture(i)
            if this_cap.isOpened():
                self.__cam_indexes.append(i)
            this_cap.release()

    def __fill_combo_box(self):
        indexes_copy = self.__cam_indexes.copy()
        for i in range(0, len(indexes_copy)):
            indexes_copy[i] = "Source " + str(indexes_copy[i])
        self.__src_combo_box["values"] = indexes_copy
        self.__src_combo_box.current(0)

    def set_video_label(self, video_label: VideoLabel):
        if not self.__video_label is None:
            return
        self.__video_label = video_label
        self.__get_cam_indexes()
        if len(self.__cam_indexes) > 0:
            self.__fill_combo_box()
            self.__video_label.set_cam_index_first_time(0)
            self.__video_label.play_cam_video()
    