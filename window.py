
from math import cos, sin, pi
import pygame

class Window:
    """ Class used to manage creating & drawing to the program's window. """
    def __init__(self, config):
        self.width = config.window_size[0]
        self.height = config.window_size[1]
        # pygame.init()
        # pygame.font.init()
        self.surface = pygame.display.set_mode(config.window_size)
        pygame.display.set_caption(config.application_title)
        # Generate and store all fonts of size 1-32.
        self.fonts = {f: pygame.font.SysFont('Ubuntu',f) for f in range(1,33)}

    def write(self, text, size, offset):
        """ Write an object to the screen. """
        font = self.fonts[size]
        self.surface.blit(font.render(text, True, (128, 128, 128)), offset)

    def draw_dialog_box(self, title, config, offset, size):
        width = 4
        box = pygame.Rect(offset, size)
        inner_border = pygame.Rect((offset[0]+width,offset[1]+width),(size[0]-width*2,size[1]-width*2))
        title_coord = (offset[0]+width+6, offset[1]+width+2)
        query_coord = (offset[0]+width+6, offset[1]+width+40)
        # Draw the background for the box.
        pygame.draw.rect(self.surface, config.color_bg, box)
        # Draw the border for the box.
        pygame.draw.rect(self.surface, config.color_fg, box, 1)
        pygame.draw.rect(self.surface, config.color_fg, inner_border, 1)
        self.write(title, 26, title_coord)
        self.write(config.query, 22, query_coord)

    def write_list(self, sentence, size, offset, spacing):
        """ Convenience wrapper for write() that repeatedly writes elements of
            a list to the screen. Allows for adjustable padding between
            elements.
        """
        font = self.fonts[size]
        if sentence == None:
            return
        for n, text in enumerate(sentence):
            if text == None:
                continue
            else:
                location = (offset[0]+n*spacing,offset[1])
                self.surface.blit(font.render(str(text), True, (128, 128, 128)), location)

    def draw_graph(self, data, offset, size):
        """ Attempt to build a useful graph. """
        y_scale = 20
        if y_scale*max(data) > size[0]:
            y_scale = max(data)/size[0]
        # color = (128, 128, 128)
        box = pygame.Rect(offset, size)
        pygame.draw.rect(self.surface, config.color_fg, box, 1)
        for n, value in enumerate(data):
            bar_size = (size[0]/len(data), y_scale*value)
            bar_loc  = (offset[0]+bar_size[0]*n, offset[1]+size[1]-bar_size[1])
            bar = pygame.Rect(bar_loc, bar_size)
            pygame.draw.rect(self.surface, config.color_fg, bar, 1)
        for n in range(0, int(y_scale)):
            pygame.draw.line(self.surface,
                             config.color_fg,
                             (offset[0]-5,offset[1]+size[1]/y_scale*n),
                             (offset[0],  offset[1]+size[1]/y_scale*n))

    def draw_z_factor(self, config):
        z = config.population[config.current_number]
        # Declare data for later use.
        # color = (160, 160, 140) # RBG values (0-255; 3)
        v_rad = config.z_radius # Vertex Radius (In Pixels).
        t_rad = config.t_radius # Text Radius (In Pixels).
        t_size = 20 # Font Size.
        # Data on how to offset text.
        t_off = [
                 config.z_coords[0]-t_size/2,
                 config.z_coords[1]-t_size/2
                ]
        vert_coords = [
                (x*v_rad+config.z_coords[0]+v_rad,
                 y*v_rad+config.z_coords[1]+v_rad)
                for x,y in z.coords
                ]
        text_coords = [
                (x*t_rad+t_off[0]+v_rad,
                 y*t_rad+t_off[1]+v_rad)
                for x,y in z.coords
                ]
        # Draw the edges of the graph, taking into account whether or not to
        # draw the non-trivial edges.
        if config.show_trivial == True:
            for a,b in z.edges:
                pygame.draw.aaline(self.surface,
                                   config.color_z,
                                   vert_coords[a],
                                   vert_coords[b])
        else:
            for a,b in z.non_trivial_edges:
                pygame.draw.aaline(self.surface,
                                   config.color_z,
                                   vert_coords[a],
                                   vert_coords[b])
        # Draw the Vertices.
        for a,b in vert_coords:
            pygame.draw.circle(self.surface,
                               config.color_z,
                               (int(a),int(b)),
                               5)
        if config.current_number < 100:
            for n, pair in enumerate(text_coords):
                self.write(str(n), 24, pair)
        self.write(str(z.n), 32, config.z_coords)

    def draw(self, z, offset, config):
        """ Used to draw all pertinent information from a ZeroFactors object
            to the screen.
        """
        self.draw_z_factor(config)
        # Begin to write to the screen.
        # title_offset = (offset[0]-t_rad, offset[1]-t_rad)
        # self.write(str(z.n), 32, title_offset)
        self.write("Factors:",  18, (20, self.height-110))
        self.write("Vertices:", 18, (20, self.height-90))
        self.write("Degrees:",  18, (20, self.height-70))
        # self.write("Colors:",   18, (20, self.height-40))
        self.write_list(z.factors_pos, 18, (100, self.height-110), 30)
        self.write_list(z.verts,       18, (100, self.height-90), 30)
        # Take into account the difference between the trivial and
        # non-trivial sets.
        if config.show_trivial == True:
            self.write_list(z.degrees, 18, (100, self.height-70), 30)
            # self.write_list(z.colors, 18, (100, self.height-40), 30)
            # self.draw_graph(z.degrees, (1200, 100), (600, 800))
        else:
            self.write_list(z.non_trivial_degrees, 18, (100, self.height-70), 30)
            # self.write_list(z.non_trivial_colors, 18, (100, self.height-40), 30)
            # self.draw_graph(z.non_trivial_degrees, (1200, 100), (600, 800))
        # Title the graph.
        # self.write("Degree of each Vertex:",  24, (1200, 60))
        # Manage drawing for different states.
        if config.state == "Dialog":
            self.draw_dialog_box("Go to term:", config, (500, 500), (300, 100))
        help_1 = "Zoom graph with +/-"
        help_2 = "Move Graph with Arrow Keys or HJKL"
        help_3 = "Press 'n' to select an arbitrary term."
        self.write(help_1, 12, (self.width-220, self.height-30))
        self.write(help_2, 12, (self.width-220, self.height-40))
        self.write(help_3, 12, (self.width-220, self.height-50))

