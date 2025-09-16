import random as ran
from functions import show_board
from functions import check_input
#from functions import ran_empry_space
from functions import ran_empry_space_middle
from functions import add_to_active_neighbour

board_size=15       # 9<  <100, idealne liche
board=[["_" for i in range(board_size+2)] for i in range(board_size+2)]         
for i in range(board_size+2):   #hraci pole cislovane on 1 do board_size s okrajem #
    board[0][i]="#"
    board[i][0]="#"
    board[board_size+1][i]="#"
    board[i][board_size+1]="#"
#  _ empty space
#  # obstacle
#  X cross
#  O nought

used=[]     # obsazena policka O nebo X
active=[]   # neobsazene (tj. je na nich "_") policka ktera soudeni s obsazenimy


# 1.radek
print("Chcete hrat s prekazkami? '1' pro Ano, '0'  pro Ne")
if int(input())==1:
    for i in range(board_size//2):
        x,y=ran.randint(2,board_size-1),ran.randint(2,board_size-1)
        board[x][y]="#"
    print("Zde jsou nahodne vygenerovane prekazky:")
    show_board(board,board_size)
    obstacles=True
else:
   obstacles=False 


#2.radek
print("Chcete zacinat? '1' pro Ano, '0' pro Ne")
if int(input())==1:
    player_starts=True
else:
    player_starts=False


#3.radek
print("Jake chcete uvodni rozlozeni krouzku/krizku? '1' pro 3 nahodne (z toho ma pouze jednu zacinajici hrac), '0' pro zadne, '-1' pro vlastni")

inp3=int(input())
if inp3==1:  #nahodne
    x,y=ran_empry_space_middle(board,board_size,3)
    board[x][y]="O"
    used.append([x,y])
    add_to_active_neighbour(x,y,active,board)
    x,y=ran_empry_space_middle(board,board_size,3)
    board[x][y]="X"
    used.append([x,y])
    add_to_active_neighbour(x,y,active,board)
    x,y=ran_empry_space_middle(board,board_size,3)
    if player_starts==False:
        board[x][y]="O"
    else:
        board[x][y]="X"
    used.append([x,y])
    add_to_active_neighbour(x,y,active,board)

elif inp3==-1:   #vlastni
    #noughts O
    print("Zadejte souradnice kolecek 'O' oddelenych mezerou, zadejte '-1' pro ukonceni ")
    inp=input()
    while inp!="-1":
        if check_input(inp,board_size)==True:
           x,y=inp.split()
           x,y=int(x),int(y)
           if board[x][y]=="_":
               board[x][y]="O"
               used.append([x,y])
               add_to_active_neighbour(x,y,active,board)
           else:
               print("Uvedene policko je jiz obsazene, vyberte jine")
               show_board(board,board_size)
        else:
            print("Zadejte souradnice kolecek 'O' tj. dve cela cisla oddelenych mezerou")
        inp=input()
    #crosses X
    print("Zadejte souradnice krizku 'X' oddelenych mezerou, zadejte '-1' pro ukonceni ")
    inp=input()
    while inp!="-1":
        if check_input(inp,board_size)==True:
           x,y=inp.split()
           x,y=int(x),int(y)
           if board[x][y]=="_":
               board[x][y]="X"
               used.append([x,y])
               add_to_active_neighbour(x,y,active,board)
           else:
               print("Uvedene policko je jiz obsazene, vyberte jine")
               show_board(board,board_size)
        else:
            print("Zadejte souradnice kolecek 'X' tj. dve cela cisla oddelenych mezerou")
        inp=input()

#else: #prazdne startovni pole



print("=================")
print("Uvodni hraci pole")
print("=================")
show_board(board,board_size)
