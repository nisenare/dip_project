# python -m pip install opencv-contrib-python pillow imutils ultralytics cvlib
# deprecated tensorflow

import tkinter as tk
from gui.main_view.main_view import MainView

def main():
    app = tk.Tk()
    main_view = MainView(app)
    app.mainloop()
    return 0

if __name__ == "__main__":
    exit(main())