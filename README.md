2D game where players explore a randomly generated maze to find treasure while avoiding traps and
monster(s).
Non-Trivial Algorithmic Problem:
- Implementation of an algorithm for generating mazes procedurally
- use of shortest path algorithm for the monster to find the player
Graphical Interface:
- Creation of a graphical interface for navigating through the maze
- displaying life as multiple hearts (each trap that is activated or each time a monster touches
the player takes a heart)
- displaying level and time since the start of the level
Reading Files:
- read a csv file that saves the players data so that the game is the same as when we quit it
- read svg file for the maze’s walls, path, player, monster, treasure and traps
Use of a Data Structure:
- Use of dictionaries to represent the maze
- Use of dictionaries to represent treasure locations (treasures[treasure_number] =
coordinates), traps (traps[trap_number] = coordinates)
- Use of dictionaries to represent monster’s locations (monsters[monster_number] =
coordinates)
- Use of dictionary to save the player’s life, level, time taken for the current level, current
position of the monster, treasure, traps (and activated traps)
Systems:
- Difficulty: The higher the level, the bigger the labyrinth, more traps, and maybe more
monsters
- Bonuses: bonuses spawns that can add hearts
Steps:
1) The maze is generated randomly depending on the level
2) players spawns at a random location in the maze
3) traps are spawned at least at a distance that corresponds to 5% of the maze size. The
number of traps depends on the level. The position is chosen randomly in all the available
empty cases of the maze. They are visible to the player
4) The longest path starting from the player to any case in the maze is computed and the
monster spawns at the end of the longest path. The monster uses a shortest path algorithm
to get to the player
5) Finally, in the 2nd longest path that we calculated previously, the treasure is spawned at 80%
of it
Goal:
The player has to get to the treasure before losing his 3 hearts. To do so, he has to dodge
traps and the monster. Each time the monster reaches the player, the monster is teleported
somewhere else in the maze. If the player loses all 3 hearths, he restarts from level 1. If the player
get to the treasure before losing all 3 hearths, he gets to the next level.