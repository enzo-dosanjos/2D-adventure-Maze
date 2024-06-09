import tkinter as tk
from PIL import ImageTk, Image
import math
from GameFiles.Observer_Observable_logic import Observer

class MazeGUI(tk.Tk, Observer):
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
        self.title("Daedalus Maze")

        # needed variables
        self.game_state = game_state

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        self.monster = monster
        self.player = player

        self.clicked_button = None

        # to adapt the display of the maze to the player's screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        if self.maze_size[0] > self.maze_size[1]:
            self.cell_size = math.floor(0.95*self.screen_width/self.maze_size[0])
        else:
            self.cell_size = math.floor(0.95*self.screen_height / self.maze_size[1])

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

    def update(self, message, *args):
        match message:  # equivalent to a if...elif...elif
            case "win":
                self.end_game_menu(True)
            case "lose":
                self.end_game_menu(False)
            case "move":
                self.update_player(*args)
            case "monster":
                self.update_monster(*args)
            case "trap":
                self.update_traps(*args)
            case "treasure":
                self.update_treasure()
            case "life":
                self.update_life()

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

    def update_life(self, step=0):
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

    def end_game_menu(self, win):
        """Displays the end game menu with level info and buttons to quit or continue."""
                # from the definition of the cell size in the initialisation
        if self.maze_size[0] > self.maze_size[1]:
            middle = 0.5*math.floor(0.95*self.screen_width)
        else:
            middle = 0.5*math.floor(0.95*self.screen_height)

        # wanted size for the end menu
        window_width = int(0.35 * self.screen_width)
        window_height = int(0.4 * self.screen_height)

        # get left and top dimension of the end menu
        background_x1 = int(middle - window_width/2)  # left
        background_y1 = int(middle - window_height/2)  # top

        # Rectangle as background for text and image
        rect_x1 = int(background_x1 + window_width * 0.2)  # left
        rect_y1 = int(background_y1 + window_height * 0.1)  # top
        rect_x2 = int(background_x1 + window_width * 0.8)  # right
        rect_y2 = int(background_y1 + window_height * 0.80)  # bottom
        self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill='#C77F40', outline='#C39159', width=self.screen_height/200)

        if not win:
            # game over text
            game_over_base_img = Image.open("./data/menus/gameover.png").convert("RGBA")
            game_over_img_w, game_over_img_h = game_over_base_img.size
            self.game_over_img = ImageTk.PhotoImage(game_over_base_img.resize((int(window_width * 0.6), int(window_width * 0.6 * game_over_img_h / game_over_img_w))))
            self.canvas.create_image(int(background_x1 + 0.5*window_width), int(background_y1 + 0.35*window_height), image=self.game_over_img)

            # Retry button
            retry_base_img = Image.open("./data/menus/retry_button.png").convert("RGBA")
            retry_base_img_w, retry_base_img_h = retry_base_img.size
            self.retry_img = ImageTk.PhotoImage(retry_base_img.resize((int(window_width * 0.35), int(window_width * 0.35 * retry_base_img_h / retry_base_img_w))))

            retry_btn = self.canvas.create_image(background_x1 + window_width*0.75, background_y1 + window_height*0.8, image=self.retry_img)
            self.canvas.tag_bind(retry_btn, "<Button-1>", lambda e: self.set_clicked_button("retry"))

        else:
            # win text
            win_base_img = Image.open("./data/menus/win.png").convert("RGBA")
            win_img_w, win_img_h = win_base_img.size
            self.win_img = ImageTk.PhotoImage(win_base_img.resize((int(window_width * 0.6), int(window_width * 0.6 * win_img_h / win_img_w))))

            self.canvas.create_image(int(background_x1 + 0.5 * window_width), int(background_y1 + 0.35 * window_height), image=self.win_img)

            # Next level button
            next_level_base_img = Image.open("./data/menus/nextlevel_button.png").convert("RGBA")
            next_level_base_img_w, next_level_base_img_h = next_level_base_img.size
            self.next_level_img = ImageTk.PhotoImage(next_level_base_img.resize((int(window_width * 0.35), int(window_width * 0.35 * next_level_base_img_h / next_level_base_img_w))))

            next_level_btn = self.canvas.create_image(background_x1 + window_width * 0.75, background_y1 + window_height * 0.8, image=self.next_level_img)
            self.canvas.tag_bind(next_level_btn, "<Button-1>", lambda e: self.set_clicked_button("nextlvl"))

        # Home button
        home_base_img = Image.open("./data/menus/home_button.png").convert("RGBA")
        home_base_img_w, home_base_img_h = home_base_img.size
        self.home_img = ImageTk.PhotoImage(home_base_img.resize(
            (int(window_width * 0.35), int(window_width * 0.35 * home_base_img_h / home_base_img_w))))
        home_btn = self.canvas.create_image(background_x1 + window_width*0.25, background_y1 + window_height*0.8, image=self.home_img)
        self.canvas.tag_bind(home_btn, "<Button-1>", lambda e: self.set_clicked_button("home"))

        # Display level and time taken
        font_size = int(min(window_width, self.screen_height) / 25)  # Dynamic font size
        self.canvas.create_text(background_x1 + window_width*0.33, background_y1 + window_height*0.65, text=f"Level: {self.game_state['level']}",
                                  font=("Arial", font_size), fill="white")
        self.canvas.create_text(background_x1 + window_width*0.62, background_y1 + window_height*0.65, text=f"Time: {round(self.game_state['score'])}s",
                                  font=("Arial", font_size), fill="white")

    def set_clicked_button(self, button_name):
        """ Handles button clicks and closes the modal window. """
        self.clicked_button = button_name

        # close the window
        self.quit()  # can't destroy otherwise, memory error


