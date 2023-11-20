import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from gui.main_view.control_frame import ControlFrame
from gui.main_view.video_label import VideoLabel
# python -m pip install pillow
# pytjon -m pip install imutils

class MainView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, *args)
        
        master.title("Validador de calidad por medio del volumen del líquido")
        master.geometry("800x450")
        master.minsize(750, 350)

        # layout principal
        master.columnconfigure(0, weight = 3)
        master.columnconfigure(1, weight = 2)
        master.rowconfigure(1, weight = 1)

        self.__video_label = VideoLabel(master)
        self.__control_frame = ControlFrame(master)
        self.__control_frame.set_video_label(self.__video_label)

    def __on_destroy(self, event):
        self.__video_label.cap_release()