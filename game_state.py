import tkinter as tk
from tkinter import messagebox
import os
from tkinter.ttk import Style
import time
import random

def save_game(board, player_turn):
    with open("game_state.txt", "w") as file:
        for row in board:
            file.write(",".join(row) + "\n")
        file.write(f"Player Turn: {player_turn}\n")
    messagebox.showinfo("Game Saved", "Game state saved successfully!")

def load_game():
    if not os.path.exists("game_state.txt"):
        return None, 1
    with open("game_state.txt", "r") as file:
        lines = file.readlines()
        board = [line.strip().split(",") for line in lines[:3]]
        player_turn = int(lines[3].split(": ")[1])
        return board, player_turn

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "-":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "-":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
        return board[0][2]
    return None

def is_draw(board):
    for row in board:
        if "-" in row:
            return False
    return True

def animate_button(button):
    button["background"] = "yellow"
    button["activebackground"] = "yellow"
    root.update()
    time.sleep(0.2)
    button["background"] = "white"
    button["activebackground"] = "white"
    root.update()

def computer_move():
    global player_turn, board, buttons
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == "-"]
    if not empty_cells:
        return

    row, col = random.choice(empty_cells)
    board[row][col] = "O"
    buttons[row][col]["text"] = "O"
    animate_button(buttons[row][col])

    winner = check_winner(board)
    if winner:
        messagebox.showinfo("Game Over", f"Player {2 if winner == 'O' else 1} ({winner}) wins!")
        root.destroy()
        return

    if is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        root.destroy()
        return

    player_turn = 1
    label_turn["text"] = "Player 1's Turn (X)"

def on_button_click(row, col):
    global player_turn, board, buttons
    if board[row][col] != "-" or player_turn != 1:
        messagebox.showwarning("Invalid Move", "This cell is already occupied or not your turn!")
        return

    board[row][col] = "X"
    buttons[row][col]["text"] = "X"
    animate_button(buttons[row][col])

    winner = check_winner(board)
    if winner:
        messagebox.showinfo("Game Over", f"Player {1 if winner == 'X' else 2} ({winner}) wins!")
        root.destroy()
        return

    if is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        root.destroy()
        return

    player_turn = 2
    label_turn["text"] = "Computer's Turn (O)"
    root.after(1000, computer_move)

def save_and_exit():
    save_game(board, player_turn)
    root.destroy()

def start_game():
    global player_turn, board, buttons, label_turn, root

    # Load game state or initialize new game
    board, player_turn = load_game()
    if not board:
        board = [["-", "-", "-"] for _ in range(3)]
        player_turn = 1

    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.configure(bg="#282c34")

    label_turn = tk.Label(root, text=f"Player {player_turn}'s Turn ({'X' if player_turn == 1 else 'O'})", font=("Arial", 16), bg="#282c34", fg="white")
    label_turn.pack(pady=10)

    frame = tk.Frame(root, bg="#282c34")
    frame.pack()

    buttons = []
    for r in range(3):
        row_buttons = []
        for c in range(3):
            btn = tk.Button(frame, text="", font=("Arial", 24), width=5, height=2, relief="ridge", bd=3, bg="white",
                            activebackground="#61afef", activeforeground="#282c34",
                            command=lambda r=r, c=c: on_button_click(r, c))
            btn.grid(row=r, column=c, padx=5, pady=5)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    save_button = tk.Button(root, text="Save and Exit", font=("Arial", 12), bg="#98c379", fg="black",
                             activebackground="#282c34", activeforeground="white", command=save_and_exit)
    save_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_game()
