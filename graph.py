import pygame
import config

from archery import aphysix

class GraphBoxManager:
    def __init__(self, screen, position, width, height) -> None:
        self.screen = screen
        self.position = position
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill(config.WHITE)
        self.running = True

         # Clock to manage frame rate
        self.clock = pygame.time.Clock()

        self.points = []
        self.initial_velocity = 87.03
        self.engine = aphysix()

        self.padding = 1/12
        self.graph_padding = self.height * self.padding

        self.font_size = 24  # Adaptive font size
        self.font = pygame.font.Font(None, self.font_size)
        #self.input_spacing = self.height // (len(self.variables) + 3)  # Spacing based on number of inputs

        
        self.active_variable = None
        self.rects = []
        self.is_done = False  # Indicates whether the button was pressed

        # Button setup
        self.button_color = (100, 200, 100)  # A nice green
        self.button_hover_color = (150, 250, 150)  # Lighter green for hover
        self.button_rect = pygame.Rect(self.width // 2 - 50, self.height - 40, 100, 30)  # Position the button at the bottom
        self.button_text = 'Done'

    def draw_axes(self, scale=1):
        # Draw horizontal axis
        # pygame.draw.line(surface, BLACK, (0, graph_height * (1 - graph_width_divider)), (graph_width, graph_height * (1 - graph_width_divider)), 2)
        x_y = self.height - self.graph_padding
        pygame.draw.line(self.surface, config.BLACK, (0, x_y), (self.width, x_y), 2)
        # Draw vertical axis
        pygame.draw.line(self.surface, config.BLACK, (self.graph_padding, 0), (self.graph_padding, self.height), 2)

        # Draw scale markers
        for x in range(int(self.graph_padding), self.width, 50):
            pygame.draw.line(self.surface, config.BLACK, (x, self.height * (1 - self.padding) - 10), (x, self.height * (1 - self.padding) + 10), 1)
            label_text = str((x - int(self.graph_padding)) * scale)
            label = self.font.render(label_text, True, config.BLACK)
            self.surface.blit(label, (x + 2, self.height * (1 - self.padding) + 12))

        for y in range(0, self.height, 50):
            pygame.draw.line(self.surface, config.BLACK, (self.graph_padding - 10, y - self.graph_padding), (self.graph_padding + 10, y - self.graph_padding), 1)
            if y != self.height - 50:
                label_text = str((self.height - y - 50) * scale)
                label = self.font.render(label_text, True, config.BLACK)
                self.surface.blit(label, (self.graph_padding + 12, y + 2))

    
    def draw_graph(self, scale=1):
        # Clear the screen and graph surface
        self.surface.fill(config.WHITE)

        # Draw axes on the graph surface
        self.draw_axes(scale=scale)
        self.screen.blit(self.surface, self.position)
        pygame.display.flip()

    def update(self, start_ticks, data_dict, points, idx, scale=1):



        # Clear the screen and graph surface
        self.surface.fill(config.WHITE)

        # Draw axes on the graph surface
        self.draw_axes(scale=scale)

        # Get the time elapsed
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        current_time = seconds / 10

        # Calculate new point
        #x = len(points) * 4  # Increase x by 4 pixels each frame
        #points = self.engine.get_data(initial_angle=initial_angle, initial_velocity=self.initial_velocity)
        y = points[idx][1]
        x = points[idx][0]
        if y > 0:
            self.points.append((x, y))

        # Draw all points on the graph surface
        for point in self.points:
            point = (point[0]*(1/scale) + self.graph_padding, self.height - self.graph_padding - point[1]*(1/scale))
            
            if x > 100:
                pygame.draw.circle(self.surface, config.BLUE, point, 2)
            else:
                pygame.draw.circle(self.surface, config.RED, point, 2)

        # Blit the graph surface onto the main screen at its position
        self.screen.blit(self.surface, self.position)

        # Update the display
        pygame.display.flip()

        # Limit to 60 frames per second
        self.clock.tick(60)

        # Stop after 5 seconds
        if y < 0:
            self.running = False

    def reset_graph(self):
        self.points = []  # Clear all points
        self.running = True  # Enable the graph to run again
        self.surface.fill(config.WHITE)  # Clear the drawing surface

"""
# Example usage in a Pygame application
pygame.init()
main_screen = pygame.display.set_mode((1000, 600))
input_manager = GraphBoxManager(main_screen, (100, 50), 1000, 400)
running = True
start_ticks = pygame.time.get_ticks()  # Timer start
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    variables = {
            'Draw Lenght': '0.5',
            'Initial Angle': math.pi/4,
            'K': '500',
            'Arrow Mass': '0.018'
        }
    #input_manager.draw_graph()
    input_manager.update(start_ticks=start_ticks, data_dict=variables, scale=1)
    #pygame.display.flip()
    running = input_manager.running
"""
