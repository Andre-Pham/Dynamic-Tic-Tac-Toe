
import tkinter as tk
import sys

from dynamic_tictactoe import *

# Define aesthetic interface constants
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
TEXT_COLOR_HIGHLIGHT = "white"
if sys.platform.startswith("darwin"):
    TEXT_COLOR_HIGHLIGHT = "black"
TEXTBOX_COLOR = "#d0d0d0"
BUTTON_COLOR = "#7e56fb"
FONT = "System"
SUCCESS_COLOR = "#22c95d"
FAIL_COLOR = "#ee4f4f"
LOAD_COLOR = "#ffad14"
BUTTON_WIDTH = 17

PLAYER_COLOR = "#00d95e"
COMPUTER_COLOR = "#d9005a"

def common_title(text):
    '''
    A label object with all consistent aesthetic features for titles used in the
    interface.
    '''
    return tk.Label(
        window,
        text=text,
        font=FONT,
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )

def common_button(text, command):
    '''
    A button object with all consistent aesthetic features for buttons used in
    the interface.
    '''
    return tk.Button(
        window,
        text=text,
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=BUTTON_COLOR,
        width=BUTTON_WIDTH,
        command=command
    )

def game_space(text, command):
    '''
    A button object with all consistent aesthetic features for buttons used in
    the interface.
    '''
    return tk.Button(
        window,
        text=text,
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=TEXTBOX_COLOR,
        width=10,
        height=3,
        command=command
    )

def common_text_input():
    '''
    A textbox object for text input with all consistent aesthetic features for
    texboxes used in the interface.
    '''
    return tk.Text(
        window,
        width=50,
        height=3,
        font=FONT,
        relief="flat",
        bg=TEXTBOX_COLOR,
        fg=TEXT_COLOR
    )

def common_text_output():
    '''
    A textbox object for text output with all consistent aesthetic features for
    textboxes used in the interface.
    '''
    return tk.Label(
        window,
        width=50,
        height=3,
        font=FONT,
        bg=TEXTBOX_COLOR,
        fg=TEXT_COLOR
    )

def common_board_space():
    '''
    A button object with all consistent aesthetic features for buttons used in
    the interface, which represents a board space (on the game board).
    '''
    return tk.Button(
        window,
        text=text,
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=BUTTON_COLOR,
        width=BUTTON_WIDTH,
        command=command
    )

def common_popup(title, message):
    '''
    A popup object with all consistent aesthetic features for popup boxes used
    in the interface.
    '''
    popup = tk.Toplevel()
    popup.geometry("350x100")
    popup.title(title)
    tk.Label(
        popup,
        text=message,
        font=FONT,
        height=3
    ).pack()
    tk.Button(
        popup,
        text="Close",
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=BUTTON_COLOR,
        width=BUTTON_WIDTH,
        command=popup.destroy
    ).pack()
    popup.mainloop()

