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
    screen = pygame.display.set_mode((SokobanState.max_rows * scale, SokobanState.max_cols * scale))

    box_img = pygame.image.load('src/sokoban_box.png')
    box_img = pygame.transform.scale(box_img, (scale, scale))

    player_img = pygame.image.load('src/sokoban_player.png')
    player_img = pygame.transform.scale(player_img, (scale, scale))

    wall_img = pygame.image.load('src/sokoban_wall.png')
    wall_img = pygame.transform.scale(wall_img, (scale, scale))

    goal_img = pygame.image.load('src/sokoban_goal.png')
    goal_img = pygame.transform.scale(goal_img, (scale, scale))

    screen.fill((0, 0, 0))

    for box in state.box_set:
        draw(screen, box_img, box.row, box.col)

    for goal in SokobanState.goal_points:
        draw(screen, goal_img, goal.row,  goal.col)

    for wall in SokobanState.map_limits:
        draw(screen, wall_img, wall.row, wall.col)

    draw(screen, player_img, state.player_coord.row, state.player_coord.col)

    # cargar las cosas
    pygame.display.update()

    # guardar la imagen
    pygame.image.save(screen, filename)


def create_gif(filenames, output):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(output, images)