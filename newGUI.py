from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtGui import QTextCursor, Qt, QTextBlockFormat
from Ui_login import Ui_Login
from Ui_main import Ui_main
import threading
import select
from chat_utils import *
import json
import time
from flappy import *

from qt_material import apply_stylesheet
import qdarktheme


class GUI():
    def __init__(self, send, recv, sm, s):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s

    def run(self):
        # global loginWindow
        app = QApplication([])
        # apply_stylesheet(app, theme = 'light_yellow.xml')
        qdarktheme.setup_theme()
        login = loginWindow(self.send, self.recv, self.sm, self.socket)
        login.show()
        app.exec()

#本来想优化一下多线程的工作逻辑但是发现太麻烦了搞不定所以我是傻逼
# class Worker(QThread):
#     finished = Signal()
#     def __init__(self, parent, statemachine, gm):
#         super().__init__(parent)
#         self.sm = statemachine
#         self.groupmembers = gm

#     def run(self):
#         # 模拟一些工作
#         group = self.sm.getgroup()
#         print('#' * 100)
#         print(threading.get_ident())
#         # self.groupmembers.clear()
#         for m in group:
#             self.groupmembers.append(m)
#         condition = True  # 根据具体条件设置
#         if condition:
#             self.finished.emit()
    
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
        self.registerButton.clicked.connect(lambda: self.register(self.usernameInput.text(), self.passwordInput.text()))
    
    def initvalues(self, send, recv, sm, s):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s

    def register(self, username, passcode):
        if len(username) > 0:
            msg = json.dumps({"action":"register", "name": username,"password": passcode})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                pass
    
    def goAhead(self, username, passcode):
        if len(username) > 0:
            msg = json.dumps({"action":"login", "name": username, "password": passcode})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.close()
                self.mainWindow = mainWindow(self.send, self.recv, self.sm, self.socket, username, passcode)
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(username)
                self.mainWindow.show()
            elif response["status"] == 'failed':
                return False
        

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
        # print(threading.get_ident())
        # self.worker = Worker(self,self.sm, self.groupmembers)
        # self.worker.finished.connect(self.refreshgroup)
        self.quitButton.pressed.connect(self.quitfrom)
        self.searchButton.pressed.connect(self.searchfor)
        self.groupSelection.activated.connect(self.connectto)
        self.refreshButton.pressed.connect(self.refreshButtonAction)
        self.textEntry.returnPressed.connect(self.sendButtonAction)
        self.textEdit.textChanged.connect(self.movetobottom)
        self.sendButton.pressed.connect(lambda: self.sendButtonAction())
        self.gameButton.pressed.connect(lambda: self.gamestart())


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
        self.maxscore = 0
        self.rank = [["Josiah", "9999999"]]

    def sendButtonAction(self):
        self.my_msg = self.textEntry.text()
        self.textEntry.clear()

    def getranking(self):
        self.my_msg = ["system","getrank"]

    def refreshButtonAction(self):
        self.groupSelection.clear()
        process = threading.Thread(target=self.refresh)
        process.daemon = True
        process.start()

    def refresh(self):
        self.my_msg = ["system", "who"]
        time.sleep(0.1)
        if self.grouplist != [] and self.sm.get_state() != S_CHATTING:
            self.groupSelection.addItems(list(self.grouplist[0].keys()))

    def quitfrom(self):
        self.my_msg = ["system", "bye"]
    
    def gamestart(self):
        self.refreshgameRankinng()
        self.flappy_thread()
    def flappy_thread(self): #写成两个函数因为觉得可能需要threading
        # 在这里调用flappy函数，并将返回值存储到self.result中
        self.score = flappy()
    
    def refreshgameRankinng(self):
        self.rankingName.clear()
        self.rankingScore.clear()
        for i in range(len(self.rank)):
            self.rankingName.append(self.rank[i][0])
            self.rankingScore.append(self.rank[i][1])

    def searchfor(self):
        #这里history还没写好
        self.sm.gethistory()
        # print(context)

    def connectto(self, index):
        self.my_msg = ["system", 'c' + self.groupSelection.itemText(index)]

    def refreshgroup(self):
        group = self.sm.getgroup()
        print('#' * 100)
        # print(threading.get_ident())
        cursor = self.groupmembers.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        for m in group:
            self.groupmembers.append(m)

    def proc(self):
        # print(threading.get_ident())
        while True: 
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            self.system_msg_selector = False
            if self.sm.freshstatus():
                self.sm.freshstatus(True)
                # self.worker.run()
                self.refreshgroup()
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
        if text[0:5] != "[You]":
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)  # 将光标移动到文本末尾
            # 获取当前块的格式
            block_format = cursor.blockFormat()
            # 设置块的对齐方式为右对齐
            block_format.setAlignment(Qt.AlignLeft)
            # 应用格式
            cursor.setBlockFormat(block_format)
            cursor.insertText(text)  # 插入文本
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.append("\n")
        else:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)  # 将光标移动到文本末尾
            # 获取当前块的格式
            block_format = cursor.blockFormat()
            # 设置块的对齐方式为右对齐
            block_format.setAlignment(Qt.AlignRight)
            # 应用格式
            cursor.setBlockFormat(block_format)
            cursor.insertText(text)  # 插入文本
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.append("\n")

    def movetobottom(self):
        scroll_bar = self.textEdit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

# if __name__ == '__main__':
#     gui = GUI(1,2,3,4)
#     gui.run()