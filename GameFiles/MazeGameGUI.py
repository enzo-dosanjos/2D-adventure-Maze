import tkinter as tk
from PIL import ImageTk, Image
import math


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

    def __init__(self, game_state, monster):
        """Initializes the MazeGUI class.

        Args:
            maze (Maze): The maze object to be displayed in the GUI.
        """
        super().__init__()
        self.game_state = game_state

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        self.monster = monster

        # to adapt the display of the maze to the player's screen size
        if self.maze_size[0] > self.maze_size[1]:
            screen_width = self.winfo_screenwidth()
            self.cell_size = math.floor(0.90*screen_width/self.maze_size[0])
        else:
            screen_height = self.winfo_screenheight()
            self.cell_size = math.floor(0.90*screen_height / self.maze_size[1])

        # Load images for game elements
        self.player_sprite = Image.open("./data/player.png").convert("RGBA")  # RGBA to handle transparency
        self.monster_sprite = Image.open("./data/monster.png").convert("RGBA")
        self.treasure_sprite = Image.open("./data/treasure.png").convert("RGBA")
        # self.trap_image = Image.open("./data/trap_image.png")
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

        ratio_w = 1/(w/(1.5*self.cell_size))
        ratio_h = 1 / (h / (1.5 * self.cell_size))

        crop_img = img.crop([left, upper, right, lower])

        if type == "perso":
            resized_img = crop_img.resize((int(w * ratio_h), int(h * ratio_h)))
        else:
            resized_img = crop_img.resize((int(w*ratio_w), int(h*ratio_h)))

        new_w, new_h = resized_img.size

        image = ImageTk.PhotoImage(resized_img)

        return image, new_w, new_h

    def main_window(self):
        """Main game window displaying the maze, hud, .."""
        self.canvas = tk.Canvas(self, width=self.maze_size[1] * self.cell_size,
                                height=self.maze_size[0] * self.cell_size)
        self.canvas.pack()

        self.bind('<KeyPress>', self.move_player)

        self.draw_maze()

        self.draw_player()
        self.draw_monster()
        self.draw_treasure()

        self.mainloop()

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

    def draw_treasure(self):
        """Draws the treasure on the canvas.

        Args:
            position (tuple): The position of the treasure in the maze (row, column).
        """
        self.treasure_image, self.treasure_w, self.treasure_h = self.crop_images(self.treasure_sprite, (2, 1), (1, 1), 'treasure')

        x, y = self.game_state['Treasure_position'][0] * self.cell_size + 1.5*(self.cell_size/2 - self.treasure_w/2), self.game_state['Treasure_position'][1] * self.cell_size + 1.5*(self.cell_size/2 - self.treasure_h/1.7)
        self.treasure = self.canvas.create_image(x, y, anchor=tk.NW, image=self.treasure_image)

    def move_player(self, event):   #todo: change name and description
        """Change the player's character's coordinates depending on the player's input.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """
        x, y = self.game_state['player_position']
        if event.keysym == 'Up':
            new_position = (x, y - 1)
            self.player_image, _, _ = self.crop_images(self.player_sprite, (4, 4), (1, 2))
        elif event.keysym == 'Down':
            new_position = (x, y + 1)
            self.player_image, w, h = self.crop_images(self.player_sprite, (4, 4), (1, 1))
        elif event.keysym == 'Left':
            new_position = (x - 1, y)
            self.player_image, w, h = self.crop_images(self.player_sprite, (4, 4), (1, 3))
        elif event.keysym == 'Right':
            new_position = (x + 1, y)
            self.player_image, w, h = self.crop_images(self.player_sprite, (4, 4), (1, 4))
        else:
            new_position = self.game_state['player_position']

        if self.maze[new_position[0]][new_position[1]].type != 'wall':
            self.game_state['player_position'] = new_position

        prev_monster_pos = self.monster.move()

        # to change monster's image according to its direction
        if prev_monster_pos[0] < self.game_state['monster_position'][0]:
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4), (1, 4))
        elif prev_monster_pos[0] > self.game_state['monster_position'][0]:
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4), (1, 3))
        elif prev_monster_pos[1] > self.game_state['monster_position'][1]:
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4), (1, 2))
        elif prev_monster_pos[1] < self.game_state['monster_position'][1]:
            self.monster_image, _, _ = self.crop_images(self.monster_sprite, (4, 4), (1, 1))

        self.canvas.itemconfig(self.player_char, image=self.player_image)
        self.canvas.itemconfig(self.monster_char, image=self.monster_image)

        self.update_player()
        self.update_monster()


    def update_player(self):
        """Updates the GUI by drawing player.

        Args:
            player_position (tuple): The position of the player in the maze (row, column).
        """
        x, y = self.game_state['player_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_w / 2), self.game_state['player_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.player_h / 1.7)
        self.canvas.moveto(self.player_char, x, y)

    def update_monster(self):
        """Updates the GUI by drawing the monster."""
        x, y = self.game_state['monster_position'][0] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_w / 2), self.game_state['monster_position'][1] * self.cell_size + 1.5 * (self.cell_size / 2 - self.monster_h / 1.7)
        self.canvas.moveto(self.monster_char, x, y)

    def update_treasure(self):
        """Updates the GUI by modifying the image of the treasure when it is oppened.
        """

    def end_game_menu(self, level, time_taken):
        """Displays the end game menu with level info and buttons to quit or continue.

        Args:
            level (int): The level reached by the player.
            time_taken (float): The time taken by the player to complete the level.
        """
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
        end_game_window.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        end_game_window.lift()
        end_game_window.attributes('-topmost', True)
    def draw_win_state(self):
        # Draw winning representation on the canvas
        self.canvas.create_text(
            300, 300,
            text="Congratulations! You've Won!",
            font=("Arial", 24),
            fill="green"
        )
