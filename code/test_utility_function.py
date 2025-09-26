#import vsech potrbnych funkci a konstant
from utility_function import utility, state_value, update_state, sign, explore
from board_examples import board1, board2, board3, board4
from constants import terminal_score, char1,char2
from functions_one import get_used
import pytest
    
# TEST: UTILITY

# test hodnoty stavu, parametricky: ("string", ocekavana-hodnota)
@pytest.mark.parametrize("string, expected",[
   ("open",5),  #otevreny za 5
   ("closed",2),    #uzavreny za 2
   ("dead",0),  #mrtvy za 0
   ("@&",0),    #odpad za 0                                            
])
def test_state_value(string,expected):
    assert state_value(string) == expected

# test update stavu, parametricky: ("string", ocekavana-hodnota)
@pytest.mark.parametrize("string, expected",[
   ("open","closed"),   #z otevreneho uzavrneny
   ("closed","dead"),   #z uzavreneho mrtvy
   ("dead","dead"),     #   to se nestane, ale kdyby nahodou
   ("@&~","dead"),      # odpad mrtvy                                               
])
def test_update_state(string,expected):
    assert update_state(string) == expected

# test znamenka charu:  
def test_sign():
    assert sign(char1) == -1    #char1 ma -1 
    assert sign(char2) == 1     #char2 ma +1

# test explor:prozkouma jeden smer (horizontalne -, vertikalne |, diagonalne_1 \, nebo  diagonalne_2 /) 
# vrati cast score ktera se ma pricist/odecist za dane policko 
def test_explore():
    #board1
    X,Y=5,4
    # horizontalne -
    assert explore(X,Y,[0,1],[0,-1],0,board1[X][Y],board1) == 0     #jednice je za 0
    #vertikalne |
    assert explore(X,Y,[1,0],[-1,0],0,board1[X][Y],board1) == 50    #polovina otevenre dvojice z char2 je za 50
    X,Y=9,7
    # horizontalne -
    assert explore(X,Y,[0,1],[0,-1],0,board1[X][Y],board1) == 50    #polovina otevenre dvojice z char2 je za 50
    #vertikalne |
    assert explore(X,Y,[1,0],[-1,0],0,board1[X][Y],board1) == 0     #jednice je za 0
    #diagonalne_1 \
    assert explore(X,Y,[1,1],[-1,-1],0,board1[X][Y],board1) == 0    #jednice je za 0
    #diagonalne_2 /
    assert explore(X,Y,[1,-1],[-1,1],0,board1[X][Y],board1) == 170    
        #polovina otevenre dvojice z char2 je za 50 + za bonus 2 (delka) * 60(extra_bonus_value)

    #board2
    # horizontalne -
    X,Y=7,7
    assert explore(X,Y,[0,1],[0,-1],0,board1[X][Y],board2) == 0     #mrtva trojice je za 0

    #board4
    # horizontalne -
    X,Y=7,7
    assert explore(X,Y,[0,1],[0,-1],0,board1[X][Y],board4) == -500  # ctvrtina uzavrne ctverice z char1 je za -500


# testy utility funkce: z daneho hraciho pole vrati jeho ohodnoceni
def test_utility_function():
    from functions_one import show_board
    from constants import char1, char2 
    #dulezite aby char1 a char2 byly stejne jako v board_examples.py (zde nejsou zadefinovany ale pouzity)

    #board1
    board_size=len(board1)-2    #rozmer hraci plochy1, -2 za okraje z obou stran tvorenych #
    used1=get_used(board1,board_size)   #pouzita pole na board1
    assert utility(board1,used1) == 580 # char2 ma tri otevrene dvojice navic 3*100 a ma bonus 280 za X_XX

    #board2
    board_size=len(board2)-2    #rozmer hraci plochy2, -2 za okraje z obou stran tvorenych #
    used2=get_used(board2,board_size)   #pouzita pole na board2
    assert utility(board2,used2) == 140 # char2 ma otevrneou a uzavrenou dvojici 100+40 , char1 ma mrtvou 3-jici

    #board3
    board_size=len(board3)-2    #rozmer hraci plochy3, -2 za okraje z obou stran tvorenych #
    used3=get_used(board3,board_size)   #pouzita pole na board3
    assert abs(utility(board3,used3)) >= terminal_score     #vyhral O

    #board4
    board_size=len(board4)-2    #rozmer hraci plochy4, -2 za okraje z obou stran tvorenych #
    used4=get_used(board4,board_size)   #pouzita pole na board4
    assert utility(board4,used4) == -1960   # uzavrna 4-ice pro char1: -2000 a +40 za uzavrenou dvojic char2



# pytest test_utility_function.py