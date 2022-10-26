import pygame
import sys
import pymunk.pygame_util
from pymunk import Vec2d
from datetime import datetime, timedelta
from settings import WIDTH, HEIGHT, TIME


class ScoreBoard():

    def __init__(self, font):
        self.image = pygame.image.load("Assets/Image/score.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos_x = WIDTH/2
        self.pos_y = self.height/2
        self.player1_name = "Player1"
        self.player2_name = "Player2"
        self.player1_score = 0
        self.player2_score = 0
        self.start_time = datetime.now()
        self.total_time = TIME
        self.counter = self.total_time
        self.isPause = True
        self.font = font

    def start(self):
        if self.isPause:
            self.start_time = datetime.now()
            self.isPause = False

    def update(self):
        if self.counter == 0:
            self.isPause = True
        if not self.isPause:
            deltaT = datetime.now() - self.start_time
            deltaT = deltaT.total_seconds()
            if deltaT <= self.total_time:
                self.counter = self.total_time - deltaT
            else:
                self.counter = 0

    def pause(self):
        self.isPause = True
        self.total_time = self.counter

    def reset(self):
        self.total_time = TIME

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x - self.width /
                    2, self.pos_y - self.height/2))
        time_left = round(self.counter)
        time_color = "green"
        if self.counter <= 10:
            time_left = round(self.counter, 2)
            time_color = "red"
        counter = self.font.render(str(time_left), True, time_color)
        player1_name = self.font.render(str(self.player1_name), True, "black")
        player1_score = self.font.render(
            str(self.player1_score), True, "white")
        player2_name = self.font.render(str(self.player2_name), True, "black")
        player2_score = self.font.render(
            str(self.player2_score), True, "white")
        screen.blit(counter, counter.get_rect(center=(WIDTH/2, 130)))
        screen.blit(player1_name, player1_name.get_rect(center=(345, 45)))
        screen.blit(player1_score, player1_score.get_rect(center=(596, 45)))
        screen.blit(player2_name, player2_name.get_rect(center=(935, 45)))
        screen.blit(player2_score, player2_score.get_rect(center=(684, 45)))


# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# font = pygame.font.Font("Assets/font2.ttf", 30)
# sc = ScoreBoard(font)
# sc.start()
# while True:
#     screen.fill("black")

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_a:
#                 sc.pause()
#                 print("pause")
#             if event.key == pygame.K_u:
#                 sc.start()
#                 print("start")
#             if event.key == pygame.K_r:
#                 sc.reset()
#                 print("reset")

#     sc.update()
#     sc.draw(screen)
#     pygame.display.update()
