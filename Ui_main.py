# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QWidget)

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(677, 555)
        main.setMinimumSize(QSize(630, 510))
        main.setMaximumSize(QSize(9999, 9999))
        main.setCursor(QCursor(Qt.ArrowCursor))
        self.gridLayout_3 = QGridLayout(main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 1, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEntry = QLineEdit(main)
        self.textEntry.setObjectName(u"textEntry")
        self.textEntry.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.textEntry, 1, 0, 1, 1)

        self.sendButton = QPushButton(main)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.sendButton, 1, 1, 1, 1)

        self.textEdit = QTextEdit(main)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 400))
        self.textEdit.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.textEdit.setReadOnly(True)
        self.textEdit.setOverwriteMode(False)

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)


        self.gridLayout_3.addLayout(self.gridLayout, 2, 1, 2, 2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gameButton = QPushButton(main)
        self.gameButton.setObjectName(u"gameButton")

        self.gridLayout_2.addWidget(self.gameButton, 5, 0, 1, 1)

        self.label = QLabel(main)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 6, 0, 1, 1)

        self.timeButton = QPushButton(main)
        self.timeButton.setObjectName(u"timeButton")

        self.gridLayout_2.addWidget(self.timeButton, 8, 0, 1, 1)

        self.searchButton = QPushButton(main)
        self.searchButton.setObjectName(u"searchButton")

        self.gridLayout_2.addWidget(self.searchButton, 2, 0, 1, 1)

        self.groupmembers = QTextEdit(main)
        self.groupmembers.setObjectName(u"groupmembers")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupmembers.sizePolicy().hasHeightForWidth())
        self.groupmembers.setSizePolicy(sizePolicy)
        self.groupmembers.setMaximumSize(QSize(190, 150))
        self.groupmembers.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.groupmembers.setReadOnly(True)

        self.gridLayout_2.addWidget(self.groupmembers, 3, 0, 1, 1)

        self.refreshButton = QPushButton(main)
        self.refreshButton.setObjectName(u"refreshButton")

        self.gridLayout_2.addWidget(self.refreshButton, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rankingName = QTextEdit(main)
        self.rankingName.setObjectName(u"rankingName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rankingName.sizePolicy().hasHeightForWidth())
        self.rankingName.setSizePolicy(sizePolicy1)
        self.rankingName.setMinimumSize(QSize(0, 50))
        self.rankingName.setMaximumSize(QSize(95, 16777215))
        self.rankingName.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.rankingName.setReadOnly(True)

        self.horizontalLayout.addWidget(self.rankingName)

        self.rankingScore = QTextEdit(main)
        self.rankingScore.setObjectName(u"rankingScore")
        sizePolicy1.setHeightForWidth(self.rankingScore.sizePolicy().hasHeightForWidth())
        self.rankingScore.setSizePolicy(sizePolicy1)
        self.rankingScore.setMaximumSize(QSize(95, 16777215))
        self.rankingScore.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.rankingScore.setReadOnly(True)

        self.horizontalLayout.addWidget(self.rankingScore)


        self.gridLayout_2.addLayout(self.horizontalLayout, 7, 0, 1, 1)

        self.quitButton = QPushButton(main)
        self.quitButton.setObjectName(u"quitButton")

        self.gridLayout_2.addWidget(self.quitButton, 9, 0, 1, 1)

        self.groupSelection = QComboBox(main)
        self.groupSelection.setObjectName(u"groupSelection")

        self.gridLayout_2.addWidget(self.groupSelection, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 3, 2, 1)

        self.horizontalSpacer = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 4, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 5, 3, 1, 1)


        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"Form", None))
        self.sendButton.setText(QCoreApplication.translate("main", u"Send", None))
        self.textEdit.setHtml(QCoreApplication.translate("main", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.gameButton.setText(QCoreApplication.translate("main", u"Flappy", None))
        self.label.setText(QCoreApplication.translate("main", u"Ranking", None))
        self.timeButton.setText(QCoreApplication.translate("main", u"CheckTime", None))
        self.searchButton.setText(QCoreApplication.translate("main", u"Search", None))
        self.refreshButton.setText(QCoreApplication.translate("main", u"Refresh", None))
        self.quitButton.setText(QCoreApplication.translate("main", u"Quit", None))
    # retranslateUi

