from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        self.hold_game = False

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()  # Destroy the score frame
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        self.hold_game = False


    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def draw_winning_line(self, line_coords):
        x1, y1 = self.convert_logical_to_grid_position(line_coords[0])
        x2, y2 = self.convert_logical_to_grid_position(line_coords[1])
        self.canvas.create_line(x1, y1, x2, y2, width=10, fill="gold")

    def display_gameover(self):
        # Update scores based on the game result
        if self.X_wins:
            self.X_score += 1
            result_text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            result_text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            result_text = 'It\'s a Tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 6, font="cmr 40 bold", fill=color, text=result_text)

        self.score_frame = Frame(self.window, bg=Green_color)

        # Create a new frame to hold the score table
        #score_frame = Frame(self.window, bg=Green_color)
        self.score_frame.place(relx=0.5, rely=0.3, anchor="n")  # Centered with margin below result_text
    
        #score_frame.place(relx=0.5, rely=0.4, anchor="center")  # Position it in the middle

        # Title for the scores table
        Label(self.score_frame, text="Scores", font="cmr 35 bold", bg=Green_color, fg="white").grid(row=0, columnspan=2, pady=(0, 10))

        # Table headers
        Label(self.score_frame, text="Player", font="cmr 25 bold", bg=Green_color, fg="white", width=15, anchor="w").grid(row=1, column=0, padx=5)
        Label(self.score_frame, text="Score", font="cmr 25 bold", bg=Green_color, fg="white", width=5).grid(row=1, column=1, padx=5)

        # Player scores
        Label(self.score_frame, text="Player 1 (X)", font="cmr 20", bg=Green_color, fg="white", anchor="w", width=15).grid(row=2, column=0, padx=5, pady=5)
        Label(self.score_frame, text=str(self.X_score), font="cmr 20", bg=Green_color, fg="white", width=5).grid(row=2, column=1, padx=5, pady=5)

        Label(self.score_frame, text="Player 2 (O)", font="cmr 20", bg=Green_color, fg="white", anchor="w", width=15).grid(row=3, column=0, padx=5, pady=5)
        Label(self.score_frame, text=str(self.O_score), font="cmr 20", bg=Green_color, fg="white", width=5).grid(row=3, column=1, padx=5, pady=5)

        Label(self.score_frame, text="Tie", font="cmr 20", bg=Green_color, fg="white", anchor="w", width=15).grid(row=4, column=0, padx=5, pady=5)
        Label(self.score_frame, text=str(self.tie_score), font="cmr 20", bg=Green_color, fg="white", width=5).grid(row=4, column=1, padx=5, pady=5)

        # Play again message
        self.canvas.create_text(size_of_board / 2, size_of_board - 50, font="cmr 20 bold", fill="gray", text="Click to play again")
        self.reset_board = True
        self.hold_game = False


    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        return np.array(grid_position) // (size_of_board / 3)

    def check_winning_line(self, player):
        player = -1 if player == 'X' else 1
        for i in range(3):
            if all(self.board_status[i, :] == player):
                return [(i, 0), (i, 2)]
            if all(self.board_status[:, i] == player):
                return [(0, i), (2, i)]
        if self.board_status[0, 0] == self.board_status[1, 1] == self.board_status[2, 2] == player:
            return [(0, 0), (2, 2)]
        if self.board_status[0, 2] == self.board_status[1, 1] == self.board_status[2, 0] == player:
            return [(0, 2), (2, 0)]
        return None

    def is_gameover(self):
        self.X_wins = self.check_winning_line('X') is not None
        self.O_wins = self.check_winning_line('O') is not None
        self.tie = not (self.X_wins or self.O_wins) and not (self.board_status == 0).any()
        gameover = self.X_wins or self.O_wins or self.tie
        if gameover:            
            winning_line = self.check_winning_line('X') or self.check_winning_line('O')            
            if winning_line:
                self.draw_winning_line(winning_line)
                # Delay for 1 second before showing the score screen
                self.hold_game = True
                self.window.after(2000, self.display_gameover)
            else:
                self.display_gameover()
                
        return gameover

    def click(self, event):
        try:
            if self.hold_game == False:            
                grid_position = [event.x, event.y]
                logical_position = tuple(map(int, self.convert_grid_to_logical_position(grid_position)))
                if not self.reset_board:
                    if self.player_X_turns and not self.is_grid_occupied(logical_position):
                        self.draw_X(logical_position)
                        self.board_status[logical_position] = -1
                        self.player_X_turns = not self.player_X_turns
                    elif not self.player_X_turns and not self.is_grid_occupied(logical_position):
                        self.draw_O(logical_position)
                        self.board_status[logical_position] = 1
                        self.player_X_turns = not self.player_X_turns
                    if self.is_gameover():
                        print('Game Over...')
                        
                else:
                    self.canvas.delete("all")
                    self.play_again()
                    self.reset_board = False
        except:
            pass

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0], logical_position[1]] != 0

game_instance = Tic_Tac_Toe()
game_instance.mainloop()
