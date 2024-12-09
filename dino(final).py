import pygame
import random

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720
FPS = 60 
GROUND_HEIGHT = 70
VOLCANO_WIDTH, VOLCANO_HEIGHT = 170, 200
LAVA_WIDTH, LAVA_HEIGHT = 20, 70
DINO_WIDTH, DINO_HEIGHT = 50, 70

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Survivor")

# load images
dino_standing_image = pygame.image.load("/Users/trannguyen/Downloads/dinoStanding.png")
dino_running1_image = pygame.image.load("/Users/trannguyen/Downloads/dinoRunning.png")
dino_running2_image = pygame.image.load("/Users/trannguyen/Downloads/dinoRunning1.png")
dino_jumping_image = pygame.image.load("/Users/trannguyen/Downloads/dinoJumping.png")
sun_image = pygame.image.load("/Users/trannguyen/Downloads/sun.png")
cloud_image = pygame.image.load("/Users/trannguyen/Downloads/cloud.png")
volcano_image = pygame.image.load("/Users/trannguyen/Downloads/volcano.png")
falling_lava_image = pygame.image.load("/Users/trannguyen/Downloads/fallingLava.png")
lava_pool_image = pygame.image.load("/Users/trannguyen/Downloads/lavaPool.png")
grass_image = pygame.image.load("/Users/trannguyen/Downloads/grass.png")

# scale images
sun_image = pygame.transform.scale(sun_image, (100,100))
cloud_image = pygame.transform.scale(cloud_image, (100,50))
grass_image = pygame.transform.scale(grass_image, (SCREEN_WIDTH/4,50))
volcano_image = pygame.transform.scale(volcano_image, (VOLCANO_WIDTH, VOLCANO_HEIGHT))
falling_lava_image = pygame.transform.scale(falling_lava_image, (LAVA_WIDTH, LAVA_HEIGHT))
dino_standing_image = pygame.transform.scale(dino_standing_image, (DINO_WIDTH, DINO_HEIGHT))
dino_running1_image = pygame.transform.scale(dino_running1_image, (DINO_WIDTH, DINO_HEIGHT))
dino_running2_image = pygame.transform.scale(dino_running2_image, (DINO_WIDTH, DINO_HEIGHT))
dino_jumping_image = pygame.transform.scale(dino_jumping_image, (DINO_WIDTH, DINO_HEIGHT))

# fonction to create grass
def grass():
    for x in range(0, SCREEN_WIDTH, int(SCREEN_WIDTH/4)):
        screen.blit(grass_image, (x, SCREEN_HEIGHT - GROUND_HEIGHT))
        
# Dino position
dino = dino_standing_image.get_rect()
dino.x = SCREEN_WIDTH / 2 - DINO_WIDTH / 2
dino.y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT 

# lava falling
lava_falling_speed = 1
#falling_lava = falling_lava_image.get_rect()
falling_lava_list = []
lava_spawn_timer = 0
lava_spawn_interval = 60

# Jumping mechanics
velocity_y = 0
jump = False
facing_left = False
dino_state = "standing"
run_animation_timer = 0
current_running_image = dino_running1_image

# game loop
clock = pygame.time.Clock()
run = True
game_over = False

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_over:    
        # background elements
        screen.fill((135, 206, 250))#sky(blue)
        screen.blit(sun_image, (460, 50))
        screen.blit(cloud_image, (100, 80))
        screen.blit(cloud_image, (300, 120))
        screen.blit(cloud_image, (560, 45))
        screen.blit(volcano_image, (170, SCREEN_HEIGHT - GROUND_HEIGHT - VOLCANO_HEIGHT))

        # ground 
        pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))  # Brown ground

        # add grass on top of the ground
        grass()

        # Dino
        image_to_draw = dino_standing_image
    
     
    
        # Dino movement
        velocity_y += 0.1
        if velocity_y > 4:
            velocity_y = 4
            dino.y += velocity_y

        # collision with the ground
        if dino.y + DINO_HEIGHT >= SCREEN_HEIGHT - GROUND_HEIGHT:
            dino.y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
        
            jump = False

    
        # Dino controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dino.x -= 1
            dino_state = "running"
            facing_left = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dino.x += 1
            dino_state = "running"
            facing_left = False
        elif (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and not jump:
            velocity_y -= 12
            jump = True
            dino_state = "jumping"
        else:
            dino_state = "standing"


        # Running animation
        if dino_state == "running":
            run_animation_timer += 1
            if run_animation_timer >= 10: 
                if current_running_image == dino_running1_image:
                    current_running_image = dino_running2_image
                else:
                    current_running_image = dino_running1_image
                run_animation_timer = 0
            image_to_draw = current_running_image
        elif dino_state == "jumping":
            image_to_draw = dino_jumping_image
        else:
            image_to_draw = dino_standing_image

        # Flip image if facing left
        if facing_left:
            image_to_draw = pygame.transform.flip(image_to_draw, True, False)
        # Draw the dino
        screen.blit(image_to_draw, dino)
    
        # avoid the dino going off screen
        dino.x = max(0, min(SCREEN_WIDTH - DINO_WIDTH, dino.x))


        # lava spawning
        lava_spawn_timer += 1
        if lava_spawn_timer >= lava_spawn_interval:
            lava_spawn_timer = 0
            x_position = random.randint(0, int(SCREEN_WIDTH-LAVA_WIDTH))
            falling_lava_list.append(pygame.Rect(x_position, 0, LAVA_WIDTH, LAVA_HEIGHT))

        # lave falling
        for falling_lava in falling_lava_list:
            falling_lava.y += lava_falling_speed
    
        # add lava
        for falling_lava in falling_lava_list:
            screen.blit(falling_lava_image, falling_lava)

        # collision with lava 
        for falling_lava in falling_lava_list:
            if dino.colliderect(falling_lava):
                game_over = True

    # game over screen
    else:
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over!!!", True, (255,0,0))
        screen.fill((135, 206, 250))
        screen.blit(text, (130, 320))
    
    pygame.display.update()

pygame.quit()
