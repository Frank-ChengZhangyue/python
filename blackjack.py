# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
player_hand = ""
dealer_hand = ""
new_deck = ""
score = 0
outcome=""
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand=[]

    def __str__(self):
        ans=""
        for j in self.hand:
            ans+= j.suit+j.rank+" "
        return ans
    def add_card(self, card):
        self.hand.append(card)
        return self.hand
    def get_value(self):
        sum=0
        for i in self.hand:
            sum += VALUES.get(i.rank)
        for i in self.hand:
            if i.rank == 'A':
               if sum +10<=21:
                  sum=sum+10
               
        return sum
    def draw(self, canvas, pos):
        for i in self.hand:
            i.draw(canvas,[pos[0]+self.hand.index(i)*80,pos[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[]
        for suit in SUITS:
            for rank in RANKS:
                card= Card(suit,rank)
                self.deck.append(card)
    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()           
                
    def __str__(self):
        ans=""
        for j in self.deck:
            ans+= j.suit+j.rank+" "
        return ans


#define event handlers for buttons
def deal():
    global player_hand,dealer_hand, in_play, new_deck,outcome,score
    if in_play == True:
        outcome="player lost!new deal! hit or stand?"
        score=score-1
    else:
        outcome ="hit or stand?"
    new_deck = Deck()
    new_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    # your code goes here
    print  player_hand, dealer_hand
    in_play = True
    

def hit():
    global  player_hand,dealer_hand,in_play,new_deck,score,outcome
    if in_play == True:
        player_hand.add_card(new_deck.deal_card())
        if player_hand.get_value()>21:
            outcome="You have busted! new deal?"
            print player_hand
            in_play = False
            score=score-1
            print score
        else:
            print player_hand
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player_hand,dealer_hand,in_play,new_deck,score,outcome
    if in_play ==True:
        while dealer_hand.get_value()<17:
            dealer_hand.add_card(new_deck.deal_card())
        if dealer_hand.get_value()>21:
            outcome= "dealer has busted! new deal?"
            print dealer_hand
            score = score+1
            print score
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
             outcome="dealer wins! new deal?"
             print player_hand, dealer_hand
             score = score-1
             print score
             in_play = False
        else:
             outcome= "you win! new deal?"
             print player_hand, dealer_hand
             score = score+1
             print score
             in_play = False
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global player_hand,dealer_hand,in_play,score
    player_hand.draw(canvas,[50,400])
    dealer_hand.draw(canvas,[50,100])
    if in_play == True:
        canvas.draw_image(card_back, [36, 48], CARD_SIZE, [86,148],CARD_SIZE)
    canvas.draw_text(str(player_hand.get_value()),[520,400],30,'brown')
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text(outcome,[20,300],30,'black')
    canvas.draw_text("player",[20,360],30,'black')
    canvas.draw_text("dealer",[20,60],30,'black')
    canvas.draw_text(str(score),[520,60],40,'black')
    if in_play == False:
       canvas.draw_text(str(dealer_hand.get_value()),[520,100],30,'brown')
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric