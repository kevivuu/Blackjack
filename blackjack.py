import numpy as np
import pandas as pd
from bjalgo import blackjack
import time

#Choose Reveal or Unreveal
while True:
    r = input("Do you want to reveal your opponents' cards? (Y/N) ")
    if r.lower() == "y":
        rev = True
        break
    elif r.lower() == "n":
        rev = False
        break
    else:
        print("Invalid response")


#Set number of players
while True:
    try:
        num = int(input("Number of players: "))
        if 0 < num <= 10:
            break
        elif num > 10:
            print("Too many players (10 max)")
        else:
            print("Invalid response")
    except ValueError:
        print("Invalid reponse")

#Dataframe for players and dealers
players = [f"Player {i}" for i in range(1, num + 1)]
cols = players + ["Dealer"]
df = pd.DataFrame('', index = range(5), columns = cols).astype(object)


#Randomly select turn + index
turn = np.random.choice(players, 1)[0]
tind = players.index(turn)

#Object
table = []
for i in range(num):
    table.append(blackjack())

#Round 1 and 2
for r in range(2):
    for p in range(num+1):
        #Reveal dealer first card
        if p == num and r == 0:
            ind = np.random.choice(range(len(table[tind].deck)), 1)[0]
            for i in range(num):
                table[i].reveal(ind, dealer = True)
            df["Dealer"].loc[r] = table[tind].memo[-1]
            # print(df, end = '\r')
            # time.sleep(1)
        #Unreveal dealer second card
        elif p == num and r == 1:
            ind = np.random.choice(range(len(table[tind].deck)), 1)[0]
            for i in range(num):
                table[i].reveal(ind, reveal = False)
            df["Dealer"].loc[r] = np.nan
            # print(df, end = '\r')
        else:
            for j in range(num):
                #Player with hand
                if p == j:
                    ind = np.random.choice(range(len(table[j].deck)), 1)[0]
                    table[j].reveal(ind, player = True)
                    others = list(range(num))
                    others.pop(j)
                    for i in others:
                        if rev == True:
                            table[i].reveal(ind)
                        else:
                            table[i].reveal(ind, reveal = False)
                    if j == tind or rev == True:
                        df[players[j]].loc[r] = table[j].memo[-1]
                        # print(df, end = '\r')
                        # time.sleep(1)
                    else:
                        df[players[j]].loc[r] = np.nan
                        # print(df, end = '\r')
                        # time.sleep(1)
           
print(players[tind]) 

memo = table[tind].memo

# print(df)
# for i in range(num):
#     a = table[i].pr_safe()
#     print(f'Pr safe: {a}')
#     b = table[i].pr_dealer(memo, num)
#     print(f'Pr dealer: {b}')

#Drawing round
for p in range(num):
    for j in range(num):
        if p == j:
            #Max 3 draws
            for r in range(2, 5):
                safe = table[j].pr_safe()
                dealt = table[j].pr_dealer(memo, num)
                #Natural blackjack
                if sum(table[j].hand) == 11 and any(np.isin(table[j].hand, 1)) == True and len(table[j].hand) == 2:
                    pass
                #Draw if value below 17
                elif sum(table[j].hand) < 17:
                    ind = np.random.choice(range(len(table[j].deck)), 1)[0]
                    table[j].reveal(ind, player = True)
                    others = list(range(num))
                    others.pop(j)
                    for o in others:
                        if rev == True:
                            table[o].reveal(ind)
                        else:
                            table[o].reveal(ind, reveal = False)
                    if j == tind or rev == True:
                        df[players[j]].loc[r] = table[j].memo[-1]
                    else:
                        df[players[j]].loc[r] = np.nan
                    pass
                #Draw if value below 17
                elif safe < dealt:
                    ind = np.random.choice(range(len(table[j].deck)), 1)[0]
                    table[j].reveal(ind, player = True)
                    others = list(range(num))
                    others.pop(j)
                    for o in others:
                        if rev == True:
                            table[o].reveal(ind)
                        else:
                            table[o].reveal(ind, reveal = False)
                    if j == tind or rev == True:
                        df[players[j]].loc[r] = table[j].memo[-1]
                    else:
                        df[players[j]].loc[r] = np.nan
                    pass
                #Stop drawing
                else:
                    pass


print(df)
# for i in range(num):
#     # print(players[i])
#     print(table[i].hand)
    # print(table[i].memo)
    # a = table[i].pr_safe()
    # print(a)
    
