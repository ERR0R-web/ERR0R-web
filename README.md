import pygame
import random

# Initialisation de pygame et configuration
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
SNAKE_BLOCK, SNAKE_SPEED = 10, 15
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def handle_key_events(x_change, y_change):
    """Gère les événements de touche pour le mouvement."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, None, True  # Quitter
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return -SNAKE_BLOCK, 0, False
            elif event.key == pygame.K_RIGHT:
                return SNAKE_BLOCK, 0, False
            elif event.key == pygame.K_UP:
                return 0, -SNAKE_BLOCK, False
            elif event.key == pygame.K_DOWN:
                return 0, SNAKE_BLOCK, False
    return x_change, y_change, False

def check_collision(x, y, snake_list):
    """Vérifie les collisions avec les bords de l'écran ou le serpent."""
    if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
        return True
    if [x, y] in snake_list[:-1]:
        return True
    return False

def game_loop():
    x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x_change, y_change = 0, 0
    snake_list, snake_length = [], 1
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    game_over = False
    while not game_over:
        # Gestion des événements
        x_change, y_change, game_over = handle_key_events(x_change, y_change)
        if game_over:
            break

        x += x_change
        y += y_change

        # Collision et nourriture
        if check_collision(x, y, snake_list):
            game_over = True
            continue

        snake_list.append([x, y])
        if len(snake_list) > snake_length:
            del snake_list[0]

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1

        # Dessin
        screen.fill(WHITE)
        for segment in snake_list:
            pygame.draw.rect(screen, BLACK, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()

game_loop()
