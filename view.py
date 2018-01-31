import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from math import *
import numpy as np

from control import *

class ClutterDisplay(tk.Frame):
    '''
    В этом приложении будут четыре графика и четыре кнопки. И одно окно
    с выпадающим меню.
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self._placeFrames()
        self._placeButtons()
        self._placeEmptyPlots()

    def _placeFrames(self):
        self._plotsArea = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        self._plotsArea.grid(row=1, rowspan=2, columnspan=2)

        self._toolbar = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        self._toolbar.grid(row=0, columnspan=4)

        self._topleft = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        self._topright = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        self._bottomleft = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        self._bottomright = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        self._topleft.grid(row=0, column=0)
        self._topright.grid(row=0, column=1)
        self._bottomleft.grid(row=1, column=0)
        self._bottomright.grid(row=1, column=1)

        return self

    def _placePlot(self, placer):
        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, placer)
        canvas.get_tk_widget().pack(side="top")
        canvas.show()
        return self

    def _placeEmptyPlots(self):
        self._placePlot(self._topleft)
        self._placePlot(self._topright)
        self._placePlot(self._bottomleft)
        self._placePlot(self._bottomright)
        return self

    def _placeButtons(self):
        self._config = tk.Button(self._toolbar, text="Настройка", command=self.setConfig)
        self._show = tk.Button(self._toolbar, text="Вывести на графики", command=self.setPlots)
        self._save = tk.Button(self._toolbar, text="Сохранить графики", command=self.savePlots)
        self._quit = tk.Button(self._toolbar, text="Выход", fg="red", command=root.destroy)

        self._config.grid(row=0, column=0)
        self._show.grid(row=0, column=1)
        self._save.grid(row=0, column=2)
        self._quit.grid(row=0, column=3)
        return self

    def setConfig(self):
        self._config["bg"] = "green"
        self._config["fg"] = "white"
        return self

    def setPlots(self):
        self._show["bg"] = "orange"
        return self

    def savePlots(self):
        self._save["bg"] = "blue"
        self._save["fg"] = "white"
        return self

    def __del__(self):
        del self._bottomleft
        del self._bottomright
        del self._topleft
        del self._topright
        del self._save
        del self._show
        del self._config
        del self._quit
        del self._plotsArea
        del self._toolbar

root = tk.Tk()
app = ClutterDisplay(master=root)
app.mainloop()
