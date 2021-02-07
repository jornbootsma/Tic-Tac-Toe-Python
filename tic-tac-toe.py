import copy
from itertools import permutations

class Game:
    def __init__(self):
        self.board = self.initializeBoard()
        self.board_keys = sorted([key for key in self.board if self.board[key] == ' '])
        self.possible_moves = copy.copy(self.board_keys)
        
        self.choose_own_names = False # self.chooseOwnNames()
        self.first_player, self.second_player = self.initializeNames()
        self.all_players = [self.first_player, self.second_player]
        
        self.symbol_1, self.symbol_2 = self.initializeSymbols()
        self.symbolsOfPlayers = self.getSymbolsOfPlayers()
        
        self.player_on_turn = self.initializePlayerOnTurn()
        
        self.number_of_moves = 0
        self.game_is_over = False
        self.winner = None
        self.max_numb_of_moves = len(self.board.keys())
        
        self.stop_game = False
        
    """
        Define the initial board to start the game. To test the game,
        one can choose a different board to start with.
        
        Returns the board to start the game with.
    """
    def initializeBoard(self):
        initial_board = {'7': ' ', '8': ' ', '9': ' ',
                         '4': ' ', '5': ' ', '6': ' ',
                         '1': ' ', '2': ' ', '3': ' '}
        
