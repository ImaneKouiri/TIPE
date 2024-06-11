import pygame
import math
import sys

from archery import aphysix

draw_lenght = 0.5
initial_angle = math.pi/4
k = 500
arrow_mass = 0.018

archery = aphysix(k, arrow_mass)
#archery.run(draw_lenght, initial_angle, step=0)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1500, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dynamic Function Graph on Surface")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock to manage frame rate
clock = pygame.time.Clock()

# Graph dimensions and position
graph_width, graph_height = 1000, 400
graph_surface = pygame.Surface((graph_width, graph_height))
graph_position = (100, 100)  # Position of the graph surface on the main screen

# Function to plot
def function(x, t):
    """Example function: A moving sine wave."""
    return x #graph_height / 2 - (x) * (graph_height / 4) 

padding = 1/12
graph_padding = graph_height * padding

# Function to draw axes on the graph surface
def draw_axes(surface):
    
    # Draw horizontal axis
    # pygame.draw.line(surface, BLACK, (0, graph_height * (1 - graph_width_divider)), (graph_width, graph_height * (1 - graph_width_divider)), 2)
    pygame.draw.line(surface, BLACK, (0, graph_height - graph_padding), (graph_width, graph_height - graph_padding), 2)
    # Draw vertical axis
    pygame.draw.line(surface, BLACK, (graph_padding, 0), (graph_padding, graph_height), 2)

    # Draw scale markers
    for x in range(int(graph_padding), graph_width, 50):
        pygame.draw.line(surface, BLACK, (x, graph_height * (1 - padding) - 10), (x, graph_height * (1 - padding) + 10), 1)
        label = font.render(str(x - int(graph_padding)), True, BLACK)
        surface.blit(label, (x + 2, graph_height * (1 - padding) + 12))

    y_pad = graph_height * padding

    for y in range(0, graph_height, 50):
        pygame.draw.line(surface, BLACK, (graph_padding - 10, y - y_pad), (graph_padding + 10, y - y_pad), 1)
        if y != graph_height - 50:
            label = font.render(str(graph_height - y - 50), True, BLACK)
            surface.blit(label, (graph_padding + 12, y + 2))

# Main loop
running = True
start_ticks = pygame.time.get_ticks()  # Timer start
points = []  # To store points that will be drawn
font = pygame.font.Font(None, 24)  # Font for labels

prelude_points = archery.run(draw_lenght, initial_angle, step=0)
y_max = max([point[-1] for point in prelude_points])
x_max = max([point[-2] for point in prelude_points])
print(len(prelude_points), x_max, y_max)

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen and graph surface
    screen.fill(WHITE)
    graph_surface.fill(WHITE)

    # Draw axes on the graph surface
    draw_axes(graph_surface)

    # Get the time elapsed
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    current_time = seconds / 10

    # Calculate new point
    #x = len(points) * 4  # Increase x by 4 pixels each frame
    point = archery.step(draw_lenght, initial_angle, seconds)
    y = point[-1]
    x = point[-2]
    if y > 0:
        points.append(archery.step(draw_lenght, initial_angle, seconds))

    # Draw all points on the graph surface
    for point in points:
        point = (point[-2] + graph_padding, graph_height - graph_padding - point[-1])
        if x > 100:
            pygame.draw.circle(graph_surface, BLUE, point, 2)
        else:
            pygame.draw.circle(graph_surface, RED, point, 2)

    # Blit the graph surface onto the main screen at its position
    screen.blit(graph_surface, graph_position)

    # Update the display
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

    # Stop after 5 seconds
    if y < 0:
        running = False

pygame.quit()


