from GameFiles.MazeGame import MazeGame
from GameFiles.MazeGameGUI import MazeGUI, MainMenu
from GameFiles.Monster import Monster
from GameFiles.Player import Player
from GameFiles.GameElements import GameElements


def generate_level(maze_size=(12, 12), nb_traps=3, save=False):  # (12, 12) is the default size
    if save:
        game = MazeGame(maze_size)
        game.load_game()
    else:
        game = MazeGame(
            maze_size)  # maze has to be at least 12 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
        game.generate_maze()
        # maze.print_maze()

    player = Player(game.game_state)

    monster = Monster(game.game_state)

    GameElements(game.game_state, nb_traps)

    Gui = MazeGUI(game.game_state, monster, player)

    game.gui = Gui

    player.gui = Gui
    player.monster = monster
    player.mazeGame = game

    monster.gui = Gui

    return game, Gui

def handle_level(save):
    game, Gui = generate_level((30, 30), 30, save=save)

    if Gui.clicked_button is not None:
        if Gui.clicked_button == 'retry':
            print('retry')
        elif Gui.clicked_button == 'nextlvl':
            print('nextlvl')
        elif Gui.clicked_button == 'home':
            print('home')

    Gui.mainloop()

    game.update_score()
    game.save_game()



def main():
    main_menu = MainMenu()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
        handle_level(save)




if __name__ == "__main__":
    main()
