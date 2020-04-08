#!/usr/bin/env python3

import sys
# from math import cos, sin, pi

# import numpy as np
import pygame
import json

from zero import ZeroFactor
from config import Config
from window import Window

def main():
    # Create program state.
    # config = Config()
    config = Config("config.json")
    dataset = {}    # Refactor to be part of the Config class.
    pygame.init()   # Start pygame.
    pygame.font.init()
    window = Window(config)
    # Main Program Loop.
    while True:
        # Check input, and change state accordingly.
        ev = pygame.event.get()
        config.manage_input(ev)
        # Blank out the screen.
        window.surface.fill(config.color_bg)
        # Generate new data only as needed.
        if config.current_number not in dataset:
            dataset[config.current_number] = ZeroFactor(config.current_number)
        # Draw new frame.
        window.draw(dataset[config.current_number], (450, 450), config)
        pygame.display.update()

if __name__ == "__main__":
    main()

