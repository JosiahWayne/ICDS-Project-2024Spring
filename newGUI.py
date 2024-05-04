from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor, Qt, QTextBlockFormat
from Ui_login import Ui_Login
from Ui_main import Ui_main
import threading
import select
from chat_utils import *
import json

class GUI():
    def __init__(self, send, recv, sm, s):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s

    def run(self):
        # global loginWindow
        app = QApplication([])
        login = loginWindow(self.send, self.recv, self.sm, self.socket)
        login.show()
        app.exec()

class loginWindow(QWidget, Ui_Login):
    def __init__(self, send, recv, sm, s): #send is a function
        super().__init__()
        self.initvalues(send, recv, sm, s)
        self.setupUi(self)
        self.setWindowTitle("ICDS Chat System Login")
        self.bindActions()

    def bindActions(self):
        self.passwordInput.returnPressed.connect(lambda: self.goAhead(self.usernameInput.text(), self.passwordInput.text()))
        self.loginButton.clicked.connect(lambda: self.goAhead(self.usernameInput.text(), self.passwordInput.text()))
    
    def initvalues(self, send, recv, sm, s):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s

    def goAhead(self, username, passcode):
        if len(username) > 0:
            msg = json.dumps({"action":"login", "name": username})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.close()
                self.mainWindow = mainWindow(self.send, self.recv, self.sm, self.socket, username, passcode)
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(username)
                self.mainWindow.show()
        

class mainWindow(QWidget, Ui_main):
    def __init__(self, send, recv, sm, s, username, passcode):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"Logged in as - {username}")
        self.initvalues(send, recv, sm, s, username, passcode)
        self.bindActions()

        process = threading.Thread(target=self.proc)
        process.daemon = True
        process.start()

    def bindActions(self):
        self.quitButton.pressed.connect(self.quitfrom)
        self.searchButton.pressed.connect(self.searchfor)
        self.groupSelection.activated.connect(self.connectto)
        self.refreshButton.pressed.connect(self.refreshButtonAction)
        self.textEntry.returnPressed.connect(self.sendButtonAction)
        self.textEdit.textChanged.connect(self.movetobottom)
        self.sendButton.pressed.connect(lambda: self.sendButtonAction())


    def initvalues(self, send, recv, sm, s, username, passcode):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.username = username
        self.passcode = passcode
        self.my_msg = ""
        self.system_msg = ""
        self.grouplist = []
        self.system_msg_selector = False

    def sendButtonAction(self):
        self.my_msg = self.textEntry.text()
        self.textEntry.clear()

    def refreshButtonAction(self):
        bacup = self.grouplist
        self.my_msg = ["system", "who"]
        if bacup == self.grouplist:
            for i in range(1000):
                continue
        self.groupSelection.clear()
        if self.grouplist != []:
            self.groupSelection.addItems(list(self.grouplist[0].keys()))

    def quitfrom(self):
        self.my_msg = ["system", "bye"]
    
    def searchfor(self):
        pass

    def connectto(self, index):
        # print()
        self.my_msg = ["system", 'c' + self.groupSelection.itemText(index)]

    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            self.system_msg_selector = False
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                if len(self.my_msg) >= 2 and self.my_msg[0] == "system":
                    self.system_msg_selector = True
                    if self.my_msg[1][0] == "c":
                        self.my_msg = self.my_msg[1]

                    if self.my_msg[1] == "time":
                        self.my_msg = self.my_msg[1]

                    if self.my_msg[1] == "who":
                        self.my_msg = self.my_msg[1]
                        self.grouplist = self.sm.proc(self.my_msg, peer_msg)
                        self.my_msg = ""
                        continue
                    if self.my_msg[1] == "bye":
                        self.my_msg = self.my_msg[1]
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                if self.my_msg != "" and not self.system_msg_selector:
                    if len(self.system_msg) == 0:
                        out = f"[You] {self.my_msg}"
                    else:
                        out = f"[You] {self.my_msg} \n\n {self.system_msg}"
                    self.addtext(out)
                    self.my_msg = ""
                    continue

                self.my_msg = ""
                self.addtext(self.system_msg)
    
    def addtext(self, text):
        # 这里想实现一个发送出去的消息右侧对其的效果，但是有bug，还没修好
        # if text[0:5] != "[You]":
        #     self.textEdit.append(text)
        # else:
        #     text = text.split('\n')
        #     cursor = self.textEdit.textCursor()
        #     cursor.movePosition(QTextCursor.End)
        #     cursor.insertText(text[0])
        #     cursor.movePosition(QTextCursor.PreviousBlock)
        #     # 获取当前块的格式
        #     block_format = cursor.blockFormat()
        #     # 设置块的对齐方式为右对齐
        #     block_format.setAlignment(Qt.AlignRight)
        #     # 应用格式
        #     cursor.setBlockFormat(block_format)
        #     for t in text[1:]:
        #         self.textEdit.append(t)
        self.textEdit.append(text)
        self.textEdit.append("")

    def movetobottom(self):
        scroll_bar = self.textEdit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

# if __name__ == '__main__':
#     gui = GUI(1,2,3,4)
#     gui.run()