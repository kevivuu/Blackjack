import numpy as np
import pandas as pd

class blackjack:
    def __init__(self, no_deck = 1):
        self.no_deck = no_deck
        self.deck = set_deck(no_deck)               # remaining cards (hidden from players)
        self.memo = np.array([], dtype = "int32")    # all cards that are revealed
        self.hand = np.array([], dtype = "int32")      # all cards in one's hand
        self.dealer = np.array([], dtype = "int32")    # all cards in dealer's hand
        self.dhand = np.array([], dtype = 'int32')      # all cards in dealer's hand (players only know 1)
    
    
    """Should I add the dealer's unturned card???"""
    def reveal(self, ind, player = False, reveal = True, dealer = False):
        #player (hand adjusted)
        if player == True:
            card = self.deck[ind]
            self.memo = np.append(self.memo, card)
            self.hand = np.append(self.hand, card)
            self.deck = np.delete(self.deck, ind)
        #revealed dealer
        elif dealer == True and reveal == True:
            card = self.deck[ind]
            self.memo = np.append(self.memo, card)
            self.dealer = np.append(self.dealer, card)
            self.dhand = np.append(self.dealer, card)
            self.deck = np.delete(self.deck, ind)
        #unrevealed dealer
        elif dealer == True and reveal == False:
            card = self.deck[ind]
            self.dhand = np.append(self.dealer, card)
            self.deck = np.delete(self.deck, ind)
        #revealed game
        elif reveal == True:
            card = self.deck[ind]
            self.memo = np.append(self.memo, card)
            self.deck = np.delete(self.deck, ind)
        #unrevealed game
        else:
            card = self.deck[ind]
            self.deck = np.delete(self.deck, ind)
    
            
    def pr_safe(self):
        length = len(self.deck)
        prob = safe(self.hand, length , self.memo)
        return(prob)
    
    def pr_dealer(self, memo, num):
        d = self.dealer[0]
        length = 52 - num * 2 + 1
        #Pr(beat player) with no draw
        mid = sum(self.hand) - d
        if mid >= 10:
            mid = 10
        beat = len(range(mid, 10))
        if beat > 0:
            beat = 16 + (beat - 1) * 4
        reps = np.isin(memo, np.arange(mid, 11))
        reps = sum(reps)
        no_draw = (beat - reps) / length
        if d + 10 < 17 or beat == 0:
            no_draw = 0
        #Pr(beat player) with draw
        draw = 0
        for i in range(1, mid + 1):
            dhand = np.array([d, i])    #dealer's hand for every i
            rep = np.isin(memo, i)
            rep = sum(rep)
            if i != 10:     #pr getting i is (4 - reps)/length (i happens in round 2)
                pr_i = (4 - rep)/length
            else:
                pr_i = (16 - rep)/length   
            memo_i = np.append(self.memo, i)
            low = sum(self.hand) - sum(dhand)
            dlen = len(self.deck) - 1       #take one away for every round drawn
            pr_bs = safe(dhand, dlen, memo_i, low = low)
            pr_draw = pr_i * pr_bs
            draw += pr_draw
        pr_dealer_beat = no_draw + draw
        return(pr_dealer_beat)
        





# Set Deck
def set_deck(n):
    deck = np.array([], dtype = 'int32')
    for i in range(1, 11):
        if i != 10:
            r = np.repeat(i, 4)
            deck = np.hstack((deck, r))
        else:
            r = np.repeat(i, 16)
            deck = np.hstack((deck, r))
    deck = np.repeat(deck, n)
    return(deck)

def safe(hand, dlen, memo, no_deck = 1, low = 1):
        diff = 21 - sum(hand)
        diff = len(range(low, diff + 1))
        reps = np.isin(memo, np.arange(low, diff + 1))
        reps = sum(reps)
        if diff < 10:
            prob = (diff * 4 * no_deck - reps) / dlen
        else:
            prob = 1
        return(prob)
