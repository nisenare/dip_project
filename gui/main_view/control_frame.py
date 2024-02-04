import tkinter as tk
import cv2
from tkinter import E, END, W, StringVar, ttk
from gui.main_view.video_label import VideoLabel

class ControlFrame(tk.Frame):

    def __init__(self, master: tk.Tk, video_label):
        super().__init__(master)
        self.grid(row = 1, column = 1, sticky = "nsew")
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.__info_frame = InfoFrame(self, video_label)
        self.__config_frame = ConfigFrame(self, video_label)

class InfoFrame(tk.LabelFrame):

    def __init__(self, master: tk.Tk, video_label):
        super().__init__(master,
            text = "Información",
            borderwidth = 1,
            relief = "solid"
        )
        self.__set_video_label(video_label)
        self.grid(row = 0,
            column = 0,
            sticky = "nsew",
            padx = (0, 10),
            pady = (0, 5)
        )
        self.columnconfigure(0, weight = 1)
        # ALTURA SECTION
        self.__altura_section = tk.Frame(self, pady = 5)
        self.__altura_section.grid(row = 0, column = 0, sticky = "nsew")
        self.__altura_section.columnconfigure(0, weight = 1)

        self.__altura_section_lbl = ttk.Label(self.__altura_section, text = "Altura")
        self.__altura_section_lbl.grid(row = 0, column = 0, sticky = "nsew", padx = 5)

        self.__altura_bottle_var = tk.StringVar()
        self.__altura_section_entry = ttk.Entry(self.__altura_section,
            state = "readonly",
            textvariable = self.__altura_bottle_var
        )
        self.__altura_section_entry.grid(row = 0, column = 1, sticky = "nsew", padx = (0, 5))
        self.__altura_section_lbl_2 = ttk.Label(self.__altura_section, text = "cm")
        self.__altura_section_lbl_2.grid(row = 0, column = 2, sticky = "nsew", padx = 5)

        # ANCHO SECTION
        self.__ancho_section = tk.Frame(self, pady = 5)
        self.__ancho_section.grid(row = 1, column = 0, sticky = "nsew")
        self.__ancho_section.columnconfigure(0, weight = 1)

        self.__ancho_section_lbl = ttk.Label(self.__ancho_section, text = "Ancho")
        self.__ancho_section_lbl.grid(row = 0, column = 0, sticky = "nsew", padx = 5)

        self.__ancho_bottle_var = tk.StringVar()
        self.__ancho_section_entry = ttk.Entry(self.__ancho_section,
            state = "readonly",
            textvariable = self.__ancho_bottle_var
        )
        self.__ancho_section_entry.grid(row = 0, column = 1, sticky = "nsew", padx = (0, 5))
        self.__ancho_section_lbl_2 = ttk.Label(self.__ancho_section, text = "cm")
        self.__ancho_section_lbl_2.grid(row = 0, column = 2, sticky = "nsew", padx = 5)

        # VOLUMEN SECTION
        self.__volumen_section = tk.Frame(self, pady = 5)
        self.__volumen_section.grid(row = 2, column = 0, sticky = "nsew")
        self.__volumen_section.columnconfigure(0, weight = 1)

        self.__volumen_section_lbl = ttk.Label(self.__volumen_section, text = "Volumen")
        self.__volumen_section_lbl.grid(row = 0, column = 0, sticky = "nsew", padx = 5)

        self.__volumen_bottle_var = tk.StringVar()
        self.__volumen_section_entry = ttk.Entry(self.__volumen_section,
            state = "readonly",
            textvariable = self.__volumen_bottle_var
        )
        self.__volumen_section_entry.grid(row = 0, column = 1, sticky = "nsew", padx = (0, 5))
        self.__volumen_section_lbl_2 = ttk.Label(self.__volumen_section, text = "ml")
        self.__volumen_section_lbl_2.grid(row = 0, column = 2, sticky = "nsew", padx = 5)


    def __set_video_label(self, video_label: VideoLabel):
        self.__video_label = video_label
        self.__video_label.set_info_frame(self)

    def update_altura_bottle(self, altura):
        self.__altura_bottle_var.set(str(altura))

    def update_ancho_bottle(self, ancho):
        self.__ancho_bottle_var.set(str(ancho))

    def update_volumen_bottle(self, volumen):
        self.__volumen_bottle_var.set(str(volumen))
        
class ConfigFrame(tk.LabelFrame):

    def __init__(self, master: tk.Tk, video_label):
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

        # SOURCE SELECTION SECTION
        self.__source_section = tk.Frame(self, pady = 5)
        self.__source_section.grid(row = 0, column = 0, sticky = "nsew")
        self.__source_section.columnconfigure(0, weight = 1)
        self.__src_combo_box = ttk.Combobox(self.__source_section, state = "readonly")
        self.__src_combo_box.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
        self.__src_combo_box.bind("<<ComboboxSelected>>", self.__set_cam_index)

        self.__set_video_label(video_label)
        
        # SCALE FACTOR SECION
        self.__scale_section = tk.Frame(self, pady = 5)
        validate_numbers = self.__scale_section.register(self.__validate_scale_factor)
        self.__scale_section.grid(row = 1, column = 0, sticky = "nsew")
        self.__scale_section.columnconfigure(0, weight = 1)
        self.__scale_label_1 = ttk.Label(self.__scale_section, 
            text = "Scale"
        )
        self.__scale_txt_entry = ttk.Entry(self.__scale_section,
            validate = "key",
            validatecommand = (validate_numbers, '%P'),
        )
        self.__scale_txt_entry.insert(END, str(18.7 / 380))
        self.__scale_label_2 = ttk.Label(self.__scale_section, 
            text = "cm/pix"
        )
        self.__scale_label_1.grid(row = 0, column = 0, sticky = W+E, padx = 5)
        self.__scale_txt_entry.grid(row = 0, column = 1, sticky = "nsew", padx = (0, 5))
        self.__scale_label_2.grid(row = 0, column = 2, sticky = W+E, padx = (0, 5))

        # RESIZE SECTION
        self.__resize_section = tk.Frame(self, pady = 5)
        self.__resize_section.grid(row = 2, column = 0, sticky = "nsew")
        self.__resize_section.columnconfigure(0, weight = 1)
        self.__resize_check = ttk.Checkbutton(self.__resize_section,
            text = "Autofit",
            command = self.__video_label.toggle_resize,
            variable = tk.IntVar(value = 0)
        )
        self.__resize_check.grid(row = 0, column = 0, sticky = "nsew", padx = 5)

    def __validate_scale_factor(self, text):
        if (
            all(char in "0123456789.-" for char in text) and
            "-" not in text[1:] and
            text.count(".") <= 1):
                try:
                    self.__video_label.change_scale_factor(float(text))
                except:
                    pass
                return True
        else:
            return False

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

    def __set_video_label(self, video_label: VideoLabel):
        self.__video_label = video_label
        self.__get_cam_indexes()
        if len(self.__cam_indexes) > 0:
            self.__fill_combo_box()
            self.__video_label.set_cam_index_first_time(0)
            self.__video_label.start_video_play()
