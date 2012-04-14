'''
Created on 2012-04-14

@author: egerlach
'''

import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, colour, initial_position, speed):
        """Builds a Box sprite
        
        @param colour - a list of RGB values for the colour of the box
        @param initial_position - a list of two values for the top left coordinate of the box
        @param speed - number of pixels per second that the box should move
        """
        # Call parent contstructor
        pygame.sprite.Sprite.__init__(self)
        
        # We need to create an image for the sprite. A 15x15 box will do
        self.image = pygame.Surface([15, 15])
        self.image.fill(colour)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
        self.going_down = True
         
        self.speed = 1000/speed
        self.next_update_time = 0
        
    def update(self, current_time, bottom):
        if self.next_update_time < current_time:
            if self.rect.bottom >= bottom:
                self.going_down = False
            elif self.rect.top <= 0:
                self.going_down = True
                
            self.rect.top += 1 if self.going_down else -1
            
            self.next_update_time += self.speed
        
        

if __name__ == '__main__':
    import sys
    pygame.init()
    
    size = width, height = 320, 240
    speed = [2,2]
    black = 0, 0, 0
    framerate = 60
    
    screen = pygame.display.set_mode(size)
    
    boxes = pygame.sprite.RenderUpdates()
    
    for b in [Box([255,0,0], [0,0], 100),
             Box([0,255,0], [60, 137], 25),
             Box([0,0,255], [180, 252], 300)]:
        boxes.add(b)
        
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN: sys.exit()
            
        screen.fill(black)
        boxes.update(pygame.time.get_ticks(), 240)
        for b in boxes.sprites():
            screen.blit(b.image, b.rect)
            
        pygame.display.flip()