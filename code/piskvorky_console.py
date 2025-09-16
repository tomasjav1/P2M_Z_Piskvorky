import board_setup  #zaroven ho spusti
from board_setup import player_starts
O_turn=player_starts
from board_setup import board_size
from board_setup import board
from board_setup import used
from board_setup import active
from functions import minimmax_make_move
from functions import player_make_move
from functions import switch_turn
from functions import print_char
import time
import sys

print("\nGAME STARTS \n")

#SAM PROTI SOBE
def duo(O_turn): 
    print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je ",end="")
    print_char(O_turn)

    inp=input()
    while inp!="-1":
        player_make_move(board,used,active,board_size,O_turn,inp)
        O_turn=switch_turn(O_turn)


        print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je ",end="")
        print_char(O_turn)

        inp=input()
#duo(O_turn)

#PROTI POCITACI
def solo(O_turn):
    if O_turn==False:   #zacina pocitac
        # tah minimaxu
        minimmax_make_move(board,used,active,2,board_size,O_turn)
        O_turn=True

        
    print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je O")
    inp=input()
    while inp!="-1":
        # tah hrace
        player_make_move(board,used,active,board_size,O_turn,inp)
        O_turn=switch_turn(O_turn)

        #delay 0.3s
        #time.sleep(0.3)
        
        # tah minimaxu
        minimmax_make_move(board,used,active,2,board_size,O_turn)
        O_turn=switch_turn(O_turn)

        #input hrace
        print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je O")
        inp=input()
solo(O_turn)

# POCITAC PROTI POCITACI
def nono(O_turn):
    score=0
    while abs(score)<900000:
        # tah minimaxu 
        minimmax_make_move(board,used,active,2,board_size,O_turn)
        O_turn=switch_turn(O_turn)

        #delay 
        time.sleep(1)
#nono(O_turn)


# python piskvorky_console.py
# Get-content input.txt | python piskvorky_console.py

