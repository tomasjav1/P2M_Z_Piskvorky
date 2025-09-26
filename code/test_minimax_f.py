#import funkci a konstant
from minimax_f import minimax, minimax_valueMIN, minimax_valueMAX, minimax_decisionMIN, minimax_decisionMAX
from board_examples import board1, board2, board4, board6
from functions_one import get_used
from constants import char1, char2, terminal_score
from math import inf 

#TEST MINIMAX

#testy valueMIN a valueMAX
#maji vracet skore na po zahrani nejlepsih tahu obou hracu, jen do dane hloubky, kde zacina MIN resp MAX hrac
def test_value_MIN_and_MAX():
    #board1
    board_size=len(board1)-2    #rozmer hraci plochy1, -2 za okraje z obou stran tvorenych #
    used1=get_used(board1,board_size)   ##pouzita pole na board1
    # hloubka 1
    assert minimax_valueMIN(board1,used1,1,-inf,inf) == 240 # hodnoty po nejlepsim tahu pro MIN (O)
    assert minimax_valueMAX(board1,used1,1,-inf,inf) == 5200 # hodnoty po nejlepsim tahu pro MAX (X)
    #hloubka 2
    assert minimax_valueMIN(board1,used1,2,-inf,inf) == 700 # hodnoty po nejlepsim tahu pro MIN (O) a po nejlepsim tahu pro MAX (X)
    assert minimax_valueMAX(board1,used1,2,-inf,inf) == 1920 # hodnoty po nejlepsim tahu pro MAX (X) po nejlepsim tahu pro MIN (O)

    #board4
    board_size=len(board4)-2    #rozmer hraci plochy4, -2 za okraje z obou stran tvorenych #
    used4=get_used(board4,board_size)   #pouzita pole na board4
    # hloubka 1
    assert abs(minimax_valueMIN(board4,used4,1,-inf,inf)) >= terminal_score #  MIN (O) hrac nasel vyherni tah
    assert minimax_valueMAX(board4,used4,1,-inf,inf) == 140 # hodnoty po nejlepsim tahu pro MAX (X)
    #hloubka 2
    assert abs(minimax_valueMIN(board4,used4,1,-inf,inf)) >= terminal_score # MIN (O) hrac nasel vyherni tah
    assert minimax_valueMAX(board4,used4,2,-inf,inf) == -160 # hodnoty po nejlepsim tahu pro MAX (X) po nejlepsim tahu pro MIN (O)

#testy decisionMIN a decisionMax
# vraci nejlepsi tah pro MIN resp MAX hrace
def test_decision_MIN_and_MAX():
    #board1
    board_size=len(board1)-2    #rozmer hraci plochy1, -2 za okraje z obou stran tvorenych #
    used1=get_used(board1,board_size)
    #hloubka 2
    assert minimax_decisionMIN(board1,used1,2,-inf,inf) == [10,6] # nejlepsi tahu pro MIN (O)
    assert minimax_decisionMAX(board1,used1,2,-inf,inf) == [10,6] # nejlepsi tahu pro MAX (X)

    #board4
    board_size=len(board4)-2    #rozmer hraci plochy4, -2 za okraje z obou stran tvorenych #
    used4=get_used(board4,board_size)
    #hloubka 2
    assert minimax_decisionMIN(board4,used4,2,-inf,inf) == [7,9] # nejlepsi tahu pro MIN (O)
    assert minimax_decisionMAX(board4,used4,2,-inf,inf) == [7,9] # nejlepsi tahu pro MAX (X)

#vraci nejlepsi tah protoho, dko je na tahu char1 je MIN hrac a char2 je MAX hrac
def test_minimax_function():
    from functions_one import show_board
    #dulezite aby char1 a char2 byly stejne jako v board_examples.py (zde nejsou zadefinovany ale pouzity)

    #board1
    board_size=len(board1)-2    #rozmer hraci plochy1, -2 za okraje z obou stran tvorenych #
    used1=get_used(board1,board_size)   #pouzita pole na board1
    assert minimax(board1,used1,2,True,board_size) == [10,6]  # tah minimaxu  pro O
    assert minimax(board1,used1,2,False,board_size) == [10,6]  # tah minimaxu pro X

    #board2
    board_size=len(board2)-2    #rozmer hraci plochy2, -2 za okraje z obou stran tvorenych #
    used2=get_used(board2,board_size)   #pouzita pole na board2
    assert minimax(board2,used2,2,False,board_size) == [8,9]  # tah minimaxu pro X

    #board4
    board_size=len(board4)-2    #rozmer hraci plochy4, -2 za okraje z obou stran tvorenych #
    used4=get_used(board4,board_size)   #pouzita pole na board4
    assert minimax(board4,used4,2,True,board_size) == [7,9]  # tah minimaxu  pro O
    assert minimax(board4,used4,2,False,board_size) == [7,9]  # tah minimaxu pro X

    #board6
    board_size=len(board6)-2    #rozmer hraci plochy6, -2 za okraje z obou stran tvorenych #
    used6=get_used(board6,board_size)      #pouzita pole na board6
    assert minimax(board6,used6,2,True,board_size) == [1,2]  # tah minimaxu  pro O
    assert minimax(board6,used6,2,False,board_size) == [15,4]  # tah minimaxu pro X

    #PS: kdyz ma jeden hrac nejlepsi tah [x,y], ktery je az moc dobry,
    # tak druhy hrac ma casto nejlepsi tah mu tento tah zabranit hrat a tedy tam zahraje
    


# pytest test_minimax_f.py