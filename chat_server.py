"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import gpt_utils
import threading

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        # self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        # self.sonnet = pkl.load(self.sonnet_f)
        # self.sonnet_f.close()
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.rank = {}
        with open("rank.txt", "r") as file:
            for i in file.readlines():
                temp = [i.split()[0],i.split()[1]]
                self.rank[temp[0]] = temp[1]

    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        # print(self.all_sockets)
        #read the msg that should have login code plus username
        userdata = "Userindex.txt"
        userindex = {"username": [], "password": []}
        file = open(userdata,"r")
        data = file.readlines()
        for l in data:
            p = l.split()
            userindex["username"].append(p[0])
            userindex["password"].append(p[1])
        file.close()
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:
                name = msg["name"]
                password = msg["password"]
                print(msg)
                print(userindex)
                if msg["action"] == "login":
                    print("login:", msg)
                    if name in userindex["username"] and userindex["password"][userindex["username"].index(name)] == password:
                        if self.group.is_member(name) != True:
                            #move socket from new clients list to logged clients
                            self.new_clients.remove(sock)
                            #add into the name to sock mapping
                            self.logged_name2sock[name] = sock
                            self.logged_sock2name[sock] = name
                            #load chat history of that user
                            if name not in self.indices.keys():
                                try:
                                    self.indices[name]=pkl.load(open(name+'.idx','rb'))
                                except IOError: #chat index does not exist, then create one
                                    self.indices[name] = indexer.Index(name)
                            print(name + ' logged in')
                            self.group.join(name)
                            mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                            mysend(sock, json.dumps({"action": "freshrank", "rank": self.rank}))
                        else: #a client under this name has already logged in
                            mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                            print(name + ' duplicate login attempt')
                    else:
                        print("failed")
                        mysend(sock, json.dumps({"action":"login", "status":"failed"}))
                elif msg["action"] == "register":
                    file = open(userdata, 'a+')
                    if name in userindex["username"]:
                        mysend(sock, json.dumps({"action": "register", "status": "duplicate"}))
                    else:
                        file.write(f"{name} {password}\n")
                        file.close()
                        mysend(sock, json.dumps({"action": "register", "status": "ok"}))
                    file.close()
                else:
                    print ('wrong code received') 
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
#==============================================================================
# handle connect request
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action":"connect", "status":"self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action":"connect", "status":"success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
                else:
                    msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, msg)
#==============================================================================
# handle messeage exchange: one peer for now. will need multicast later
#==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                #said = msg["from"]+msg["message"]
                said2 = text_proc(msg["message"], from_name)
                print(said2)
                self.indices[from_name].add_msg_and_index(said2)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)
                    mysend(to_sock, json.dumps({"action":"exchange", "from":msg["from"], "message":msg["message"]}))
                    print({"action":"exchange", "from":msg["from"], "message":msg["message"]})
                if msg["gpt"] == True:
                    self.gptres = ""
                    self.gptcontext = msg["context"]
                    self.gpttheguys = the_guys
                    self.gptsaid2 = said2
                    process = threading.Thread(target=self.chattogpt)
                    process.daemon = True
                    process.start()
#==============================================================================
#                 encrpytion model
#==============================================================================
            elif msg["action"]=="input":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action":"generate_key", "from":msg["from"], "to":g, "message":msg["message"]}))
                print(msg)
            elif msg["action"]=="exchange_key":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                to=msg["to"]
                for g in the_guys[1:]:
                    if g==to:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"exchange_key", "from":msg["from"], "to":to, "public_key":msg["public_key"]}))
                print(msg)
            elif msg["action"]=="exchange_encrypted_msg":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                encrypted_msg=msg["encrypted_msg"]
                to=msg["to"]
                for g in the_guys[1:]:
                    if g==to:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"exchange_encrypted_msg", "from":msg["from"], "to":to,"encrypted_msg":encrypted_msg}))
                print(msg)
#==============================================================================
#                 listing available peers
#==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all()
                print(msg)
                mysend(from_sock, json.dumps({"action":"list", "results":msg}))

            elif msg["action"] == "getgroup":
                msg = self.group.list_me(msg["from"])
                mysend(from_sock, json.dumps({"action":"getgroup", "grouplist":msg}))

            elif msg["action"] == "getrank":
                rank = self.rank
                print(rank)
                mysend(from_sock, json.dumps({"action":"getrank", "rank":rank}))
            
            elif msg["action"] == "updaterank":
                print("ok!")
                name = msg["name"]
                score = msg["score"]
                print(name, score)
                if int(self.rank[name]) <= int(score):
                    self.rank[name] = score
                with open("rank.txt", "w") as file:
                    for i in self.rank.keys():
                        file.write(f"{i} {self.rank[i]}\n")
                mysend(from_sock,json.dumps({"action": "updaterank", "results":'ok'}))
                for g in self.all_sockets[1:]:
                    mysend(g, json.dumps({"action": "freshrank", "rank": self.rank}))
            
            elif msg["action"] == "gethistory":
                user = msg["from"]
                msg = self.indices[user].gethistory()
                print(msg)
                mysend(from_sock, json.dumps({"action":"gethistory", "results":msg}))
#==============================================================================
#             retrieve a sonnet
#==============================================================================
            elif msg["action"] == "poem":
                poem_indx = int(msg["target"])
                from_name = self.logged_sock2name[from_sock]
                print(from_name + ' asks for ', poem_indx)
                poem = self.sonnet.get_poem(poem_indx)
                poem = '\n'.join(poem).strip()
                print('here:\n', poem)
                mysend(from_sock, json.dumps({"action":"poem", "results":poem}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))
#==============================================================================
#                 search
#==============================================================================
            elif msg["action"] == "search":
                term = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                print('search for ' + from_name + ' for ' + term)
                # search_rslt = (self.indices[from_name].search(term))
                search_rslt = '\n'.join([x[-1] for x in self.indices[from_name].search(term)])
                print('server side search: ' + search_rslt)
                mysend(from_sock, json.dumps({"action":"search", "results":search_rslt}))
#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action":"disconnect"}))
#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================

        else:
            #client died unexpectedly
            self.logout(from_sock)

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def chattogpt(self):
        print(self.gptcontext)
        self.gptres = gpt_utils.chattoGPT(self.gptcontext)
        # while self.gptres != "":
        #     continue
        print(self.gptres)
        the_guys = self.gpttheguys
        said2 = self.gptsaid2
        for g in the_guys:
            to_sock = self.logged_name2sock[g]
            self.indices[g].add_msg_and_index(said2)
            mysend(to_sock, json.dumps({"action":"exchange", "from":"[GPT]:", "message":self.gptres}))

    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)

def main():
    server=Server()
    server.run()

main()
