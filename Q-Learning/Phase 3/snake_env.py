"""
Snake Eater Q learning basic algorithm
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random


class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.previous_positions = []
        self.reset()

    def reset(self):
        # Resets the environment with default values
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.food_eaten = 0  # Counter for the food eaten
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        self.previous_positions.append(self.snake_pos)
        self.update_snake_position(action)
        reward = self.calculate_reward()
        self.update_food_position()
        state = self.get_state()
        self.game_over = self.check_game_over()
        return state, reward, self.game_over

    # Allowed Actions
    def get_allowed_actions(self):
        # Initialize with all actions unavailable
        allowed_actions = [0] * 4
        # Snake can only move in directions orthogonal to its current movement
        if self.direction != 'DOWN':
            allowed_actions[0] = 1  # UP
        if self.direction != 'UP':
            allowed_actions[1] = 1  # DOWN
        if self.direction != 'LEFT':
            allowed_actions[2] = 1  # RIGHT
        if self.direction != 'RIGHT':
            allowed_actions[3] = 1  # LEFT
        return allowed_actions

    def get_closest_body_part_direction(self):
        closest_distance = float('inf')
        closest_part = None

        for part in self.snake_body:
            distance = abs(part[0] - self.food_pos[0]) + abs(part[1] - self.food_pos[1])
            if distance < closest_distance:
                closest_distance = distance
                closest_part = part

        if closest_part[0] < self.food_pos[0]:
            return 'RIGHT'
        elif closest_part[0] > self.food_pos[0]:
            return 'LEFT'
        elif closest_part[1] < self.food_pos[1]:
            return 'DOWN'
        else:
            return 'UP'

    # State Description
    def discretize_distance(self, distance_x, distance_y):
        # Calculate Manhattan distance
        manhattan_distance = abs(distance_x) + abs(distance_y)
        # Normalize the distance based on frame size
        normalized_distance = manhattan_distance / max(self.frame_size_x, self.frame_size_y)
        # Define discretization thresholds
        close_threshold = 0.3
        medium_threshold = 0.6
        # Discretize based on the normalized distance
        if normalized_distance <= close_threshold:
            return 1  # CLOSE
        elif close_threshold < normalized_distance <= medium_threshold:
            return 2  # MEDIUM DISTANCE
        else:
            return 3  # FAR

    def get_state(self):
        # Get snake and food positions
        snake_x, snake_y = self.snake_pos
        food_x, food_y = self.food_pos

        # Get relative distances and discretized distances
        relative_horizontal = 1 if food_x < snake_x else 2 if food_x > snake_x else 3
        # 1 -> LEFT
        # 2 -> RIGHT
        # 3 -> SAME
        relative_vertical = 1 if food_y < snake_y else 2 if food_y > snake_y else 3
        # 1 -> ABOVE
        # 2 -> BELOW
        # 3 -> SAME
        distance_x = food_x - snake_x
        distance_y = food_y - snake_y
        discretized_distance_food = self.discretize_distance(distance_x, distance_y)

        # Get the direction of the closest body part to the food
        closest_body_part_direction = self.get_closest_body_part_direction()
        if closest_body_part_direction == 'UP':
            closest_body_part_direction = 1
        elif closest_body_part_direction == 'DOWN':
            closest_body_part_direction = 2
        elif closest_body_part_direction == 'LEFT':
            closest_body_part_direction = 3
        elif closest_body_part_direction == 'RIGHT':
            closest_body_part_direction = 4

        # Convert boolean actions to integer for easier Q-table indexing
        state = (relative_horizontal, relative_vertical, discretized_distance_food, closest_body_part_direction)

        # Obtain the row number
        if self.game_over:
            print("dead")
            row = 108
        else:
            row = state[0] * 3 + state[1] * 3 + state[2] * 3 + state[3] * 4
        return row

    def get_body(self):
        return self.snake_body

    def get_food(self):
        return self.food_pos

    # Reward Function Design
    def calculate_reward(self):
        reward = 0
        # Assign rewards based on distance and game state
        if self.snake_pos == self.food_pos:
            reward += 550  # Increase reward for eating food
        else:
            reward -= 3  # Small penalty for every tick without eating

        snake_x, snake_y = self.snake_pos
        food_x, food_y = self.food_pos
        distance_x = food_x - snake_x
        distance_y = food_y - snake_y
        disc_distance = self.discretize_distance(distance_x, distance_y)

        if disc_distance == 1:
            reward += 50  # Increase reward for moving closer to food
        elif disc_distance == 3:
            reward -= 40  # Increase penalty for moving away from food

        # Reward the snake for moving in the correct direction
        if (snake_x < food_x and self.direction == "RIGHT") or \
                (snake_y < food_y and self.direction == "DOWN") or \
                (snake_x > food_x and self.direction == "LEFT") or \
                (snake_y > food_y and self.direction == "UP"):
            reward += 40
        if snake_x == food_x or snake_y == food_y:
            reward += 40

        # New condition: Reward the snake for moving in a straight line towards the food
        if (snake_x < food_x and self.direction == "RIGHT" and distance_y == 0) or \
                (snake_y < food_y and self.direction == "DOWN" and distance_x == 0) or \
                (snake_x > food_x and self.direction == "LEFT" and distance_y == 0) or \
                (snake_y > food_y and self.direction == "UP" and distance_x == 0):
            reward += 60

        # Penalize the snake for moving towards the wall
        if (snake_x > self.frame_size_x - 15 > food_x) or \
                (snake_y > self.frame_size_y - 15 > food_y) or \
                (snake_x < 15 < food_x) or (snake_y < 15 < food_y):
            reward -= 80

        # Additional penalties for game over
        if self.game_over:
            if self.food_eaten == 0:
                reward -= 300  # Additional penalty for not eating any food
            else:
                reward -= 150
        # Penalize the snake for moving into itself
        if any((self.snake_pos[0] == part[0] and self.snake_pos[1] == part[1]) for part in self.snake_body[1:]):
            reward -= 4

        # Penalty for loop behavior
        if self.snake_pos in self.previous_positions:
            reward -= 5

        return reward

    def check_game_over(self):
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True

        return False

    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'

        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.direction = direction
        self.snake_body.insert(0, list(self.snake_pos))

        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
            self.food_eaten += 1
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.snake_body.pop()

    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                             random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
