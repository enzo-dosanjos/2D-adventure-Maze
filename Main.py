from GameFiles.Maze import Maze
from GameFiles.MazeGameGUI import MazeGUI
from GameFiles.Monster import Monster
from GameFiles.Player import Player

def main():
    maze = Maze((55, 55))  # maze has to be at least 9 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
    maze.generate_maze()

    player = Player(maze)

    monster = Monster(maze, player)

    Gui = MazeGUI(maze, player, monster)




if __name__ == "__main__":
    main()