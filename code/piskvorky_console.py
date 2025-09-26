#import funkci a konstant
from board_setup import board_s
board, used, active, char1_turn = board_s()
from functions_one import minimmax_make_move, player_make_move, switch_turn, print_char
from constants import terminal_score, board_size, char1
from time import sleep
from sys import exit

print("\nGAME STARTS \n")

#SAM PROTI SOBE
def duo(char1_turn): 
    print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je ",end="")
    print_char(char1_turn)

    inp=input()
    while inp!="-1":    # ukonceni programu
        player_make_move(board,used,active,board_size,char1_turn,inp) # tah hrace
        char1_turn=switch_turn(char1_turn)      #prohozeni hrace

        print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je ",end="")
        print_char(char1_turn)

        inp=input()
#duo(char1_turn)

#PROTI POCITACI
def solo(char1_turn):
    if char1_turn==False:   #zacina pocitac
        # tah minimaxu
        minimmax_make_move(board,used,active,2,board_size,char1_turn)
        char1_turn=True

        
    print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je",char1)
    inp=input()
    while inp!="-1":
        # tah hrace
        player_make_move(board,used,active,board_size,char1_turn,inp)
        char1_turn=switch_turn(char1_turn)

        #delay 0.3s
        #time.sleep(0.3)
        
        # tah minimaxu
        minimmax_make_move(board,used,active,2,board_size,char1_turn)
        char1_turn=switch_turn(char1_turn)

        #input hrace
        print("Zadejte souradnice dalsiho tahu: radek mezera sloupec. Na tahu je",char1)
        inp=input()
solo(char1_turn)

# POCITAC PROTI POCITACI
def nono(char1_turn):
    score=0
    while abs(score)<terminal_score:
        # tah minimaxu 
        minimmax_make_move(board,used,active,2,board_size,char1_turn)   #tah minimaxu
        char1_turn=switch_turn(char1_turn)  #prohozeni tahu

        #delay 
        sleep(0.1)
#nono(char1_turn)


# python piskvorky_console.py
# Get-content input.txt | python piskvorky_console.py

