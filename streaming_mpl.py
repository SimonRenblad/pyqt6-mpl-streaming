from PyQt6 import QtCore, QtWidgets, QtGui
import numpy as np
import random
import sys
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.sc)
        # for live plotting use a timer and in-place update the plot with .set_yaxis for performance
        self.n = 50
        self.xdata = list(range(50))
        self.ydata = [random.randint(0, 10) for _ in range(50)]
        self._plot_ref = None
        self.update_plot()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.update_data)
        self.timer2.start()

    def update_data(self):
        self.xdata.append(self.n)
        self.ydata.append(random.randint(0, 10))
        self.n += 1

    def update_plot(self):
        if self._plot_ref is None:
            plot_refs = self.sc.axes.plot(self.xdata, self.ydata, 'r')
            self._plot_ref = plot_refs[0]
        else:
            self._plot_ref.set_data(self.xdata, self.ydata)
        self.sc.axes.relim()
        self.sc.axes.autoscale_view(True, True, True)
        self.sc.draw()


def main():
    app = QtWidgets.QApplication(["demo application"])
    main_window = MainWindow()
    main_window.show()
    return sys.exit(app.exec())


if __name__ == "__main__":
    main()
