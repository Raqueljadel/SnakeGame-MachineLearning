"""
Snake Eater
Made with PyGame
Last modification in January 2024 by José Carlos Pulido
Machine Learning Classes - University Carlos III of Madrid
"""
import os
import sys
import time
import random
import pandas as pd
import pygame

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 120

# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)


# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        # food in limit of frame size -> cannot go there (game_over)
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0] // 10)) * 10,
                         random.randrange(1, (FRAME_SIZE[1] // 10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.region_direction = region_snake_direction(self)
        self.obstacles = nearest_obstacle_direction(self)

        self.score = 0
        self.prev_score = self.score

        self.end_reason = None
        self.food_eaten = False
        self.old_direction = 'RIGHT'


# Region Direction
def region_snake_direction(game):
    center_x, center_y = FRAME_SIZE_X // 2, FRAME_SIZE_Y // 2
    snake_head_x, snake_head_y = game.snake_pos[0], game.snake_pos[1]
    snake_tail_x, snake_tail_y = game.snake_body[-1][0], game.snake_body[-1][1]

    head_direction = determine_direction(center_x, center_y, snake_head_x, snake_head_y)
    tail_direction = determine_direction(center_x, center_y, snake_tail_x, snake_tail_y)

    return [head_direction, tail_direction]


def determine_direction(center_x, center_y, snake_x, snake_y):
    if snake_y >= center_y and snake_x >= center_x:
        return 'NORTH-EAST'
    elif snake_y >= center_y and snake_x <= center_x:
        return 'NORTH-WEST'
    elif snake_y < center_y and snake_x > center_x:
        return 'SOUTH-EAST'
    else:
        return 'SOUTH-WEST'


# Game Over
def game_over(game):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X / 8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Move the snake
def move_keyboard(game, event):
    # Whenever a key is pressed down
    game.old_direction = game.direction
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    return change_to


# Move the snake
def move_tutorial_1(game):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    next_positions = {
        'LEFT': [game.snake_pos[0] - 10, game.snake_pos[1]],
        'RIGHT': [game.snake_pos[0] + 10, game.snake_pos[1]],
        'UP': [game.snake_pos[0], game.snake_pos[1] - 10],
        'DOWN': [game.snake_pos[0], game.snake_pos[1] + 10]

    }
    # Calculates the direction towards the food
    diff_x = game.snake_pos[0] - game.food_pos[0]
    diff_y = game.snake_pos[1] - game.food_pos[1]
    primary_direction = None
    if abs(diff_y) < abs(diff_x):
        primary_direction = 'LEFT' if diff_x > 0 else 'RIGHT'
    else:
        primary_direction = 'UP' if diff_y > 0 else 'DOWN'

    # If the primary direction is safe, it moves in that direction
    next_position = next_positions[primary_direction]
    if (
        0 <= next_position[0] < FRAME_SIZE_X and
        0 <= next_position[1] < FRAME_SIZE_Y and
        next_position not in game.snake_body
    ):
        return primary_direction

    # If the primary direction is not safe, it searches a safe direction
    for direction in directions:
        next_position = next_positions[direction]
        if (
            0 <= next_position[0] < FRAME_SIZE_X and
            0 <= next_position[1] < FRAME_SIZE_Y and
            next_position not in game.snake_body
        ):
            return direction
    # If no safe direction is found, it follows the current direction
    # If the current direction neither is safe, it chooses a random direction
    next_position = next_positions[game.direction]
    if (
        0 <= next_position[0] < FRAME_SIZE_X and
        0 <= next_position[1] < FRAME_SIZE_Y and
        next_position not in game.snake_body
    ):
        return game.direction
    else:
        return random.choice(directions)

# Function to calculate direction of the nearest obstacle
def nearest_obstacle_direction(game):
    head_x, head_y = game.snake_pos
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    obstacles = []

    # Check for walls
    if head_x == 0:
        obstacles.append('LEFT')
    elif head_x == FRAME_SIZE_X - 10:
        obstacles.append('RIGHT')
    if head_y == 0:
        obstacles.append('UP')
    elif head_y == FRAME_SIZE_Y - 10:
        obstacles.append('DOWN')

    # Check for snake body segments
    for segment in game.snake_body[1:]:
        segment_x, segment_y = segment
        if segment_x == head_x and segment_y < head_y:
            obstacles.append('UP')
        elif segment_x == head_x and segment_y > head_y:
            obstacles.append('DOWN')
        elif segment_y == head_y and segment_x < head_x:
            obstacles.append('LEFT')
        elif segment_y == head_y and segment_x > head_x:
            obstacles.append('RIGHT')

    # If there are multiple obstacles, prioritize vertical over horizontal
    if 'UP' in obstacles and 'DOWN' in obstacles:
        obstacles.remove('DOWN')
    if 'LEFT' in obstacles and 'RIGHT' in obstacles:
        obstacles.remove('RIGHT')

    # If no obstacles detected, return the current direction
    if not obstacles:
        return game.direction

    # Otherwise, return the direction of the nearest obstacle
    return obstacles[0]

# PRINTING DATA FROM GAME STATE
def print_state(game):
    print("--------GAME STATE--------")
    print("FrameSize:", FRAME_SIZE_X, FRAME_SIZE_Y)
    print("Direction:", game.direction)
    print("Snake X:", game.snake_pos[0], ", Snake Y:", game.snake_pos[1])
    print("Snake Body:", game.snake_body)
    print("Food X:", game.food_pos[0], ", Food Y:", game.food_pos[1])
    print("Score:", game.score)


def print_line_data(game):
    line_data = [
        DIFFICULTY,
        game.snake_pos[0],
        game.snake_pos[1],
        len(game.snake_body),
        game.food_pos[0],
        game.food_pos[1],
        game.food_eaten,
        food_eaten_count,
        game.old_direction,
        game.direction,
        game.region_direction[0],
        game.region_direction[1],
        game.obstacles,
        game.prev_score,
        game.score,
        game.end_reason,
        gameOver
    ]

    return line_data


# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
game = GameState((FRAME_SIZE_X, FRAME_SIZE_Y))
food_eaten_count = 0
while True:
    gameOver = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
        # game.direction = move_keyboard(game, event)

    # UNCOMMENT WHEN METHOD IS IMPLEMENTED
    game.direction = move_tutorial_1(game)

    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    elif game.direction == 'DOWN':
        game.snake_pos[1] += 10
    elif game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    elif game.direction == 'RIGHT':
        game.snake_pos[0] += 10

    # Region direction
    game.region_direction = region_snake_direction(game)
    # Nearest Obstacle
    game.obstacles = nearest_obstacle_direction(game)

    # Snake body growing mechanism
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.prev_score = game.score
        game.score += 100
        food_eaten_count += 1
        game.food_eaten = True
        game.food_spawn = False

    else:
        game.snake_body.pop()
        game.food_eaten = False
        game.prev_score = game.score
        game.score -= 1

    # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X // 10)) * 10, random.randrange(1, (FRAME_SIZE_Y // 10)) * 10]

    game.food_spawn = True

    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Check if the snake hits the walls
    if any(coord < 0 or coord > size - 10 for coord, size in zip(game.snake_pos, (FRAME_SIZE_X, FRAME_SIZE_Y))):
        game.end_reason = "Wall_Touched"
        gameOver = True

    # Touching the snake body
    if any(game.snake_pos == block for block in game.snake_body[1:]):
        game.end_reason = "Body_Touched"
        gameOver = True

    show_score(game, 1, WHITE, 'consolas', 15)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)
    # PRINTING STATE AND IN ARFF
    print_state(game)

    # After game logic, write game state to ARFF
    file_name = 'GameState.arff'
    if not os.path.isfile(file_name):
        with open(file_name, "w", newline='') as file:
            # Write header
            file.write('@relation GameState \n\n')
            # Write attributes
            attributes = [
                ('Difficulty', 'NUMERIC'),
                ('Head_X', "NUMERIC"),
                ('Head_Y', "NUMERIC"),
                ('Snake_Body_Length', "NUMERIC"),
                ('Food_Position_X', "NUMERIC"),
                ('Food_Position_Y', "NUMERIC"),
                ('Food_Eaten', '{True, False}'),
                ('Eaten_Food_Count', "NUMERIC"),
                ('Old_Direction', "{UP, DOWN, LEFT, RIGHT}"),
                ('Direction', "{UP, DOWN, LEFT, RIGHT}"),
                ('Head_Region_Direction', '{NORTH-EAST, NORTH-WEST, SOUTH-EAST, SOUTH-WEST}'),
                ('Tail_Region_Direction', '{NORTH-EAST, NORTH-WEST, SOUTH-EAST, SOUTH-WEST}'),
                ('Nearest_Obstacle', "{UP, DOWN, LEFT, RIGHT}"),
                ('Score', "NUMERIC"),
                ('Next_Score', 'NUMERIC'),
                ('Cause_Death', '{None, Body_Touched, Wall_Touched}'),
                ('OVER', '{True, False}}')
            ]
            for attribute in attributes:
                file.write('@attribute {} {}\n'.format(attribute[0], attribute[1]))
            file.write('\n@DATA\n')
    else:
        with open(file_name, "a", newline='') as file:
            # Write data
            data = ','.join(map(str, print_line_data(game)))
            file.write(data + '\n')

    if gameOver:
        game_over(game)




