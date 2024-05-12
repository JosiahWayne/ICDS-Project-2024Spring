# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.setEnabled(True)
        Login.resize(400, 400)
        Login.setMinimumSize(QSize(400, 400))
        Login.setMaximumSize(QSize(400, 400))
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 67, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Login)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.usernameInput = QLineEdit(Login)
        self.usernameInput.setObjectName(u"usernameInput")

        self.horizontalLayout_2.addWidget(self.usernameInput)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.passwordInput = QLineEdit(Login)
        self.passwordInput.setObjectName(u"passwordInput")
        self.passwordInput.setInputMethodHints(Qt.InputMethodHint.ImhHiddenText|Qt.InputMethodHint.ImhNoAutoUppercase|Qt.InputMethodHint.ImhNoPredictiveText|Qt.InputMethodHint.ImhSensitiveData)
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout.addWidget(self.passwordInput)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 3)

        self.verticalSpacer_3 = QSpacerItem(20, 67, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 5, 2, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.loginButton = QPushButton(Login)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(80, 32))

        self.verticalLayout_3.addWidget(self.loginButton)

        self.registerButton = QPushButton(Login)
        self.registerButton.setObjectName(u"registerButton")
        self.registerButton.setMaximumSize(QSize(80, 16777215))

        self.verticalLayout_3.addWidget(self.registerButton)


        self.gridLayout.addLayout(self.verticalLayout_3, 3, 2, 2, 1)

        self.horizontalSpacer_4 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 3, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.label.setText(QCoreApplication.translate("Login", u"Username", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"Password", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"Login", None))
        self.registerButton.setText(QCoreApplication.translate("Login", u"Register", None))
    # retranslateUi

