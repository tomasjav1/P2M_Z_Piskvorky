#import funkci
from constants import board_size,char1,char2
from functions_one import show_board, return_char_Op
from board_setup import board_s
from unittest import mock

#TESTY BOARD-SETUP
# input1: Chcete hrat s nahodnymi prekazkami? "1" pro ANO
# input2: Chcete aby zaninal char1 (hrac)? "1" pro ANO
# input3: Jake chcete startovni rozlozeni hraci plochy? 
#       "1" pro 3 nahodne kameny, kde 2 ziska nezacinajici hrac
#       "-1" pro vlastni

# test: prazdne pole bez rekazek, zacina hrac
def test_board_setup1(monkeypatch):
    inputs=iter(["0","1","0"])  #input
    monkeypatch.setattr('builtins.input', lambda _: next(inputs)) #takto jsem mocknul input
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == []
    assert active == []
    assert char1_turn == True   #kontrola zda zacina hrac ci nikoliv

# test: prazdne pole bez rekazek, zacina "PC"
def test_board_setup2(monkeypatch):
    inputs=iter(["a","&q","@@"])    #input
    monkeypatch.setattr('builtins.input', lambda _: next(inputs)) #takto jsem mocknul input
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == []   #pouzite
    assert active == [] #aktivni
    assert char1_turn == False  #kontrola zda zacina hrac ci nikoliv

# test: pole bez rekazek s vlstni startovnim rozlozenim, zacina "PC"
def test_board_setup3(monkeypatch):
    inputs=iter(["a","&q","-1","1 q","1 322","3 3","-1","q 3 ","4 4","-1"])     
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == [[3,3],[4,4]]    #pouzite
    #aktivni
    assert active == [[4, 3], [4, 2], [3, 4], [2, 2], [2, 3], [2, 4], [3, 2], [5, 5], [5, 4], [5, 3], [4, 5], [3, 5]]
    assert char1_turn == False  #kontrola zda zacina hrac ci nikoliv

# test: pole bez prekazek s 3 nahodne vygenerovanyma startovnima polema
@mock.patch('random.randint')   #takto jsem mocknul randint
@mock.patch("builtins.input")   #takto jsem mocknul input
def test_board_setup4(mock_input,mock_randint):
    mock_input.side_effect = ["0", "1", "1"]    #input
    # random-int: souradnice 3 startovnich policek  
    # zmanipulovanej randint
    mock_randint.side_effect = [7,8, 1,3, 1,3, 8,14]    #pole 1,3 jsem uz pouzil, vygeneruju dalsi (dokud neboude volne)
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == [[7,8],[1,3],[8,14]]     #pouzita policka
    # aktivni policka
    assert active == [[8, 9], [8, 8], [8, 7], [7, 9], [6, 7], [6, 8], [6, 9], [7, 7], [2, 4], [2, 3], [2, 2], [1, 4], [1, 2], [9, 15], [9, 14], [9, 13], [8, 15], [7, 13], [7, 14], [7, 15], [8, 13]]
    assert char1_turn == True   #kontrola zda zacina hrac ci nikoliv
    #kontrola zda ty 3 policka jsou opravdu obsazena tak jak maji
    assert (board[7][8],board[1][3],board[8][14]) == (char1,char2,return_char_Op(char1_turn))  
     
# test: pole s prekazkami
@mock.patch('random.randint')   #takto jsem mocknul randint
@mock.patch("builtins.input")   #takto jsem mocknul input
def test_board_setup5(mock_input,mock_randint):
    mock_input.side_effect = ["1", "0", "0"]    #input
    l=[7,8, 1,3, 8,14, 5,5, 9,8, 3,13, 9,12]    # 7 policke s prekazkami #
    mock_randint.side_effect = l   #zmanipulovanej randint
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == []
    assert active == []
    assert char1_turn == False  #kontrola zda zacina hrac ci nikoliv
    #kontrola prekazek na hracim poli
    for i in range(0,len(l),2):
        assert board[int(l[i])][int(l[i+1])] == "#"

# test: pole s prekazkami
@mock.patch('random.randint')   #takto jsem mocknul randint
@mock.patch("builtins.input")   #takto jsem mocknul input
def test_board_setup6(mock_input,mock_randint):
    mock_input.side_effect = ["1", "0", "0"]    #input
    # 6 policke s prekazkami #, protoze posledni 2 jsou identicke
    l=[7,8, 1,3, 8,14, 5,5, 9,8, 3,13, 3,13]
    mock_randint.side_effect = l   #zmanipulovanej randint
    board, used, active, char1_turn = board_s() #spusteni board_setup
    assert used == []
    assert active == []
    assert char1_turn == False  #kontrola zda zacina hrac ci nikoliv
    #kontrola prekazek na hracim poli
    for i in range(0,len(l),2):
        assert board[int(l[i])][int(l[i+1])] == "#"


@mock.patch('random.randint')   #takto jsem mocknul randint
@mock.patch("builtins.input")   #takto jsem mocknul input
def test_board_setup7(mock_input,mock_randint):
    mock_input.side_effect = ["1", "0", "1"]    #input
    l=[7,8, 1,3, 8,14, 5,5, 9,8, 3,13, 9,12]    # pole se souradnicema prekazek
    mock_randint.side_effect = l    #zmanipulovanej randint
    board, used, active, char1_turn = board_s()     #spusteni board_setup
    assert used == [[9,11],[8,11],[7,10]]   #pouzita policka
    #aktivni policka
    assert active == [[10, 12], [10, 11], [10, 10], [8, 10], [8, 12], [9, 10], [7, 11], [7, 12], [8, 9], [6, 9], [6, 10], [6, 11], [7, 9]]
    assert char1_turn == False  #kontrola zda zacina hrac ci nikoliv
    #kontrola prekazek na hracim poli
    for i in range(0,13,2):
        print(int(l[i]),int(l[i+1]))
        assert board[int(l[i])][int(l[i+1])] == "#"
    #kontrola zda ty 3 policka jsou opravdu obsazena tak jak maji
    assert (board[9][11],board[8][11],board[7][10]) == (char1,char2,return_char_Op(char1_turn))

# pytest test_board_setup.py
