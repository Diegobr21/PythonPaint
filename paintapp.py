"""Main script for painting app
"""
# Imports
import sys
import pygame
import pygame_widgets
import ctypes
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from color_picker import *

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
window_width, window_height = 640, 480
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 20)

# Variables
slider = Slider(screen, 50, 200, 250, 50, min=1, max=50, step=1)
#output = TextBox(screen, 5, 300, 50, 50, fontSize=30)

#output.disable()  # Act as label instead of textbox

# Our Buttons will append themself to this list
objects = []



# Initial brush size
brushSize = 30
brushSizeSteps = 3

# Drawing Area Size
canvasSize = [800, 800]

ROWS = COLS = 100
PIXEL_SIZE = window_width // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initial color
drawColor = BLACK


DRAW_GRID_LINES = True


# Button Class
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

# Handler Functions

#? Drawing with grid
def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid

def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                                          PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (canvasSize[0], i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, canvasSize[0]))

#? Color picker 

def drawColorPicker(): 
    global window_width, window_height, drawColor   
    screen2 = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    screen2.fill((30, 30, 30))
    picker = ColorPicker(screen2)
    close, color_update = picker.run()
    if(close):

        print(color_update)

        #pygame.quit()
    drawColor = color_update

# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color

def updateGrid():
    global DRAW_GRID_LINES
    DRAW_GRID_LINES = not(DRAW_GRID_LINES)

# Changing the Brush Size
#Using slider now
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

def changebrushSize_slider(slider_value):
    global brushSize
    brushSize = slider_value

# Save the surface to the Disk
#todo: open file explorer to save in desired folder/filename select (give default still)
def save():
    pygame.image.save(canvas, "canvas.png")

# Button Variables.
buttonWidth = 120
buttonHeight = 35

# Buttons and their respective functions.
#todo: color picker palette
#todo: different brush types
buttons = [
    # ['Black', lambda: changeColor([0, 0, 0])],
    # ['White', lambda: changeColor([255, 255, 255])],
    # ['Red', lambda: changeColor([255, 0, 0])],
    # ['Blue', lambda: changeColor([0, 0, 255])],
    # ['Green', lambda: changeColor([0, 255, 0])],
    ['Color', lambda: drawColorPicker()],
    #['GridLines', lambda: updateGrid()],
    # ['Brush Larger', lambda: changebrushSize('greater')],
    # ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Save', save],
]

# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

# Canvas
canvas = pygame.Surface(canvasSize)
canvas.fill((255, 255, 255))

# Game loop.
while True:
    screen.fill((30, 30, 30))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #? brush update
    #output.setText(slider.getValue())
    changebrushSize_slider(slider.getValue())
    if(drawColor == [255, 255, 255]):
        slider.colour = [0, 0, 0]
        slider.handleColour = drawColor
    else:
        slider.handleColour = drawColor
        slider.colour = [255, 255, 255]
    pygame_widgets.update(events)
    
    

    # Drawing the Buttons
    for object in objects:
        object.process()
    # Draw the Canvas at the center of the screen
    x, y = screen.get_size()
    screen.blit(canvas, [x/2 - canvasSize[0]/2, y/2 - canvasSize[1]/2])
    # Drawing with the mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # Calculate Position on the Canvas
        dx = mx - x/2 + canvasSize[0]/2
        dy = my - y/2 + canvasSize[1]/2
        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )
    # Reference Dot
    pygame.draw.circle(
        screen,
        drawColor,
        [105, 105],
        brushSize,
    )

    pygame.display.flip()
    
    fpsClock.tick(fps)

