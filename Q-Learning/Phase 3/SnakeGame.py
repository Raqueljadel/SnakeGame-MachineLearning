"""
Snake Eater Game
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import pygame
import sys
from snake_env import SnakeGameEnv
from q_learning import QLearning


def main():
    # Window size
    FRAME_SIZE_X = 500
    FRAME_SIZE_Y = 500

    # Colors (R, G, B)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)

    difficulty = 50  # Adjust as needed
    render_game = True  # Show the game or not
    growing_body = True  # Makes the body of the snake grow
    training = True  # Defines if it should train or not
    num_episodes = 1000  # Define the number of episodes for training
    ep_reward = []  # Initialize an empty list to store rewards of each episode
    total_food = 0

    pygame.init()
    env = SnakeGameEnv(FRAME_SIZE_X, FRAME_SIZE_Y, growing_body)
    # Define the number of states and actions correctly based on your discretization
    ql = QLearning(n_states=109, n_actions=4)  # Example, adjust n_states accordingly

    if render_game:
        game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
        fps_controller = pygame.time.Clock()

    for episode in range(num_episodes):
        state = env.reset()
        game_over = False
        total_reward = 0

        while not game_over:
            allowed_actions = env.get_allowed_actions()
            # 1. Choose an action based on the current state
            action = ql.choose_action(state, allowed_actions)
            # 2. Execute the chosen action and observe the next state and reward
            next_state, reward, game_over = env.step(action)
            # 3. Update the Q-table using the (state, action, reward, next state) tuple
            ql.update_q_table(state, action, reward, next_state)
            # 4. Update the current state to the next state for the next iteration
            state = next_state
            # Update total reward for tracking
            total_reward += reward

            # Render
            if render_game:
                game_window.fill(BLACK)
                snake_body = env.get_body()
                food_pos = env.get_food()
                for pos in snake_body:
                    pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

                pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

            if env.check_game_over():
                break

            if render_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()
                fps_controller.tick(difficulty)

        total_food += env.food_eaten
        ep_reward.append(total_reward)  # Append the total reward of the current episode to cum_reward
        ql.save_q_table()  # Save the Q-table after each episode if you wish
        print(f"Episode {episode + 1}, Total reward: {total_reward}")

    # Calculate the mean reward
    mean_reward = sum(ep_reward) / num_episodes
    print(f"Min reward {min(ep_reward)}, Max reward {max(ep_reward)}, Mean reward {mean_reward}, "
          f"Food Eaten {total_food}, Num of episodes {num_episodes}")


if __name__ == "__main__":
    main()
