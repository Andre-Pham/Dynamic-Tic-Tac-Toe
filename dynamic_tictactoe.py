
import copy
import math

HELP_MESSAGE = \
'''
Moves should be in the form "row, column".
So if you wanted to go to the first row, first column,
you'd type "1, 1"
'''

class Board:
    def __init__(self, required_in_a_row, num_of_rows, num_of_cols):
        self.required_in_a_row = required_in_a_row
        self.num_of_rows = num_of_rows
        self.num_of_cols = num_of_cols

        self.game_board = self.create_board(num_of_rows, num_of_cols)

    def flatten_board(self, board=None):
        '''
        Empties nested lists into a flat list and returns it.
        '''
        if board == None:
            board = self.game_board
        return [element for sublist in board for element in sublist]

    def check_if_winner_exists(self, board=None, competitor='either'):
        '''
        Checks if there is a certain number of elements in a row on the board,
        that be vertically, horizontally or diagonally. If so, it returns True.
        Otherwise, it returns False.
        '''
        #Assign board to the game board if not specified; sets game board as
        #default parameter
        if board == None:
            board = self.game_board
        #Check for X in a row, horizontally.
        for row in board:
            for index in range(len(row)):
                for i in range(self.required_in_a_row):
                    #Breaks if the row starts with an 'x', and is searching for computer wins.
                    if competitor == 'computer' and row[index] == 'x':
                        break
                    #Breaks if the row starts with an 'o', and is searching for player wins.
                    elif competitor == 'player' and row[index] == 'o':
                        break
                    #Breaks if the row starts with an '_'.
                    elif row[index] == '_':
                        break
                    #Checks neighbouring (horizontal) value.
                    try:
                        if row[index] != row[index+i]:
                            break
                    except:
                        break
                    #If a certain amount of neighbouring horizontal values are equal to each other.
                    if i == self.required_in_a_row-1:
                        return True
        #Check for X in a row, vertically.
        columns = list(zip(*board))
        for column in columns:
            for index in range(len(column)):
                for i in range(self.required_in_a_row):
                    #Breaks if the column starts with an 'x', and is searching for computer wins.
                    if competitor == 'computer' and column[index] == 'x':
                        break
                    #Breaks if the column starts with an 'o', and is searching for player wins.
                    elif competitor == 'player' and column[index] == 'o':
                        break
                    #Breaks if the column starts with an '_'.
                    elif column[index] == '_':
                        break
                    #Checks neighbouring (vertial) value.
                    try:
                        if column[index] != column[index+i+1]:
                            break
                    except:
                        break
                #If a certain amount of neighbouring vertial values are equal to each other.
                if i == self.required_in_a_row-1:
                    return True
        #Check for diagonals.
        for index1 in range(len(board)):
            for index2 in range(len(board[0])):
                diagonal_SE = True #South East
                diagonal_SW = True #South West
                for i in range(self.required_in_a_row):
                    #No win if the row starts with an 'x', and is searching for computer wins.
                    if competitor == 'computer' and board[index1][index2] == 'x':
                        diagonal_SE, diagonal_SW = False, False
                        break
                    #No win if the row starts with an 'o', and is searching for player wins.
                    elif competitor == 'player' and board[index1][index2] == 'o':
                        diagonal_SE, diagonal_SW = False, False
                        break
                    #No win if row starts with '_'.
                    elif board[index1][index2] == '_':
                        diagonal_SE, diagonal_SW = False, False
                        break
                    #Checks neighbouring diagonal values SE direction.
                    try:
                        if board[index1][index2] != board[index1+i][index2+i]:
                            diagonal_SE = False
                    except:
                        diagonal_SE = False
                    #Makes sure it's not checking diagonal values using negative coordinates.
                    if index2-i < 0:
                        diagonal_SW = False
                    #Checks neighbouring diagonal values SW direction.
                    try:
                        if board[index1][index2] != board[index1+i][index2-i]:
                            diagonal_SW = False
                    except:
                        diagonal_SW = False
                    #Cancels search if confirmed that it's not diagonal in either direction.
                    if diagonal_SE == False and diagonal_SW == False:
                        break
                #If a certain amount of neighbouring diagonal values are equal to each other.
                if diagonal_SE or diagonal_SW:
                    return True
        #If all above fails, the game isn't over yet.
        return False

    def check_if_full_board(self):
        '''
        Checks if game is a draw by checking if any of the board values are
        '_'. If any are, the game isn't over. Otherwise, all values are
        either 'o' or 'x' and hence the game is over, with a draw.
        '''
        flattened_board = self.flatten_board()
        for i in flattened_board:
            if i == '_':
                return False
        return True

    def create_board(self, num_rows, num_cols):
        '''
        Creates a board according to speficied number of columns and rows.
        Every coordinate is '_'. Returns the board created.
        '''
        return [['_' for i in range(num_cols)] for x in range(num_rows)]

    def apply_player_turn(self, row, col):
        '''
        Changes speficied column and row value (both starting at 1) to 'x'.
        '''
        self.game_board[row][col] = 'x'

    def print_current_board(self):
        '''
        Takes the current board and prints it in the console in a more readable
        format.
        '''
        board_print = copy.deepcopy(self.game_board)
        #Prints the numbers of the columns.
        print('   ' + '  '.join([str(i+1) for i in range(len(board_print[0]))]))
        #Prints the numbers of the rows, and the actual rows.
        for num, row in enumerate(board_print):
            print(f'{str(num+1)}  {"  ".join(row)}')
        #Prints an extra return.
        print('')

    def take_player_turn(self):
        '''
        Allows the player to enter their desired move, converts it to a coordinate
        in a list format, applies the player's turn to the current board then
        prints the new updated board in a readable format.
        '''
        #Validation.
        while True:
            #Collects the player's move as coordinates.
            player_input = input('Enter your move: ')
            if player_input == 'help':
                print(HELP_MESSAGE)
                continue
            try:
                row = int(player_input.split(', ')[0])
                column = int(player_input.split(', ')[-1])
                if self.game_board[row-1][column-1] != '_':
                    print('Invalid entry! Place taken. Try again.\n')
                    continue
                break
            except:
                print('Invalid entry! Invalid formatting. Try again.\n')
        #Applies their turn to the board.
        self.apply_player_turn(row, column)
        #Prints the current board.
        self.print_current_board()

    def generate_all_computer_options(self):
        '''
        Generates a list of coordinates that the computer can take its next turn
        at. For example, [[0, 1], [0, 2]].
        This is done by finding all the coordinates on the board that have a value
        of an integer. If they're an integer, they must not be taken by an 'x' or
        'o', meaning the computer can take its turn there.
        '''
        computer_options = []
        for row_index, row in enumerate(self.game_board):
            for col_index in range(len(row)):
                if self.game_board[row_index][col_index] == '_':
                    computer_options.append([row_index, col_index])
        return computer_options

    def simulate_computer_turn(self, row, col):
        '''
        Simulates a deep copy of the current board and applies an 'o' as the
        computer's turn at the given coordinates.
        '''
        copy_board = copy.deepcopy(self.game_board)
        copy_board[row][col] = 'o'
        return copy_board

    def simulate_all_computer_turns(self):
        '''
        Using the coordinates for possible turns found by
        self.generate_all_computer_options(), it goes through each one and creates a
        copy of the board with that coordinate applied as a turn, then adds
        all the boards into a list.
        '''
        all_computer_turns = []
        computer_options = self.generate_all_computer_options()
        for coordinate in computer_options:
            all_computer_turns.append(self.simulate_computer_turn(coordinate[0], coordinate[1]))
        return all_computer_turns

    def generate_next_perm(self, permutation):
        '''
        Generates the next permutation sequence in lexiographic order using the
        previous permutation sequence. See:
        https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
        '''
        length = len(permutation)
        next_perm = permutation[:]
        for i in range(length-2, -1, -1):
            if permutation[i] < permutation[i+1]:
                break
        for j in range(length-1, i, -1):
            if permutation[j] > permutation[i]:
                break
        next_perm[i], next_perm[j] = next_perm[j], next_perm[i]
        return next_perm[:i+1] + list(reversed(next_perm[i+1:]))

    def generate_permutations(self, vlist):
        '''
        Generates all permutations of a given list in lexiographic order. See:
        https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
        '''
        first_seq = sorted(vlist)
        last_seq = list(reversed(first_seq))
        permutations = [first_seq]
        while permutations[-1] != last_seq:
            permutations += [self.generate_next_perm(permutations[-1])]
        return permutations

    def generate_score_for_simulation(self, simulation):
        '''
        Generates a score for a given simulated board based on how many future
        outcomes from the simulated board win and lose.
        '''
        flattened_board = self.flatten_board(simulation)
        num_of_turns_taken = flattened_board.count('_')
        permutation_seed = ['x' if i%2 == 0 else 'o' for i in range(num_of_turns_taken)]
        permutations = self.generate_permutations(permutation_seed)
        #Each permutation has each of its elements placed in all the empty spots
        #of the current simulated board to generate a possible future board that
        #is full. If that future board leads to either the player or computer
        #winning, it is worth considering when generating the final score.
        simulated_outcomes = []
        for permutation in permutations:
            copy_board = copy.deepcopy(simulation)
            for index1, row in enumerate(copy_board):
                for index2, element in enumerate(row):
                    if element == '_':
                        copy_board[index1][index2] = permutation[-1]
                        permutation.pop()
            if self.check_if_winner_exists(copy_board):
                simulated_outcomes.append(copy_board)
        #This adds a point for every board where the computer wins, and subtracts a
        #point for every board where the computer loses.
        score = 0
        for outcome in simulated_outcomes:
            if self.check_if_winner_exists(outcome, 'computer'):
                score += 1
            if self.check_if_winner_exists(outcome, 'player'):
                score -= 1
        return score

    def check_if_first_turn(self):
        '''
        Determines whether the board is empty (hence the turn being taken is the
        first) or not. If so, returns True. Otherwise, returns False.
        '''
        flattened_board = self.flatten_board()
        if flattened_board.count('o') == 0:
            return True
        return False

    def subtract_scores_indices(self):
        '''
        This identifies all the indices of coordinates that form the perimeter of
        the board, for a flat board of all the future possible simulated outcomes.
        For example, say you have board:
        ['_', '_', 'x']
        ['o', '_', '_']
        ['o', '_', '_']
        Flattened, the board is:
        ['_', '_', 'x', 'o', '_', '_', 'o', '_', '_']
        The following future indices to choose for the next more are as so:
        ['0', '1', 'x', 'o', '2', '3', 'o', '4', '5']
        This function returns the indices on the outside perimeter of the board.
        Hence for this example, it would return:
        [0, 1, 3, 4, 5]
        It would skip 3, because thats not part of the outside perimeter as shown
        on the 2D board.
        '''
        flattened_board = self.flatten_board()
        #These are the indices of the flattened board that form the perimeter.
        perimeter_indices = set()
        for i in range(0, self.num_of_rows*self.num_of_cols, self.num_of_cols):
            perimeter_indices.add(i)
            perimeter_indices.add(i-1+self.num_of_cols)
        for i in range(0, self.num_of_rows):
            perimeter_indices.add(i)
            perimeter_indices.add(i+self.num_of_rows*(self.num_of_cols-1))
        #This selects indices of the flattened function that are empty, and part
        #of the perimeter, and allocates the correct index to each, indicated
        #by the index_counter.
        subtract_indices = []
        index_counter = 0
        for index, element in enumerate(flattened_board):
            if element == '_':
                if index in perimeter_indices:
                    subtract_indices.append(index_counter)
                index_counter += 1
        return subtract_indices

    def find_optimal_computer_turn(self):
        '''
        This returns the coordinates of the best computer turn possible, such
        as [1, 1], by using scores generated for each possible future turn.
        '''
        list_of_options = self.generate_all_computer_options()
        list_of_options_simulated = self.simulate_all_computer_turns()
        #If one of the options leads to an instant computer win, just choose that.
        for sim in list_of_options_simulated:
            if self.check_if_winner_exists(sim):
                return list_of_options[list_of_options_simulated.index(sim)]
        #Percentage gain and progress, because generation can sometimes take a while.
        percentage_gain = 100/len(list_of_options)
        progress = 0
        #If the player doesn't want to wait for turn 1, it can instantly be generated.
        if self.check_if_first_turn():
            return [(len(self.game_board) - 1)//2, (len(self.game_board[0]) - 1)//2]
        #Generates scores in the same index for each option, in a list.
        scores = []
        for num, sim in enumerate(list_of_options_simulated):
            ########################################################################
            #Code for showing the player the progress of the computer's turn.
            if percentage_gain < 8:
                if percentage_gain < 6:
                    print(f'Computer processing... {round(progress)}%')
                    progress += percentage_gain
                else:
                    if num%2 == 0:
                        print(f'Computer processing... {round(progress)}%')
                    progress += percentage_gain
            ########################################################################
            scores.append(self.generate_score_for_simulation(sim))
        #Return to the next row in the console, if required.
        if percentage_gain < 8:
            print('')
        #Adjust for boards where both player and computer win. This just
        #reduces the scores of the perimeter scores by 10%.
        for i in self.subtract_scores_indices():
            scores[i] -= 0.1*scores[i]
        #The greatest score is the largest one. Returns the move with the greatest score.
        best_option_index = scores.index(max(scores))
        return list_of_options[best_option_index]

    def apply_computer_turn(self, optimal_turn):
        '''
        Changes the specified location on the board to an 'o'.
        '''
        self.game_board[optimal_turn[0]][optimal_turn[1]] = 'o'

def gain_valid_int_input(message):
    '''
    Validates a user input as an integer greater than 0.
    '''
    while True:
        try:
            vinput = int(input(message))
            if vinput < 1:
                print('Invalid input! Try again.\n')
                continue
            return vinput
        except:
            print('Invalid input! Try again.\n')

#Game start
if __name__ == "__main__":
    #Game setup.
    required_in_a_row_input = gain_valid_int_input('How many is required in a row to win? ')
    num_of_rows = gain_valid_int_input('How many rows for the game board? ')
    num_of_cols = gain_valid_int_input('How many columns for the game board? ')
    speed_turn_one = False
    while True:
        ask = input('Speed up computer\'s first turn? (yes/no) ')
        if ask == 'yes':
            speed_turn_one = True
            break
        elif ask == 'no':
            break
        else:
            print('Invalid input! Try again.\n')
    print('During your turn, type "help" for help.')
    print('Computer goes first!\n')
    board = Board(required_in_a_row_input, num_of_rows, num_of_cols, speed_turn_one)
    while True:
        board.apply_computer_turn(board.find_optimal_computer_turn())
        print('Computer takes turn:')
        board.print_current_board()
        if board.check_if_winner_exists():
            print('The computer won!!!')
            break
        if board.check_if_full_board():
            print('It\'s a draw!!!')
            break

        board.take_player_turn()
        if board.check_if_winner_exists():
            print('You won!!!')
            break
        if board.check_if_full_board():
            print('It\'s a draw!!!')
            break
