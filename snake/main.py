import random
import pygame
import time
pygame.init()
#caption
pygame.display.set_caption("Snake")
#textues:
background = pygame.image.load("textures/green_background.jpg")
red_t = pygame.image.load('textures/red.png')
yellow_t = pygame.image.load('textures/gold.png')
white_t = pygame.image.load('textures/white.png')
snake_textures = [red_t, yellow_t, white_t]

#parameters:
height = 800
width = 800
window = pygame.display.set_mode((width, height))
size = 50
snake_size = 1
snake_size_AI = 1
snake_dir = (0, 0)
snake_dir_AI = (0, 0)
snake_rect = pygame.Rect(snake_dir[0], snake_dir[1], size, size)
snake_rect_AI = pygame.Rect(snake_dir[0], snake_dir[1], size, size)
segments = [snake_rect.copy()]
segments_AI = [snake_rect_AI.copy()]
snake_dir = (0, 0)
snake_speed = 1
delay = 100
score = 0

run = True
game_over = False


def message(text):
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, (255, 255, 255))
    text_rect = message.get_rect(center=(width/2, height/2))
    window.blit(message, text_rect)


def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = (10, 10)
    window.blit(score_text, score_rect)


def AI_snake_move():
    global snake_dir_AI, snake_rect_AI
    if snake_dir_AI == (0, 0):  # Jeśli wąż AI stoi w miejscu
        snake_dir_AI = (size, 0)  # Ustawiamy początkowy kierunek ruchu

    # Sprawdzamy, czy wąż AI dotarł do krawędzi planszy
    if snake_rect_AI.x <= 0 or snake_rect_AI.x >= width - size or snake_rect_AI.y <= 0 or snake_rect_AI.y >= height - size:
        if snake_dir_AI == (size, 0):
            snake_dir_AI = (0, size)
        elif snake_dir_AI == (0, size):
            snake_dir_AI = (-size, 0)
        elif snake_dir_AI == (-size, 0):
            snake_dir_AI = (0, -size)
        elif snake_dir_AI == (0, -size):
            snake_dir_AI = (size, 0)
    else:
        snake_rect_AI.x += snake_dir_AI[0]
        snake_rect_AI.y += snake_dir_AI[1]


def snake_move():
    global snake_dir

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (size, 0):
        snake_dir = (-size, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-size, 0):
        snake_dir = (size, 0)
    if keys[pygame.K_UP] and snake_dir != (0, size):
        snake_dir = (0, -size)
    if keys[pygame.K_DOWN] and snake_dir != (0, -size):
        snake_dir = (0, size)


def draw_food(food_rect):
    pygame.draw.rect(window, (139,35,35),food_rect)


def get_food_rect():
    foodx = random.randrange(0, width, 50)
    foody = random.randrange(0, height, 50)
    food_rect = pygame.Rect(foodx, foody, size, size)
    return food_rect

def draw_snake():
    global snake_size, snake_rect, segments, score
    for segment in segments:
        if score < 50:
            window.blit(snake_textures[2], segment)
        if score >= 50 and score < 150:
            window.blit(snake_textures[1], segment)
        if score >= 150:
            window.blit(snake_textures[0], segment)

def draw_snake_AI():
    global segments_AI
    for segment in segments_AI:
        window.blit(snake_textures[1], segment)


def delete_segments(segments):
    global snake_size
    if len(segments) > snake_size:
        del segments[0]


def check_collision():
    global segments, game_over
    head = segments[0]
    for segment in segments[1:]:
        if segment.colliderect(head):
            game_over = True


def eating(x, y, food_rect):
    global score, snake_size
    if x == food_rect[0] and y == food_rect[1]:
        snake_size += 1
        score += 10
        return get_food_rect()
    return food_rect


def get_starting_position():
    x = random.randrange(50, width, 50)
    y = random.randrange(50, height, 50)
    return x, y


def Gameloop():
    global run, game_over, snake_size, snake_rect, segments, snake_speed, score, snake_rect_AI, segments_AI, snake_size_AI

    food_rect = get_food_rect()
    food_rect1 = get_food_rect()
    x,y = get_starting_position()
    x_AI, y_AI = get_starting_position()

    while run:
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not game_over:
            snake_move()
            x += snake_dir[0]
            y += snake_dir[1]
            AI_snake_move()
            x_AI += snake_dir_AI[0]
            y_AI += snake_dir_AI[1]

            snake_rect = pygame.Rect(x, y, size, size)
            snake_rect_AI = pygame.Rect(x_AI, y_AI, size, size)
            segments.append(snake_rect)
            segments_AI.append(snake_rect_AI)
            delete_segments(segments)
            delete_segments(segments_AI)
            if x > width or x < 0 or y > height or y < 0:
                game_over = True
            if x_AI > width or x_AI < 0 or y_AI > height or y_AI < 0:
                game_over = True

            window.blit(pygame.transform.scale(background, (height, width)), (0, 0))
            draw_snake()
            draw_snake_AI()
            draw_food(food_rect)
            draw_food(food_rect1)
            food_rect = eating(x, y, food_rect)
            food_rect = eating(x_AI, y_AI, food_rect)
            food_rect1 = eating(x, y, food_rect1)
            food_rect1 = eating(x_AI, y_AI, food_rect1)
            check_collision()
            draw_score(score)
        pygame.display.update()
        window.fill((0, 0, 0))

        if game_over:
            text = 'Game Over'
            message(text)
            pygame.display.update()
            time.sleep(1)
            run = False
    pygame.quit()


if __name__ == '__main__':
    Gameloop()
