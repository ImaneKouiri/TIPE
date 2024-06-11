import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dynamic Function Graph Setup")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Variables with default values
variables = {
    'amplitude': '100',
    'frequency': '0.05',
    'duration': '5',
    'speed': '4'
}

# Font for drawing text
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)

# Function to draw text
def draw_text(text, position, input_box=False, active=False):
    text_surface = input_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(topleft=position)
    if input_box:
        pygame.draw.rect(screen, LIGHT_GRAY if not active else WHITE, text_rect.inflate(20, 10), 0, 5)
        pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 10), 2, 5)
    screen.blit(text_surface, text_rect)
    return text_rect

# Input handling
active_variable = None
running = True
while running:
    screen.fill(WHITE)
    
    # Draw labels and inputs for variables
    y_pos = 100
    rects = []
    for var_name, value in variables.items():
        label_rect = draw_text(f"{var_name}:", (50, y_pos))
        input_rect = draw_text(value, (200, y_pos), input_box=True, active=(active_variable == var_name))
        rects.append((label_rect, input_rect, var_name))
        y_pos += 50
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Deactivate all inputs if the click is outside any input box
            if not any(input_rect.collidepoint(event.pos) for label_rect, input_rect, var_name in rects):
                active_variable = None
            else:
                # Activate the clicked input box
                for label_rect, input_rect, var_name in rects:
                    if input_rect.collidepoint(event.pos):
                        active_variable = var_name
                        break
        elif event.type == pygame.KEYDOWN and active_variable:
            if event.key == pygame.K_BACKSPACE:
                variables[active_variable] = variables[active_variable][:-1]
            elif event.key == pygame.K_RETURN:
                active_variable = None  # Move focus away from the text box
            else:
                char = event.unicode
                # Update the variable value if it's a valid character and within a reasonable length
                if char.isalnum() or char in '.-':
                    new_text = variables[active_variable] + char
                    # Make sure new text will fit in the box
                    if input_font.size(new_text)[0] < rects[0][1].width - 25:
                        variables[active_variable] = new_text
    
    # Display the frame
    pygame.display.flip()

    # Placeholder for continuation condition or exit
    # For example, press ESCAPE to exit the loop and start the graph
    if pygame.key.get_pressed()[pygame.K_RETURN]:
        running = False
        # Here, convert string inputs to appropriate types
        amplitude = float(variables['amplitude'])
        frequency = float(variables['frequency'])
        duration = int(variables['duration'])
        speed = int(variables['speed'])
        print("Starting graph with settings:", amplitude, frequency, duration, speed)
        # Add code here to transition to graph drawing using these variables

pygame.quit()
