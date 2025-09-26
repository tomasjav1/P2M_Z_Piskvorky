# import funkci a konstant
from functions_one import show_board, check_input, ran_empry_space_middle,ran_empry_space, add_to_active_neighbour
from constants import board_size, char1, char2

def board_s():
    # vytvoreni hraciho pole, ktere je cislovane on 1 do board_size s okrajem #
    # na hracim poli najdeme pouze 4-charaktery:
    #  _ prazne pole, # prekazku, char1, char2
    board=[["_" for i in range(board_size+2)] for i in range(board_size+2)]
    # hraci pole je cislovane jako matice (jen zacinam od 0):
    # board[0][0]   board[0][1]   board[0][2] ...
    # board[1][0]   board[1][1]   board[1][2] ...
    # board[2][0]   board[2][1]   board[2][2] ...
    #     .             .             .     .
    #     .             .             .        .
    for i in range(board_size+2):   #tvorba okraju #
        board[0][i]="#" #prvni radek
        board[i][0]="#" #prcni sloupec
        board[board_size+1][i]="#" #posledni radek
        board[i][board_size+1]="#" #posleni sloupec

    used=[]     # obsazena policka tj. policka s char1 nebo char2
    active=[]   # volna (tj. je na nich "_") policka ktera soudeni s obsazenimy


    # 1.radek INPUTU        Chcete hrat s prekazkami?
    print("Chcete hrat s prekazkami? '1' pro Ano, '0'  pro Ne")
    inp1=input("")
    if inp1=="1":
        # nahodne vygenerovani prekazek
        from random import randint
        for i in range(board_size//2):
            x,y=randint(2,board_size-1),randint(2,board_size-1)
            board[x][y]="#"
        print("Zde jsou nahodne vygenerovane prekazky:")
        show_board(board,board_size)

 
    #2.radek INPUTU     Chcete zacinat?
    #hrac hraje za char1
    print("Chcete zacinat? '1' pro Ano, '0' pro Ne")
    inp2=input("")
    if inp2=="1":
        char1_turn=True #char1 zacina
    else:
        char1_turn=False #char2 zacina


    #3.radek INPUTU     Jake chcete uvodni rozlozeni?
    print("Jake chcete uvodni rozlozeni ",char1,"/",char2,"? '1' pro 3 nahodne (z toho ma pouze jednu zacinajici hrac), '0' pro zadne, '-1' pro vlastni")
    inp3=input("")

    if inp3=="1":  #nahodne kde nezacinaji-ci dostane 2 pole a zacinajici pouze jedno
        x,y=ran_empry_space_middle(board,board_size,3)  #nahodne souradnice volneho pole +-uprostred
        board[x][y]=char1   
        used.append([x,y])  #pridame pole do obsazenych
        add_to_active_neighbour(x,y,active,board) #pridame volne sousedy pole do aktivnich

        x,y=ran_empry_space_middle(board,board_size,3)  #nahodne souradnice volneho pole +-uprostred
        board[x][y]=char2
        used.append([x,y])  #pridame pole do obsazenych
        add_to_active_neighbour(x,y,active,board)   #pridame volne sousedy pole do aktivnich
        if [x,y] in active:  #x,y uz neni vone tim padem ho neni aktivni
            active.remove([x,y])

        x,y=ran_empry_space_middle(board,board_size,3)  #nahodne souradnice volneho pole +-uprostred
        #podle toh kdo zacina tak tomu dam treti pole bud char1 nebo char2
        if char1_turn==False:
            board[x][y]=char1   #nezacinajici je char1
        else:
            board[x][y]=char2   #nezacinajici je char2
        used.append([x,y])  #pridame pole do obsazenych
        add_to_active_neighbour(x,y,active,board)   #pridame volne sousedy pole do aktivnich
        if [x,y] in active:  #x,y uz neni vone tim padem ho neni aktivni
            active.remove([x,y])

    elif inp3=="-1":   #vlastni
        #char1
        print("Zadejte souradnice ",char1,"oddelenych mezerou, zadejte '-1' pro ukonceni ")
        inp=input("")
        while inp!="-1":    #nonstop -1 pro ukonceni
            if check_input(inp,board_size)==True:   #input je validni souradnice na hrac. poli
               x,y=inp.split()
               x,y=int(x),int(y)
               if board[x][y]=="_":     #kontrola zda je volne
                   board[x][y]=char1
                   if [x,y] in active:  #x,y uz neni vone tim padem ho neni aktivni
                       active.remove([x,y])
                   used.append([x,y])   #pridame pole do obsazenych
                   add_to_active_neighbour(x,y,active,board)    #pridame volne sousedy pole do aktivnich
               else:
                   print("Uvedene policko je jiz obsazene, vyberte jine")
                   show_board(board,board_size)
            else:
                print("Zadejte souradnice ",char1," tj. dve cela cisla oddelenych mezerou")
            inp=input("")
        #char2
        print("Zadejte souradnice ",char1," oddelenych mezerou, zadejte '-1' pro ukonceni ")
        inp=input("")
        while inp!="-1":    #nonstop -1 pro ukonceni
            if check_input(inp,board_size)==True:   #input je validni souradnice na hrac. poli
               x,y=inp.split()
               x,y=int(x),int(y)
               if board[x][y]=="_":     #kontrola zda je volne
                   board[x][y]=char2
                   if [x,y] in active:  #x,y uz neni vone tim padem ho neni aktivni
                       active.remove([x,y])
                   used.append([x,y])   #pridame pole do obsazenych
                   add_to_active_neighbour(x,y,active,board)    #pridame volne sousedy pole do aktivnich
               else:
                   print("Uvedene policko je jiz obsazene, vyberte jine")
                   show_board(board,board_size)
            else:
                print("Zadejte souradnice ",char2," tj. dve cela cisla oddelenych mezerou")
            inp=input("")

    #else: #prazdne startovni pole

    #nyni mame startovni pole
    print("=================")
    print("Uvodni hraci pole")
    print("=================")
    show_board(board,board_size)

    return board, used, active, char1_turn

#board, used, active, char1_turn = board_s()
