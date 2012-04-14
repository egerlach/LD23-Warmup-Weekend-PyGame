'''
Created on 2012-04-14

@author: egerlach
'''

import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, colour, initial_position):
        """Builds a Box sprite
        
        @param colour - a list of RGB values for the colour of the box
        @param initial_position - a list of two values for the top left coordinate of the box
        """
        # Call parent contstructor
        pygame.sprite.Sprite.__init__(self)
        
        # We need to create an image for the sprite. A 15x15 box will do
        self.image = pygame.Surface([15, 15])
        self.image.fill(colour)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
class MovingBox(Box):
    def __init__(self, colour, initial_position, speed):
        """Builds a Box sprite that moves up and down on its own
        
        @param colour - a list of RGB values for the colour of the box
        @param initial_position - a list of two values for the top left coordinate of the box
        @param speed - number of pixels per second that the box should move
        """
        Box.__init__(self, colour, initial_position)
        
        self.going_down = True
         
        self.speed = 1000/speed
        self.next_update_time = 0
        
    def update(self, current_time):
        if self.next_update_time < current_time:
            self.move()
            self.next_update_time += self.speed
            
    def move(self):
        pass
        
class UpDownBox(MovingBox):
    def __init__(self, colour, initial_position, speed, bottom):
        """Builds a Box sprite that moves up and down on its own
        
        @param colour - a list of RGB values for the colour of the box
        @param initial_position - a list of two values for the top left coordinate of the box
        @param speed - number of pixels per second that the box should move
        """
        MovingBox.__init__(self, colour, initial_position, speed)
        
        self.going_down = True
        self.bottom = bottom
         
    def move(self):    
        if self.rect.bottom >= self.bottom:
            self.going_down = False
        elif self.rect.top <= 0:
            self.going_down = True
            
        self.rect.top += 1 if self.going_down else -1
        
            
class PlayerBox(UpDownBox):
    
    def __init__(self, colour, initial_position, speed, screen):
        """Builds a Box sprite that responds to keyboard commands of the player
        
        @param colour - a list of RGB values for the colour of the box
        @param initial_position - a list of two values for the top left coordinate of the box
        @param speed - number of pixels per second that the box should move while a key is held down
        """
        MovingBox.__init__(self, colour, initial_position, speed)
        
        self.direction = [0,0]
        self.clamp_rect = screen.get_rect()
        
    def move(self):
        self.rect.move_ip(*self.direction)
        self.rect.clamp_ip(self.clamp_rect)
    
    def stop(self):
        self.direction = [0,0]
        
    def up(self):
        self.direction = [0, -1]
    
    def down(self):
        self.direction = [0, 1]
    
    def left(self):
        self.direction = [-1, 0]
    
    def right(self):
        self.direction = [1, 0]
        
    def process_key(self, key):
        if key == pygame.K_DOWN:
            self.down()
        elif key == pygame.K_UP:
            self.up()
        elif key == pygame.K_LEFT:
            self.left()
        elif key == pygame.K_RIGHT:
            self.right()
        else:
            return False
        return True
        
def mainloop():        
    pygame.init()
    
    size = width, height = 320, 240
    speed = [2,2]
    black = 0, 0, 0
    framerate = 60
    
    screen = pygame.display.set_mode(size)
    background = pygame.Surface(size)
    background.fill([0,0,0])
    
    boxes = pygame.sprite.RenderUpdates()
    
    for b in [UpDownBox([255,0,0], [0,0], 100, 240),
             UpDownBox([0,255,0], [60, 137], 25, 240),
             UpDownBox([0,0,255], [180, 252], 300, 240)]:
        boxes.add(b)
        
    player = PlayerBox([255,255,0], [200, 10], 100, screen)
    boxes.add(player)
    
    keys_down = set()
    arrow_keys = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]
        
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            elif event.type == pygame.KEYDOWN:
                if player.process_key(event.key):
                    if event.key in arrow_keys:
                        keys_down.add(event.key)
                else:
                    if event.key == pygame.K_ESCAPE:
                        return
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.key)
                if len(keys_down) == 0:
                    player.stop()
            
        boxes.update(pygame.time.get_ticks())
        boxes.clear(screen, background)
        boxes.draw(screen)
            
        pygame.display.flip()

if __name__ == '__main__':
    mainloop()