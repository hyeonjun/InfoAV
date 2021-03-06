# -*- coding:utf-8 -*-

import sys
from Optimization import *
import Info
from SelectionPath import *
import Settings
from TempRemove.TempClean import TempRemove
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * # 기본적인 UI 구성요소를 제공하는 위젯(클래스)

class InfonetAV(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):
        # 타이틀 바에 나타나는 창의 제목 설정
        self.setWindowTitle('Infonet Anti-Virus')
        # 어플리케이션 아이콘으로 설정, QIcon 객체 생성
        self.setWindowIcon(QIcon(".\image\Icon.jpg"))
        # self.move(300,300) # 위젯 스크린의 x=300px, y=300px의 위치로 이동
        self.setFixedSize(850, 530) # 위젯의 크기를 너비 800px, 높이 500px로 조절
        self.center() # 중앙에 위치

        # pixmap = QPixmap('C:\Users\wngus\GUIproject\image\InfonetVeccine.jpg') # 파일 이름을 입력해주고, OPixmap 객체를 만든다.
        # pixmap.scaledToWidth(800) # 출력될 이미지의 폭을 변경, 높이는 scaledToHeight/폭은 비례해서 조정됨
        label = QLabel(self)
        label.setGeometry(QRect(0, 0, 850, 230))
        label.setPixmap(QPixmap(".\image\InfonetVeccine2.png"))

        """
        lbl_img = QLabel() # 라벨을 하나 만든다
        lbl_img.setPixmap(pixmap) # pixmap을 라벨에 표시될 이미지로 설정
        # 이미지의 너비, 높이를 반환
        # lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        lbl_size = QLabel(self)
        lbl_size.setAlignment(Qt.AlignCenter) # 가운데 정렬
        
        vbox = QVBoxLayout() # 수평 박스 레이아웃을 하나 만들어 라벨을 배치
        vbox.addWidget(lbl_img) # 라벨에 이미지 넣음
        vbox.addWidget(lbl_size) # 가운데 정렬
        """

        """
        # 라벨 (라벨 텍스트, 부모 위젯)
        IVlabel = QLabel(self)
        IVlabel.setAlignment(Qt.AlignVCenter) # 라벨의 배치 설정
        # Qt.AlignCenter -> 수평,수직 방향 모드 가운데 위치
        # Qt.AlignVCenter -> 수직 방향으로만 가운데에 설정
        # Qt.AlignVCenter -> 수평방향으로 가운데
        font = IVlabel.font() # 폰트 만듬
        font.setPointSize(20) # 폰트의 크기 설정, 설정 안하면 디폴트 크기인 13으로 설정
        # font.setFamily('Times New Roman') # 폰트의 종류를 설정
        # font.setBold(True) # 폰트를 진하게 함
        IVlabel.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(IVlabel)

        self.setLayout(layout)
        """

        # 푸시 버튼(버튼에 나타날 텍스트, 버튼이 속할 부모 클래스)
        AScanBtn1 = QPushButton(self)
        # 버튼 위치 설정
        AScanBtn1.move(0,230)
        AScanBtn1.setFixedSize(286,300)
        # 선택되거나 선택되지 않은 상태를 유지
        # AScanBtn1.setCheckable(True)
        # 버튼의 상태가 바뀌게 됨
        # AScanBtn1.toggle()
        AScanBtn1.clicked.connect(self.AScanButtonClicked)
        img1 = QIcon()
        img1.addPixmap(QPixmap('.\image\localScan.png'), QIcon.Normal, QIcon.Off)
        AScanBtn1.setIcon(img1)
        AScanBtn1.setIconSize(QSize(286,300))

        PScanBtn1 = QPushButton(self)
        PScanBtn1.move(286,230)
        PScanBtn1.setFixedSize(286,300)
        # PScanBtn1.setCheckable(True)
        # PScanBtn1.toggle()
        PScanBtn1.clicked.connect(self.PScanButtonClicked)
        img2 = QIcon()
        img2.addPixmap(QPixmap('.\image\SelectionScan.png'), QIcon.Normal, QIcon.Off)
        PScanBtn1.setIcon(img2)
        PScanBtn1.setIconSize(QSize(286,300))

        OptimalBtn = QPushButton(self)
        OptimalBtn.move(572,230)
        OptimalBtn.setFixedSize(278,300)
        # OptimalBtn.setCheckable(True)
        # OptimalBtn.toggle()
        OptimalBtn.clicked.connect(self.OptimalButtonClicked)
        img3 = QIcon()
        img3.addPixmap(QPixmap('.\image\Optimal.png'), QIcon.Normal, QIcon.Off)
        OptimalBtn.setIcon(img3)
        OptimalBtn.setIconSize(QSize(278, 300))

        InfoBtn = QPushButton(self)
        InfoBtn.setGeometry(QRect(739, 171, 28, 28))
        img4 = QIcon()
        img4.addPixmap(QPixmap(".\image\Info.png"), QIcon.Normal, QIcon.Off)
        InfoBtn.setIcon(img4)
        InfoBtn.setIconSize(QSize(28,28))
        InfoBtn.clicked.connect(self.InfoButtonClicked)

        SetBtn = QPushButton(self)
        SetBtn.setGeometry(QRect(787, 171, 28, 28))
        img5 = QIcon()
        img5.addPixmap(QPixmap(".\image\Set.png"), QIcon.Normal, QIcon.Off)
        SetBtn.setIcon(img5)
        SetBtn.setIconSize(QSize(28,28))
        SetBtn.clicked.connect(self.SetButtonClicked)

    def AScanButtonClicked(self):
        from InfonetVaccine.IV import IV
        set1 = Setting.fileSet
        set2 = Setting.disinfectSet
        self.ui = IV('.', set1.checkState(),set2.checkState())
        self.ui.show()


    def PScanButtonClicked(self):
        set1 = Setting.fileSet
        set2 = Setting.disinfectSet
        self.ui = SelectionPath(set1.checkState(), set2.checkState())
        self.ui.show()

    def OptimalButtonClicked(self):
        self.ui1 = TempRemove()
        self.ui1.show()

    def InfoButtonClicked(self):
        InfoWindow.show()

    def SetButtonClicked(self):
        Setting.show()

    def center(self):
        qr = self.frameGeometry() # 창의 위치와 크기 정보를 가져옴
        # 사용하는 모니터 화면의 가운데 위치를 파악
        cp = QDesktopWidget().availableGeometry().center()
        # 창의 직사강형 위치를 화면의 중심의 위치로 이동
        qr.moveCenter(cp)
        # 현재 창을 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동
        # 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타남
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    IV= InfonetAV()
    InfoWindow = Info.InfoWindow()
    Setting = Settings.SettingWindow()
    IV.show() # 위젯을 스크린에 보여줌
    app.exec_()
