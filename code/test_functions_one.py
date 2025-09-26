#importy funkci a konstant
from functions_one import check_int, check_split, check_input, get_list_add_to_active_neighbour, get_mm_active
from functions_one import get_used, get_player_input, switch_turn, ran_empry_space, ran_empry_space_middle
from constants import board_size
import pytest
from board_examples import board2,board5
 
# FUNCTIONS TESTY: testy ruznych funkci pozity napric projektem

# parametricke testovani (string, ocekavana-hodnota)
# test check_int ktera vraci true pokud jeji argument (string) lze konvertovat na cele cislo
@pytest.mark.parametrize("string, expected",[
   ("12",True),     #12 lze konvertovat na cele cislo
   ("187",True),    #187 lze konvertovat na cele cislo
   ("1qw",False),   # 1qw NELZE -||-
   ("w&",False),    # w& NELZE -||-
   ("11 w",False),  # 11 NELZE -||-
   ("",False),  #  NELZE -||-
])
def test_check_int(string,expected):
    assert check_int(string) == expected

# test_check_split vrati True pokud na jeji argument (string) lze zavolat funkce split()
# tj. je ve stringu prave jedna (souvisla) mezera ktera rozdeluje string na 2 kratsi (nedegenerovane) 
@pytest.mark.parametrize("string, expected",[
   ("1 3",True),    # lze rozdelit mezerou na 1,3
   ("1    1b",True),       # lze rozdelit mezerou na 1,1b
   ("3 2w ",False), # NELZE rozdelit mezerou - jsou tam 2
   ("1 @ &",False), # NELZE rozdelit mezerou - jsou tam 2
   ("4567",False), # NELZE rozdelit mezerou neni tam ani jedna
   (" 23",False),  # NELZE rozdelit mezerou -je na zacatku
   (" 2 4",False), # NELZE rozdelit mezerou - jsou tam 2
   (" ",False),  # NELZE  
   ("",False),   #NELZE                                                    
])
def test_check_split(string,expected):
    assert check_split(string) == expected

#test zda vrati True pokud se jedna o dvojici celych cisel oddelenych mezerou (oddeleni pres funci split) 
# a tyto 2 cela cisla-oznacme je x,y musi splovat: 1<=y<=board_size, 1<=x<=board_size
@pytest.mark.parametrize("string, expected",[
   ("1 331",False), # cela cisla ale nelezi na sachovnici
   ("221 6",False), # cela cisla ale nelezi na sachovnici
   ("2 6 ",False), # nelze split() na 2 stringy pomoci mezery
   ("3 2w",False), # "2w" neni cele cislo
   ("@&",False), #nelze split() na 2 stringy pomoci mezery
   ("q",False), #nelze split() na 2 stringy pomoci mezery
   ("",False), #nelze
   ("4 5",True), #spravne                                                      
])
def test_check_input(string,expected):
    assert check_input(string,board_size) == expected

# test zda funkce zdaneho policka vrati list sousednich policek, ktera jsou volna a jiz nejosu v poli  active 
def test_get_list_add_to_active_neighbour():
    #z pole [6,3] volame funcki get_list_add_to_active_neighbour:  pole [7,4] je zabrane
    assert get_list_add_to_active_neighbour(6,3,[],board2) == [[7,3],[7,2],[6,4],[5,2],[5,3],[5,4],[6,2]]
    #z pole [6,3] volame funcki get_list_add_to_active_neighbour:  pole [7,4] je zabrane a [6,4],[7,3] jsou aktivni
    assert get_list_add_to_active_neighbour(6,3,[[6,4],[7,3]],board2) == [[7,2],[5,2],[5,3],[5,4],[6,2]]
    # tu samou funkci volame z [14,14], vsechny sousedni jsou volna a nejsou v aktive
    assert get_list_add_to_active_neighbour(14,14,[],board5) == [[15,15],[15,14],[15,13],[14,15],[13,13],[13,14],[13,15],[14,13]]

# z hraciho pole vrati obsazena tj. vsechna policka na kterych je char1 nebo char2
def test_get_used():
    assert get_used(board5,board_size) == [[3,3],[4,4],[9,9],[14,14]]
    assert get_used(board2,board_size) == [[6, 3], [7, 4], [7, 6], [7, 7], [7, 8], [7, 9], [8, 8], [9, 8]]

# test zda z hraciho pole vrati aktivni tj. vsechna volna policka ktera sousedi k obsazenym
def test_get_mm_active():
   used5=get_used(board5,board_size)
   assert get_mm_active(board5,used5,board_size) == [[4, 3], [4, 2], [3, 4], [2, 2], [2, 3], [2, 4], [3, 2], [5, 5], [5, 4], [5, 3], [4, 5], [3, 5], [10, 10], [10, 9], [10, 8], [9, 10], [8, 8], [8, 9], [8, 10], [9, 8], [15, 15], [15, 14], [15, 13], [14, 15], [13, 13], [13, 14], [13, 15], [14, 13]]

# test zda True prohodi na False a naopak
def test_switch_turn():
    assert switch_turn(True) == False
    assert switch_turn(False) == True

# test zda bude chtit od hrace input dokud nazada validni souradnice volneho polcika na hraci plose
def test_get_player_input1(monkeypatch):
    inputs=iter(["0","3 a","5 3"]) # "0" a "3 a" nejsou validni souradnice, ale 5 3 josu
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_player_input(input(""),board_size,board5) == (5,3)

def test_get_player_input2(monkeypatch):
    inputs=iter(["@","3 789","3 3","4 4","5 5"]) 
    #prvni 2 nejsou validni souradnice, dalsi 2 policka jsou zabrana, nakonec 5 5 je validni
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_player_input(input(""),board_size,board5) == (5,5)
    
def test_get_player_input3(monkeypatch):
    inputs=iter(["5 3"]) #hle na prvni pokus
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_player_input(input(""),board_size,board5) == (5,3)

from unittest import mock
@mock.patch('random.randint')
#test zda vrati nahodne volne policko na hraci plose
def test_ran_empry_space(mock_randint):
    mock_randint.side_effect = [6,7]   #volne pole
    assert ran_empry_space(board5,board_size) == (6,7)

    mock_randint.side_effect = [3,3, 4,4, 2,5]   #prvne zkusim obsazena pole 3,3 a 4,4 a pote dostanu volne 2,5
    assert ran_empry_space(board5,board_size) == (2,5)

@mock.patch('random.randint')
#test zda vrati nahodne volne policko na hraci plose +- uprostred
def test_ran_empry_space(mock_randint):
    mock_randint.side_effect = [7,8]   #volne pole
    assert ran_empry_space_middle(board5,board_size,3) == (7,8)

    mock_randint.side_effect = [9,9, 8,10]   #prvne zkusim obsazena pole 9,9 a pote dostanu volne 8,10
    assert ran_empry_space_middle(board5,board_size,3) == (8,10)

# pytest test_functions_one.py