class Interface:
    def __init__(self, window, geometry, title, bg):
        # Define interface object for the application
        self.window = window
        # Define list which tracks of all tkinter objects being displayed
        # on the interface (so that they can be removed when necessary)
        self.drawn_elements = []

        self.num_of_rows = 3
        self.num_of_cols = 3
        self.num_to_win = 3

        self.num_of_spaces = self.num_of_rows*self.num_of_cols

        self.board = None

        # Set properties of interface
        window.geometry(geometry)
        window.title(title)
        window.configure(bg=bg)

        # Set grid configurations of interface
        window.grid_rowconfigure(0, weight=0)
        window.grid_columnconfigure(0, weight=1)

        # Define tkinter elements for the main menu page
        self.main_menu_elements = [
            common_title("Main Menu"),
            common_button("Rows: 3", lambda: self.change_rows()),
            common_button("Columns: 3", lambda: self.change_cols()),
            common_button("To Win: 3", lambda: self.change_to_win()),
            common_button("START GAME", lambda: self.draw_game_board()),
            common_button("Quit", lambda: self.quit_interface()),
            common_title("*Maximum 20 board spaces allowed (9/20)")
        ]

        # Define tkinter elements for the game page
        self.game_board_elements = []

        self.game_board_additional_elements = [
            common_title("Objective: 3 in a row! (Computer's turn)"),
            common_text_output(),
            common_button("Back to Menu", lambda: self.draw_main_menu())
        ]

    # FUNCTIONS TO UPDATE AND CHANGE INTERFACE

    def quit_interface(self):
        '''
        Closes the application.
        '''
        window.destroy()
        popup.destroy()
        exit()

    def clear_all(self):
        '''
        Removes all elements from the interface.
        '''
        for elmt in self.drawn_elements:
            elmt.grid_forget()

    def draw_main_menu(self):
        '''
        Changes all elements on the interface to display main menu page.
        '''
        self.clear_all()
        self.drawn_elements = []

        window.geometry("450x255")

        for order, elmt in enumerate(self.main_menu_elements):
            elmt.grid(
                pady=5,
                row=order,
                column=0
            )
            self.drawn_elements.append(elmt)

        for row_num in range(self.num_of_rows):
            window.grid_rowconfigure(row_num, weight=0)
        for col_num in range(self.num_of_cols):
            window.grid_columnconfigure(col_num, weight=0)

        # Set grid configurations of interface
        window.grid_rowconfigure(0, weight=0)
        window.grid_columnconfigure(0, weight=1)

    def draw_game_board(self):
        '''
        Changes all elements on the interface to display 'text to visrep' page.
        '''
        self.clear_all()
        self.drawn_elements = []

        self.game_board_elements = []

        window.geometry(f"{self.num_of_cols*125}x{self.num_of_rows*155}")

        num_of_spaces = self.num_of_cols*self.num_of_rows
        for space_index in range(num_of_spaces):
            self.game_board_elements.append(game_space("", lambda space_index=space_index: self.take_player_turn(space_index)))

        num_placed_in_row = 0
        live_row = 0
        live_col = 0

        for elmt in self.game_board_elements:
            elmt.grid(
                padx=3,
                pady=3,
                row=live_row,
                column=live_col,
                sticky="nsew"
            )
            live_col += 1
            num_placed_in_row += 1
            self.drawn_elements.append(elmt)
            if num_placed_in_row == self.num_of_cols:
                live_row += 1
                live_col = 0
                num_placed_in_row = 0

        for index, elmt in enumerate(self.game_board_additional_elements):
            elmt.grid(
                padx=3,
                pady=3,
                row=self.num_of_rows+index,
                column=0,
                columnspan=self.num_of_cols,
                sticky="nsew"
            )
            window.grid_rowconfigure(self.num_of_rows+index, weight=0)
            self.drawn_elements.append(elmt)

        for row_num in range(self.num_of_rows):
            window.grid_rowconfigure(row_num, weight=1)
        for col_num in range(self.num_of_cols):
            window.grid_columnconfigure(col_num, weight=1)

        self.start_game()

    # FUNCTIONS THAT REACT TO USER INTERACTION

    def change_rows(self):
        if (self.num_of_rows+1)*self.num_of_cols > 20:
            self.num_of_rows = 3
        else:
            self.num_of_rows += 1

        self.main_menu_elements[1].config(
            text=f"Rows: {self.num_of_rows}"
        )

        self.main_menu_elements[6].config(
            text=f"*Maximum 20 board spaces allowed ({self.num_of_cols*self.num_of_rows}/20)"
        )

    def change_cols(self):
        if (self.num_of_cols+1)*self.num_of_rows > 20:
            self.num_of_cols = 3
        else:
            self.num_of_cols += 1

        self.main_menu_elements[2].config(
            text=f"Columns: {self.num_of_cols}"
        )

        self.main_menu_elements[6].config(
            text=f"*Maximum 20 board spaces allowed ({self.num_of_cols*self.num_of_rows}/20)"
        )

    def change_to_win(self):
        max_to_win = max(self.num_of_cols, self.num_of_rows)
        if self.num_to_win+1 > max_to_win:
            self.num_to_win = 3
        else:
            self.num_to_win += 1

        self.main_menu_elements[3].config(
            text=f"To Win: {self.num_to_win}"
        )

    def take_computer_turn(self):
        self.board.apply_computer_turn(self.board.find_optimal_computer_turn())

        space_index = 0
        for row in self.board.game_board:
            for space in row:
                if space == "x":
                    self.game_board_elements[space_index].configure(
                        text="x",
                        bg=PLAYER_COLOR
                    )
                elif space == "o":
                    self.game_board_elements[space_index].configure(
                        text="o",
                        bg=COMPUTER_COLOR
                    )
                space_index += 1

    def take_player_turn(self, space_index):
        flattened_board = self.board.flatten_board()
        print(space_index)
        if flattened_board.count("x") == flattened_board.count("o") or flattened_board[space_index] != "_":
            return

        column_index = int(space_index%self.num_of_cols)
        row_index = int((space_index - column_index)/self.num_of_cols)

        self.board.apply_player_turn(row_index, column_index)

        space_index = 0
        for row in self.board.game_board:
            for space in row:
                if space == "x":
                    self.game_board_elements[space_index].configure(
                        text="x",
                        bg=PLAYER_COLOR
                    )
                elif space == "o":
                    self.game_board_elements[space_index].configure(
                        text="o",
                        bg=COMPUTER_COLOR
                    )
                space_index += 1

        self.take_computer_turn()

    def start_game(self):
        self.board = Board(self.num_to_win, self.num_of_rows, self.num_of_cols, True)

        self.take_computer_turn()
        '''
        while True:

            space_index = 0
            for row in self.board.game_board:
                for space in row:
                    if space == "x":
                        self.game_board_elements[space_index].configure(
                            text="x"
                        )
                    elif space == "o":
                        self.game_board_elements[space_index].configure(
                            text="o"
                        )
                    space_index += 1

            board.apply_computer_turn(board.find_optimal_computer_turn())
            print('Computer takes turn:')
            board.print_current_board()
            if board.check_if_winner_exists():
                print('The computer won!!!')
                break
            if board.check_if_full_board():
                print('It\'s a draw!!!')
                break

            space_index = 0
            for row in self.board.game_board:
                for space in row:
                    if space == "x":
                        self.game_board_elements[space_index].configure(
                            text="x"
                        )
                    elif space == "o":
                        self.game_board_elements[space_index].configure(
                            text="o"
                        )
                    space_index += 1

            board.take_player_turn()
            if board.check_if_winner_exists():
                print('You won!!!')
                break
            if board.check_if_full_board():
                print('It\'s a draw!!!')
                break
        '''

# Set up window
window = tk.Tk()
interface = Interface(window, "450x255", "Dynamic Tic-Tac-Toe", BACKGROUND_COLOR)
interface.draw_main_menu()

# Run window
window.mainloop()
