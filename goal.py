import math
from turtle import back
from venv import create
import pygame
import pymunk
import pymunk.pygame_util
from settings import WIDTH, HEIGHT


class Goal():
    def __init__(self, space):
        self.back = pygame.image.load("Assets/Image/goal1.png")
        self.front = pygame.image.load("Assets/Image/goal2.png")
        rects = [
            [(30, HEIGHT - 440), (20, HEIGHT), math.pi/18],
            [(WIDTH - 30, HEIGHT - 440), (20, HEIGHT), -math.pi/18],
            [(60, HEIGHT - 440), (110, 20), 0],
            [(WIDTH - 60, HEIGHT - 440), (110, 20), 0],
            [(WIDTH/2, 10), (WIDTH, 20), 0]
        ]

        for pos, size, angle in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            body.angle = angle
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.5
            space.add(body, shape)

    def draw(self, screen, ball):
        screen.blit(self.back, (WIDTH - 113, HEIGHT - 445))
        screen.blit(pygame.transform.flip(
            self.back, flip_x=True, flip_y=False), (-14, HEIGHT - 445))
        ball.draw(screen)
        screen.blit(self.front, (WIDTH - 110, HEIGHT - 445))
        screen.blit(pygame.transform.flip(
            self.front, flip_x=True, flip_y=False), (-59, HEIGHT - 445))
