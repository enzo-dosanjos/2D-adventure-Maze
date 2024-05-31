from GameFiles.MazeGame import MazeGame
from GameFiles.MazeGameGUI import MazeGUI
from GameFiles.Monster import Monster
from GameFiles.Player import Player
from GameFiles.GameElements import Treasure

def main():
    maze = MazeGame((15, 15))  # maze has to be at least 9 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
    maze.generate_maze()
    # maze.print_maze()

    player = Player(maze.game_state)

    monster = Monster(maze.game_state)

    Treasure(maze.game_state)

    Gui = MazeGUI(maze.game_state, monster, player)

    player.gui = Gui
    player.monster = monster
    player.mazeGame = maze

    monster.gui = Gui

    Gui.mainloop()

    #print(maze.game_state)




if __name__ == "__main__":
    main()