#        initial_board = {'7': 'O', '8': 'X', '9': ' ',
#                         '4': 'O', '5': 'X', '6': ' ',
#                         '1': 'X', '2': 'O', '3': ' '}
        return initial_board
        
    """
        Choose the symbols you want to use during the game.
        symbol_1 indicates the symbol representing player 1
        symbol_2 indicates the symbol representing player 2
        
        Returns the symbols that are used for both players in the game.
    """
    def initializeSymbols(self):
        symbol_1 = 'X'; symbol_2 = 'O'
        return symbol_1, symbol_2
    
    """
        If input == 'yes', a boolean True is returned and players can choose their own names.
        Else, a boolean False is returned and the standard names 'Player 1' and 'Player 2' are used.
        
        Returns whether or not players can choose their own name based on given input.
    """
    def chooseOwnNames(self):
        print('Do you want to choose your own names? (yes/no)')
        choose_own_names = input()
        if choose_own_names == 'yes' or choose_own_names == 'Yes' or choose_own_names == 'YES':
            choose_own_names = True
        else:
            choose_own_names = False
        return choose_own_names
    
    """
        If players can choose their own name, this function will ask for this.
        Otherwise the standard names 'Player 1' and 'Player 2' are used.
        
        Returns the names of the players playing the game.
    """
    def initializeNames(self):
        if self.choose_own_names:
            print('What is the name of player 1?')
            player_1 = input()
            print('What is the name of player 2?')
            player_2 = input()
        else:
            player_1 = '1'; player_2 = '2'
        
        return player_1, player_2
        
    """
        This function checks the current state of the board.
        If the game is started with a blank board, player 1 will start the game.
        Otherwise, it is checked which player has done most moves up to this point.
        This situation can occur when a different initial solution is chosen to test the game.
        
        Returns the name of the player that is on turn.
    """
    def initializePlayerOnTurn(self):
        numb_of_symb_1 = list(self.board.values()).count(self.symbol_1)
        numb_of_symb_2 = list(self.board.values()).count(self.symbol_2)
        
        if numb_of_symb_2 < numb_of_symb_1:
            player_on_turn = self.all_players[1]
        else:
            player_on_turn = self.all_players[0]
        return player_on_turn
    
    """ Prints the current board with all actions taken. """
    def printBoard(self):
        print()
        print(self.board['7'] + '|' + self.board['8'] + '|' + self.board['9'])
        print('-+-+-')
        print(self.board['4'] + '|' + self.board['5'] + '|' + self.board['6'])
        print('-+-+-')
        print(self.board['1'] + '|' + self.board['2'] + '|' + self.board['3'])
    
    """ Creates and returns a dictionary to define the symbols that belong to each player. """
    def getSymbolsOfPlayers(self):
        moves = {self.all_players[0]: self.symbol_1, self.all_players[1]: self.symbol_2}
        return moves
        
    """
        First, it is checked if there is a winner.
        If not, it is checked if there is a draw or there can still be made a move.
        
        Returns True if there is a winner or a draw.
        Returns False otherwise.
    """
    def gameIsOver(self):
        game_is_over = False; winner = None
        
        someone_won, winner = self.playerWon()
        if someone_won:
            game_is_over = True
            return game_is_over, winner
        
        if self.number_of_moves >= 5:
            game_ends_with_draw = self.gameEndsWithDraw()
        else:
            game_ends_with_draw = False
            
        if game_ends_with_draw:
            game_is_over = True
            return game_is_over, winner
        
        return game_is_over, winner
    
    """
        The function draws all possible ending situations that can happen starting
        at an current state of the board. If none of these ending situations is a
        win, this means that the game definitely ends with a draw.
        
        Returns True is the game ends with a draw.
        Returns False otherwise.
    """
    def gameEndsWithDraw(self):
        game_ends_with_draw = True
        perms = permutations(self.possible_moves)
        for perm in perms:
            copy_game = copy.deepcopy(self)
            for i in perm:
                copy_game.updateGame(i)
            
            if copy_game.winner:
                game_ends_with_draw = False
                return game_ends_with_draw
                
        return game_ends_with_draw
    
    """
        Checks if someone has won the game at the current state.
        
        Return True and the corresponding winner if someone has won the game.
        Return False and no winner otherwise.
    """
    def playerWon(self):
        someone_won = False; winner = None
        
        if self.board['7'] == self.board['8'] == self.board['9'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['7'])
        elif self.board['4'] == self.board['5'] == self.board['6'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['4'])
        elif self.board['1'] == self.board['2'] == self.board['3'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['1'])
        elif self.board['1'] == self.board['4'] == self.board['7'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['1'])
        elif self.board['2'] == self.board['5'] == self.board['8'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['2'])
        elif self.board['3'] == self.board['6'] == self.board['9'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['3'])
        elif self.board['1'] == self.board['5'] == self.board['9'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['1'])
        elif self.board['3'] == self.board['5'] == self.board['7'] != ' ':
            someone_won = True; winner = get_key(self.symbolsOfPlayers, self.board['3'])
            
        state = [someone_won, winner]
        
        return state
    
    """
        Updates some of the content in the game.
        Given a move done by the player on turn, this move is removed from the
        set of possible moves. This move is also settled in the board.
        
        Since a specific player has made a move, it is not the turn of the other player.
        
        In the end, the function GameIsOver is called to see if the game continues
        or if the result has already been determined.
    """
    def updateGame(self, move):
        self.number_of_moves += 1
        self.possible_moves.remove(move)
        self.board[move] = self.symbolsOfPlayers[self.player_on_turn]
        self.player_on_turn = self.all_players[1 - self.all_players.index(self.player_on_turn)]
        self.game_is_over, self.winner = self.gameIsOver()
    
    """
        This function is called to play the game.
        While the game is not over, a player can make a move.
    """
    def playGame(self):
        print('\nThe game starts. Good luck and have fun!')
        self.printBoard()
        while not self.game_is_over:
            indices = list(range(len(self.possible_moves)))
            possible_moves = [int(self.possible_moves[i]) for i in indices]
            if self.choose_own_names:
                print('\nIt\'s your turn, ' + self.player_on_turn + '. What is your next move? ' + str(possible_moves))
            else:
                print('\nIt\'s your turn, player ' + self.player_on_turn + '. What is your next move? ' + str(possible_moves))
                
            move = input()
            
            if move == 'quit' or move == 'Quit' or move == 'QUIT':
                self.stop_game = True
            
            if self.stop_game:
                break
            
            # Check if it is a legal move 
            while move not in self.possible_moves:
                if self.stop_game:
                    break
                print('Invalid move. Please fill in another empty spot.')
                move = input()
                if move == 'quit' or move == 'Quit' or move == 'QUIT':
                    self.stop_game = True
            
            self.updateGame(move)
            self.printBoard()
        
        if self.game_is_over:
            if self.winner:
                if self.choose_own_names:
                    print(self.winner + ' has won the game. Congratulations!')
                else:
                    print('Player ' + self.winner + ' has won the game. Congratulations!')
            else:
                print('The game is over. The result is a draw.')
        else:
            print('The game has stopped prematurely')

""" Returns the key that belongs to a certain value in the given dictionary. """
def get_key(my_dict, val):
    for key, value in my_dict.items(): 
         if val == value: 
             return key 

"""
    Prints the definition of the board. This indicates what the meaning is
    of each number 1-9 and where your symbol is placed if you choose one.
"""
def printBoardDefinition():
    print('Type \'quit\' to stop the game prematurely whenever you want.\n')
    print('\nThe board is defined as follows:\n')
    print('7' + '|' + '8' + '|' + '9')
    print('-+-+-')
    print('4' + '|' + '5' + '|' + '6')
    print('-+-+-')
    print('1' + '|' + '2' + '|' + '3')
    print('\n')

def main():
    printBoardDefinition()
    
    while True:
        game = Game()
        game.playGame()
        
        if game.stop_game:
            break
        
        restart = input('Do you want to play again? (yes/no)')
        if restart != 'yes' and restart != 'Yes' and restart != 'YES':
            game.stop_game = True
        
        if game.stop_game:
            break
    
if __name__ == "__main__":
    main()