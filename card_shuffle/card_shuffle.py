import numpy as np
import matplotlib.pyplot as plt

# Program to shuffle cards as a human might

# Acient proverb if you shuffle 7 times the cards are completely randomized

# Here we think of how a human shuffles cards.

# Step 1 split the deck in two not always perfect decks
# they miss getting split halveway in two by a few cards each time.
# we call it guassian with a std devation of a few cards

# Step 2 shuffle the cards: the cards are suffeled by inter-dispersing
# a few (1-5ish) cards at at time. call this a poisson process with
# a small lambda

# Step 3 once one half of the deck is exahusted the rest of the cards
# go on top

# Interesing thought does it always have to be one card
# is zero and option?
# I think it is possilbe for a chuck of cards from the right stack
# to fall and the no cards from the left stack and then a chuck of
# cards from the right stack to fall again so zero is a possibility

#----two changeable paramters-----

sig = 2 #how good are you at cutting the deck in half bigger is worse
lamb = 2 #how good are you at interdispersing cards biger is worse

#being worse at splitting the deck might actually be better?

#question how best to measure randomness?

def shuffle(cards, split_sigma, shuffle_lambda):
    # split the deck
    left_half_num = np.int(52/2+np.round(np.random.normal(0,split_sigma))) # center at 0 cards
    left_half_num_start = left_half_num
    right_half_num = 52 - left_half_num
    left_deck = cards[0:left_half_num]
    right_deck = cards[left_half_num:]
    shuffled_cards = []
    # first card comes from the left or right deck?
    start_left = np.random.randint(0,2)
    i = 0 +start_left
    shuffling = True
    while shuffling:
        n_cards = np.random.poisson(shuffle_lambda)
        print(i,left_half_num,right_half_num,len(shuffled_cards),n_cards)
        if np.mod(i,2) == 0:
            left_half_num = left_half_num -n_cards
            if n_cards >0:
                shuffled_cards = np.append(shuffled_cards,left_deck[0:n_cards]) #add cards to new deck from left
                left_deck = np.delete(left_deck,range(0,n_cards))  #remove cards from left deck        
        else:
            right_half_num = right_half_num - n_cards
            if n_cards >0: 
                shuffled_cards = np.append(shuffled_cards,right_deck[0:n_cards]) #add cards to new deck from right
                right_deck = np.delete(right_deck,range(0,n_cards))  #remove cards from right deck

        if left_half_num <=0: #finished
            shuffling = False
            shuffled_cards = np.append(shuffled_cards,right_deck[0:]) #grab all of remaining cards in right
        if right_half_num <=0: #finished
            shuffling = False
            shuffled_cards = np.append(shuffled_cards,left_deck[0:]) #grab all of remaining cards in left
            
        i = i+1

    return shuffled_cards,left_half_num_start,i-start_left

cards = np.arange(0,52)
shuffled_cards = cards

left_deck_nums = []
number_of_chuncks = []

plt.figure(1,figsize = (19,10))
plt.suptitle("10 shuffles: sigma = "+str(sig)+", lambda = "+str(lamb))

for i in range(0,10):
    print(i)
    plt.subplot(3,5,(i+1))
    shuffled_cards,left_deck_num,chunck_num = shuffle(shuffled_cards,sig,lamb)
    left_deck_nums = np.append(left_deck_nums,left_deck_num)
    number_of_chuncks = np.append(number_of_chuncks,chunck_num)
    
    plt.plot(range(0,52),range(0,52),"o",label = "orginal distribution",mec = "k")
    #new index derived using argsort
    plt.plot(range(0,52),np.argsort(shuffled_cards),"o",label = "new distribution " +str(i+1)+" shuffles",mec = "k")
    plt.plot(range(0,52)[0],np.argsort(shuffled_cards)[0],"+")
    plt.xlabel("original card index")
    plt.ylabel("new card index")
    plt.ylim(0,70)
    plt.legend()

plt.subplot(3,1,3)
bar_width = 0.25
plt.bar(np.arange(1,11)-bar_width/2,left_deck_nums,bar_width,label  = "left deck size")
plt.bar(np.arange(1,11)+bar_width/2,52-left_deck_nums,bar_width,label  = "right deck size")
plt.bar(np.arange(1,11)+3*bar_width/2+0.05,number_of_chuncks,bar_width,label  = "number of card chunks",alpha = 0.5)

plt.xlabel("Shuffle number")
plt.legend()
plt.xlim(0.5,12.5)
plt.xticks(np.arange(1,11))

plt.savefig("Human_card_shuffle.pdf")
    
plt.show()
