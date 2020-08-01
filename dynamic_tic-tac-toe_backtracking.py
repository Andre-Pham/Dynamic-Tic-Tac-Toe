
import copy
import math

help_message = \
'''
Moves should be in the form "row, column".
So if you wanted to go to the first row, first column,
you'd type "1, 1"
'''

def flatten_board(board):
    '''
    Empties nested lists into a flat list and returns it.
    '''
    return [element for sublist in board for element in sublist]

def check_if_winner_exists(board, required_in_a_row, competitor = 'either'):
    '''
    Checks if there is a certain number of elements in a row on the board,
    that be vertically, horizontally or diagonally. If so, it returns True.
    Otherwise, it returns False.
    '''
    #Check for X in a row, horizontally.
    for row in board:
        for index in range(len(row)):
            for i in range(required_in_a_row):
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
                if i == required_in_a_row-1:
                    return True
    #Check for X in a row, vertically.
    columns = list(zip(*board))
    for column in columns:
        for index in range(len(column)):
            for i in range(required_in_a_row):
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
            if i == required_in_a_row-1:
                return True
    #Check for diagonals.
    for index1 in range(len(board)):
        for index2 in range(len(board[0])):
            diagonal_SE = True #South East
            diagonal_SW = True #South West
            for i in range(required_in_a_row):
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

def check_if_full_board(board):
    '''
    Checks if game is a draw by checking if any of the board values are
    '_'. If any are, the game isn't over. Otherwise, all values are
    either 'o' or 'x' and hence the game is over, with a draw.
    '''
    flattened_board = flatten_board(board)
    for i in flattened_board:
        if i == '_':
            return False
    return True

def create_board(num_rows, num_cols):
    '''
    Creates a board according to speficied number of columns and rows.
    Every coordinate is '_'. Returns the board created.
    '''
    return [['_' for i in range(num_cols)] for x in range(num_rows)]

def apply_player_turn(board, row, col):
    '''
    Changes speficied column and row value (both starting at 1) to 'x'.
    '''
    board[row-1][col-1] = 'x'

def print_current_board(board):
    '''
    Takes the current board and prints it in the console in a more readable
    format.
    '''
    board_print = copy.deepcopy(board)
    #Prints the numbers of the columns.
    print('   ' + '  '.join([str(i+1) for i in range(len(board_print[0]))]))
    #Prints the numbers of the rows, and the actual rows.
    for num, row in enumerate(board_print):
        print(f'{str(num+1)}  {"  ".join(row)}')
    #Prints an extra return.
    print('')

def take_player_turn(board):
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
            print(help_message)
            continue
        try:
            row = int(player_input.split(', ')[0])
            column = int(player_input.split(', ')[-1])
            if board[row-1][column-1] != '_':
                print('Invalid entry! Place taken. Try again.\n')
                continue
            break
        except:
            print('Invalid entry! Invalid formatting. Try again.\n')
    #Applies their turn to the board.
    apply_player_turn(board, row, column)
    #Prints the current board.
    print_current_board(board)

def generate_all_computer_options(board):
    '''
    Generates a list of coordinates that the computer can take its next turn
    at. For example, [[0, 1], [0, 2]].
    This is done by finding all the coordinates on the board that have a value
    of an integer. If they're an integer, they must not be taken by an 'x' or
    'o', meaning the computer can take its turn there.
    '''
    computer_options = []
    for row_index, row in enumerate(board):
        for col_index in range(len(row)):
            if board[row_index][col_index] == '_':
                computer_options.append([row_index, col_index])
    return computer_options

def simulate_computer_turn(board, row, col):
    '''
    Simulates a deep copy of the current board and applies an 'o' as the
    computer's turn at the given coordinates.
    '''
    copy_board = copy.deepcopy(board)
    copy_board[row][col] = 'o'
    return copy_board

def simulate_all_computer_turns(board):
    '''
    Using the coordinates for possible turns found by
    generate_all_computer_options(), it goes through each one and creates a
    copy of the board with that coordinate applied as a turn, then adds
    all the boards into a list.
    '''
    all_computer_turns = []
    computer_options = generate_all_computer_options(board)
    for coordinate in computer_options:
        all_computer_turns.append(simulate_computer_turn(board, coordinate[0], coordinate[1]))
    return all_computer_turns

