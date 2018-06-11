"""This is Blackjack, and welcome to jackass. Also, hi, Python linter."""
from math import floor
from random import randint

class Deck(object):
    """Creates a new deck of cards with its respective methods"""
    suits = ["♥️", "♣️", "♦️", "♠️"]
    def reset_deck(self, amt, deck_type):
        """(re)create the deck and set necessary values"""
        if deck_type == "poker":
            self.cards = list(range(0, amt*52))
            self.cardlist = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        elif deck_type == "skat":
            self.cards = list(range(0, amt*32))
            self.cardlist = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        else:
            raise ValueError("Not a valid deck type: " + deck_type)

    def __init__(self, amt=1, deck_type="poker"):
        self.amt = amt
        self.deck_type = deck_type
        self.reset_deck(amt, deck_type)
    def draw_card(self):
        """removes one 'card' from the list and returns its value"""
        temp_card = self.cards.pop(randint(0, len(self.cards)-1))
        suit = self.suits[floor(temp_card / len(self.cardlist))]
        val = self.cardlist[temp_card % len(self.cardlist)]
        return {"suit": suit, "val": val, "card": suit+val}

#some_deck = Deck()
#print(some_deck.draw_card())

class Hand(object):
    """A place to store cards that have been drawn."""
    cards = []
    def __init__(self, owner="none"):
        self.owner = owner
    def add_card(self, deck):
        """draw a card from the specified deck."""
        self.cards.append(deck.draw_card())
    def rem_card(self, i):
        """remove/play a card from your hand."""
        pass
        #to do

def calc_jack_score(hand):
    """determines the hands blackjack score"""
    score, aces, bust = 0, 0, False
    print(hand.cards)
    for card in hand.cards:
        print(card)
        if card["val"] in ["J", "Q", "K"]:
            score += 10
        elif card["val"] == "A":
            aces += 1
        else:
            score += int(card["val"])
    while aces > 0:
        if score <= 10 and aces < 2: #two aces with 11 would be 22(bust) anyways.
            score += 11
        else:
            score += 1
        aces -= 1
    if score > 21:
        bust = True
    return score, bust

my_hand = Hand("baa")
some_deck = Deck()
for i in range(2):
    my_hand.add_card(some_deck)
print(calc_jack_score(my_hand), my_hand)
