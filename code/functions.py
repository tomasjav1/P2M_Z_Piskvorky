def show_board_simple(board,board_size):
    # vypise board
    #print(board,"\n")
    for i in range(1,board_size+1):

        for j in range(1,board_size+1):
            print(board[i][j],end="")
        print()
    
def show_board(board,board_size):
    # vypise board s nazvy sloupcu a radku
    #nazvy sloupcu
    print("",end="   ")     # odsazeni kvuli nazvum radku
    for k in range(1,board_size+1):
        if k//10!=0:
            print(k//10,end="")
        else:
            print(" ",end="")
    print("\n",end="   ")     # odsazeni kvuli nazvum radku
    for k in range(1,board_size+1):
        print(k%10,end="")
    print()

    for i in range(1,board_size+1):
        #nazvy radku
        if i<10:
            print("",i,end=" ")
        else:   # dvou-ciferne pojmenovani radku
            print(i,end=" ")
        # pole
        for j in range(1,board_size+1):
            print(board[i][j],end="")
        print()

def check_int(x):   
    # vrati True pokud x je cele cislo
    for digit in x:
        if 48<=ord(digit)<=57:  #ASCII 48-57 je 0-9
            continue
        else:
            return False
    return True

def check_split(inp):
    # vrati True pokud muzu na inp zavolat funkci split() bez erroru 
    # tj. je ve stringu prave jedna (souvisla) mezera
    l=len(inp)
    k=0
    while k<l and inp[k]!=" ":
        k+=1

    if k==l:  #v inp neni mezera
        return False    
    else:   
        while k<l and inp[k]==" ":      #dojdu az na konec mezery
            k+=1
        
        if k==l:  #za koncem mezery neni jinej char
            return False 
        else:
            while k<l and inp[k]!=" ":
                k+=1

            if k==l:  #konec
                return True
            else:   #vize mezer
                return False

def check_input(inp,board_size):    
    # vrati True pokud je validni input 
    # tj. 2 cela cisla oddelene mezerou 
    if check_split(inp)==True:
        x,y=inp.split()
        if check_int(x)==True and check_int(y)==True:
            x,y=int(x),int(y)
            if 1<=x<=board_size and 1<=y<=board_size:
                return True
            else:
                print("Zadane policko je mimo hraci plochu, obe souradnice musi byt mezi 1 a",board_size)
                return False
        else:
            print("Vstup musi byt dvojice celych cisel oddelenych mezerou")
            return False
    else:
        print("Vstup musi byt dvojice celych cisel oddelenych mezerou")
        return False

def add_to_active_neighbour(x,y,active,board):    
    # prozkouma vsechny sousedy x,y a udela je aktivni pokud jsou volne "_"
    delta=[[1,1],[1,0],[1,-1],[0,1],[-1,-1],[-1,0],[-1,1],[0,-1]]
    for step in delta:
        X,Y=x+step[0],y+step[1]
        if board[X][Y]=="_" and [X,Y] not in active:
            active.append([X,Y])

def ran_empry_space(board,board_size):
    #vrati souradnice nahodneho policka
    import random as ran
    x,y=ran.randint(2,board_size-1),ran.randint(2,board_size-1)
    while board[x][y]!="_":
        x,y=ran.randint(2,board_size-1),ran.randint(2,board_size-1)
    return x,y

def ran_empry_space_middle(board,board_size,n):
    #vrati souradnice nahodneho policka ve ctverci kolem sterdu o velikost 2n+1
    import random as ran
    middle=(board_size+1)//2
    x,y=ran.randint(middle-n,middle+n),ran.randint(middle-n,middle+n)
    while board[x][y]!="_":
        x,y=ran.randint(middle-n,middle+n),ran.randint(middle-n,middle+n)
    return x,y

def get_mm_active(mm_board,mm_used,board_size):
    # udela pole aktivnich policek
    mm_active=[]
    if len(mm_used)>0:
        for el in mm_used:
            add_to_active_neighbour(el[0],el[1],mm_active,mm_board)
    else:   #prvni tah minimaxu kde na poli nejsou zadne obsazene policka
        x,y=ran_empry_space_middle(mm_board,board_size,2)
        mm_active.append([x,y])
    return mm_active

def minimmax_make_move(board,used,active,depth,board_size,O_turn):
    # tah minimaxu
    from utility_function import utility
    from minimax_f import minimax
    import sys

    if O_turn==True:
        charR="O"
    else:
        charR="X"

    move=minimax(board,used,depth,O_turn,board_size)
    print(move)
    if board[move[0]][move[1]]=="_":
        board[move[0]][move[1]]=charR
        used.append(move)
        if move in active:
            active.remove(move)
        add_to_active_neighbour(move[0],move[1],active,board)
        print("AKTIVNI POLICKA:",len(active))
        score=utility(board,used)
        print("SCORE:",score)
        print()
        if abs(score)>=900000:   # konec
                show_board(board,board_size)
                print()
                print("======")
                print(charR,"wins")
                print("======")
                sys.exit()
        show_board(board,board_size)
    else:
        print("minimax se snazi tahnout na obsazene policko")
        print("tah",move[0],move[1])
        print("char tam kam chce hrat",board[move[0]][move[1]])

def get_player_input(inp,board_size,board):
    # dostane souradnice pole dokud hrac nezada spravne vstup
    while check_input(inp,board_size)!=True:
        inp=input()
    x,y=inp.split()
    x,y=int(x),int(y)
    if board[x][y]=="_":
        return x,y
    else:
        get_player_input(input(),board_size,board)

def player_make_move(board,used,active,board_size,O_turn,inp):
    # tah hrace
    from utility_function import utility
    import sys

    if O_turn==True:
        charR="O"
    else:
        charR="X"

    x,y=get_player_input(inp,board_size,board)

    used.append([x,y])
    board[x][y]=charR
    if [x,y] in active:
        active.remove([x,y])
    add_to_active_neighbour(x,y,active,board)
    print("AKTIVNI POLICKA:",len(active))
    score=utility(board,used)
    print("SCORE:",score)
    print()
    if abs(score)>=900000:   # konec
        show_board(board,board_size)
        print()
        print("======")
        print(charR,"wins")
        print("======")
        sys.exit()
    show_board(board,board_size)
     
def switch_turn(O_turn):
    if O_turn==False:
        return True
    else:
        return False
    
def print_char(O_turn):
    if O_turn==True:
        print("O")
    else:
        print("X")