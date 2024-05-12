from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
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
import pygame

from qt_material import apply_stylesheet
import qdarktheme


class GUI():
    def __init__(self, send, recv, sm, s):
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s

    def run(self):
        app = QApplication([])
        self.appsitt = app
        # apply_stylesheet(app, theme = 'light_teal.xml')
        qdarktheme.setup_theme()
        login = loginWindow(self.send, self.recv, self.sm, self.socket)
        login.show()
        app.exec()

#本来想优化一下多线程的工作逻辑但是发现太麻烦了搞不定所以我是傻逼
    
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
    
    def loginfailed(self):
        QMessageBox.warning(self,"Login Failed","Login Failed. Please check your username and password.")

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
                self.loginfailed()
        

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
        self.timeButton.pressed.connect(self.checktime)
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

    def sendButtonAction(self):
        self.my_msg = self.textEntry.text()
        self.textEntry.clear()

    def getranking(self):
        self.my_msg = ["system", "getrank#!@#!@!!!#!@!#!@#!$!$#%:::system"]

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
        self.refreshgameRanking()
        self.flappy_thread()    
    def flappy_thread(self): #写成两个函数因为觉得可能需要threading
        self.score = flappy()
        self.my_msg = ["system", f"sys::updaterank{str(self.score)}"]
    

    def refreshgameRanking(self):
        self.getgameRankingThread()
        # rankprocess = threading.Thread(target=self.getgameRankingThread)
        # rankprocess.daemon = True
        # rankprocess.start()
        
    def clearcontext(self, obj):
        cursor = obj.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()

    def getgameRankingThread(self):
        self.clearcontext(self.rankingName)
        self.clearcontext(self.rankingScore)
        sorted_scores = sorted(self.rank.items(), key=lambda x: int(x[1]), reverse=True)
        for name, score in sorted_scores:
            self.rankingName.append(name)
            self.rankingScore.append(score)
            
        
    def searchfor(self):
        search_msg = self.textEntry.text()
        self.textEntry.clear()
        self.my_msg = ["system", f"?{search_msg}"]
        
    def checktime(self):
        self.my_msg = ["system", "time"]

    def getcontext(self):
        context = self.sm.gethistory()
        return context

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
        self.maxscore = 0
        self.rank = {"Josiah": "9999999"}
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
            if peer_msg != []:
                print(peer_msg)
                pm = json.loads(peer_msg)
                if pm["action"] == "freshrank":
                    peer_msg = []
                    self.rank = pm["rank"]
                    self.refreshgameRanking()
                    continue
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                if len(self.my_msg) >= 2 and self.my_msg[0] == "system":
                    self.system_msg_selector = True
                    if self.my_msg[1][0] == "c":
                        self.my_msg = self.my_msg[1]

                    if self.my_msg[1] == "time":
                        self.my_msg = self.my_msg[1]

                    if self.my_msg[1] == "getrank#!@#!@!!!#!@!#!@#!$!$#%:::system":
                        self.my_msg = self.my_msg[1]
                        self.rank = self.sm.proc(self.my_msg, peer_msg)
                        self.my_msg = ""
                        continue

                    if "sys::updaterank" in self.my_msg[1]:
                        self.my_msg = self.my_msg[1]
                        self.rank = self.sm.proc(self.my_msg, peer_msg)
                        self.my_msg = ""
                        continue

                    if self.my_msg[1] == "who":
                        self.my_msg = self.my_msg[1]
                        self.grouplist = self.sm.proc(self.my_msg, peer_msg)
                        self.my_msg = ""
                        continue
                    if self.my_msg[1] == "bye":
                        self.my_msg = self.my_msg[1]
                    
                    if self.my_msg[1][0] == "?":
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
                # self.system_msg = str(peer_msg)   
                self.my_msg = ""
                if pm["action"] != "generate_key" and pm["action"] != "exchange_key":
                    self.addtext(self.system_msg)
    
    def addtext(self, text):
        if len(text) >= 5 and text[0:5] != "[You]":
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