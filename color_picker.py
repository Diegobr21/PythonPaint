

import pygame
import sys


class ColorPicker(object):
    def __init__(self, screen):
        self.done = False
        self.screen = screen
        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.clock = pygame.time.Clock()
        self.fps = 30
        
        self.square_size = 20
        self.colors = pygame.color.THECOLORS
        self.labels = []
        self.color_names = []
        self.current_color = None
        
    def draw(self, surface):
        self.screen.fill(pygame.Color("black"))
        square_size = 20
        left = 0
        top = 0
        for color in self.colors:
            pygame.draw.rect(self.screen, self.colors[color],
                               (left, top, square_size, square_size))
            left += square_size
            if left + square_size > surface.get_width():
                top += square_size
                left = 0
        for label in self.labels:
            surface.blit(label[0], label[1])
            
    def update(self):
        self.labels = []
        left = 0
        top = 450
        if self.current_color:
            rgb_label = self.font.render("{}".format(self.current_color), True,
                                                     pygame.Color("white"), pygame.Color("black"))
            rgb_rect = rgb_label.get_rect(topleft=(left, top))
            self.labels.append((rgb_label, rgb_rect))
            left += rgb_rect.width + 10
        # for name in self.color_names:
        #     name_text = self.font.render("{0}".format(name), True,
        #                                                pygame.Color("white"), pygame.Color("black"))
        #     name_rect = name_text.get_rect(topleft=(left, top))
        #     left = name_rect.right + 20
        #     self.labels.append((name_text, name_rect))
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.current_color = self.screen.get_at(event.pos)
                self.done = True
                # self.color_names = []
                # for name, value in self.colors.items():
                #     if value == self.current_color:
                #         self.color_names.append(name)
                
        return self.current_color
                        
    
    def run(self):    
        while not self.done:
            self.event_loop()
            #self.update()
            self.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.fps)
        return True, self.current_color
       

# if __name__ == "__main__":      
#     pg.init()
#     screen = pg.display.set_mode((300, 300))
#     pg.display.set_caption("Color Picker")

#     picker = ColorPicker(screen)
#     close, color_update = picker.run()
#     if(close):

#         print(color_update)

#         pg.quit()
#     pg.quit()
#     sys.exit()
#     print(color_update)
