# Daedalus Maze

A 2D game where players explore a procedurally generated maze to find a treasure while avoiding traps and a dark echo of himself (a monster).

## Installation

To install the game, with a cmd in the directory you want to install the game in:
- clone the repo: git clone https://github.com/enzo-dosanjos/2D-adventure-Maze.git
- go in the game's directory: cd 2D-adventure-Maze
- install the required libraries: pip install -r requirements.txt
- Then, launch the game: python3 main.py

## Game Controls
Use the arrow keys to move in the maze (The player's character is the bright one).

## Levels Generation Steps
1) The maze is generated randomly depending on the level.
2) The player spawns at a random location in the maze
3) The euclidian distance from the player to any case in the maze is computed and the monster spawns at longest one. The monster uses a shortest path algorithm to get to the player
4) The treasure is spawned randomly in the maze
5) The traps are spawned at least at a distance that corresponds to 5% of the maze size. The number of traps depends on the level. The position is chosen randomly in all the available empty cases of the maze. Once they are activated, they cannot be activated a second time.

## Gameplay
The player spawns with 3 hearts. He has to get to the treasure before losing all his hearts. To do so, he has to dodge the traps and the monster. The monster moves at the same time as the player do so you have to think before each moves. Each time the monster reaches the player, the player loses a hearth and a new monster spawns. If the player walks on a trap he loses a hearth but so do the monster. The strategy is to dodge the traps and make the monster walk on traps that are blocking the way to the treasure by checking where the player should be for the monster to spawn at the wanted location. 
If the player loses all 3 hearths, he either has the choice to retry the game or to go to the main menu to restart from level 1. If the player get to the treasure before losing all 3 hearths, he either has the choice to get to the next level or go to the main menu.

If you want to continue from where you stopped last time, simply click the continue button in the main menu, the game is saved at all time.
