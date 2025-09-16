
def utility(board,used):     # vypocita score 
    # TODO HODNOCENI JE ZAVISLE NA TOM KDO JE PRAVE NA TAHU
    # mezi tahy hodnoceni extremne skace

    # hodnoceni:
    lenght_value=[0,0,10,20,250,1000000,1000000,1000000,1000000,1000000]     #hodnota 0, 1-tice,2-jice, 3-jice, 4-rice a vyhry
    bonus_value=40   # odmena za X_X tj. 1-mezeru mezi dvema stejnymy policky
    extra_bonus_value=60   #extra odmena za XX_X a XX_XX a XXX_X
    # ve skutecnosti 2-jici potitam 2x, 3-jici pocitam 3x,... atd 
    # protoze kazdy dil n-tice pocitam nezavisle, takze n-krat
    # ----------
    # Skutecne honoty n-tic (po zapocitani vicenasobneho zapocitani) jsou lenght_value[length]*length
    # 1-tice: 0
    # 2-jice: 20
    # 3-jice: 60
    # 4-rice: 1000
    # 5-tice tj vyhra: 1000000
    #-----------
    # bonus take pocitam vinenasobne a to za kazde policko retezce s mezerou
    # estra bonus je za dvojici/trojici-mezera-pokracovani_retezce
    # bonus = "pocet 1-nicek v retezci" *40 + "2 za kazdou cast 2-ky a 3 za kazdou cast 3-ky"*60
    # X_X   -> bonus = (1+1)*40        = 80
    # XX_X  -> bonus = 1*40+(2+2)*60   = 280
    # X_X_X -> bonus = (1+1+1)*40      = 120
    # XXX_X -> bonus = 1*40+(3+3+3)*60 = 580  
    # XX_XX -> bonus = (2+2+2+2)*60    = 480

    
    def state_value(state):     #hodnota stavu
        if state=="open":   # sitace ___OO__ tj. lze rozsirit na petici=vyhru
            return 5
        elif state=="closed":   # sitace ___OOX tj. lze rozsirit na petici=vyhru POUZE z jedne strany
            return 2
        else: # state=="dead"   # sitace X_OO_X nebo XOO__X tj. NE-lze rozsirit na petici=vyhru
            return 0
    
    def sign(char):  # X-score pricitam, O-score odecitam
        if char=="X":
            return 1
        else: #char=="O"
            return -1

    # rychly update stavu
    def update_state(state):
        if state=="open":
            state="closed"
        else:   #state="closed"
            state="dead"
        return state
    
    def show_value_of_positions():
        print("======== HODNOTY ========")
        print("hodnoty otevrene n-tice")
        for i in range(1,5):
            print(i,"-ice",lenght_value[i]*state_value("open"))
        print("hodnoty uzavrene n-tice")
        for i in range(1,5):
            print(i,"-ice",lenght_value[i]*state_value("closed"))
        print("hodnoty NE-mrtveho bonusu")
        print("""
        X_X   -> bonus = (1+1)*40        = 80
        X_X_X -> bonus = (1+1+1)*40      = 120
        XX_X  -> bonus = 1*40+(2+2)*60   = 280
        XXX_X -> bonus = 1*40+(3+3+3)*60 = 580  
        XX_XX -> bonus = (2+2+2+2)*60    = 480
        ZDE SE NEZAPOCITAVAJI HODNOTY 2,3-ice KTERE MAJI SAMI O SOBE, ALE JEN BONUS 
        """)
    #show_value_of_positions()

    def explore_one_dicecton(x,y,k,num_in_row,num_spaces,state,bonus):
        # z pozice x,y prozkouma ve smeru k 
        # spocita souvislou delku
        # urci stav ale jen napul, ten je treba upresnit z poctu mezer viz X_OO_X nebo XOO__X
        # -
        # pro prozkoumani napr. horiznani delky (a jeho stavu) je nutno spustit 2x (doleva a doprava)
        # kde poprve num_in_row=1, num_spaces=0 a state="open"
        
        while 1: #don't worry, be happy
            #print(x+k[0],y+k[1])
            #print(board[x+k[0]][y+k[1]])
            #print(char)
            if board[x+k[0]][y+k[1]]==char: #proudloueni retezce
                num_in_row+=1
                x+=k[0]
                y+=k[1]
                continue

            elif board[x+k[0]][y+k[1]]==charOp or board[x+k[0]][y+k[1]]=="#":   #zmena stavu a konec
                state=update_state(state)
                break
        
            else: #board[x+k[0]][y+k[1]]=="_"  #zjisteni poct mezer a potencialni bonus
                num_spaces+=1
                x+=k[0]
                y+=k[1]

                if board[x+k[0]][y+k[1]]==char:
                    # na pozici x,y je mezera
                    # na pozicich x+k[0],y+k[1] a x-k[0],y-k[1] je char
                    # =>trojice 0_0 (resp. X_X) =>BONUS
                    bonus=True

                    # update mezer k dalsi kontrole umrtveni a spocteni delky
                    num_spaces+=1
                    x+=k[0]
                    y+=k[1]
                    if board[x+k[0]][y+k[1]]==char or board[x+k[0]][y+k[1]]=="_":
                        num_spaces+=1
                        x+=k[0]
                        y+=k[1]
                        if board[x+k[0]][y+k[1]]==char or board[x+k[0]][y+k[1]]=="_":
                            num_spaces+=1
                    
                #if board[x+k[0]][y+k[1]]==charOp or board[x+k[0]][y+k[1]]=="#":
                #   print("do nothing")   # nic se nestane

                elif board[x+k[0]][y+k[1]]=="_":    #dalsi kontrola umrtveni
                    num_spaces+=1
                    x+=k[0]
                    y+=k[1]

                    if board[x+k[0]][y+k[1]]==char or board[x+k[0]][y+k[1]]=="_":
                        num_spaces+=1

                    #if board[x+k[0]][y+k[1]]==charOp or board[x+k[0]][y+k[1]]=="#":
                    #   print("do nothing")   # nic se nestane
                break

        return num_in_row,num_spaces,state,bonus

    def explore(X,Y,k,l,score): 
        # spocita pocet stejnych charakteru jako na pozici X,Y  ve smerech (list delky 2) k,l
        # tj horizontalne - , verticalne | , diagonalne1 \ , diagonalne2 / 
        # a urci stav otevreny/uzavreny/mrtvy
        length=1    #sam o sobe
        num_spaces=0
        state="open"
        bonus=False
        length,num_spaces,state,bonus=explore_one_dicecton(X,Y,k,length,num_spaces,state,bonus)
        length,num_spaces,state,bonus=explore_one_dicecton(X,Y,l,length,num_spaces,state,bonus)
        # k=-l, ale takle musel bych jit po elementech k a l
        # uprsneni stavu
        if state=="dead":   #situace X00000X zde O vyhrava 
            if length>=5:
                return sign(char)*1000000

        else: # state=="open" or state=="closed":
            if length+num_spaces<5:     # situace X_OO_X, XOO__X => dvojice OO je ve skutecnosti mrtva
                state="dead"
            # jinak state je presne
        # else state="dead" je uz presne
        # ted vim prsne delku a stav retezce

        # bonus
        if bonus==True and state!="dead":
            if length==1:
                score+=sign(char)*bonus_value
                #print(sign(char)*bonus_value,"bonus")
            else:   #length>1
                score+=sign(char)*length*extra_bonus_value
                #print(sign(char)*length*extra_bonus_value,"bonus")

        #print(X,Y,"souradnice X Y")
        #print(board[X][Y],"char na X Y")
        #print(length,"lenght")
        score+=sign(char)*state_value(state)*lenght_value[length]
        
        #if length>1:
        #    if state!="dead":
        #        print(sign(char)*state_value(state)*lenght_value[length],"gain")
        #        if k==[0,1] and l==[0,-1]:
        #            print(length,state,char,sign(char),"horizontal - ")
        #        elif k==[1,0] and l==[-1,0]:
        #            print(length,state,char,sign(char),"vertical | ")
        #        elif k==[1,1] and l==[-1,-1]:
        #            print(length,state,char,sign(char),"diagonal1 \\")
        #        elif k==[1,-1] and l==[-1,1]:
        #            print(length,state,char,sign(char),"diagonal2 /")

        return score

    # ze vsechnobsazenzch policek ("X" nebo "O") vypocitam score
    score=0
    for cell in used:
        X,Y=cell[0],cell[1]
        #print("EXPLORE FROM",X,Y)   
        char=board[X][Y]
        #oposite to char:
        if char=="O":  
            charOp="X"
        else:
            charOp="O"

        #horizontalne -
        score=explore(X,Y,[0,1],[0,-1],score)
        #vertikalne |
        score=explore(X,Y,[1,0],[-1,0],score)
        #diagonalne_1 \
        score=explore(X,Y,[1,1],[-1,-1],score)
        #diagonalne_2 /
        score=explore(X,Y,[1,-1],[-1,1],score)
        #print("===================")

    #print("utility:","po tahu",X,Y,"je score",score)
    return score
     

def test_utility_f():
    #utility-functions tests

    boardS=15
    from functions import show_board

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
    print(used,"pouzite policka")
    print("Score from utility function:")
    scoreA=utility(board,used)
    print(scoreA)

# test_utility_f()
#   Get-content utility_test.txt | python utility_function.py