#!/usr/bin/env python3

import sys
from math import cos, sin, pi

import numpy as np
import pygame

""" === Nerdy Math Shit =================================================== """
class ZeroFactor:
    """ Generates & stores all of the data pertinent to the topic of
        Zero-Factor Analysis for some arbitrary integer.
    """
    def __init__(self, n):
        self.n = n
        self.verts = range(0, n)
        self.edges = [(a,b) for a in self.verts for b in self.verts[a+1:] if a*b % n == 0]
        self.non_trivial_edges = list(filter(lambda pair: 0 not in pair, self.edges))
        self.cardinality = len(self.edges) # Of the set of edges.
        self.degrees = [sum(1 for pair in self.edges if x in pair) for x in range(0,n)]
        self.non_trivial_degrees = [sum(1 for pair in self.non_trivial_edges if x in pair) for x in range(0,n)]
        self.factors = [a for a in range(0,n) for b in range(0,n) if a*b == n]
        # Used to easily write on the screen.
        self.factors_pos = list(map(lambda x: x if x in self.factors else None, self.verts))
        # Only relevant to drawing fancily on a screen. Projects to the unit circle.
        self.coords = [(cos(o*pi*2/n-pi/2),sin(o*pi*2/n-pi/2)) for o in range(0, n)]
        # Coloring algorithm currently broken. Incorrect results.
        self.colors =             ZeroFactor.get_colors(self.verts, self.edges)
        self.non_trivial_colors = ZeroFactor.get_colors(self.verts, self.non_trivial_edges)

    def get_colors(vert_set, edge_set):
        """ Given data on a graph, returns a list of colors coresponding to
            each vertex.
            ---
            Currently broken, returns list of all the same color.
            ---
        """
        colors = [None for _ in vert_set]
        # Begin coloring the graph.
        if len(edge_set) == 0:
            return
        for vert in vert_set:
            colors_seen = []
            for edge in edge_set:
                if vert in edge and colors[vert] != None:
                    colors_seen.append(colors[vert])
            for n in range(1, len(vert_set)):
                if n not in colors_seen:
                    colors[vert] = n
                    break
        return colors

""" === End Nerdy Math Shit =============================================== """

class Config:
    """ Singleton style object used to manage configuration state of
        program.
    """
    def __init__(self):
        self.show_trivial = False
        self.current_number = 1

    def manage_input(self, ev, config):
        """ Manages altering internal state via keybinds. """
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse Wheel to scroll through data.
                if event.button == 4:
                    self.current_number += 1
                elif event.button == 5:
                    self.current_number -= 1
                # Never go below 1.
                self.current_number = max(1, self.current_number)
            elif event.type == pygame.KEYDOWN:
                # Toggle showing trivial data.
                if event.key == pygame.K_SPACE:
                    config.show_trivial = not config.show_trivial

