import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.8
JUMP_STRENGTH = -20
GROUND_Y = HEIGHT - 60

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)

# Load assets
giraffe_img = pygame.image.load("giraffe.png")
giraffe_img = pygame.transform.scale(giraffe_img, (80, 80))
rock_img = pygame.image.load("rock.png")
rock_img = pygame.transform.scale(rock_img, (40, 40))
apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (30, 30))

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Giraffe Adventure")

# Game variables
giraffe_x, giraffe_y = 50, GROUND_Y - 80
giraffe_velocity = 0
is_jumping = False
obstacles = []
apples = []
clock = pygame.time.Clock()
running = True
score = 0
lives = 3
speed = 3

# Game loop
while running:
    screen.fill(BLUE)
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, 60))  # Draw ground
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                giraffe_velocity = JUMP_STRENGTH
                is_jumping = True
    
    # Update giraffe movement
    giraffe_velocity += GRAVITY
    giraffe_y += giraffe_velocity
    if giraffe_y >= GROUND_Y - 80:
        giraffe_y = GROUND_Y - 80
        is_jumping = False
    
    # Generate obstacles
    if random.randint(1, 100) < 2 and (len(obstacles) == 0 or obstacles[-1][0] < WIDTH - 150):
        obstacles.append([WIDTH, GROUND_Y - 40])
    if random.randint(1, 100) < 2:
        apples.append([WIDTH, GROUND_Y - random.randint(50, 100)])
    
    # Move obstacles
    for rock in obstacles:
        rock[0] -= speed
    obstacles = [rock for rock in obstacles if rock[0] > -40]
    
    # Move apples
    for apple in apples:
        apple[0] -= speed
    apples = [apple for apple in apples if apple[0] > -30]
    
    # Check for collisions
    for rock in obstacles:
        if giraffe_x + 80 > rock[0] and giraffe_x < rock[0] + 40 and giraffe_y + 80 > rock[1]:
            lives -= 1
            obstacles.remove(rock)
            if lives == 0:
                running = False  # Game Over if all lives lost
    
    for apple in apples:
        if giraffe_x + 80 > apple[0] and giraffe_x < apple[0] + 30 and giraffe_y < apple[1] + 30 and giraffe_y + 80 > apple[1]:
            apples.remove(apple)
            score += 1  # Increase score if apple caught
    
    # Increase speed every 10 apples collected
    if score % 10 == 0 and score > 0 and speed < 10:
        speed += 1
    
    # Draw elements
    screen.blit(giraffe_img, (giraffe_x, giraffe_y))
    for rock in obstacles:
        screen.blit(rock_img, (rock[0], rock[1]))
    for apple in apples:
        screen.blit(apple_img, (apple[0], apple[1]))
    
    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
