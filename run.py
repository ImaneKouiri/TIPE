
import pygame
import sys

import config
from inputv2 import InputBoxManager
from graph import GraphBoxManager

from archery import aphysix

pygame.init()
main_screen = pygame.display.set_mode((1600, 600))
graph_size = (1000, 400)
graph_pos = ()
graph_manager = GraphBoxManager(main_screen, (50, 50), 1000, 500)

input_size = (500, 400)
input_pos = (50, 50)
input_manager = InputBoxManager(main_screen, (1100, 50), 500, 300)

start_tick_set = False
running = True

scale = 1
tries = 0
idx = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        event_result = input_manager.handle_event(event)
        if event_result == 'reset':
            graph_manager.reset_graph()  # Reset the graph manager
            start_tick_set = False  # Allow timer to reset
            tries = 0  # Reset tries if used for tracking attempts
            
    input_manager.update()        
    
    if input_manager.is_done:
        if start_tick_set:
            
            data_dict = input_manager.variables
            initial_angle = float(data_dict["Angle"])
            max_x, max_y, points = graph_manager.engine.get_data(initial_angle=initial_angle, initial_velocity= graph_manager.initial_velocity)
            scale = 1/5
            graph_manager.update(start_ticks=start_ticks, data_dict=input_manager.variables, points=points, idx=idx, scale=scale)
            running = True #graph_manager.running
            if graph_manager.running:
                idx += 1
            else:
                tries += 1
                idx = 0
                input_manager.is_done = None
            #print("Done button clicked. Final values:", input_manager.variables)
            continue
        else:
            start_ticks = pygame.time.get_ticks()  # Timer start
            start_tick_set = True
        #running = False  # Optionally stop the loop if the done button is pressed
    if tries > 0 or not graph_manager.running:
        graph_manager.update(start_ticks=start_ticks, data_dict=input_manager.variables, points=points, idx=idx, scale=scale)
    
    main_screen.fill(config.WHITE)  # Clear main screen with black color
    input_manager.draw()
    if tries == 0:
        graph_manager.draw_graph(scale=scale)
    else:
        graph_manager.update(start_ticks=start_ticks, data_dict=input_manager.variables, points=points, idx=idx, scale=scale)
    pygame.display.flip()