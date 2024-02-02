import tkinter as tk
import cv2
from tkinter import ttk
from gui.main_view.control_frame import ControlFrame
from gui.main_view.video_label import VideoLabel

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
        self.__control_frame = ControlFrame(master, self.__video_label)
