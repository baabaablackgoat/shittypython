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

class Hand(object):
    """A place to store cards that have been drawn."""
    def __init__(self, owner="none"):
        self.owner = owner
        self.cards = []
    def add_card(self, deck):
        """draw a card from the specified deck."""
        self.cards.append(deck.draw_card())

def calc_jack_score(given_hand):
    """Determines the given hands blackjack score"""
    score, aces, bust = 0, 0, False
    for card in given_hand.cards:
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
    return {"score":score, "bust":bust}

def hand_to_string(hand):
    """Turns the hand object into a string of card values."""
    output = ""
    for card in hand.cards:
        output += card["card"] + " "
    return output

def jack_dealer(player_score,dealer_hand,deck):
    """Evaluates the game against a virtual dealer. Requires player score, dealer's deck, and the deck being played."""
    dealer_score = calc_jack_score(dealer_hand)
    while dealer_score["score"] < 18: #Dealer draws on 17 and stays on 18.
        dealer_hand.add_card(deck)
        dealer_score = calc_jack_score(dealer_hand)
    if dealer_score["bust"]:
        print("You win! The dealer went bust with %d (%s)"% (dealer_score["score"],hand_to_string(dealer_hand))) 
    elif player_score["score"] > dealer_score["score"]:
        print("You win! You had a score of %d, whilst the dealer only got to %d (%s)." % (player_score["score"],dealer_score["score"],hand_to_string(dealer_hand)))
    else:
        print("You have lost. The dealer had a score of %d (%s), being equal or better to your %d." % (dealer_score["score"],hand_to_string(dealer_hand),player_score["score"]))

def play_jack():
    """the actual game function"""
    print("_"*20 + "\n")
    print("Welcome to shitty blackjack.")
    print("_"*20 + "\n")
    jack_deck = Deck()
    player_hand = Hand("player")
    dealer_hand = Hand("dealer")
    for _ in range(2): #distribute cards one at a time. Player gets first card.
        player_hand.add_card(jack_deck)
        dealer_hand.add_card(jack_deck)
    player_score = calc_jack_score(player_hand)

    while not player_score["bust"]:
        print("Your current hand: %s (%d)" % (hand_to_string(player_hand), player_score["score"]))
        print("The dealer's hole card is %s." % dealer_hand.cards[0]["card"])
        user = input("Any input/press enter for another card. 'stop', 'no', or 'n' to stay. \n")
        if user.lower() in ["stop", "no", "n"]:
            break
        player_hand.add_card(jack_deck)
        player_score = calc_jack_score(player_hand)

    if player_score["bust"]:
        print("You have lost. You went bust with %s (%d)." % (hand_to_string(player_hand), player_score["score"]))
    else:
        print("You have stopped on %d. (%s)" % (player_score["score"], hand_to_string(player_hand)))
        jack_dealer(player_score,dealer_hand,jack_deck) # Game is handed off to jack_dealer

play_jack()