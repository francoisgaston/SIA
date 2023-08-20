from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from data_structures.SokobanState import SokobanState
import imageio

scale = 50


def draw(screen, element, x, y):
    screen.blit(element, (x*scale, y*scale))


def print_state(state, filename):
    # init
    pygame.init()
    
    #display
    screen = pygame.display.set_mode((SokobanState.max_cols * scale, SokobanState.max_rows * scale))

    box_img = pygame.image.load('src/map/sokoban_box.png')
    box_img = pygame.transform.scale(box_img, (scale, scale))

    player_img = pygame.image.load('src/map/sokoban_player.png')
    player_img = pygame.transform.scale(player_img, (scale, scale))

    wall_img = pygame.image.load('src/map/sokoban_wall.png')
    wall_img = pygame.transform.scale(wall_img, (scale, scale))

    goal_img = pygame.image.load('src/map/sokoban_goal.png')
    goal_img = pygame.transform.scale(goal_img, (scale, scale))

    screen.fill((0, 0, 0))

    for box in state.box_set:
        draw(screen, box_img, box.col, box.row)

    for goal in SokobanState.goal_points:
        draw(screen, goal_img, goal.col,  goal.row)

    for wall in SokobanState.map_limits:
        draw(screen, wall_img, wall.col, wall.row)

    draw(screen, player_img, state.player_coord.col, state.player_coord.row)

    # cargar las cosas
    pygame.display.update()

    # guardar la imagen
    pygame.image.save(screen, filename)


def create_gif(filenames, output):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(output, images)