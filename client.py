from PyQt6 import QtCore, QtWidgets, QtGui
import numpy as np
import random
import sys
import matplotlib
import socket
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.style as mplstyle
mplstyle.use('fast')
import threading
import queue


HOST, PORT = "localhost", 9999


class Connection:
    def __init__(self, queue):
        self.queue = queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def target(self):
        try:
            self.sock.connect((HOST, PORT))
            while True:
                datastr = ""
                received = ""
                while received != "\n":
                    datastr += received
                    received = self.sock.recv(1).decode()
                self.queue.put(int(datastr))
        except:
            pass


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)


class MainWindow(QtWidgets.QMainWindow):
    operate = QtCore.pyqtSignal()

    def __init__(self, connection, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.sc)
        # for live plotting use a timer and in-place update the plot with .set_yaxis for performance
        self.connection = connection 
        self.queue = connection.queue

        self.n = 50
        self.xdata = list(range(50))
        self.ydata = [random.randint(0, 10) for _ in range(50)]
        self._plot_ref = None
        self.update_plot()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_data(self, res):
        self.xdata.append(self.n)
        self.ydata.append(res)
        self.n += 1

    def update_plot(self):
        try:
            while True:
                data = self.queue.get_nowait()
                self.update_data(data)
        except queue.Empty:
            pass
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
    q = queue.Queue()
    connection = Connection(q)
    main_window = MainWindow(connection)
    main_window.show()
    thread = threading.Thread(target=connection.target)
    thread.start()
    app.exec()
    connection.sock.close()
    thread.join()


if __name__ == "__main__":
    main()
