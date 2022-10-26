import pygame, pymunk, pymunk.pygame_util, math
import random
from settings import WIDTH, HEIGHT

class Ball():
    def __init__(self, space):
        self.image = pygame.image.load("Assets/Image/ball.png").convert_alpha()
        self.body = None
        self.shape = None
        self.newBall(space)
        self.pos = WIDTH/2 - self.image.get_width()/2, HEIGHT/2 - 150 - self.image.get_height()/2
        
    def draw(self, screen):
        if self.body != None:
            pos_x, pos_y = self.body._get_position()
            angle = -math.degrees(self.body._get_angle())
            orig_rect = self.image.get_rect()
            rot_image = pygame.transform.rotate(self.image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            self.pos = pos_x - rot_image.get_width()/2, pos_y - rot_image.get_height()/2
            screen.blit(rot_image, self.pos)
        
    def removeBall(self, space):
        space.remove(self.body, self.shape)
        self.body = None
        self.shape = None
        
    def newBall(self, space):
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = (WIDTH/2, HEIGHT/2 - 150)
        shape = pymunk.Circle(body, self.image.get_width()/2)
        shape.mass = 0.5
        shape.elasticity = 0.7
        shape.friction = 0.65
        space.add(body, shape)
        self.body = body
        self.shape = shape
        random_num = random.randint(0,1)
        if random_num == 0:
            self.body.apply_impulse_at_local_point((-100, 0))
        else:
            self.body.apply_impulse_at_local_point((100, 0))
    
    def isGoal(self):
        pos_x, pos_y = self.body._get_position()
        if pos_x <= 40 and pos_y >= 330:
            return 1 #Left
        if pos_x >= 1240 and pos_y >= 330:
            return -1 #Right