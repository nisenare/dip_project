import tkinter as tk
import gui.cons
import cv2
import imutils
from PIL import Image
from PIL import ImageTk
# python -m pip install pillow
# pytjon -m pip install imutils

class MainView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, *args)
        
        master.title("Validador de calidad por medio del volumen del líquido")
        master.geometry("700x500")
        master.minsize(600, 400)
        self.resized = False

        # layout principal
        master.columnconfigure(0, weight = 3)
        master.columnconfigure(1, weight = 2)
        master.rowconfigure(1, weight = 1)

        self.title_frame = tk.Frame(master, height = 30, borderwidth = 1, relief = "solid")
        self.video_label = tk.Label(master, borderwidth = 1, relief = "solid", background = "black")
        self.control_frame = tk.Frame(master)

        self.video_label.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
        self.control_frame.grid(row = 1, column = 1, sticky = "nsew")

        # layout control
        self.control_frame.rowconfigure(0, weight = 1)
        self.control_frame.rowconfigure(1, weight = 1)
        self.control_frame.columnconfigure(0, weight = 1)

        self.info_frame = tk.LabelFrame(self.control_frame, text = "Información", borderwidth = 1, relief = "solid")
        self.config_frame = tk.LabelFrame(self.control_frame, text = "Configuración", borderwidth = 1, relief = "solid")

        self.info_frame.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 10), pady = (0, 5))
        self.config_frame.grid(row = 1, column = 0, sticky = "nsew", padx = (0, 10), pady = (5, 10))
        # contenido video
        # self.video_label_content.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 30)
        # self.video_label.bind("<Configure>", self._image_resize)
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self._get_video()

    def _get_video(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret == True:
            h = abs(int(self.master.winfo_height()))
            print(frame.shape)
            frame = self._image_resize(frame, height = h)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image = im)
            self.video_label.config(image = img)
            self.video_label.image = img
            self.video_label.after(10, self._get_video)
        else:
            self.video_label.image = ""
            self.cap.release()

    
    def _image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
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