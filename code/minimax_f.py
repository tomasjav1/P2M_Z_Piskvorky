# import funkci a konstant
from sys import exit
from math import inf
from time import process_time
from utility_function import utility
from functions_one import get_mm_active, show_board
from constants import terminal_score, char1, char2, board_size

global counter  #pocitadlo prohledanych pozic
counter=0

def minimax_valueMIN(mm_board,mm_used,depth,alpha,beta):
    #vrati hodnotu kterou ziskam optimalni tahem Min hracem, nasledovanou optimalnim tahem MAX hrace atd... 
    # dokud se nedostanu na hloubku 0
    #char1 je min hrac
    
    global counter
    counter+=1
    util=utility(mm_board,mm_used)  #skore
    if depth==0:   #maximalni hloubka dosazena
        return util
    elif abs(util)>=terminal_score:    #konec hry ->vyhra (hrace MAX)
        return util
    value=inf  #infinity
    mm_active=get_mm_active(mm_board,mm_used,board_size)    #aktivni policka
    for move in mm_active:  
        #pro vsechny tahy z aktivnich polickek, ziskej nejlepsi hodnotu z tahu pro Max hrace a z toho udejej min
        mm_used.append(move)    #pridani tahu do pouzitych
        mm_board[move[0]][move[1]]=char1    #tah
        value=min(value,minimax_valueMAX(mm_board,mm_used,depth-1,alpha,beta))
        mm_used.pop()   #odebrani tahu z puzitych
        mm_board[move[0]][move[1]]="_"  #odebrani tahu
        if value<=alpha:    #pruning
            return value
        beta=min(value,beta)
    return value

def minimax_valueMAX(mm_board,mm_used,depth,alpha,beta):
    #vrati hodnotu kterou ziskam optimalni tahem MAAX hracem, nasledovanou optimalnim tahem MIN hrace atd... 
    # dokud se nedostanu na hloubku 0
    #char2 je max hrac
    global counter
    counter+=1
    util=utility(mm_board,mm_used)
    if depth==0:   #maximalni hloubka dosazena
        return util
    elif abs(util)>=terminal_score:    #konec hry ->vyhra (hrace MIN)
        #print(util),"utility po tahu hrace MIN")
        return util
    value=-inf  #-infinity
    mm_active=get_mm_active(mm_board,mm_used,board_size)
    for move in mm_active:
        #pro vsechny tahy z aktivnich polickek, ziskej nejlepsi hodnotu z tahu pro Min hrace a z toho udejej max
        mm_used.append(move)    #pridani tahu do pouzitych
        mm_board[move[0]][move[1]]=char2    #tah
        value=max(value,minimax_valueMIN(mm_board,mm_used,depth-1,alpha,beta))
        mm_used.pop()   #odebrani tahu z pouzitych
        mm_board[move[0]][move[1]]="_"  #odebrani tahu
        if value>=beta:     #pruning
            return value
        alpha=max(value,alpha)
    return value

def minimax_decisionMIN(mm_board,mm_used,depth,alpha,beta):
    #vrati optimalni tah pro Min hrace 
    #char1 je min hrac
    global counter
    counter+=1
    if depth==0:   #jen kdyz je error
        print("v decisionu nejde mit hloubku 0")
        exit()
    value=inf  #infinity
    mm_active=get_mm_active(mm_board,mm_used,board_size)    #aktivni policka
    for move in mm_active: 
        #pro vsechny tahy z aktivnich polickek, ziskej nejlepsi tah pro Min hrace 
        mm_used.append(move)    #pridani tahu do pouzitych
        mm_board[move[0]][move[1]]=char1  #tah  
        new_val=minimax_valueMAX(mm_board,mm_used,depth-1,alpha,beta)   
        if value>new_val:       #nasel jsem lepsi tah
            optimal_move=move   #zapamatovani (dosud) nejlepsiho tahu
            value=new_val       #zapamatovani (dosud) nejlepsi hodnoty
        mm_used.pop()   #odebrani tahu z pouzitych
        mm_board[move[0]][move[1]]="_"  #odebrani tahu
    #na konci dosud nejlepsi je opravdu nejlepsi
    return optimal_move

def minimax_decisionMAX(mm_board,mm_used,depth,alpha,beta):
    #vrati optimalni tah pro Max hrace
    #char2 je max hrac
    global counter
    counter+=1
    if depth==0:   #jen kdyz je error
        print("v decisionu nejde mit hloubku 0")
        exit()
    value=-inf  #-infinity
    mm_active=get_mm_active(mm_board,mm_used,board_size)    #aktivni policka
    for move in mm_active:
        #pro vsechny tahy z aktivnich polickek, ziskej nejlepsi tah pro Max hrace
        mm_used.append(move)    #pridani tahu do pouzitych
        mm_board[move[0]][move[1]]=char2     #pridani tahu
        new_val=minimax_valueMIN(mm_board,mm_used,depth-1,alpha,beta)   
        if value<new_val:    #nasel jsem lepsi tah
            optimal_move=move   #zapamatovani (dosud) nejlepsiho tahu
            value=new_val       #zapamatovani (dosud) nejlepsi hodnoty
        mm_used.pop()   #odebrani tahu z pouzitych
        mm_board[move[0]][move[1]]="_"  #odebrani tahu
    #na konci dosud nejlepsi je opravdu nejlepsi
    return optimal_move

def minimax(board,used,depth,char1_turn,board_size):
    global counter
    counter=0   #pocet prohledanych pozic

    start_time=process_time()   #cas startu

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
        
    print("nejlepsi tah podle minimaxu pro",end=" ")
    if char1_turn==True:
        print(char1)    
        mm_move=minimax_decisionMIN(mm_board,mm_used,depth,-inf,inf)  #char1 je Min hrac
        mm_board[mm_move[0]][mm_move[1]]=char1
    else:
        print(char2)
        mm_move=minimax_decisionMAX(mm_board,mm_used,depth,-inf,inf) #char2 je Max hrac
        mm_board[mm_move[0]][mm_move[1]]=char2
    #print(mm_move)
 
    #print("COUNTER:",counter)
    end_time=process_time() #cas konce
    #print("CAS: ","%.5f" % (end_time-start_time))  #uplynuly tah

    return mm_move  #vrati nejlepsi tah

# Get-content test.txt | python minimax_f.py
# python minimax.py

# TODO HEURISTIKY
# TODO ohodnotit policka ktere mam proheledat nejdriv aby bylo alfa-beta pruning co nejefektivnejsi (zavisi na poradi)

# TODO vyhra v tomhle kole a v pristim je stjne ohodnocena, ale lepsi je hrat tu drivejsi vyhru, coz minimax lae nedela