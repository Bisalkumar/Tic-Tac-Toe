import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar()
        self.num_games = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Player 1 (X) Name:").grid(row=0, column=0)
        tk.Label(self.root, text="Player 2 (O) Name:").grid(row=1, column=0)
        tk.Label(self.root, text="Number of Games:").grid(row=2, column=0)

        self.player1_entry = tk.Entry(self.root, textvariable=self.player1_name)
        self.player1_entry.grid(row=0, column=1)

        self.player2_entry = tk.Entry(self.root, textvariable=self.player2_name)
        self.player2_entry.grid(row=1, column=1)

        self.num_games_entry = tk.Entry(self.root, textvariable=self.num_games)
        self.num_games_entry.grid(row=2, column=1)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, columnspan=2)

    def start_game(self):
        player1 = self.player1_name.get()
        player2 = self.player2_name.get()
        num_games = self.num_games.get()

        if player1 == "" or player2 == "" or num_games == "":
            messagebox.showerror("Error", "All fields are required.")
            return

        if not num_games.isdigit():
            messagebox.showerror("Error", "Number of games must be a positive integer.")
            return

        self.root.destroy()
        self.play_games(player1, player2, int(num_games))

    def play_games(self, player1, player2, num_games):
        self.games_played = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.num_games_total = num_games
        self.show_game_board(player1, player2, num_games)

    def show_game_board(self, player1, player2, num_games):
        self.game_window = tk.Tk()
        self.game_window.title("Tic Tac Toe Game")

        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.game_window, text="", width=10, height=3,
                                                   command=lambda r=row, c=col: self.on_button_click(r, c, player1, player2))
                self.buttons[row][col].grid(row=row, column=col)

    def on_button_click(self, row, col, player1, player2):
        button = self.buttons[row][col]

        if button["text"] == "":
            button["text"] = self.current_player
            button["state"] = "disabled"

            if self.check_winner(row, col):
                if self.current_player == "X":
                    self.player1_wins += 1
                else:
                    self.player2_wins += 1
                self.games_played += 1
                self.update_scores(player1, player2, self.player1_wins, self.player2_wins, self.games_played)
                if self.games_played == self.num_games_total:
                    self.declare_final_winner(player1, player2)
                else:
                    self.reset_board()

            elif self.check_draw():
                self.games_played += 1
                self.update_scores(player1, player2, self.player1_wins, self.player2_wins, self.games_played)
                if self.games_played == self.num_games_total:
                    self.declare_final_winner(player1, player2)
                else:
                    self.reset_board()

            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, row, col):
        symbol = self.current_player

        # Check rows
        if all(self.buttons[row][c]["text"] == symbol for c in range(3)):
            return True

        # Check columns
        if all(self.buttons[r][col]["text"] == symbol for r in range(3)):
            return True

        # Check diagonals
        if all(self.buttons[i][i]["text"] == symbol for i in range(3)) or \
           all(self.buttons[i][2 - i]["text"] == symbol for i in range(3)):
            return True

        return False

    def check_draw(self):
        return all(button["text"] != "" for row in self.buttons for button in row)

    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button["text"] = ""
                button["state"] = "active"
        self.current_player = "X"

    def update_scores(self, player1, player2, player1_wins, player2_wins, games_played):
        score_label = tk.Label(self.game_window, text=f"{player1}: {player1_wins}  |  {player2}: {player2_wins}  |  Games Played: {games_played}/{self.num_games_total}")
        score_label.grid(row=3, columnspan=3)

    def declare_final_winner(self, player1, player2):
        final_winner = player1 if self.player1_wins > self.player2_wins else player2
        messagebox.showinfo("Final Winner", f"{final_winner} wins the series with {max(self.player1_wins, self.player2_wins)} out of {self.num_games_total} games!")
        self.game_window.destroy()
        self.root = tk.Tk()
        game = TicTacToeGame(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
