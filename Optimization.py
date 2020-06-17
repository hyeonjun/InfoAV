# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * # 기본적인 UI 구성요소를 제공하는 위젯(클래스)

class Ui_OptimalWindow(object):
    def initUI(self, OptimalWindow):
        OptimalWindow.setObjectName("OptimalWindow")
        OptimalWindow.setWindowTitle('Optimization')
        OptimalWindow.setWindowIcon(QIcon(".\image\Icon.jpg"))
        OptimalWindow.resize(600, 579)  # 위젯의 크기를 너비 800px, 높이 500px로 조절
        OptimalWindow.center()  # 중앙에 위치

        self.title = QLabel(OptimalWindow)
        self.title.setGeometry(QRect(0, 0, 600, 78))
        self.title.setText("")
        self.title.setPixmap(QPixmap(".\OptimalImage\\Optimization.jpg"))

        self.Main = QLabel(OptimalWindow)
        self.Main.setGeometry(QRect(0, 79, 600, 500))
        self.Main.setText("")
        self.Main.setPixmap(QPixmap(".\OptimalImage\\Main.png"))

        self.ScanInfo = QTextEdit(OptimalWindow)
        self.ScanInfo.setGeometry(QRect(40, 109, 500, 400))

    def center(self):
        qr = self.frameGeometry() # 창의 위치와 크기 정보를 가져옴
        # 사용하는 모니터 화면의 가운데 위치를 파악
        cp = QDesktopWidget().availableGeometry().center()
        # 창의 직사강형 위치를 화면의 중심의 위치로 이동
        qr.moveCenter(cp)
        # 현재 창을 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동
        # 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타남
        self.move(qr.topLeft())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    OptimalWindow = QWidget()
    ui = Ui_OptimalWindow()
    ui.initUI(OptimalWindow)
    OptimalWindow.show()
    app.exec_()