class MainMenu(tk.Tk):
    """
    Class to create a menu for a 2D maze adventure game.

    Attributes:
        window_width (int): The width of the window.
        window_height (int): The height of the window.
        clicked_button (str): The name of the clicked button.
        canvas (tk.Canvas): The canvas to hold the background and buttons.

        background_base_img (Image): The original background image.
        background_img_w (int): The width of the original background image. Used to keep proportionality
        background_img_h (int): The height of the original background image. Used to keep proportionality
        background_img (ImageTk.PhotoImage): The resized background image. Needed for the canvas
        background (int): The canvas ID of the background image. Needed for the canvas

        title_base_img (Image): The original title image.
        title_img_w (int): The width of the original title image. Used to keep proportionality
        title_img_h (int): The height of the original title image. Used to keep proportionality
        title_img (ImageTk.PhotoImage): The resized title image. Needed for the canvas
        title (int): The canvas ID of the title image. Needed for the canvas

        new_game_base_img (Image): The original "New Game" button image.
        new_game_img_w (int): The width of the original "New Game" button image. Used to keep proportionality
        new_game_img_h (int): The height of the original "New Game" button image. Used to keep proportionality
        new_game_img (ImageTk.PhotoImage): The resized "New Game" button image. Needed for the canvas
        new_game_btn (int): The canvas ID of the "New Game" button. Needed for the canvas

        continue_base_img (Image): The original "Continue" button image.
        continue_img_w (int): The width of the original "Continue" button image. Used to keep proportionality
        continue_img_h (int): The height of the original "Continue" button image. Used to keep proportionality
        continue_img (ImageTk.PhotoImage): The resized "Continue" button image. Needed for the canvas
        continue_btn (int): The canvas ID of the "Continue" button. Needed for the canvas

        quit_base_img (Image): The original "Quit" button image.
        quit_img_w (int): The width of the original "Quit" button image. Used to keep proportionality
        quit_img_h (int): The height of the original "Quit" button image. Used to keep proportionality
        quit_img (ImageTk.PhotoImage): The resized "Quit" button image. Needed for the canvas
        quit_btn (int): The canvas ID of the "Quit" button. Needed for the canvas
    """
    def __init__(self):
        """Initialize the MazeGameMenu class, setting up the main window and elements."""
        super().__init__()
        self.title("Daedalus Maze")

        self.window_width = self.winfo_screenwidth()
        self.window_height = self.winfo_screenheight()

        # Set the window geometry to full screen
        self.geometry(f"{self.window_width}x{self.window_height}")

        self.clicked_button = "Quit"  # to get the clicked button at the end

        self.create_widgets()

        self.check_window_size()
        self.mainloop()

    def create_widgets(self):
        """Create and configure the widgets for the game menu."""
        self.canvas = tk.Canvas(self, highlightthickness=False)  # to remove the border of the canvas
        self.canvas.pack(fill="both", expand=True)

        # background image
        self.background_base_img = Image.open("./data/menus/background.png")
        self.background_img_w, self.background_img_h =self.background_base_img.size  # need the size to resize while keeping proportion

        # to handle vertical and horizontal screens
        if int(self.window_height / self.background_img_h * self.background_img_w) < self.window_width:
            self.background_img = ImageTk.PhotoImage(self.background_base_img.resize((self.window_width, int(self.window_width / self.background_img_w * self.background_img_h))))  # height is computed according to width to keep proportions
        else:
            self.background_img = ImageTk.PhotoImage(self.background_base_img.resize((int(self.window_height / self.background_img_h * self.background_img_w), self.window_height)))  # width is computed according to height
        self.background = self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        # game title
        self.title_base_img = Image.open("./data/menus/logo.png").convert("RGBA")   # RGBA for the alpha channel transparency
        self.title_img_w, self.title_img_h = self.title_base_img.size
        self.title_img = ImageTk.PhotoImage(self.title_base_img.resize((int(0.45 * self.window_width), int(0.45 * self.window_width / self.title_img_w * self.title_img_h))))  # height is computed according to width
        self.title = self.canvas.create_image(int(0.5 * self.window_width), int(0.2 * self.window_height), anchor='center', image=self.title_img)


        # buttons
        # new game button
        self.new_game_base_img = Image.open("./data/menus/play_button.png").convert("RGBA")
        self.new_game_img_w, self.new_game_img_h = self.new_game_base_img.size
        self.new_game_img = ImageTk.PhotoImage(self.new_game_base_img.resize((int(0.15 * self.window_width), int(0.15 * self.window_width / self.new_game_img_w * self.new_game_img_h))))

        self.new_game_btn = self.canvas.create_image(int(0.5 * self.window_width), int(0.5 * self.window_height), anchor='center', image=self.new_game_img)
        # to change size when the button is hovered
        self.canvas.tag_bind(self.new_game_btn, "<Enter>", lambda e: self.on_hover(self.new_game_btn, self.new_game_base_img, self.new_game_img_w, self.new_game_img_h))
        self.canvas.tag_bind(self.new_game_btn, "<Leave>", lambda e: self.on_leave(self.new_game_btn, self.new_game_img))

        self.canvas.tag_bind(self.new_game_btn, "<Button-1>", lambda e: self.set_clicked_button("New Game"))

        # continue button
        self.continue_base_img = Image.open("./data/menus/continue_button.png").convert("RGBA")
        self.continue_img_w, self.continue_img_h = self.new_game_base_img.size
        self.continue_img = ImageTk.PhotoImage(self.continue_base_img.resize((int(0.15 * self.window_width), int(0.15 * self.window_width / self.continue_img_w * self.continue_img_h))))

        self.continue_btn = self.canvas.create_image(int(0.5 * self.window_width), int(0.6 * self.window_height), anchor='center', image=self.continue_img)
        # to change size when the button is hovered
        self.canvas.tag_bind(self.continue_btn, "<Enter>", lambda e: self.on_hover(self.continue_btn, self.continue_base_img, self.continue_img_w, self.continue_img_h))
        self.canvas.tag_bind(self.continue_btn, "<Leave>", lambda e: self.on_leave(self.continue_btn, self.continue_img))

        self.canvas.tag_bind(self.continue_btn, "<Button-1>", lambda e: self.set_clicked_button("Continue"))

        # quit button
        self.quit_base_img = Image.open("./data/menus/quit_button.png").convert("RGBA")
        self.quit_img_w, self.quit_img_h = self.quit_base_img.size
        self.quit_img = ImageTk.PhotoImage(self.quit_base_img.resize((int(0.15 * self.window_width), int(0.15 * self.window_width / self.quit_img_w * self.quit_img_h))))
        self.quit_btn = self.canvas.create_image(int(0.5 * self.window_width), int(0.7 * self.window_height), anchor='center', image=self.quit_img)
        # to change size when the button is hovered
        self.canvas.tag_bind(self.quit_btn, "<Enter>", lambda e: self.on_hover(self.quit_btn, self.quit_base_img, self.quit_img_w, self.quit_img_h))
        self.canvas.tag_bind(self.quit_btn, "<Leave>", lambda e: self.on_leave(self.quit_btn, self.quit_img))

        self.canvas.tag_bind(self.quit_btn, "<Button-1>", lambda e: self.set_clicked_button("Quit"))

    def on_hover(self, button, base_image, w, h):
        """Handle hover event to resize the button image."""
        new_width = int(0.15 * self.window_width * 1.05)
        new_height = int(0.15 * self.window_width / w * h * 1.05)
        self.new_img = ImageTk.PhotoImage(base_image.resize((new_width, new_height)))  # self because the canvas.itemconfig function needs it
        self.canvas.itemconfig(button, image=self.new_img)

    def on_leave(self, button, image):
        """Handle leave event to reset the button image."""
        self.canvas.itemconfig(button, image=image)

    def check_window_size(self):
        """continuously check the window size to resize element if needed"""
        self.update()  # need to update otherwise, the windows' width and height wouldn't change

        # check if the window size changed to avoid hovered button from resetting
        if self.window_width != self.winfo_width() or self.window_height != self.winfo_height():
            self.window_width != self.winfo_width()
            self.window_height = self.winfo_height()

            # resize elements according to the window's size
            self.resize_elements()

        # repeat every 200ms
        self.after(200, self.check_window_size)

    def resize_elements(self):
        """Resize and reposition elements based on the current window size."""
        # to handle vertical and horizontal screens
        if int(self.window_height / self.background_img_h * self.background_img_w) < self.window_width:
            self.background_img = ImageTk.PhotoImage(self.background_base_img.resize((self.window_width,
                                                                                      int(self.window_width / self.background_img_w * self.background_img_h))))  # height is computed according to width to keep proportions
        else:
            self.background_img = ImageTk.PhotoImage(self.background_base_img.resize((
                                                                                     int(self.window_height / self.background_img_h * self.background_img_w),
                                                                                     self.window_height)))  # width is computed according to height
        self.canvas.itemconfig(self.background, image=self.background_img)

        # Resize and move title
        self.title_img = ImageTk.PhotoImage(self.title_base_img.resize((int(0.45 * self.window_width), int(0.45 * self.window_width / self.title_img_w * self.title_img_h))))
        self.canvas.itemconfig(self.title, image=self.title_img)
        self.canvas.coords(self.title, int(0.5 * self.window_width), int(0.2 * self.window_height))

        # Resize and move buttons
        # new game button
        self.new_game_img = ImageTk.PhotoImage(self.new_game_base_img.resize(
            (int(0.15 * self.window_width), int(0.15 * self.window_width / self.new_game_img_w * self.new_game_img_h))))
        self.canvas.itemconfig(self.new_game_btn, image=self.new_game_img)
        self.canvas.coords(self.new_game_btn, int(0.5 * self.window_width), int(0.5 * self.window_height))

        # continue button
        self.continue_img = ImageTk.PhotoImage(self.continue_base_img.resize(
            (int(0.15 * self.window_width), int(0.15 * self.window_width / self.continue_img_w * self.continue_img_h))))
        self.canvas.itemconfig(self.continue_btn, image=self.continue_img)
        self.canvas.coords(self.continue_btn, int(0.5 * self.window_width), int(0.6 * self.window_height))

        # quit button
        self.quit_img = ImageTk.PhotoImage(self.quit_base_img.resize(
            (int(0.15 * self.window_width), int(0.15 * self.window_width / self.quit_img_w * self.quit_img_h))))
        self.canvas.itemconfig(self.quit_btn, image=self.quit_img)
        self.canvas.coords(self.quit_btn, int(0.5 * self.window_width), int(0.7 * self.window_height))



    def set_clicked_button(self, button_name):
        """Set the clicked button and close the window."""
        self.clicked_button = button_name
        self.destroy()  # destroy the window after clicking