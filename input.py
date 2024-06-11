import pygame
import sys

class InputBoxManager:
    def __init__(self, screen, position, width, height):
        self.screen = screen
        self.position = position
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))  # Fill with white background

        self.variables = {
            'Draw Lenght': '0.5',
            'Initial Angle': '0.78',
            'K': '500',
            'Arrow Mass': '0.018'
        }

        self.font_size = max(20, height // (len(self.variables) + 6))  # Adaptive font size
        self.font = pygame.font.Font(None, self.font_size)
        self.input_spacing = self.height // (len(self.variables) + 3)  # Spacing based on number of inputs

        
        self.active_variable = None
        self.rects = []
        self.is_done = False  # Indicates whether the button was pressed

        # Button setup
        self.button_color = (100, 200, 100)  # A nice green
        self.button_hover_color = (150, 250, 150)  # Lighter green for hover
        self.button_rect = pygame.Rect(self.width // 2 - 50, self.height - 40, 100, 30)  # Position the button at the bottom
        self.button_text = 'Start'

    def draw_text(self, text, position, input_box=False, active=False):
        text_surface = self.font.render(text, True, (0, 0, 0))  # Black color for text
        text_rect = text_surface.get_rect(topleft=position)
        if input_box:
            text_rect.width = max(self.width // 2, text_surface.get_width() + 20)  # Ensure width based on surface width
            pygame.draw.rect(self.surface, (200, 200, 200) if not active else (255, 255, 255), text_rect.inflate(20, 10), 0, 5)
            pygame.draw.rect(self.surface, (0, 0, 0), text_rect.inflate(20, 10), 2, 5)
        self.surface.blit(text_surface, text_rect)
        return text_rect

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        local_mouse_x = mouse_pos[0] - self.position[0]
        local_mouse_y = mouse_pos[1] - self.position[1]
        button_color = self.button_hover_color if self.button_rect.collidepoint(local_mouse_x, local_mouse_y) else self.button_color

        pygame.draw.rect(self.surface, button_color, self.button_rect)
        text_surface = self.font.render(self.button_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mouse_x -= self.position[0]  # Adjust for position of the surface in the main screen
            mouse_y -= self.position[1]

            if self.button_rect.collidepoint(mouse_x, mouse_y):
                print("pressed")
                print(self.variables)
                print(self.active_variable)
                self.is_done = True
            elif not any(input_rect.collidepoint((mouse_x, mouse_y)) for _, input_rect, _ in self.rects):
                self.active_variable = None
            else:
                for label_rect, input_rect, var_name in self.rects:
                    if input_rect.collidepoint((mouse_x, mouse_y)):
                        self.active_variable = var_name
                        break

        elif event.type == pygame.KEYDOWN and self.active_variable:
            if event.key == pygame.K_BACKSPACE:
                self.variables[self.active_variable] = self.variables[self.active_variable][:-1]
            elif event.key == pygame.K_RETURN:
                self.active_variable = None  # Move focus away from the text box
            else:
                char = event.unicode
                if char.isalnum() or char in '.-':
                    new_text = self.variables[self.active_variable] + char
                    if self.font.size(new_text)[0] < self.width - 50:  # Ensure text fits within width
                        self.variables[self.active_variable] = new_text

    def update(self):
        self.surface.fill((255, 255, 255))  # Clear surface with white color
        y_pos = self.input_spacing // 2  # Start y position for drawing
        self.rects = []
        for var_name, value in self.variables.items():
            label_rect = self.draw_text(f"{var_name}:", (20, y_pos))
            input_rect = self.draw_text(value, (self.width // 3, y_pos), input_box=True, active=(self.active_variable == var_name))
            self.rects.append((label_rect, input_rect, var_name))
            y_pos += self.input_spacing  # Increment position for the next input

        self.draw_button()  # Draw the completion button

    def draw(self):
        # Blit the surface onto the main screen at its position
        self.screen.blit(self.surface, self.position)


"""
# Example usage in a Pygame application
pygame.init()
main_screen = pygame.display.set_mode((800, 600))
input_manager = InputBoxManager(main_screen, (50, 50), 500, 300)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        input_manager.handle_event(event)

    input_manager.update()
    if input_manager.is_done:
        print("Done button clicked. Final values:", input_manager.variables)
        running = False  # Optionally stop the loop if the done button is pressed

    main_screen.fill((0, 0, 0))  # Clear main screen with black color
    input_manager.draw()
    pygame.display.flip()
"""