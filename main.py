import pygame
from pygame import mixer
import sys
import pymunk
import pymunk.pygame_util
import math
from button import Button
from player import Player
from ball import Ball
from ground import Ground
from goal import Goal
from scoreboard import ScoreBoard
from settings import HEIGHT, WIDTH, FPS, DT

pygame.init()
mixer.init()
music_playing = False

KICK_SOUND = mixer.Sound("Assets/Sound/kick.wav")
G_START = mixer.Sound("Assets/Sound/gStart.wav")
G_END = mixer.Sound("Assets/Sound/gEnd.wav")
GOAL_SOUND = mixer.Sound("Assets/Sound/goalScored.wav")

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Head Soccer")
CLOCK = pygame.time.Clock()
BG = pygame.image.load("Assets/Image/background.png")
LOGO = pygame.image.load("Assets/Image/logo.png")
GOALLLL = pygame.image.load("Assets/Image/goallll.png")

def get_font(font_path, size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(font_path, size)

def draw(player1, player2, goal, ball, sc):
    player1.draw(SCREEN)
    player2.draw(SCREEN)
    goal.draw(SCREEN, ball)
    sc.update()
    sc.draw(SCREEN)
    pygame.display.update()

def player_selection(text):
    head_path = None
    selected = None
    font = get_font("Assets/font2.ttf", 50)
    title = font.render(text, True, "white")
    title_rect = title.get_rect(center=(WIDTH/2, 100))
    COMFIRM_BUTTON = Button(image=None, pos=(WIDTH/2, 700),
                          text_input="COMFIRM", font=get_font("Assets/font.ttf", 20), base_color="White", hovering_color="Green")
    
    SELECTION_TABLE = pygame.image.load("Assets/Image/player_selection.png")
    SELECTION_BORDER = pygame.image.load("Assets/Image/select_border.png")
    with open("Assets/player.txt", 'r') as f:
        PLAYRER_LIST = f.read().splitlines()
    # print(PLAYRER_LIST)
    POS_LIST = [(217, 125), (311, 125), (405, 125), (499, 125), (593, 125),
                (687, 125), (781, 125), (875, 125), (969, 125),
                (217, 252), (311, 252), (405, 252), (499, 252), (593, 252),
                (687, 252), (781, 252), (875, 252), (969, 252),
                (217, 379), (311, 379), (405, 379), (499, 379), (593, 379),
                (687, 379), (781, 379), (875, 379), (969, 379),
                (217, 506), (311, 506), (405, 506), (499, 506), (593, 506),
                (687, 506), (781, 506), (875, 506), (969, 506)]
    while True:
        SCREEN.blit(SELECTION_TABLE, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        COMFIRM_BUTTON.changeColor((mouse_x, mouse_y))
        COMFIRM_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(POS_LIST)):
                    if mouse_x >= POS_LIST[i][0] and mouse_x <= POS_LIST[i][0] + 94 and mouse_y >= POS_LIST[i][1] and mouse_y <= POS_LIST[i][1] + 99:
                        head_path = PLAYRER_LIST[i]
                        selected = POS_LIST[i]
                        break;
                    if COMFIRM_BUTTON.checkForInput((mouse_x, mouse_y)) and head_path != None:
                        return head_path
        if selected != None:
            SCREEN.blit(SELECTION_BORDER, selected)
        SCREEN.blit(title, title_rect)
        pygame.display.update()

def play():
    global music_playing
    if not music_playing:
        mixer.music.load("Assets/Sound/play.wav")
        mixer.music.set_volume(0.2)
        mixer.music.play(loops=-1)
    field_bg = pygame.image.load("Assets/Image/Bg.jpg").convert_alpha()
    head_path1 = player_selection("Chọn nhân vật cho Player1")
    shoe_path1 = "Assets/Image/shoe1.png"
    head_path2 = player_selection("Chọn nhân vật cho Player2")
    shoe_path2 = "Assets/Image/shoe2.png"
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(SCREEN)
    player1 = Player(head_path1, shoe_path1, (240, 560), True, space)
    player2 = Player(head_path2, shoe_path2, (946, 560), False, space)
    ball = Ball(space)
    ground = Ground(space)
    goal = Goal(space)
    sc = ScoreBoard(get_font("Assets/font2.ttf", 35))
    SCREEN.blit(field_bg, (0, 0))
    draw(player1, player2, goal, ball, sc)
    G_START.play()
    pygame.time.delay(int(G_START.get_length() * 1000))
    sc.start()
    while True:
        SCREEN.blit(field_bg, (0, 0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.moving = True
                    player1.face_right = False
                if event.key == pygame.K_d:
                    player1.moving = True
                    player1.face_right = True
                if event.key == pygame.K_w:
                    player1.jumping = True
                if event.key == pygame.K_c:
                    player1.shooting = True
                if event.key == pygame.K_LEFT:
                    player2.moving = True
                    player2.face_right = False
                if event.key == pygame.K_RIGHT:
                    player2.moving = True
                    player2.face_right = True
                if event.key == pygame.K_UP:
                    player2.jumping = True
                if event.key == pygame.K_m:
                    player2.shooting = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and not player1.face_right:
                    player1.moving = False
                if event.key == pygame.K_d and player1.face_right:
                    player1.moving = False
                if event.key == pygame.K_LEFT and not player2.face_right:
                    player2.moving = False
                if event.key == pygame.K_RIGHT and player2.face_right:
                    player2.moving = False
        player1.update()
        player2.update()
        if player1.collision(ball.image, ball.pos):
            KICK_SOUND.play()
            if player1.shoe_angle > 0:
                ball.body.angle = -math.radians(player1.shoe_angle * 1.5)
                if player1.moving:
                    ball.body.apply_impulse_at_local_point((400, 0))
                else:
                    ball.body.apply_impulse_at_local_point((200, 0))
            elif player1.shoe_angle < 0:
                ball.body.angle = math.pi - math.radians(player1.shoe_angle * 1.5)
                if player1.moving:
                    ball.body.apply_impulse_at_local_point((400, 0))
                else:
                    ball.body.apply_impulse_at_local_point((200, 0))
        if player2.collision(ball.image, ball.pos):
            KICK_SOUND.play()
            if player2.shoe_angle > 0:
                ball.body.angle = -math.radians(player2.shoe_angle * 1.5)
                if player2.moving:
                    ball.body.apply_impulse_at_local_point((400, 0))
                else:
                    ball.body.apply_impulse_at_local_point((200, 0))
            elif player2.shoe_angle < 0:
                ball.body.angle = math.pi - math.radians(player2.shoe_angle * 1.5)
                if player2.moving:
                    ball.body.apply_impulse_at_local_point((400, 0))
                else:
                    ball.body.apply_impulse_at_local_point((200, 0))
        if ball.isGoal() == 1:
            sc.player2_score += 1
            sc.pause()
            SCREEN.blit(GOALLLL, GOALLLL.get_rect(center = (WIDTH/2, 300)))
            draw(player1, player2, goal, ball, sc)
            GOAL_SOUND.play()
            pygame.time.delay(int(GOAL_SOUND.get_length() * 1000))
            player1.setDefaultPos()
            player2.setDefaultPos()
            ball.removeBall(space)
            ball.newBall(space)
            KICK_SOUND.play()
            sc.start()
        if ball.isGoal() == -1:
            sc.player1_score += 1
            sc.pause()
            SCREEN.blit(GOALLLL, GOALLLL.get_rect(center = (WIDTH/2, 300)))
            draw(player1, player2, goal, ball, sc)
            GOAL_SOUND.play()
            pygame.time.delay(int(GOAL_SOUND.get_length() * 1000))
            player1.setDefaultPos()
            player2.setDefaultPos()
            ball.removeBall(space)
            ball.newBall(space)
            KICK_SOUND.play()
            sc.start()
        # space.debug_draw(draw_options)
        draw(player1, player2, goal, ball, sc)
        # pygame.image.save(SCREEN, "screenshot.jpeg")
        if sc.counter <= 0:
            G_END.play()
            pygame.time.wait(int(G_END.get_length() * 1000))
            end(sc)
            return
        space.step(DT)
        CLOCK.tick(FPS)


def end(sc):
    OPTIONS_BACK = Button(image=None, pos=(90, 60),
                          text_input="BACK", font=get_font("Assets/font.ttf", 20), base_color="White", hovering_color="Green")
    result = None
    font = get_font("Assets/font2.ttf", 100)
    if sc.player1_score > sc.player2_score:
        result = font.render(f"{sc.player1_name} chiến thắng", True, "white")
    elif sc.player1_score < sc.player2_score:
        result = font.render(f"{sc.player2_name} chiến thắng", True, "white")
    else:
        result = font.render(f"Tỉ số hoà", True, "white")
    result_rect = result.get_rect(center=(WIDTH/2, 2*HEIGHT/5))
    score = font.render(f"{sc.player1_score} - {sc.player2_score}", True, "white")
    score_rect = score.get_rect(center=(WIDTH/2, 4*HEIGHT/5))
    while True:
        SCREEN.fill("black")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return
        SCREEN.blit(result, result_rect)
        SCREEN.blit(score, score_rect)
        pygame.display.update()

def how_to_play():
    HOW_TO_PLAY_IM = pygame.image.load("Assets/Image/howto.png")
    OPTIONS_BACK = Button(image=None, pos=(90, 60),
                          text_input="BACK", font=get_font("Assets/font.ttf", 20), base_color="White", hovering_color="Green")

    while True:
        SCREEN.blit(HOW_TO_PLAY_IM, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def about():
    ABOUT_IM = pygame.image.load("Assets/Image/credit.png")
    OPTIONS_BACK = Button(image=None, pos=(90, 60),
                          text_input="BACK", font=get_font("Assets/font.ttf", 20), base_color="White", hovering_color="Green")

    while True:
        SCREEN.blit(ABOUT_IM, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    global music_playing
    if not music_playing:
        mixer.music.load("Assets/Sound/home.wav")
        mixer.music.play(loops=-1)
        music_playing = True
    PLAY_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(332, 400),
                         text_input="PLAY", font=get_font("Assets/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
    HOW_TO_PLAY_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(947, 400),
                                text_input="HOW TO PLAY", font=get_font("Assets/font.ttf", 50), base_color="#d7fcd4", hovering_color="White")
    ABOUT_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(332, 550),
                          text_input="ABOUT", font=get_font("Assets/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(947, 550),
                         text_input="QUIT", font=get_font("Assets/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")

    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(LOGO, (184, 20))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, HOW_TO_PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.music.stop()
                    music_playing = False
                    play()
                if HOW_TO_PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    how_to_play()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
