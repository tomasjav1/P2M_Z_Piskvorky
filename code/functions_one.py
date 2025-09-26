#soubor (nesouvisejicich) funkci pouzitych napric projektem
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
    if x==None or x=="":
        return False
    for digit in x:
        if 48<=ord(digit)<=57:  #ASCII 48-57 je 0-9
            continue
        else:
            #neni cislice
            return False
    #x je cele nezaporne cislo
    return True

def check_split(inp):
    # vrati True pokud muzu na inp zavolat funkci split() bez erroru 
    # tj. je ve stringu prave jedna (souvisla) mezera
    if inp==None or inp=="":
        return False
    elif  inp[0]==" ":
        return False
    
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
    # vrati True pokud je input validni souradnice na hraci plose
    # tj. 2 cela nezaporna cisla oddelene mezerou meti 1 a board_size
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

def get_list_add_to_active_neighbour(x,y,mm_active,mm_board):   
    l=[] 
    # prozkouma vsechny sousedy x,y a udela list policek ktere se maji pridat do aktivnich
    delta=[[1,1],[1,0],[1,-1],[0,1],[-1,-1],[-1,0],[-1,1],[0,-1]]
    for step in delta:
        X,Y=x+step[0],y+step[1]
        if mm_board[X][Y]=="_" and [X,Y] not in mm_active:
            l.append([X,Y])
    return l

def ran_empry_space(board,board_size): 
    #vrati souradnice nahodneho policka
    from random import randint
    x,y=randint(2,board_size-1),randint(2,board_size-1)
    while board[x][y]!="_":
        x,y=randint(2,board_size-1),randint(2,board_size-1)
    return x,y

def ran_empry_space_middle(board,board_size,n):
    #vrati souradnice nahodneho policka ve ctverci kolem sterdu o velikost 2n+1
    from random import randint
    middle=(board_size+1)//2
    x,y=randint(middle-n,middle+n),randint(middle-n,middle+n)
    while board[x][y]!="_":
        x,y=randint(middle-n,middle+n),randint(middle-n,middle+n)
    return x,y

def get_mm_active(mm_board,mm_used,board_size):
    # udela pole aktivnich policek
    mm_active=[]
    if len(mm_used)>0:
        for el in mm_used:
            add_to_active_neighbour(el[0],el[1],mm_active,mm_board)
    else:   #prvni tah minimaxu kde na poli nejsou zadne obsazene policka -> vygeneruj nahodne uprostred
        x,y=ran_empry_space_middle(mm_board,board_size,2)
        mm_active.append([x,y])
    return mm_active

def get_used(board,board_size):
    #vyrobi a vrati pole used za pomoci hraci plochy
    from constants import char1, char2
    used=[]
    for i in range(1,board_size+1):
        for j in range(1,board_size+1):
            if board[i][j]==char1 or board[i][j]==char2:
                used.append([i,j])
    return used

def minimmax_make_move(board,used,active,depth,board_size,char1_turn):
    # udela tah minimaxu pro daneho hrace z danou hloubkou
    # vcetne pridani policka do pouzitych, jeho sousedu do aktivnich (kteri tam jiz nejsou)
    # vytiskne pole po tahu,...

    # tah minimaxu
    from utility_function import utility
    from constants import terminal_score
    from minimax_f import minimax
    
    #charR je na tahu
    charR=return_char(char1_turn)

    move=minimax(board,used,depth,char1_turn,board_size)    #optimalni tah podle minimaxu
    print("TAH MINIMAXU:",move)
    if board[move[0]][move[1]]=="_":
        board[move[0]][move[1]]=charR
        used.append(move)
        if move in active:
            active.remove(move)
        add_to_active_neighbour(move[0],move[1],active,board)
        #print("AKTIVNI POLICKA:",len(active))
        score=utility(board,used)
        print("SCORE:",score)
        print()
        if abs(score)>=terminal_score:   # VYHRA, muze vyhrat jen ten co je na tahu       <--o
            #score>=terminal_score -> vyhral char2, score<=terminal_score -> vyhral char1  __/
            victory(charR,board,board_size)     #vypise pole a ukokci hru
        show_board(board,board_size)    #vytiskne pole
    else:   #Houstone mame problem 
        print("minimax se snazi tahnout na obsazene policko")
        print("tah",move[0],move[1])
        print("char tam kam chce hrat",board[move[0]][move[1]])

def get_player_input(inp,board_size,board):
    # dostane souradnice pole dokud hrac nezada spravne vstup
    #tj. 2 cela kaldna cisla oddelena mezerou mezi 1 a board_size a na toto policko je jeste navic volne
    while check_input(inp,board_size)!=True:    #kontola validnich souradnic na hraci plose
        inp=input("")
    x,y=inp.split()
    x,y=int(x),int(y)
    if board[x][y]=="_":    #kontrola volnosti
        return x,y
    else:   #policko je obsazene, nevadi, hrac zkusi znova
        x,y=get_player_input(input(""),board_size,board)
        return x,y

def player_make_move(board,used,active,board_size,char1_turn,inp):
    # udela tah daneho hrace
    # vcetne pridani policka do pouzitych, jeho sousedu do aktivnich (kteri tam jiz nejsou)
    # vytiskne pole po tahu,...

    # tah hrace
    from utility_function import utility
    from constants import terminal_score

    #charR je na tahu
    charR=return_char(char1_turn)

    x,y=get_player_input(inp,board_size,board)  #tah hrace

    board[x][y]=charR   
    used.append([x,y])  # pole x,y je nyni obsazene
    if [x,y] in active:     #pole x,y uz neni aktivni (pokud bylo)
        active.remove([x,y])
    add_to_active_neighbour(x,y,active,board)
    #print("AKTIVNI POLICKA:",len(active))
    score=utility(board,used)
    print("SCORE:",score)
    print()
    if abs(score)>=terminal_score:   # VYHRA, muze vyhrat jen ten, co je na tahu       <--o
        #score>=terminal_score -> vyhral char2, score<=terminal_score -> vyhral char1   __/
        victory(charR,board,board_size)     #vypise pole a ukoci hru
    show_board(board,board_size)    #vypise pole
     
def switch_turn(char1_turn):
    # prohodni True na False a naopak
    if char1_turn==False:
        return True
    else:
        return False
    
def print_char(char1_turn):
    #vytiskne toho, kdo je na tahu
    if char1_turn==True:
        from constants import char1
        print(char1)
    else:
        from constants import char2
        print(char2)

def return_char_Op(char1_turn):
    #vrati toho, kdo NENI na tahu
    if char1_turn==True:
        from constants import char2
        return char2
    else:
        from constants import char1
        return char1
    
def return_char(char1_turn):
    #vrati toho, kdo JE na tahu
    if char1_turn==False:
        from constants import char2
        return char2
    else:
        from constants import char1
        return char1
    
def victory(charR,board,board_size):
    # vypise hraci pole a ukonci hru
    show_board(board,board_size)
    print()
    print("==================")
    print("    ",charR,"wins")
    print("==================")
    from sys import exit
    exit()  #ukonceni programu
