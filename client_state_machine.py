"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.fresh = False
        self.history = ""

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def freshstatus(self, c=False):
        if c == True:
            self.fresh = not self.fresh
            return not self.fresh
        else:
            return self.fresh
    
    def gethistory(self):
        return self.history

    def getgroup(self):
        msg = json.dumps({"action":"getgroup", "from": self.me})
        mysend(self.s, msg)
        grouplst = json.loads(myrecv(self.s))["grouplist"]
        # print(grouplst)
        return grouplst
    
    def getrank(self):
        msg = json.dumps({"action":"getrank"})
        mysend(self.s, msg)
        print("recved")
        recv = myrecv(self.s)
        print(recv)
        print("############")
        rank = json.loads(recv)["rank"]
        print(rank)
        print("############")
        return rank

    def updatescore(self, name, score):
        msg = json.dumps({"action":"updaterank", "name":name, "score": score})
        mysend(self.s, msg)
        print("sent")
        result = json.loads(myrecv(self.s))["results"]
        # print(result)

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    self.out_msg = []
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    # self.out_msg += 'Here are all the users in the system:\n'
                    # print(self.out_msg)
                    self.out_msg += logged_in

                elif my_msg == "getrank#!@#!@!!!#!@!#!@#!$!$#%:::system":
                    return self.getrank()

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.freshstatus(True)
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                
                elif "sys::updaterank" in my_msg:
                    score = my_msg[15:]
                    self.updatescore(self.me, score)
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    self.freshstatus(True)

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                self.history += "I" + ":" + my_msg + "\n"
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                    self.freshstatus(True)
                    mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "gpt": False}))
                
                elif len(my_msg) >= 4 and my_msg[0:4] == "@GPT":
                    context = self.gethistory()
                    mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "context":context, "gpt": True}))

                elif my_msg == "getrank#!@#!@!!!#!@!#!@#!$!$#%:::system":
                    return self.getrank()
                
                elif "sys::updaterank" in my_msg:
                    score = my_msg[15:]
                    self.updatescore(self.me, score)

                else:
                    mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "gpt": False}))
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                # print(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                    self.freshstatus(True)
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                    self.freshstatus(True)
                else:
                    self.out_msg += peer_msg["from"] + ' ' + peer_msg["message"]
                    self.history += peer_msg["from"] + ":" + peer_msg["message"] + "\n"
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.history = ""
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
