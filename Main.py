from GameFiles.MazeGame import MazeGame
from GameFiles.MazeGameGUI import MazeGUI, MainMenu
from GameFiles.Monster import Monster
from GameFiles.Player import Player
from GameFiles.GameElements import GameElements


def generate_level(maze_size, nb_traps, level, save, retry):
    """
    to generate and initialize a game level
    Args:
        maze_size (tuple): The dimensions of the maze (width, height).
        nb_traps (int): The number of traps to place in the maze.
        level (int): The current game level.
        save (bool): Flag indicating whether to load a saved game state.
        retry (bool): Flag indicating whether the player is retrying the level

    Returns:
        The game and GUI objects
    """
    if retry:
        game = MazeGame()
        game.load_game()
        reset_level(game, level)
    else:
        if save:
            game = MazeGame(maze_size)
            game.load_game()
            print(game.game_state['life'] == 0)
            if game.game_state['life'] == 0:
                reset_level(game, level)
        else:
            game = MazeGame(maze_size)  # maze has to be at least 12 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
            game.generate_maze()

            game.game_state["level"] = level  # because if we load a game, the level is already saved

        player = Player(game.game_state, game)

        monster = Monster(game.game_state)

    GameElements(game.game_state, nb_traps)

    # Observer
    Gui = MazeGUI(game.game_state, monster, player)
    game.add_observer(Gui)
    player.add_observer(Gui)
    monster.add_observer(Gui)

    player.monster = monster

    Gui.mainloop()  # Blocks here until window is closed
    game.save_game()

    return game, Gui

def reset_level(game, level):
    game.game_state["life"] = 3  # reset life
    game.game_state["level"] = level

    player = Player(game.game_state, game)
    player.reset_position()

    monster = Monster(game.game_state)
    monster.reset_position()

    for trap in game.game_state['traps']:
        game.game_state['traps'][trap][0] = False  # reset every trap

def handle_level(maze_size=(12, 12), nb_traps=3, level=1, save=False, retry=False):
    """
    Args:
        maze_size (tuple): The dimensions of the maze (width, height). Defaults to (12, 12)
        nb_traps (int): The number of traps to place in the maze. Defaults to 3
        level (int): The current game level. Defaults to 1
        save (bool): Flag indicating whether to load a saved game state. (Defaults to False)
        retry (bool): Flag indicating whether the player is retrying the level. (Defaults to False)
    """
    game, gui = generate_level(maze_size, nb_traps, level, save, retry)

    if gui.clicked_button == 'retry':
        gui.destroy()
        handle_level(maze_size, nb_traps, game.game_state["level"], False, True)

    elif gui.clicked_button == 'nextlvl':
        gui.destroy()

        maze_size = (maze_size[0] + 1, maze_size[1] + 1)
        nb_traps += 2
        game.game_state["level"] = game.game_state["level"] + 1

        handle_level(maze_size, nb_traps, game.game_state["level"], False)

    elif gui.clicked_button == 'home':
        gui.destroy()
        handle_main_menu(game.game_state["level"])

def handle_main_menu(level):
    main_menu = MainMenu()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
        handle_level(save=save, level=level)

def main():
    main_menu = MainMenu()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
        handle_level(save=save)





if __name__ == "__main__":
    main()
