import random
import pygame
import time
pygame.init()
#caption
pygame.display.set_caption("Snake")
#textues:
background = pygame.image.load("green_background.jpg")
red_t = pygame.image.load('red.png')
yellow_t = pygame.image.load('gold.png')
white_t = pygame.image.load('white.png')
snake_textures = [red_t, yellow_t, white_t]

#parameters:
height = 800
width = 800
window = pygame.display.set_mode((width, height))
green = (0,255,0)
size = 50
snake_size = 1
snake_dir = (0,0)
snake_rect = pygame.Rect(snake_dir[0], snake_dir[1], size, size)
segments = [snake_rect.copy()]
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
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_text, score_rect)
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
    global snake_size, score
    if x == food_rect[0] and y == food_rect[1]:
        snake_size += 1
        score += 10
        return get_food_rect()
    return food_rect

def Gameloop():
    global run, game_over, snake_size, snake_rect, segments, snake_speed, score

    food_rect = get_food_rect()
    food_rect1 = get_food_rect()
    x = random.randrange(50, width, 50)
    y = random.randrange(50, height, 50)
    while run:
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not game_over:
            snake_move()
            x += snake_dir[0]
            y += snake_dir[1]

            snake_rect = pygame.Rect(x, y, size, size)
            segments.append(snake_rect)
            delete_segments(segments)
            if x >= width or x <= 0 or y >= height or y <= 0:
                game_over = True

            window.blit(pygame.transform.scale(background, (height, width)), (0, 0))
            draw_snake()
            draw_food(food_rect)
            draw_food(food_rect1)
            food_rect = eating(x, y, food_rect)
            food_rect1 = eating(x, y, food_rect1)
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





