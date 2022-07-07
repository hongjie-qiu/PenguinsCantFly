import pygame
import random

# Game window set up
pygame.init()
pygame.mixer.init()
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
# game font
font = pygame.font.Font('assets/Terserah.ttf', 24)
huge_font = pygame.font.Font('assets/Terserah.ttf', 48)
# game window caption
pygame.display.set_caption('Penguins Can\'t Fly!')
# game screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (135, 206, 235)

# Drawing clouds
clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
cloud_images = []
for i in range(1, 4):
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    cloud_images.append(img)

# player variables
player_x = 240
player_y = 40
penguin = pygame.transform.scale(pygame.image.load('assets/penguin.png'), (50, 50))
direction = -1
y_speed = 0
gravity = 0.2
x_speed = 3
x_direction = 0
game_over = False

# score variables
score = 0
total_distance = 0
file = open('high_scores.txt', 'r')
read = file.readlines()
first_high = int(read[0])
high_score = first_high

# enemy variables
shark = pygame.transform.scale(pygame.image.load('assets/jetpack_shark.png'), (300, 200))
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]

# Sounds and music
pygame.mixer.music.load('assets/theme.wav')
bounce = pygame.mixer.Sound('assets/bounce2.wav')
end_sound = pygame.mixer.Sound('assets/game_over2.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

# Drawing the clouds
def draw_clouds(cloud_list, images):
    platforms = []
    for j in range(len(cloud_list)):
        image = images[cloud_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_list[j][0] + 5, cloud_list[j][1] + 40), (120, 10))
        screen.blit(image, (cloud_list[j][0], cloud_list[j][1]))
        #pygame.draw.rect(screen, 'gray', platform)
        platforms.append(platform); 
    return platforms

# Drawing the penguin
def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 7, y_pos + 40), (36, 10))
    #pygame.draw.rect(screen, 'green', player_rect, 3)
    return player_rect

# Drawing the shark
def draw_enemies(enemy_list, shark_img):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] + 40, enemy_list[j][1] + 50), (215, 70))
        #pygame.draw.rect(screen, 'orange', enemy_rect, 3)
        enemy_rects.append(enemy_rect)
        if enemy_list[j][2] == 1:
            screen.blit(shark_img, (enemy_list[j][0], enemy_list[j][1]))
        elif enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(shark_img, 1, 0), (enemy_list[j][0], enemy_list[j][1]))
    return enemy_rects

# Defining shark movement
def move_enemies(enemy_list, current_score):
    enemy_speed = 2 + current_score // 15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1: #shark going right
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1      
        elif enemy_list[j][2] == -1: #shark going left
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1

        if enemy_list[j][1] < - 100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)

    return enemy_list

# Updating objects during the game
def update_objects(cloud_list, play_y, enemy_list):
    lowest_cloud = 0
    update_speed = 10
    if play_y > 200:
        play_y -= update_speed
        for q in range(len(enemy_list)):
            enemy_list[q][1] -= update_speed

        for j in range(len(cloud_list)):
            cloud_list[j][1] -= update_speed
            if cloud_list[j][1] > lowest_cloud:
                lowest_cloud = cloud_list[j][1]

        if lowest_cloud < 750: 

            # randomly generating 1 or 2 clouds
            num_clouds = random.randint(1, 2)

            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)

                # appending the cloud
                cloud_list.append([x_pos, y_pos, cloud_type])
            else:
                # first cloud on the left side
                x_pos = random.randint(0, WIDTH / 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)

                # second cloud on the right side
                x_pos2 = random.randint(WIDTH / 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint(1, 3)

                # appending the clouds
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2])
    
    return play_y, cloud_list, enemy_list

run = True
while run:
    # initializing game screen
    screen.fill(bg)
    timer.tick(fps)
    
    cloud_platforms = draw_clouds(clouds, cloud_images) # initializing clouds
    
    player = draw_player(player_x, player_y, penguin, direction) # initializing player

    enemy_boxes = draw_enemies(enemies, shark) # initializing enemy
    enemies = move_enemies(enemies, score)

    # updating all the objects during the game 
    player_y, clouds, enemies = update_objects(clouds, player_y, enemies)

    # simulating game over
    if game_over:
        end_text = huge_font.render('Penguin Can\'t Fly!', True, 'black')
        end_text2 = font.render('Game Over: Press Enter to Restart', True, 'black')
        screen.blit(end_text, (65, 180))
        screen.blit(end_text2, (60, 280))
        player_y = -300
        y_speed = 0

    # handle bouncing
    for i in range(len(cloud_platforms)):
        if direction == -1 and player.colliderect(cloud_platforms[i]):
            y_speed *= -1
            if y_speed > -2:
                y_speed = -2
            bounce.play()
        
    # handling user controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
            if event.key == pygame.K_RETURN and game_over:
                # reset game status
                game_over = False
                # reset player
                player_x = 240
                player_y = 40
                direction = -1
                y_speed = 0
                x_speed = 3
                x_direction = 0
                # reset enemy
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                # reset clouds
                clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                # reset score
                score = 0
                total_distance = 0
                # reset music
                pygame.mixer.music.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0
            

    # Applying limitations to bouncing
    if y_speed < 10 and not game_over:
        y_speed += gravity

    # Movements during game play
    player_y += y_speed
    if y_speed < 0:
        direction = 1
    else:
        direction = -1
    player_x += x_speed * x_direction

    # Modifying movement for passing through left and right walls
    if player_x > WIDTH:
        player_x = -30
    elif player_x < -50:
        player_x = WIDTH - 20 
    
    # Collision detection for shark
    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            end_sound.play()
            game_over = True

            if score > first_high:
                file = open('high_scores.txt', 'w')
                write_score = str(score)
                file.write(write_score)
                first_high = score

    # Tracking Score
    total_distance += y_speed
    score = round(total_distance / 100)
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 70))
    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 40))


    pygame.display.flip()

pygame.quit()