class Window:
    """ Class used to manage creating & drawing to the program's window. """
    def __init__(self, x, y, title):
        self.width = x
        self.height = y
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((x, y))
        pygame.display.set_caption(title)
        self.fonts = {
                 8: pygame.font.SysFont('Ubuntu',  8, False, False),
                10: pygame.font.SysFont('Ubuntu', 10, False, False),
                12: pygame.font.SysFont('Ubuntu', 12, False, False),
                14: pygame.font.SysFont('Ubuntu', 14, False, False),
                16: pygame.font.SysFont('Ubuntu', 16, False, False),
                18: pygame.font.SysFont('Ubuntu', 18, False, False),
                20: pygame.font.SysFont('Ubuntu', 20, False, False),
                22: pygame.font.SysFont('Ubuntu', 22, False, False),
                24: pygame.font.SysFont('Ubuntu', 24, False, False),
                26: pygame.font.SysFont('Ubuntu', 26, False, False),
                28: pygame.font.SysFont('Ubuntu', 28, False, False),
                30: pygame.font.SysFont('Ubuntu', 30, False, False),
                32: pygame.font.SysFont('Ubuntu', 32, False, False),
                }

    def write(self, text, size, offset):
        """ Write an object to the screen. """
        font = self.fonts[size]
        self.surface.blit(font.render(text, True, (128, 128, 128)), offset)

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
        color = (128, 128, 128)
        box = pygame.Rect(offset, size)
        pygame.draw.rect(self.surface, color, box, 1)
        for n, value in enumerate(data):
            bar_size = (size[0]/len(data), y_scale*value)
            bar_loc  = (offset[0]+bar_size[0]*n, offset[1]+size[1]-bar_size[1])
            bar = pygame.Rect(bar_loc, bar_size)
            pygame.draw.rect(self.surface, color, bar, 1)
        for n in range(0, int(y_scale)):
            pygame.draw.line(self.surface,
                             color,
                             (offset[0]-5,offset[1]+size[1]/y_scale*n),
                             (offset[0],  offset[1]+size[1]/y_scale*n))

    def draw(self, z, offset, config):
        """ Used to draw all pertinent information from a ZeroFactors object
            to the screen.
        """
        # Declare data for later use.
        color = (160, 160, 140) # RBG values (0-255; 3)
        v_rad = 300 # Vertex Radius (In Pixels).
        t_rad = 340 # Text Radius (In Pixels).
        t_size = 20 # Font Size.
        t_trans = [offset[0]-t_size/2, offset[1]-t_size/2]  # Data on how to offset text.
        vert_coords = [(x*v_rad+offset[0], y*v_rad+offset[1])  for x,y in z.coords]
        text_coords = [(x*t_rad+t_trans[0],y*t_rad+t_trans[1]) for x,y in z.coords]
        # Draw the edges of the graph, taking into account whether or not to
        # draw the non-trivial edges.
        if config.show_trivial == True:
            for a,b in z.edges:
                pygame.draw.aaline(self.surface, color, vert_coords[a], vert_coords[b])
        else:
            for a,b in z.non_trivial_edges:
                pygame.draw.aaline(self.surface, color, vert_coords[a], vert_coords[b])
        # Draw the Vertices.
        for a,b in vert_coords:
            pygame.draw.circle(self.surface, color, (int(a),int(b)), 5)
        for n, pair in enumerate(text_coords):
            self.write(str(n), 24, pair)
        # Begin to write to the screen.
        title_offset = (offset[0]-t_rad, offset[1]-t_rad)
        self.write(str(z.n), 32, title_offset)
        self.write("Factors:",  18, (20, self.height-100))
        self.write("Vertices:", 18, (20, self.height-80))
        self.write("Degrees:",  18, (20, self.height-60))
        # self.write("Colors:",   18, (20, self.height-40))
        self.write_list(z.factors_pos, 18, (100, self.height-100), 30)
        self.write_list(z.verts,       18, (100, self.height-80), 30)
        # Take into account the difference between the trivial and
        # non-trivial sets.
        if config.show_trivial == True:
            self.write_list(z.degrees, 18, (100, self.height-60), 30)
            # self.write_list(z.colors, 18, (100, self.height-40), 30)
            self.draw_graph(z.degrees, (1200, 100), (600, 800))
        else:
            self.write_list(z.non_trivial_degrees, 18, (100, self.height-60), 30)
            # self.write_list(z.non_trivial_colors, 18, (100, self.height-40), 30)
            self.draw_graph(z.non_trivial_degrees, (1200, 100), (600, 800))
        # Title the graph.
        self.write("Degree of each Vertex:",  24, (1200, 60))

def main():
    # Create program state.
    config = Config()
    dataset = {}    # Refactor to be part of the Config class.
    pygame.init()   # Start pygame.
    window = Window(1920, 1080, "Zero Factor Analysis")
    # Main Program Loop.
    while True:
        # Check input.
        ev = pygame.event.get()
        config.manage_input(ev, config)
        # Blank out the screen.
        window.surface.fill( (32, 32, 32) )
        # Generate new data only as needed.
        if config.current_number not in dataset:
            dataset[config.current_number] = ZeroFactor(config.current_number)
        # Draw new frame.
        window.draw(dataset[config.current_number], (450, 450), config)
        pygame.display.update()

if __name__ == "__main__":
    main()

