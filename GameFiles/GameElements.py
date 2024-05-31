import random
class GameElements:
    def __init__(self, nb_traps):
        """Initialize every game elements in the maze

        Attributes:
            nb_traps (int): The number of traps in the game.
        """

        self.nb_traps = nb_traps

        self.traps = []
        for i in range(nb_traps):
            self.traps.append(Trap(self.traps))

        self.treasure = Treasure()

class Trap:
    """Class representing a trap.

    Attributes:
        trap_position (tuple): The position of the trap in the maze.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, list_traps):
        """Initialize the Trap instance.

        Slots:
            activated (Boolean): the status of the trap set to disactivated.

        """
        super().__init__()
        self.traps = list_traps
        self.trap_position = self.init_trap_position()
        self.activated = False

    def init_trap_position(self):
        """spawns a trap at a random position in the maze.

        Return
            trap_posi (list) = The list containing the position of the coordinates of the traps.
        """
        trap_posi = []
       
        max_distance = (5 * self.maze.maze_size)/100
        player_position = self.player.position
        if trap not in self.traps:
            for i in range(len(self.maze.maze)):
                for j in range(len(self.maze.maze[0])):
                    # trap position inside maze 
                    if self.maze.maze[i][j].type != 'wall':
                        # find randomly genrated position in maze not on walls!
                        distance = math.sqrt((i - player_position[0]) ** 2 + (j - player_position[1]) ** 2)
                        if distance <= max_distance:
                            trap_posi = [random.randint(player_position[i] - max_distance, max_distance + player_position[i]),random.randint(player_position[i][j] - max_distance, max_distance + player_position[i][j])]
                            
        return trap_posi

    def activate_trap(self, player, maze_size, traps):
        """Determine when the trap is activated.
        Return:
            activated (Boolean): The status of the trap set to activated (True) or not (False).

        """
        dist = ((player.position[0] - self.trap_position[0]) ** 2 + (player.position[1] - self.trap_position[1]) ** 2) ** 0.5
        if dist <= 5 * self.maze_size / 100:
             self.activated = True
        return self.activated



class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        treasure_position (tuple): The position of the treasure in the maze.
    """

    def __init__(self, game_state):
        """Initialize the Treasure instance.

        Args:
            treasure_position (tuple): The position of the treasure in the maze.

        """
        super().__init__()
        self.game_state = game_state
        game_state['Treasure_position'] = self.init_treasure_position()


    def init_treasure_position(self):
        """Spawns the treasure at a random position in the maze, taking care that it doesn't appear on walls.

        Returns:
            (x,y) (tuple): position of the treasure in the maze as a tuple of x position and y position.
        """
        x = 0
        y = 0
        while self.game_state['maze'][x][y].type != 'path':
            x = random.randint(0, self.game_state['maze_size'][0] - 1)
            y = random.randint(0, self.game_state['maze_size'][1] - 1)
        return (x, y)
        
                    

    def treasure_reached(self, player, gui):
        """When the treasure is reached."""
        if player.position == self.treasure_position:
            gui.draw_win_state()
