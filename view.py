import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from math import *
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self["bg"] = "red"
        self.grid(rowspan=2, columnspan=1)
        self._createButtons()
        self._createPlots()

    def _makePlot(self, placer, _title):
        _figure = Figure(figsize=(8,6), dpi=100)
        _ax = _figure.add_subplot(111)
        _ax.set_title(_title)
        _canvas = FigureCanvasTkAgg(_figure, placer)
        _canvas.get_tk_widget().grid(row=0)
        return _figure, _ax, _canvas

    def _createPlots(self):
        self._plotsArea = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        self._plotsArea.grid(row=1, column=0, columnspan=2)
        self._topleft = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        self._topleft.grid(row=0, column=0)
        self._fig, self._ax, self._canvas = self._makePlot(self._topleft,
                "new")
        # self._canvas = FigureCanvasTkAgg(self._figure, self._plotsArea)
        self._canvas.show()
        self._canvas.get_tk_widget().grid(row=1)
        return self

    def _createButtons(self):
        self._toolbar = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        self._toolbar.grid(row=0, column=0)

        self._addCase = tk.Button(self._toolbar)
        self._addCase["text"] = "Добавить исследование"
        self._addCase["command"] = self._setConfig
        self._addCase.grid(row=0, column=0)

        self._play = tk.Button(self._toolbar)
        self._play["text"] = "Вывести на график"
        self._play["command"] = self._drawCurves
        self._play.grid(row=0, column=1)

        self._save = tk.Button(self._toolbar)
        self._save["text"] = "Сохранить"
        self._save["command"] = self._savepdf
        self._save.grid(row=0, column=2)

        self._QUIT = tk.Button(self._toolbar, text="QUIT", fg="red", command=root.destroy)
        self._QUIT.grid(row=0, column=3)

        return self

    def _setConfig(self):
        self._addCase["bg"] = "green"
        return self

    def _drawCurves(self):
        self._ax.plot(np.arange(0, pi, pi / 180), np.sin(np.arange(0, pi, pi / 180)))
        self._canvas.show()
        return self

    def _savepdf(self):
        self._fig.savefig("plotty.pdf")
        return self

    def __del__(self):
        del self._addCase
        del self._play
        del self._save
        del self._QUIT
        del self._fig
        del self._canvas
        del self._toolbar

root = tk.Tk()
app = Application(master=root)
app.mainloop()
