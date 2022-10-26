import pygame
from pygame import mixer
import pymunk
import pymunk.pygame_util
import math
from pymunk import Vec2d
from settings import PLAYER_MAX_VELOCITY_X, PLAYER_MAX_VELOCITY_Y, GRAVITY

MASS = 10
# mixer.init()
# KICK_SOUND = mixer.Sound("Assets/Sound/kick.wav")


class Player(pygame.sprite.Sprite):
    moving = False
    jumping = False
    falling = True
    shooting = False
    velo_x = 5
    velo_y = 5
    angle_rot = 0.2

    def __init__(self, head_path, shoe_path, pos, face_right, space):
        pygame.sprite.Sprite.__init__(self)
        self.default_pos = pos
        self.default_dicr = face_right
        self.head_r = pygame.image.load(head_path).convert_alpha()
        self.shoe_r = pygame.image.load(shoe_path).convert_alpha()
        self.head_l = pygame.transform.flip(
            self.head_r, flip_x=True, flip_y=False)
        self.shoe_l = pygame.transform.flip(
            self.shoe_r, flip_x=True, flip_y=False)
        self.face_right = self.default_dicr
        self.head = self.head_r
        self.shoe = self.shoe_r
        self.h_width = self.head.get_width()
        self.h_height = self.head.get_height()
        self.s_width = self.shoe.get_width()
        self.s_height = self.shoe.get_height()
        if not face_right:
            self.head = self.head_l
            self.shoe = self.shoe_l
        self.head_x = pos[0] + self.h_width/2
        self.head_y = pos[1] - 102 + self.h_height/2
        self.shoe_x = self.head_x
        self.shoe_y = pos[1] - 22 + self.s_height/2
        self.shoe_angle = 0.0
        self.rot_shoe = self.shoe

        h_moment = pymunk.moment_for_circle(50, 0, 33)
        self.h_body = pymunk.Body(
            50, h_moment, body_type=pymunk.Body.KINEMATIC)
        self.h_body.position = (self.head_x, self.head_y)
        self.h_shape = pymunk.Circle(self.h_body, 33)
        self.h_shape.elasticity = 0.7
        self.h_shape.friction = 0.65
        space.add(self.h_body, self.h_shape)
        self.alreadyCollision = False

        # s_moment = pymunk.moment_for_circle(10, 0, 8)
        # self.s_body = pymunk.Body(
        #     50, s_moment, body_type=pymunk.Body.KINEMATIC)
        # self.s_body.position = (self.shoe_x, self.shoe_y)
        # self.s_shape = pymunk.Circle(self.s_body, 8)
        # self.s_shape.elasticity = 0.7
        # self.s_shape.friction = 0.65
        # space.add(self.s_body, self.s_shape)

    def update(self):
        if self.moving:
            if self.face_right:
                if self.head_x <= 1136:
                    self.head_x += self.velo_x
                    self.shoe_x = self.head_x
                    self.h_body.position = (self.head_x, self.head_y)
                    # self.s_body.position = (self.shoe_x, self.shoe_y)
                    self.head = self.head_r
                    self.shoe = self.shoe_r
            else:
                if self.head_x >= 144:
                    self.head_x -= self.velo_x
                    self.shoe_x = self.head_x
                    self.h_body.position = (self.head_x, self.head_y)
                    self.head = self.head_l
                    self.shoe = self.shoe_l

        if self.jumping:
            self.head_y -= self.velo_y * 4
            self.shoe_y -= self.velo_y * 4
            self.h_body.position = (self.head_x, self.head_y)
            self.velo_y -= GRAVITY
            if (self.velo_y < -5):
                self.jumping = False
                self.velo_y = 5
        if self.shooting:
            if self.face_right:
                self.shoe_angle = 45 * \
                    math.cos(math.pi/2 * self.angle_rot - math.pi/2)
                self.angle_rot += 0.2
            else:
                self.shoe_angle = -45 * \
                    math.cos(math.pi/2 * self.angle_rot - math.pi/2)
                self.angle_rot += 0.2
            if self.angle_rot > 2:
                self.angle_rot = 0.2
                self.shooting = False

    def collision(self, object, pos):
        mask1 = pygame.mask.from_surface(self.rot_shoe)
        mask2 = pygame.mask.from_surface(object)
        x = pos[0] - self.shoe_x + self.rot_shoe.get_width()/2
        y = pos[1] - self.shoe_y + self.rot_shoe.get_height()/2
        # print (mask1.overlap(mask2, (x, y)))
        if mask1.overlap(mask2, (x, y)) != None and not self.alreadyCollision and self.shooting and self.angle_rot <= 1:
            self.alreadyCollision = True
            return True
        if mask1.overlap(mask2, (x, y)) == None:
            self.alreadyCollision = False
        return False

    def draw(self, screen):
        screen.blit(self.head, (self.head_x - self.h_width /
                    2, self.head_y - self.h_height/2))
        self.rot_shoe = pygame.transform.rotate(self.shoe, self.shoe_angle)
        screen.blit(self.rot_shoe, (self.shoe_x - self.rot_shoe.get_width() /
                    2 + self.shoe_angle/2, self.shoe_y - self.rot_shoe.get_height()/2))

    def setDefaultPos(self):
        self.head_x = self.default_pos[0] + self.h_width/2
        self.head_y = self.default_pos[1] - 102 + self.h_height/2
        self.shoe_x = self.head_x
        self.shoe_y = self.default_pos[1] - 22 + self.s_height/2
        self.h_body.position = (self.head_x, self.head_y)
        self.face_right = self.default_dicr
        if self.default_dicr:
            self.head = self.head_r
            self.shoe = self.shoe_r
        else:
            self.head = self.head_l
            self.shoe = self.shoe_l