def simulate_outcomes(partial, required_in_a_row, computer_or_player_winning):
    '''
    This take a board, and simulates every possible combination of outcomes
    and then returns the total outcomes where the computer wins.
    '''
    def options(partial):
        '''
        Returns every possible next board state in a list, accounting for who's
        turn it is. So if its the computer's turn, it makes a list of all
        the boards that could exist after the computer takes its next turn.
        '''
        #If its already game over, there are no moves to be made.
        if check_if_winner_exists(partial, required_in_a_row):
            return []
        #If the number of 'x's is equal to the number of 'o's, its the computer's turn.
        flattened_board = flatten_board(partial)
        if flattened_board.count('x') == flattened_board.count('o'):
            virtual_turn = 'o'
        else:
            virtual_turn = 'x'
        #Goes through every element on board. If its an integer, that is a coordinate
        #where the computer/player can take its next turn, hence a copy of the board
        #with that move applied is created and added to the list to be returned.
        returned_options = []
        for index1, row in enumerate(partial):
            for index2, element in enumerate(row):
                if element == '_':
                    board_copy = copy.deepcopy(partial)
                    board_copy[index1][index2] = virtual_turn
                    returned_options.append(board_copy)
        return returned_options

    #Backtracking method using recursion.
    if check_if_winner_exists(partial, required_in_a_row, computer_or_player_winning):
        return [partial]
    else:
        output = []
        for augmented in options(partial):
            output += simulate_outcomes(augmented, required_in_a_row, computer_or_player_winning)
        return output

def remove_duplicates_and_count(vlist):
    '''
    Removes the duplicates from a list, and returns its length.
    (Could not use a more efficient method due to nested lists being used)
    '''
    filtered_list = []
    for num in vlist:
        if num not in filtered_list:
            filtered_list.append(num)
    return len(filtered_list)

def num_filtered_outcomes(board, required_in_a_row, computer_or_player_winning):
    '''
    Removes all the duplicates from the list of possible future outcomes that
    were simulated, then returns the length of the list.
    If computer_or_player_winning is 'computer', it returns the number of outcomes
    where the computer wins. If computer_or_player_winning is 'player', it returns
    the number of outcomes where the player wins (i.e. the computer loses).
    '''
    computer_outcomes = simulate_outcomes(board, required_in_a_row, computer_or_player_winning)
    return remove_duplicates_and_count(computer_outcomes)

def find_optimal_computer_turn(board, required_in_a_row):
    '''
    Finds the optimal computer turn in the form of coordinates for its next
    moves, based on its list of options and scores associated with them. The
    scores are equal to: (number of future outcomes where computer wins after
    making that move - number of future outcomes where computer loses after
    making that move).
    '''
    #Find all the options in coodinate form for the computer's next move.
    list_of_options = generate_all_computer_options(board)
    #Find all the simulations in board form for the computer's next move.
    list_of_options_simulated = simulate_all_computer_turns(board)
    #For every simulation found, if a winner exists, it must be the computer,
    #because it's the computer's turn. Hence the optimal move is the move that lead
    #to that winning simulation, which is the winning move for the computer.
    for simulation in list_of_options_simulated:
        if check_if_winner_exists(simulation, required_in_a_row):
            return list_of_options[list_of_options_simulated.index(simulation)]
    #This is for the showing the player the computer's progress in deciding.
    percentage_gain = math.floor(100/len(list_of_options))
    percentage_progress = 0
    #Generates every score for every move in the same index as the respective move.
    scores = []
    for simulation in list_of_options_simulated:
        print(f'Computer thinking... {percentage_progress}%')
        scores.append( \
            num_filtered_outcomes(simulation, required_in_a_row, 'computer') \
            - num_filtered_outcomes(simulation, required_in_a_row, 'player'))
        percentage_progress += percentage_gain
    #The greatest score is the largest one. Returns the move with the greatest score.
    best_option_index = scores.index(max(scores))
    return list_of_options[best_option_index]

def apply_computer_turn(board, optimal_turn):
    '''
    Changes the specified location on the board to an 'o'.
    '''
    board[optimal_turn[0]][optimal_turn[1]] = 'o'

def gain_valid_int_input(message):
    '''
    Validates a user input as an integer.
    '''
    while True:
        try:
            return int(input(message))
            break
        except:
            print('Invalid input! Try again.\n')

#Game start
if __name__ == "__main__":
    #Game setup.
    required_in_a_row_input = gain_valid_int_input('How many is required in a row to win? ')
    num_of_rows = gain_valid_int_input('How many rows for the game board? ')
    num_of_cols = gain_valid_int_input('How many columns for the game board? ')
    game_board = create_board(num_of_rows, num_of_cols)
    print('During your turn, type "help" for help.')
    print('Computer goes first!\n')
    #Loops until game is over.
    while True:
        apply_computer_turn(game_board, find_optimal_computer_turn(game_board, required_in_a_row_input))
        print('\nComputer takes turn:')
        print_current_board(game_board)
        if check_if_winner_exists(game_board, required_in_a_row_input):
            print('The computer won!!!')
            break
        if check_if_full_board(game_board):
            print('It\'s a draw!!!')
            break

        take_player_turn(game_board)
        if check_if_winner_exists(game_board, required_in_a_row_input):
            print('You won!!!')
            break
        if check_if_full_board(game_board):
            print('It\'s a draw!!!')
            break
