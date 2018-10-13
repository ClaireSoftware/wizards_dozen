"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
 
Explanation video: http://youtu.be/QplXBw_NK5Y
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
 
"""
 
import pygame
import time
from pygame.locals import *
from itertools import cycle
import os
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
powderblue=(176, 224, 230)
counter=0;
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 

# Game Initialization
pygame.init()
 
# Center the Game Application
#os.environ['SDL_VIDEO_CENTERED'] = '1'
 
 
# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText
 
# Game Fonts
font = "Retro.ttf"
 
 
# Game Framerate
clock = pygame.time.Clock()
FPS=60


def main_menu(screen):
    screen_width=800
    screen_height=600
    screen.fill(blue);
 
    menu=True
    selected="start"
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        return 0;e
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        # Main Menu UI
        title=text_format("A Wizard's Dozen", font, 90, yellow)
        font2 = "STIXGeneral.ttf"
        authors=text_format("by Aryana Dendy, Brandy Barfield, Claire Chambers," +
        " and Elizabeth Skeie", font2, 20, yellow);
        if selected=="start":
            text_start=text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)
 
        title_rect=title.get_rect()
        author_rect=authors.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(authors, (screen_width/2 - (author_rect[2]/2), 150));
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
    # -- Methods
    myIterator=cycle(range(3));
    images = ['resources/walking/tiles-0.png','resources/walking/tiles-1.png',
                  'resources/walking/tiles-2.png']
    leftimages = ['resources/walking/tiles-0-left.png','resources/walking/tiles-1-left.png','resources/walking/tiles-2-left.png']
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 64
        height = 64
        self.image = pygame.image.load("resources/walking/tiles-0.png");
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y 
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += .5
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -20
        #self.image = pygame.image.load("resources/walking/tiles-0-left.png");
 
    def go_right(self):
       
        """ Called when the user hits the right arrow. """
        #self.image = pygame.image.load(images[next(self.myIterator)]);
        self.change_x = 12
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.image.load("resources/dirt.png");
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    """ Enemy """

    def __init__(self,image):
        super().__init__()

        self.image = pygame.image.load(image);
        self.rect = self.image.get_rect();
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1650
 
        # Array with width, height, x, and y of platform # Difference of 160?
        level = [[210, 35, 500, 500],
                 [210, 35, 710, 450],
                 [210, 35, 870, 450],
                 [210, 35, 1000, 450],
                 [210, 35, 1120, 400],
                 [210, 35, 1250, 350],
                 [210, 35, 1400, 300],
                 [310, 100, 1560, 300],
                 ]
        images = [['resources/dragon.png',1650,250]]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        for enemy in images:
            sprite = Enemy(images[0][0]);
            sprite.rect.x=images[0][1];
            sprite.rect.y=images[0][2];
            self.enemy_list.add(sprite);
 
 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 35, 500, 500],
                 [210, 35, 870, 450],
                 [200, 35, 1000, 450],
                 [210, 35, 1220, 400],
                 [190, 35, 1450, 425],
                 [100, 35, 1300, 300],
                 [310, 35, 1560, 300],
        ]
        images = [['resources/dragon.png',1650,250]]
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        for enemy in images:
            sprite = Enemy(images[0][0]);
            sprite.rect.x=images[0][1];
            sprite.rect.y=images[0][2];
            self.enemy_list.add(sprite);
        
class Level_03(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 35, 500, 500],
                 [210, 35, 710, 450],
                 [210, 35, 870, 450],
                 [210, 35, 1000, 450],
                 [210, 35, 1120, 400],
                 [210, 35, 1250, 350],
                 [210, 35, 1400, 300],
                 [310, 100, 1560, 300],
                 ]
        images = [['resources/dragon.png',1650,250]]
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        for enemy in images:
            sprite = Enemy(images[0][0]);
            sprite.rect.x=images[0][1];
            sprite.rect.y=images[0][2];
            self.enemy_list.add(sprite);
        

def levelAlert(screen,message):
        alert=text_format(message, font, 30, black)
        alert_rect=alert.get_rect()
        area=screen.get_rect();
        # Main Menu Text
        screen.blit(alert, (area[2]/8 - (alert_rect[2]/2), 0))
    
def main():
    """ Main Program """
    pygame.init()
    background = pygame.image.load('resources/castle_background.png')
    background_rect = background.get_rect()
    background2 = pygame.image.load('resources/level2back.png');
    background2_rect = background2.get_rect();
    background3 = pygame.image.load('resources/lev3back.png');
    background3_rect = background3.get_rect();
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Side-scrolling Platformer")
    main_menu(screen)
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player));
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    rightwalk=False;
    leftwalk=False;
    while not done:
        if current_level_no == 0:
            screen.blit(background,background_rect);
        elif current_level_no ==1:
            screen.blit(background2,background2_rect);
        elif current_level_no == 2:
            screen.blit(background3,background3_rect);

        
        levelAlert(screen, ("You are on level " +str((current_level_no +1)) +"!"));
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                    leftwalk=True;
                if event.key == pygame.K_RIGHT:
                    rightwalk=True;
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                    leftwalk=False;
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                    rightwalk=False;
 
        # Update the player.
        if rightwalk:
            #print("rightwalk");
            player.image = pygame.image.load(player.images[next(player.myIterator)]);
        if leftwalk:
            #print("leftwalk");
            player.image = pygame.image.load(player.leftimages[next(player.myIterator)]);

        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        #print(current_position);
        if pygame.sprite.spritecollide(player, current_level.enemy_list, False):
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                pygame.draw.rect(screen, white, [0, 0, 800, 600], 2)
                break;
            
            
            
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(FPS)
 
        # Go ahead and update the screen with what we've drawn.
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.

    time.sleep(10);
    pygame.quit()
 
if __name__ == "__main__":
    main()
