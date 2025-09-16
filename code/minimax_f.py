import time
import sys
import math
from utility_function import utility
from functions import get_mm_active
from functions import show_board

def minimax(board,used,depth,O_turn,board_size):
    global counter
    counter=0   #pocet prohledanych pozic

    start_time=time.process_time()
    # vytvoreni duplikace pole used a board, ktere budu pouzivat pri minimaxu,
    # nechci posilat reference ale hodnoty
    mm_used=[]
    for i in used:
        row=[]
        for j in i:
            row.append(j)
        mm_used.append(row)
    mm_board=[]
    for i in board:
        row=[]
        for j in i:
            row.append(j)
        mm_board.append(row)
        
    def minimax_valueMIN(mm_board,mm_used,depth,alpha,beta):
        global counter
        counter+=1
        
        util=utility(mm_board,mm_used)
        if depth==0:   #maximalni hloubka dosazena
            return util

        elif abs(util)>=900000:    #konec hry
            #print(util),"utility po tahu hrace MAX")
            return util

        value=math.inf  #infinity
        mm_active=get_mm_active(mm_board,mm_used,board_size)
        for move in mm_active:
            mm_used.append(move)
            mm_board[move[0]][move[1]]="O"     #O je min hrac
            value=min(value,minimax_valueMAX(mm_board,mm_used,depth-1,alpha,beta))
            mm_used.pop()
            mm_board[move[0]][move[1]]="_"
            if value<=alpha:    #pruning
                return value
            beta=min(value,beta)

        #print(value,na_tahu,"valueMIN")
        return value


    def minimax_valueMAX(mm_board,mm_used,depth,alpha,beta):
        global counter
        counter+=1

        util=utility(mm_board,mm_used)
        if depth==0:   #maximalni hloubka dosazena
            return util

        elif abs(util)>=900000:    #konec hry
            #print(util),"utility po tahu hrace MIN")
            return util

        value=-math.inf  #-infinity
        mm_active=get_mm_active(mm_board,mm_used,board_size)
        for move in mm_active:
            mm_used.append(move)
            mm_board[move[0]][move[1]]="X"     #X je max hrac
            value=max(value,minimax_valueMIN(mm_board,mm_used,depth-1,alpha,beta))
            mm_used.pop()
            mm_board[move[0]][move[1]]="_"
            if value>=beta:     #pruning
                return value
            alpha=max(value,alpha)

        #print(value,na_tahu,"valueMIN")
        return value


    def minimax_decisionMIN(mm_board,mm_used,depth,alpha,beta):
        global counter
        counter+=1
        
        if depth==0:   #jen kdyz je error
            print("v decisionu nejde mit hloubku 0")
            sys.exit()

        value=math.inf  #infinity
        mm_active=get_mm_active(mm_board,mm_used,board_size)
        for move in mm_active:
            mm_used.append(move)
            mm_board[move[0]][move[1]]="O"     #O je min hrac
            new_val=minimax_valueMAX(mm_board,mm_used,depth-1,alpha,beta)   
            if value>new_val:    #nasel jsem lepsi tah
                optimal_move=move
                value=new_val
            mm_used.pop()
            mm_board[move[0]][move[1]]="_"


        #print(optimalni_tah,na_tahu)
        return optimal_move

    def minimax_decisionMAX(mm_board,mm_used,depth,alpha,beta):
        global counter
        counter+=1

        if depth==0:   #jen kdyz je error
            print("v decisionu nejde mit hloubku 0")
            sys.exit()

        value=-math.inf  #-infinity
        mm_active=get_mm_active(mm_board,mm_used,board_size)
        for move in mm_active:
            mm_used.append(move)
            mm_board[move[0]][move[1]]="X"     #X je max hrac
            new_val=minimax_valueMIN(mm_board,mm_used,depth-1,alpha,beta)   
            if value<new_val:    #nasel jsem lepsi tah
                optimal_move=move
                value=new_val
            mm_used.pop()
            mm_board[move[0]][move[1]]="_"
        #print(optimalni_tah,na_tahu)
        return optimal_move



    print("nejlepsi tah podle minimaxu s hloubkou",depth,"pro",end=" ")
    if O_turn==True:
        print("O")
        mm_move=minimax_decisionMIN(mm_board,mm_used,depth,-math.inf,math.inf)
        mm_board[mm_move[0]][mm_move[1]]="O"
    else:
        print("X")
        mm_move=minimax_decisionMAX(mm_board,mm_used,depth,-math.inf,math.inf)
        mm_board[mm_move[0]][mm_move[1]]="X"
    #print(mm_move)
    #print("hraci plocha po tahu")
    #show_board(mm_board,15)
        
    print("COUNTER:",counter)
    end_time=time.process_time()
    print("CAS: ","%.5f" % (end_time-start_time))

    return mm_move



def test_minimax_f(depth):
    #minimax-f tests
    boardS=15
    from functions import show_board
    # nacteni pole ze souboru/inputu
    board=[["_" for i in range(boardS+2)] for i in range(boardS+2)]
    for i in range(boardS+2):
        line=input()
        for j in range(boardS+2):
            board[i][j]=line[j]

    used=[] # used se normalne buduje behem hry
    for i in range(1,boardS+1):
        for j in range(1,boardS+1):
            if board[i][j]=="O" or board[i][j]=="X":
                used.append([i,j])

    show_board(board,boardS)
    minimax(board,used,depth,True)

#test_minimax_f(2)   #DEPTH MUSI BYT SUDE DELKY aby neprohral v dalsim tahu #TODO upravit i na liche

# Get-content test.txt | python minimax_f.py
# python minimax.py


# TODO HEURISTIKY
# TODO ohodnotit policka ktere mam proheledat nejdriv aby bylo alfa-beta pruning co nejefektivnejsi (zavisi na poradi)

# TODO vyhra v tomhle kole a v pristim je stjne ohodnocena, ale lepsi je hrat tu drivejsi vyhru, coz minimax lae nedela