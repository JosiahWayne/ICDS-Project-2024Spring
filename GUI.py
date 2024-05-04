#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021
Adjusted on May 1 2024

@author: bing
@Second Author: Josiah
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        style = ttk.Style()
        style.theme_use("clam") # 主题选择
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

        self.ChatRelw = 0.65 #聊天主界面的相对宽度
        self.BackgroundColor = "#17202A" #聊天大块元素的背景颜色
        self.grouplist = []
        self.system_msg_selector = False

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.30, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 14")
          
        self.labelName.place(relheight = 0.1,
                             relx = 0.24, 
                             rely = 0.30)
        # create a entry box for 
        # typing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
        self.entryName.bind("<Return>", lambda event, self=self: self.goAhead(self.entryName.get()))
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.30)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
  
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 700,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1 * self.ChatRelw)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1 * self.ChatRelw,
                        rely = 0.07,
                        relheight = 0.012)

        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1 * self.ChatRelw, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1 * self.ChatRelw,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
        self.entryMsg.bind("<Return>", lambda event: self.sendButton(self.entryMsg.get()))

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        self.textCons["yscrollcommand"] = scrollbar.set

        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)

        self.textCons.config(state = DISABLED)

        ####下面是console的代码
        #添加右侧容器
        self.vtclineWidth = 0.01
        self.labelRight = Label(
            self.Window,
            bg = self.BackgroundColor,
        )
        self.labelRight.place(
            relx = 1 * self.ChatRelw,
            rely = 0,
            relwidth = 1 - self.ChatRelw,
            relheight = 1
        )

        #添加分割线
        self.vtcline = Label(self.labelRight,
            height = 1,
            bg = "#666666"
        )
        self.vtcline.place(
            relwidth = self.vtclineWidth,
            relx = 0,
            rely = 0,
            relheight = 1
        )

        #添加时间按钮
        self.buttonTime = Button(
            self.labelRight,
            text = "Time",
            bg = "#ABB2B9",
            command = lambda : self.getTimeButton()
        )
        self.buttonTime.place(
            relx = self.vtclineWidth,
            rely = 0.05,
            relheight = 0.1,
            relwidth = 1 - self.vtclineWidth
        )

        #添加群组选择栏
        self.groupSelection = ttk.Combobox(
            self.labelRight,
            values = self.grouplist
        )
        self.groupSelection.place(
            relx = self.vtclineWidth,
            rely = 0.05 + 0.1,
            relwidth = 1 - self.vtclineWidth - 0.2
        )
        self.groupSelection.bind("<<ComboboxSelected>>", self.connectto)

        self.refreshButton = Button(
            self.labelRight,
            text = "Refresh",
            bg = "#ABB2B9",
            command = lambda : self.freshGroupList()
        )
        self.refreshButton.place(
            relx = 0.8,
            rely = 0.05 + 0.1,
            relwidth = 0.2
        )

        self.quitButton = Button(
            self.labelRight,
            text = "Quit",
            bg = "#ABB2B9",
            command = lambda : self.disconnect()
        )
        self.quitButton.place(
            relx = self.vtclineWidth,
            rely = 0.9,
            relwidth = 1 - self.vtclineWidth,
            relheight = 0.1
        )
    
    def disconnect(self):
        self.my_msg = "bye"

    def connectto(self, event):
        selected_item = self.groupSelection.get()
        self.my_msg = ["system", 'c' + selected_item]

    def freshGroupList(self):
        self.my_msg = ["system","who"]
        while len(self.grouplist) == 0:
            continue
        print(self.grouplist)
        self.groupSelection["values"] = list(self.grouplist[0].keys())

    def getTimeButton(self):
        self.my_msg = ["system","time"]

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            self.system_msg_selector = False
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                if len(self.my_msg) >= 2 and self.my_msg[0] == "system": #这边还没写之前的判断逻辑，记得写
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
        self.textCons.config(state = NORMAL)
        self.textCons.insert(END, text +"\n\n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()