from GameFiles.MazeGame import MazeGame
from GameFiles.MazeGameGUI import MazeGUI
from GameFiles.Monster import Monster
from GameFiles.Player import Player
from GameFiles.GameElements import Treasure
from tkinter import messagebox
import tkinter as tk
def main():
    maze = MazeGame((55, 55))  # maze has to be at least 9 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
    maze.generate_maze()
    # maze.print_maze()

    player = Player(maze.game_state)

    monster = Monster(maze.game_state)

    Treasure(maze.game_state)

    Gui = MazeGUI(maze.game_state, monster)

    #print(maze.game_state)
def load_game():
    messagebox.showinfo("Load Game", "Loading game...")
def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Game Menu")

btn_new_game = tk.Button(root, text="Start a new game", command=main)
btn_load_game = tk.Button(root, text="Load", command=load_game)
btn_exit = tk.Button(root, text="Exit", command=exit_program)

btn_new_game.pack(pady=10)
btn_load_game.pack(pady=10)
btn_exit.pack(pady=10)

root.mainloop()
