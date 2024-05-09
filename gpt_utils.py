import requests
import json

import threading
import select
from chat_utils import *
import time

url = "https://openai.api2d.net/v1/chat/completions"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fk226555-DCh9BjnQ8juitfMYRT0Ypw12cknERR0f' # <-- 把 fkxxxxx 替换成你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
}
context = ''
data = {
  "model": "gpt-3.5-turbo-0125",
  "messages": [{"role": "user", "content": ""}],
  "stream": False,
}


class GPT():
    def __init__(self) -> None:
        pass

    def chattoGPT(self,context, msg=''):
        pm = context + msg
        prompt = pm + "\nAI:"
        data["messages"][0]["content"] = prompt
        response = requests.post(url, headers=headers, json=data)
        ans = response.json()
        return ans["choices"][0]["message"]['content']

class chatprocess():
    def __init__(self, send, recv, sm, s, username, passcode):
        self.initvalues(send, recv, sm, s, username, passcode)
        self.gpt = GPT()
        process = threading.Thread(target=self.proc)
        process.daemon = True
        process.start()

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

    def quitfrom(self):
        self.my_msg = ["system", "bye"]

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
                    if self.my_msg[1] == "bye":
                        self.my_msg = self.my_msg[1]
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                if self.my_msg != "" and not self.system_msg_selector:
                    if len(self.system_msg) == 0:
                        out = f"[You] {self.my_msg}"
                    else:
                        out = f"[You] {self.my_msg} \n\n {self.system_msg}"
                    self.my_msg = ""
                    continue
                if "@GPT" in self.system_msg:
                    print(context)
                    context = self.sm.gethistory()
                    self.my_msg = self.gpt.chattoGPT(context)
                self.my_msg = ""