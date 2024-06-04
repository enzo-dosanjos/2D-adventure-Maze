import random
import tkinter as tk
from PIL import ImageTk, Image
import math
from time import sleep


class MazeGUI(tk.Tk):
    """Class for creating a graphical user interface (GUI) for the maze game.

    Attributes:
        maze (Maze): The maze object to be displayed in the GUI.
        player (Player): The player object to be displayed in the GUI.
        monster (Monster): The monster object to be displayed in the GUI.
        cell_size (int): The size of each cell in pixels.
        player_image (tk.PhotoImage): The image representing the player.
        monster_image (tk.PhotoImage): The image representing the monster.
        treasure_image (tk.PhotoImage): The image representing the treasure.
    """

    def __init__(self, game_state, monster, player):
        """Initializes the MazeGUI class.

        Args:
            maze (Maze): The maze object to be displayed in the GUI.
        """
        super().__init__()
        self.game_state = game_state

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        self.monster = monster
        self.player = player

        # to adapt the display of the maze to the player's screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        if self.maze_size[0] > self.maze_size[1]:
            self.cell_size = math.floor(0.8*self.screen_width/self.maze_size[0])
        else:
            self.cell_size = math.floor(0.8*self.screen_height / self.maze_size[1])

        # Load images for game elements
        # characters
        self.player_sprite = Image.open("./data/player.png").convert("RGBA")  # RGBA to handle transparency
        self.monster_sprite = Image.open("./data/monster.png").convert("RGBA")

        # treasure
        self.treasure_sprite = Image.open("./data/treasure.png").convert("RGBA")

        # traps
        self.bear_trap_sprite = Image.open("./data/traps/Bear_Trap.png").convert("RGBA")
        self.fire_trap_sprite = Image.open("./data/traps/Fire_Trap.png").convert("RGBA")
        self.spike_trap_sprite = Image.open("./data/traps/Spike_Trap.png").convert("RGBA")
        self.traps = {}  # dict to store the traps canvas element

        # life
        self.life_sprite = Image.open("./data/HUD/life.png").convert("RGBA")
        self.lose_life_sprite = Image.open("./data/HUD/lose_life.png").convert("RGBA")

        self.title("Maze Game")

        self.main_window()


    def crop_images(self,  img, split, nb, type = 'perso'):
        """Crop given images to a certain part

       Args:
           img : Image to crop
           split (tuple) : number of parts in the image in height and width
           nb (tuple) : number of the wanted part in width and height
        """

        w, h = img.size

        left = (nb[0] - 1) * w / split[0]
        right = nb[0] * w / split[0]
        upper = (nb[1] - 1) * h / split[1]
        lower = nb[1] * h / split[1]

        crop_img = img.crop([left, upper, right, lower])

        if type == "perso":
            ratio_h = 1 / (h / (1.5 * self.cell_size))
            resized_img = crop_img.resize((int(w * ratio_h), int(h * ratio_h)))
        elif type == 'life':
            w_size = 0.1 * self.screen_width  # take 10% of the player's screen
            h_size = w_size / w * h / split[1]
            resized_img = crop_img.resize((int(w_size), int(h_size)))
        elif type == 'treasure':
            ratio_w = 1 / (w / (1.1 * self.cell_size))
            ratio_h = 1 / (h / (1.1 * self.cell_size))
            resized_img = crop_img.resize((int(w*ratio_w), int(h*ratio_h)))
        else:
            ratio_w = 1 / (w / self.cell_size)
            ratio_h = 1 / (h / self.cell_size)
            resized_img = crop_img.resize((int(w * ratio_w), int(h * ratio_h)))

        new_w, new_h = resized_img.size

        image = ImageTk.PhotoImage(resized_img)

        return image, new_w, new_h

    def main_window(self):
        """Main game window displaying the maze, hud, .."""
        self.canvas = tk.Canvas(self, width=self.maze_size[1] * self.cell_size,
                                height=self.maze_size[0] * self.cell_size)
        self.canvas.pack()

        self.bind('<Up>', self.player.move_player)
        self.bind('<Down>', self.player.move_player)
        self.bind('<Left>', self.player.move_player)
        self.bind('<Right>', self.player.move_player)

        self.draw_maze()

        self.draw_traps()
        self.draw_treasure()
        self.draw_player()
        self.draw_monster()

        self.draw_life()

    def draw_maze(self):
        """Draws the maze on the canvas."""
        # Load images for walls and paths
        self.w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bbot_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/full_bbottom_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # last line
        self.bbot_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bbottom_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bbot_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bbottom_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_l_bbot_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_left_bbottom_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_r_bbot_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_right_bbottom_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # first line
        self.ttop_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/ttop_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.ttop_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/ttop_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_l_ttop_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_left_ttop_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_r_ttop_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_right_ttop_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # first column
        self.ll_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/lleft_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.ll_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/lleft_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_lleft_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_lleft_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_lleft_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_lleft_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # last column
        self.rr_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/rright_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.rr_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/rright_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_rright_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_rright_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_rright_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_rright_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # corners
        self.tt_rr_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/ttop_rright_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.tt_ll_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/ttop_lleft_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bb_rr_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bbot_rright_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bb_ll_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bbot_lleft_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # vertical and horizontal walls
        self.bot_w_v_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bottom_wall_vertical.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_v_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_vertical.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # corners
        self.top_l_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/top_left_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.top_r_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/top_right_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bot_l_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bottom_left_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bot_r_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bottom_right_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.r_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/right_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.l_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/left_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.top_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/top_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.bot_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/bottom_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # group of walls
        self.l_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/left_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.r_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/right_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.f_top_l_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_left_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_r_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_right_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_l_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bottom_left_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_r_c_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bottom_right_corner.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.f_top_r_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_right_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_l_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_left_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_r_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_right_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_l_m_w_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_left_mid_wall.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.f_top_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_r_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_right_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_top_l_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_top_left_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.f_bot_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_r_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_right_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.f_bot_l_w_h_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/filled_bot_left_wall_horizontal.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.w_top_l = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_bot_l = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_bot_left_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_bot_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_bot_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.w_top_l_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_bot_l_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_bot_left_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_l_bot_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_bot_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_r_bot_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_right_bot_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_l_bot_l = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_bot_left_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_r_bot_l = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_right_bot_left_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.w_top_l_r_bot_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_right_bot_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_r_bot_l_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_right_bot_left_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_l_bot_l_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_bot_left_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))
        self.w_top_l_r_bot_l = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_right_bot_left_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        self.w_top_l_r_bot_l_r = ImageTk.PhotoImage(Image.open("./data/Maze_assets/wall_top_left_right_bot_left_right_hole.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        # path
        self.p_img = ImageTk.PhotoImage(Image.open("./data/Maze_assets/path.png").convert("RGBA").resize((self.cell_size, self.cell_size)))

        for i in range(self.maze_size[0]):
            for j in range(self.maze_size[1]):
                cell = self.maze[i][j]

                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                neighbors = cell.get_cell_neighbors(self.maze, self.maze_size, "any")

                if cell.type == "wall":
                    if 0 < cell.coord[0] < self.maze_size[0] - 1 and 0 < cell.coord[1] < self.maze_size[1] - 1:
                        # vertical wall
                        if neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_v_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_v_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "path" and neighbors[3].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bot_w_v_img)

                        # horizontal wall
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_h_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "path" and neighbors[2].type == "path" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_h_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_h_img)

                        # corners
                        elif neighbors[0].type == "path" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.top_l_c_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.top_r_c_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "path" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bot_r_c_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "path" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bot_l_c_img)

                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "path" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.r_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.l_m_w_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.top_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bot_m_w_img)

                        # filled horizontal
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_r_w_h_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_l_w_h_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_r_w_h_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_l_w_h_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_w_h_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_w_h_img)

                        # filled corners
                        elif neighbors[0].type == "path" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j+1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_l_c_img)
                        elif neighbors[0].type == "path" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_r_c_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "path" and neighbors[3].type == "path" and self.maze[i-1][j-1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_r_c_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "path" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_l_c_img)

                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "path" and self.maze[i-1][j-1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_r_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "wall" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_l_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "wall" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_r_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path" and self.maze[i+1][j+1].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_l_m_w_img)

                        # surrounded by walls
                        # no walls in the corners
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_r_bot_l_r)

                        # one wall in the corner
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_r_bot_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_r_bot_l)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_bot_l_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_r_bot_l_r)

                        # 2 walls in the corners
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_bot_l_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_bot_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_r_bot_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l_bot_l)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_r_bot_l)

                        # 3 walls in the corners
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_l)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_top_r)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_bot_l)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_bot_r)

                        # 4 walls in the corners
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)

                        # filled vertical
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_l_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path" and self.maze[i-1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_l_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j+1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_r_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall" and self.maze[i+1][j-1].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_r_m_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "wall" and neighbors[2].type == "wall" and neighbors[3].type == "path":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.l_w_img)
                        elif neighbors[0].type == "wall" and neighbors[1].type == "path" and neighbors[2].type == "wall" and neighbors[3].type == "wall":
                            self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.r_w_img)

                        else:
                            self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")  # in case I forgot a possible case
                    else:
                        if cell.coord != (0, 0) and cell.coord != (self.maze_size[0] - 1, 0) and cell.coord != (0, self.maze_size[1] - 1) and cell.coord != (self.maze_size[0] - 1, self.maze_size[1] - 1):
                            # bottom line
                            if cell.coord[1] == self.maze_size[1] - 1 and neighbors[0].type == "wall" and self.maze[i-1][j-1].type == "wall" and self.maze[i+1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bbot_w_img)
                            elif cell.coord[1] == self.maze_size[1] - 1 and neighbors[0].type == "wall" and self.maze[i-1][j-1].type == "wall" and self.maze[i+1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_l_bbot_w_img)
                            elif cell.coord[1] == self.maze_size[1] - 1 and neighbors[0].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_r_bbot_w_img)
                            elif cell.coord[1] == self.maze_size[1] - 1 and neighbors[0].type == "wall" and self.maze[i-1][j-1].type == "path" and self.maze[i+1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bbot_m_w_img)
                            elif cell.coord[1] == self.maze_size[1] - 1:
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bbot_w_img)

                            # top line
                            elif cell.coord[1] == 0 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "wall" and self.maze[i+1][j+1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)
                            elif cell.coord[1] == 0 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "wall" and self.maze[i+1][j+1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_l_ttop_w_img)
                            elif cell.coord[1] == 0 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_r_ttop_w_img)
                            elif cell.coord[1] == 0 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i+1][j+1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.ttop_m_w_img)
                            elif cell.coord[1] == 0:
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.ttop_w_img)

                            # left side
                            elif cell.coord[0] == 0 and neighbors[2].type == "wall" and self.maze[i+1][j+1].type == "wall" and self.maze[i+1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)
                            elif cell.coord[0] == 0 and neighbors[2].type == "wall" and self.maze[i+1][j+1].type == "path" and self.maze[i+1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_lleft_w_img)
                            elif cell.coord[0] == 0 and neighbors[2].type == "wall" and self.maze[i+1][j+1].type == "wall" and self.maze[i+1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_lleft_w_img)
                            elif cell.coord[0] == 0 and neighbors[2].type == "wall" and self.maze[i+1][j+1].type == "path" and self.maze[i+1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.ll_m_w_img)
                            elif cell.coord[0] == 0:
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.ll_w_img)

                            # right side
                            elif cell.coord[0] == self.maze_size[0] - 1 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "wall" and self.maze[i-1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)
                            elif cell.coord[0] == self.maze_size[0] - 1 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i-1][j-1].type == "wall":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_top_rright_w_img)
                            elif cell.coord[0] == self.maze_size[0] - 1 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "wall" and self.maze[i-1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bot_rright_w_img)
                            elif cell.coord[0] == self.maze_size[0] - 1 and neighbors[1].type == "wall" and self.maze[i-1][j+1].type == "path" and self.maze[i-1][j-1].type == "path":
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.rr_m_w_img)
                            elif cell.coord[0] == self.maze_size[0] - 1:
                                self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.rr_w_img)
                            else:
                                self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                        else:
                            # top left corner
                            if cell.coord == (0, 0):
                                if self.maze[i+1][j+1].type == "wall":
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)
                                else:
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.tt_ll_c_img)
                            # bottom left corner
                            elif cell.coord == (0, self.maze_size[0] - 1):
                                if self.maze[i+1][j-1].type == "wall":
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bbot_w_img)
                                else:
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bb_ll_c_img)
                            # top right corner
                            elif cell.coord == (self.maze_size[1] - 1, 0):
                                if self.maze[i-1][j+1].type == "wall":
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.w_img)
                                else:
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.tt_rr_c_img)
                            # bottom right corner
                            elif cell.coord == (self.maze_size[0] - 1, self.maze_size[1] - 1):
                                if self.maze[i-1][j-1].type == "wall":
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.f_bbot_w_img)
                                else:
                                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.bb_rr_c_img)

                else:
                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.p_img)


    def draw_player(self):
        """Draws the player character on the canvas."""
        self.player_image, self.player_w, self.player_h = self.crop_images(self.player_sprite, (4, 4), (1, 1))

        x, y = self.game_state['player_position'][0] * self.cell_size + 1.5*(self.cell_size/2 - self.player_w/2), self.game_state['player_position'][1] * self.cell_size + 1.5*(self.cell_size/2 - self.player_h/1.7)
        self.player_char = self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)

    def draw_monster(self):
        """Draws the monster on the canvas."""
        self.monster_image, self.monster_w, self.monster_h = self.crop_images(self.monster_sprite, (4, 4), (1, 1))

        x, y = self.game_state['monster_position'][0] * self.cell_size + 1.5*(self.cell_size/2 - self.monster_w/2), self.game_state['monster_position'][1] * self.cell_size + 1.5*(self.cell_size/2 - self.monster_h/1.7)
        self.monster_char = self.canvas.create_image(x, y, anchor=tk.NW, image=self.monster_image)

    def draw_traps(self):
        """Draws the traps on the canvas."""
        self.traps_imgs = {1: (self.bear_trap_sprite, 4), 2: (self.fire_trap_sprite, 14), 3: (self.spike_trap_sprite, 14)}  # associate a number to an image and the number of frames for the animation

        for trap_pos, [activated, type] in self.game_state['traps'].items():

            sprite, frames = self.traps_imgs[type]

            if not activated:
                trap_image, trap_w, trap_h = self.crop_images(sprite, (frames, 1), (1, 1), 'trap')
            else:
                trap_image, trap_w, trap_h = self.crop_images(sprite, (frames, 1), (frames, 1), 'trap')  # take the last image if it is already activated (for save loads)
            x, y = trap_pos[0] * self.cell_size, trap_pos[1] * self.cell_size + (self.cell_size/2 - trap_h/1.8)
            # Create the image on the canvas
            new_trap = self.canvas.create_image(x, y, anchor=tk.NW, image=trap_image)

            # Store the trap image and canvas object in a dictionaries. Needed to modify the image after
            self.traps[trap_pos] = [sprite, frames, trap_image, new_trap]

    def draw_treasure(self):
        """Draws the treasure on the canvas."""
        self.treasure_image, self.treasure_w, self.treasure_h = self.crop_images(self.treasure_sprite, (2, 1), (1, 1), 'treasure')

        x, y = self.game_state['treasure_position'][0] * self.cell_size + 2*(self.cell_size - self.treasure_w), self.game_state['treasure_position'][1] * self.cell_size + 1.5*(self.cell_size/2 - self.treasure_h/1.7)
        self.treasure = self.canvas.create_image(x, y, anchor=tk.NW, image=self.treasure_image)

    def draw_life(self):
        """Draws the treasure on the canvas."""
        life = self.game_state['life']
        self.life_image, _, _ = self.crop_images(self.life_sprite, (1, 4), (1, 4 - life), 'life')

        x, y = 0, self.game_state['maze_size'][0] * self.cell_size
        self.life_display = self.canvas.create_image(x, y, anchor=tk.SW, image=self.life_image)


    def update_player(self, player_direction, step=0):
        """Updates the GUI by drawing the player."""
        # get the row of the sprite corresponding to the direction
        corresponding_row = {'Up': 2, 'Down': 1, 'Left': 3, 'Right': 4}

        if step < 4:
            # Update player image
            self.player_image, _, _ = self.crop_images(self.player_sprite, (4, 4), (step + 1, corresponding_row[player_direction]))
            self.canvas.itemconfig(self.player_char, image=self.player_image)

            # Calculate target position
            x, y = (self.game_state['player_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_w / 2),
                    self.game_state['player_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_h / 1.7))
            # Calculate movement step
            if player_direction in ('Left', 'Right'):
                if player_direction == 'Right':
                    move_step_x = x + ((step/4) - 1)*self.cell_size
                else:
                    move_step_x = x - ((step/4) - 1)*self.cell_size
                move_step_y = y
            else:
                move_step_x = x
                if player_direction == 'Down':
                    move_step_y = y + ((step/4) - 1)*self.cell_size
                else:
                    move_step_y = y - ((step/4) - 1)*self.cell_size

            self.canvas.moveto(self.player_char, move_step_x, move_step_y)

            self.after(40, self.update_player, player_direction, step + 1)

        else:
            self.player_image, _, _ = self.crop_images(self.player_sprite, (4, 4), (1, corresponding_row[player_direction]))
            self.canvas.itemconfig(self.player_char, image=self.player_image)

            x, y = self.game_state['player_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_w / 2), \
                   self.game_state['player_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_h / 1.7)
            self.canvas.moveto(self.player_char, x, y)

    def update_monster(self, monster_direction, step=0):
        """Updates the GUI by drawing the monster."""
        # Get the row of the sprite corresponding to the direction
        corresponding_row = {'Up': 2, 'Down': 1, 'Left': 3, 'Right': 4}

        if step < 4:
            # Update monster image based on direction and step
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4),
                                                        (step + 1, corresponding_row[monster_direction]))
            self.canvas.itemconfig(self.monster_char, image=self.monster_image)

            # Calculate target position
            x, y = (
            self.game_state['monster_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_w / 2),
            self.game_state['monster_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_h / 1.7))

            # Calculate movement step
            if monster_direction in ('Left', 'Right'):
                if monster_direction == 'Right':
                    move_step_x = x + ((step / 4) - 1) * self.cell_size
                else:
                    move_step_x = x - ((step / 4) - 1) * self.cell_size
                move_step_y = y
            else:
                move_step_x = x
                if monster_direction == 'Down':
                    move_step_y = y + ((step / 4) - 1) * self.cell_size
                else:
                    move_step_y = y - ((step / 4) - 1) * self.cell_size

            self.canvas.moveto(self.monster_char, move_step_x, move_step_y)

            self.after(40, self.update_monster, monster_direction, step + 1)

        else:
            # reset to default monster image
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4),
                                                        (1, corresponding_row[monster_direction]))
            self.canvas.itemconfig(self.monster_char, image=self.monster_image)

            x, y = (
            self.game_state['monster_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_w / 2),
            self.game_state['monster_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_h / 1.7))
            self.canvas.moveto(self.monster_char, x, y)

    def update_traps(self, coord, step=0):
        """Updates the GUI by modifying the image of the trap when it is activated."""
        if step < self.traps[coord][1]:
            self.traps[coord][-2], _, _ = self.crop_images(self.traps[coord][0], (self.traps[coord][1], 1), (step+1, 1), 'trap')
            self.canvas.itemconfig(self.traps[coord][-1], image=self.traps[coord][-2])
            self.after(40, self.update_traps, coord, step+1)
        else:
            self.traps[coord][-2], _, _ = self.crop_images(self.traps[coord][0], (self.traps[coord][1], 1), (self.traps[coord][1], 1), 'trap')
            self.canvas.itemconfig(self.traps[coord][-1], image=self.traps[coord][-2])

    def update_treasure(self):
        """Updates the GUI by modifying the image of the treasure when it is oppened."""
        self.treasure_image, _, _ = self.crop_images(self.treasure_sprite, (2, 1), (2, 1), 'treasure')
        self.canvas.itemconfig(self.treasure, image=self.treasure_image)

    def update_life(self, step):
        """Updates the GUI by modifying the image of the life when the player loses a heart."""
        life = self.game_state['life']

        # Animate the lost of life by making the displayed hearts blink
        if step == 0:
            self.life_image, _, _ = self.crop_images(self.life_sprite, (1, 4), (1, 4 - life), 'life')
            self.canvas.itemconfig(self.life_display, image=self.life_image)
            self.after(100, self.update_life, 1)

        elif step == 1:
            self.life_image, _, _ = self.crop_images(self.lose_life_sprite, (1, 4), (1, 4 - life), 'life')
            self.canvas.itemconfig(self.life_display, image=self.life_image)
            self.after(100, self.update_life, 2)

        elif step == 2:
            self.life_image, _, _ = self.crop_images(self.life_sprite, (1, 4), (1, 4 - life), 'life')
            self.canvas.itemconfig(self.life_display, image=self.life_image)


    def end_game_menu(self, level, time_taken):
        """Displays the end game menu with level info and buttons to quit or continue.

        Args:
            level (int): The level reached by the player.
            time_taken (float): The time taken by the player to complete the level.
        """
        #todo
        #create a new window for the end game menu
        end_game_window = tk.Toplevel(self)
        end_game_window.title("End Game Menu")

        # labels to display level info and time taken
        level_label = tk.Label(end_game_window, text=f"Level: {level}")
        time_label = tk.Label(end_game_window, text=f"Time Taken: {time_taken} seconds")

        # quit or continue
        quit_button = tk.Button(end_game_window, text="Quit", command=self.quit)
        continue_button = tk.Button(end_game_window, text="Continue", command=end_game_window.destroy)

        #the widgets
        level_label.grid(row=0, column=0, padx=10, pady=5)
        time_label.grid(row=1, column=0, padx=10, pady=5)
        quit_button.grid(row=2, column=0, padx=10, pady=5)
        continue_button.grid(row=2, column=1, padx=10, pady=5)

        # Center the widow on the top of the screen
        end_game_window.geometry("+%d+%d" % (self.winfo_selfx() + 50, self.winfo_selfy() + 50))
        end_game_window.lift()
        end_game_window.attributes('-topmost', True)
    def draw_win_state(self):
        #todo
        #Draw winning representation on the canvas
        self.canvas.create_text(
            300, 300,
            text="Congratulations! You've Won!",
            font=("Arial", 24),
            fill="green"
        )

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Menu")

        self.window_width = self.winfo_screenwidth()
        self.window_height = self.winfo_screenheight()

        self.geometry(f"{self.window_width}x{self.window_height}")  # Taille de la fenêtre initiale

        self.clicked_button = "Quit"  # to get the clicked button at the end

        self.create_widgets()

        self.check_window_size()
        self.mainloop()

    def create_widgets(self):
        # Ajouter le Canvas principal
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Ajouter le fond d'écran
        self.background_image = ImageTk.PhotoImage(
            Image.open("./data/menus/background.png").resize((self.window_width, self.window_height)))
        self.background_label = self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Ajouter le titre du jeu
        self.title_image = ImageTk.PhotoImage(Image.open("./data/menus/logo.png").convert("RGBA").resize(
            (int(0.4 * self.window_width), int(0.4 * self.window_height))))
        self.title_label = self.canvas.create_image(self.window_width // 2, int(0.2 * self.window_height),
                                                    anchor='center', image=self.title_image)

        # Créer et positionner les boutons
        self.new_game_image_normal = ImageTk.PhotoImage(Image.open("./data/menus/play_button.png").convert("RGBA"))
        self.new_game_button = self.canvas.create_image(self.window_width // 2, int(0.5 * self.window_height),
                                                        anchor='center', image=self.new_game_image_normal)
        self.canvas.tag_bind(self.new_game_button, "<Enter>",
                             lambda e: self.on_hover(self.new_game_button, self.new_game_image_normal, 1.1))
        self.canvas.tag_bind(self.new_game_button, "<Leave>",
                             lambda e: self.on_leave(self.new_game_button, self.new_game_image_normal))
        self.canvas.tag_bind(self.new_game_button, "<Button-1>", lambda e: self.set_clicked_button("New Game"))

        self.continue_image_normal = ImageTk.PhotoImage(Image.open("./data/menus/continue_button.png").convert("RGBA"))
        self.continue_button = self.canvas.create_image(self.window_width // 2, int(0.6 * self.window_height),
                                                        anchor='center', image=self.continue_image_normal)
        self.canvas.tag_bind(self.continue_button, "<Enter>",
                             lambda e: self.on_hover(self.continue_button, self.continue_image_normal, 1.1))
        self.canvas.tag_bind(self.continue_button, "<Leave>",
                             lambda e: self.on_leave(self.continue_button, self.continue_image_normal))
        self.canvas.tag_bind(self.continue_button, "<Button-1>", lambda e: self.set_clicked_button("Continue"))

        self.quit_image_normal = ImageTk.PhotoImage(Image.open("./data/menus/Exit_button.png").convert("RGBA"))
        self.quit_button = self.canvas.create_image(self.window_width // 2, int(0.7 * self.window_height),
                                                    anchor='center', image=self.quit_image_normal)
        self.canvas.tag_bind(self.quit_button, "<Enter>",
                             lambda e: self.on_hover(self.quit_button, self.quit_image_normal, 1.1))
        self.canvas.tag_bind(self.quit_button, "<Leave>",
                             lambda e: self.on_leave(self.quit_button, self.quit_image_normal))
        self.canvas.tag_bind(self.quit_button, "<Button-1>", lambda e: self.set_clicked_button("Quit"))

    def on_hover(self, button, image, scale_factor):
        self.canvas.itemconfig(button, image=image)
        current_coords = self.canvas.coords(button)
        self.canvas.coords(button, current_coords[0], current_coords[1])
        new_width = int(self.canvas.bbox(button)[2] * scale_factor)
        new_height = int(self.canvas.bbox(button)[3] * scale_factor)
        image_resized = ImageTk.PhotoImage(Image.open(image.cget("file")).convert("RGBA").resize((new_width, new_height)))
        self.canvas.itemconfig(button, image=image_resized)

    def check_window_size(self):
        """continuously check the window size to resize element if needed"""
        self.update()  # need to update otherwise, the windows' width and height wouldn't change
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()

        # Redimensionner les éléments en fonction de la taille de la fenêtre
        self.resize_elements(self.window_width, self.window_height)

        # Vérifier la taille de la fenêtre toutes les 100 millisecondes
        self.after(100, self.check_window_size)

    def resize_elements(self, window_width, window_height):
        # Resize
        pass
        # self.title_image.(window_width, window_height)


        # # Repositionner les boutons
        # self.button_x = int((canvas_width - self.button_width) / 2)
        # self.start_y = int((canvas_height - (3 * self.button_height + 2 * self.button_spacing)) / 2)
        #
        # self.new_game_button.place(x=self.button_x, y=self.start_y, width=self.button_width,
        #                            height=self.button_height)
        # self.continue_button.place(x=self.button_x, y=self.start_y + self.button_height + self.button_spacing,
        #                            width=self.button_width, height=self.button_height)
        # self.quit_button.place(x=self.button_x, y=self.start_y + 2 * (self.button_height + self.button_spacing),
        #                        width=self.button_width, height=self.button_height)


    def set_clicked_button(self, button_name):
        self.clicked_button = button_name
        self.destroy()  # Exit mainloop after clicking