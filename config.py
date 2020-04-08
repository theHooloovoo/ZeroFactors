
import sys
import pygame
import json

from zero import ZeroFactor

class Config:
    """ Singleton style object used to manage configuration state of
        program.
    """
    def __init__(self, f_path):
        with open(f_path, 'r') as f_in:
            # print(f_in.read())
            print("Building from {}".format(f_path))
            data = json.loads(f_in.read())
            self.window_size = data["General"]["Resolution"]
            self.application_title = data["General"]["Title"]
            self.z_coords = data["Z Factor Graph"]["Coordinates"]
            self.z_radius = data["Z Factor Graph"]["Vert Radius"]
            self.t_radius = data["Z Factor Graph"]["Text Radius"]
            self.color_bg = data["General"]["Background"]
            self.color_fg = data["General"]["Foreground"]
            self.color_z  = data["General"]["Color Z"]
            self.show_trivial = False
            self.current_number = 1
            self.pop_max = data["General"]["Starting Pop"]
            self.n_list = range(0, self.pop_max+1)
            self.population = {n: ZeroFactor(n) for n in range(1,self.pop_max+1)}
            print("Generated the first {} graphs!".format(self.pop_max))
            self.state = None
            self.query = ""

    def manage_input(self, ev):
        """ Manages altering internal state via keybinds.
            `ev` is the result of pygame.event.get()
        """
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.state == None:
                if event.type == pygame.MOUSEBUTTONUP:
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
                        self.show_trivial = not self.show_trivial
                    elif event.key == pygame.K_n:
                        self.state = "Dialog"
                self.manage_z_graph(event)
            elif self.state == "Dialog":
                query = self.manage_dialog(event, is_number=True)
                if query != None:
                    try:
                        self.current_number = int(query)
                        if self.current_number not in self.population:
                            self.population[self.current_number] = ZeroFactor(self.current_number)
                    except:
                        print("Err!", query, "cannot be parsed as a number!")

    def manage_z_graph(self, event):
        """ Manages moving and scaling the Z-Factor graph.
            Arrow Key/HJKL move the graph, while +/- manipulate the drawing
            radius of the graph.
        """
        if event.type == pygame.KEYDOWN:
            # Check for graph scaling (+/-).
            rad_inc = 10
            if event.key == pygame.K_MINUS:
                self.z_radius -= rad_inc
                self.z_radius = max(self.z_radius, 0)
                self.t_radius -= rad_inc
                self.t_radius = max(self.t_radius, rad_inc)
            elif event.key == pygame.K_EQUALS:
                self.z_radius += rad_inc
                self.t_radius += rad_inc
            coord_inc = 10
            # Check for Graph Translation (Arrow/HJKL).
            # Keep in mind that the window coordinates system has (0,0) be the
            # top left corner, so vertical movement has to be flipped.
            if event.key in [pygame.K_LEFT, pygame.K_h]:
                self.z_coords[0] -= coord_inc
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                self.z_coords[0] += coord_inc
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                self.z_coords[1] += coord_inc
            elif event.key in [pygame.K_UP, pygame.K_k]:
                self.z_coords[1] -= coord_inc

    def manage_dialog(self, event, is_number=False):
        """ Generic method designed to manage queries from dialog boxes. """
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.state = None
                self.query = ""
            elif event.key == pygame.K_RETURN:
                temp = self.query
                self.state = None
                self.query = ""
                return temp
            elif event.key == pygame.K_BACKSPACE:
                self.query = self.query[:-1]
            else:
                if is_number == True:
                    try:
                        int(event.unicode)
                        self.query += event.unicode
                    except:
                        pass
                else:
                    self.query += event.unicode

    def factors_list(factors, start, end):
        """ Returns a list of numbers that are divisble by all of the terms in
            factors.
        """
        results = []
        for n in range(start, end):
            flag = True
            for f in factors:
                if n % f != 0:
                    flag = False
                    break
            if flag == True:
                results.append(n)
