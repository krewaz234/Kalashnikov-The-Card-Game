import socket
import time
import random

SERVER_PORT = 9090
ID_OFFSET = 45632

#transforms the query to server into list with words
def commandtolist(com):
    l = []
    f = com.find(' ')
    while f != -1:
        l.append(com[:f])
        com = com[f + 1:]
        f = com.find(' ')
    l.append(com)
    return l

#transforms the decimal number into 36-base number (string type)
def decTo36str(number):
    numerals = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num36 = ''
    while number != 0:
        num36 += numerals[number % 36]
        number = number // 36
    return num36

def generateSessionID():
    symbols = '0123456789QWERTYUIOPASDFGHJKLZXCVBNM'
    while True:
        sID = ''
        for i in range(4):
            sID += random.choice(symbols)
        if not sID in SESSIONS.keys():
            return sID

def generateDeck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck

def sortCardsInArm(cards):
    ranks = ['ace', 'king', '4', '7']
    new_cards = []
    useful_cards_ind = []

    for i in range(4):
        if cards[i].rank in ranks:
            new_cards.append(cards[i])
            useful_cards_ind.append(i)

    for i in range(4):
        if not i in useful_cards_ind:
            new_cards.append(cards[i])

    return new_cards

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class Session(object):
    def __init__(self):
        # self.sock.listen(2)
        # self.player1_connection, self.player1_address = self.sock.accept()
        # print("(debug) connected:", self.player1_address)
        # self.player2_connection, self.player2_address = self.sock.accept()
        # print("(debug) connected: ", self.player2_address)
        self.player1_cards = []
        self.player2_cards = []
        self.deck = generateDeck()

        #dealing the cards
        for i in range(4):
            self.player1_cards.append(self.deck[0])
            del self.deck[0]
            self.player2_cards.append(self.deck[0])
            del self.deck[0]

        self.discard_pile1 = []
        self.discard_pile2 = []
        self.shelf = []
        self.turn = 1
        self.isshooting1 = False
        self.isshooting2 = False
        self.player1_points = 0
        self.player2_points = 0

    def discardACard(self, player, card_id):
        if player == 1:
            self.discard_pile1.append(self.player1_cards[card_id])
            del self.player1_cards[card_id]
            self.player1_cards.append(self.deck[0])
            self.player1_cards = sortCardsInArm(player1_cards)
        else:
            self.discard_pile2.append(self.player2_cards[card_id])
            del self.player2_cards[card_id]
            self.player2_cards.append(self.deck[0])
            self.player2_cards = sortCardsInArm(player2_cards)
        del self.deck[0]

SESSIONS = {}

# sock = socket.socket()
# sock.bind(('192.168.0.105', SERVER_PORT))
# sock.listen(1)
# connection, address = sock.accept()
# print("connected:", address)
# while True:
#     data = connection.recv(1024)
#     if data:
#         print(data)
#     #sock.send(byte(data.upper()))
#     time.sleep(.1)
# connection.close()

req_sock = socket.socket()
req_sock.bind(('192.168.0.101', 1024))
while True:
    req_sock.listen(1)
    req_con, req_addr = req_sock.accept()
    print("connected:", req_addr)
    req = str(req_con.recv(1024))[2:-1]
    if req:
        lreq = commandtolist(req)
        if lreq[0] == "CREATE":
            session_id = generateSessionID()
            SESSIONS[session_id] = Session()
            req_con.send(bytes(session_id, encoding='utf-8'))
            print(SESSIONS)
            
        if lreq[0] == "DELETE":
            sID = lreq[1]
            del SESSIONS[sID]
    
    req_con.close()
