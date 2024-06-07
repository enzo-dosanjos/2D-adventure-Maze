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

    Gui.mainloop()

    return game, Gui

def retry_level():
    game = MazeGame((12, 12))  # default size, not needed
    game.load_game()

    game.game_state["life"] = 3  # reset life

    player = Player(game.game_state)
    game.game_state['player_position'] = player.init_player_pos()

    monster = Monster(game.game_state)
    game.game_state['monster_position'] = monster.init_monster_pos()

    GameElements(game.game_state, 5)  # default number of traps, not needed

    for trap in game.game_state['traps']:
        game.game_state['traps'][trap][0] = False  # reset every trap

    Gui = MazeGUI(game.game_state, monster, player)

    game.gui = Gui

    player.gui = Gui
    player.monster = monster
    player.mazeGame = game

    monster.gui = Gui

    Gui.mainloop()

    return game, Gui

def handle_level(maze_size, nb_traps, save):
    game, gui = generate_level(maze_size, nb_traps, save)

    if gui.clicked_button == 'retry':
        gui.destroy()  # need to destroy after getting the clicked button otherwise, can't fint the var in memory
        game.save_game()
        game, gui = retry_level()

    elif gui.clicked_button == 'nextlvl':
        gui.destroy()
        maze_size = (maze_size[0] + 1, maze_size[1] + 1)
        nb_traps += 2
        game.game_state["level"] = game.game_state["level"] + 1
        game.save_game()
        handle_level(maze_size, nb_traps, False)

    elif gui.clicked_button == 'home':
        gui.destroy()
        game.save_game()
        main()

    gui.mainloop()  # Blocks here until window is closed
    game.save_game()


def main():
    main_menu = MainMenu()
    if main_menu.clicked_button != "Quit":
        if main_menu.clicked_button == "Continue":
            save = True
        else:
            save = False
        initial_size = (12, 12)  # starting size
        initial_traps = 5  # starting number of traps
        handle_level(initial_size, initial_traps, save)





if __name__ == "__main__":
    main()
