################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI FILE
from ui_main import Ui_MainWindow

# IMPORT FUNCTIONS
from ui_functions import *
from PySide2.QtGui import *
from PySide2.QtCore import QRect, Slot, Qt

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#embed matplot plot to a widget needs this
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim([0, width])
        self.axes.set_ylim([0, height])

        super(MplCanvas, self).__init__(fig)


def get_inputImage(self):
    global path_to_file
    path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("~/Desktop/"), self.tr("Images (*.jpg *.png *.jpeg)"))
    load_image(self, path_to_file)

def load_image(self, image_path):
    pixmap = QPixmap(image_path)
    self.ui.label_inputImage.setPixmap(pixmap)


def compute_draw_graph(self):

    start_time = time.time()
    #preprocess image
    img = cv2.imread(path_to_file,0)
    img= cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

    # mirror the image in y direction
    img=img[::-1,:]
    h, w = img.shape
    

    sc = MplCanvas(self, w, h, dpi=125)
    

    #indices= cv2.findNonZero(img)
    

    
    #get white coordinates in binary image
    indices = np.where(img == [255])
    
 
    #set data to plot
    sc.axes.plot(indices[1], indices[0], '.')
    #delete last drew plot
    for i in reversed(range(self.lay.count())): 
        self.lay.itemAt(i).widget().setParent(None)

    self.lay.addWidget(sc)
    print("--- %s seconds ---" % (time.time() - start_time))


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)





        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.ui.btn_inputImage.clicked.connect(lambda: get_inputImage(self))
        self.ui.pushButton_getGraph.clicked.connect(lambda: compute_draw_graph(self))


        #widget to show graph image
        self.lay = QtWidgets.QVBoxLayout(self.ui.widget)


        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))



        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    

    sys.exit(app.exec_())
