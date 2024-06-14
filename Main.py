from GameFiles.MazeGame import MazeGame
from GameFiles.MazeGameGUI import MazeGUI, MainMenu
from GameFiles.Monster import Monster
from GameFiles.Player import Player
from GameFiles.GameElements import GameElements


def generate_level(maze_size, nb_traps, level, save, retry):
    """
    Generate and initialize a game level, configuring the game_state based on input parameters

    Args:
        maze_size (tuple): Dimensions of the maze (width, height).
        nb_traps (int): Number of traps to place in the maze.
        level (int): Current game level.
        save (bool): indicate if a saved game_state should be loaded.
        retry (bool): indicate if the player is retrying the level.

    Returns:
        The game and GUI objects
    """
    if retry:
        game = MazeGame()
        game.load_game()
        player, monster = reset_level(game, level)
    else:
        if save:
            game = MazeGame(maze_size)
            game.load_game()
            if game.game_state['life'] == 0:
                player, monster = reset_level(game, level)
            else:
                player = Player(game.game_state, game)

                monster = Monster(game.game_state)
        else:
            game = MazeGame(maze_size)  # maze has to be at least 12 in height and length because the maze is surrounded by walls and needs to generate at least a path inside
            game.generate_maze()

            game.game_state["level"] = level  # because if we load a game, the level is already saved

            player = Player(game.game_state, game)

            monster = Monster(game.game_state)

    # Initialize the game elements
    GameElements(game.game_state, nb_traps)

    # Observer
    Gui = MazeGUI(game.game_state, monster, player)
    game.add_observer(Gui)
    player.add_observer(Gui)
    monster.add_observer(Gui)

    player.monster = monster

    Gui.mainloop()  # Start the GUI event loop, blocking until the window closes
    game.save_game()  # Save game state after window is closed

    return game, Gui

def reset_level(game, level):
    """
    Reset the game level to its initial state while retaining the same level settings.

    Args:
        game (MazeGame): The game object.
        level (int): The level number to reset.

    Returns:
        the player and monster objects after reset.
    """
    game.game_state["life"] = 3  # reset life
    game.game_state["level"] = level

    # reset the player's position
    player = Player(game.game_state, game)
    player.reset_position()

    # reset the monster's position
    monster = Monster(game.game_state)
    monster.reset_position()

    # reset every trap
    for trap in game.game_state['traps']:
        game.game_state['traps'][trap][0] = False

    return player, monster

def handle_level(maze_size=(12, 12), nb_traps=3, level=1, save=False, retry=False):
    """
    Handle the setup and continuation of game levels based on user interactions.

    Args:
        maze_size (tuple): Dimensions of the maze (width, height).
        nb_traps (int): Number of traps to place in the maze.
        level (int): Current game level.
        save (bool): indicate if a saved game_state should be loaded.
        retry (bool): indicate if the player is retrying the level.
    """
    # generate the level with the wanted parameters
    game, gui = generate_level(maze_size, nb_traps, level, save, retry)

    # Respond to player interactions in the GUI
    if gui.clicked_button == 'retry':
        gui.destroy()  # destroy the window because the mainloop is at the end of generate_level
        handle_level(maze_size, nb_traps, game.game_state["level"], False, True)

    elif gui.clicked_button == 'nextlvl':
        gui.destroy()

        maze_size = (maze_size[0] + 1, maze_size[1] + 1)  # the size increase when you go to the next level
        nb_traps += 2  # the number of traps increase by 2
        game.game_state["level"] = game.game_state["level"] + 1  # the level increase

        handle_level(maze_size, nb_traps, game.game_state["level"], False)

    elif gui.clicked_button == 'home':
        gui.destroy()
        handle_main_menu(game.game_state["level"])

def handle_main_menu(level):
    """
    Handle the main menu actions based on user choice.

    Args:
        level (int): Current level for gameplay continuation.
    """
    main_menu = MainMenu()
    main_menu.mainloop()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
            level = 1  # reset the level to 1 if the player clicks on play
        handle_level(save=save, level=level)

def main():
    """ Entry point of the game. Manages the initial game menu """
    main_menu = MainMenu()
    main_menu.mainloop()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
        handle_level(save=save)





if __name__ == "__main__":
    main()
