import pygame
import sys
import random

def draw_floor():
    wn.blit(floor_surface,(floor_x_pos,900))
    wn.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            wn.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            wn.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            return False

    if birdRect.top <= -100 or birdRect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):  
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = birdFrames[birdIndex]
    new_bird_rect = new_bird.get_rect(center = (100,birdRect.centery))
    return new_bird,new_bird_rect

def scoreDisplay(gameState):
    if gameState == 'main_game':
        scoreSurface = gameFont.render(str(int(score)),True,(255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288,100))
        wn.blit(scoreSurface,scoreRect)
    if gameState == 'game_over':
        scoreSurface = gameFont.render(f'Score: {int(score)}' ,True,(255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288,100))
        wn.blit(scoreSurface,scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}' ,True,(255,255,255))
        highScoreRect = highScoreSurface.get_rect(center = (288,850))
        wn.blit(highScoreSurface,highScoreRect)

def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore


pygame.init()
wn = pygame.display.set_mode((576,1024))
pygame.display.set_caption('floopy bird')
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.ttf',40)


gravity = 0.25
bird_movement = 0
gameActive = True
score = 0
highScore = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


birdDownFlap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownFlap,birdMidFlap,birdUpFlap]
birdIndex = 0
bird_surface = birdFrames[birdIndex]
birdRect = bird_surface.get_rect(center = (100,512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

'''
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)
birdRect = bird_surface.get_rect(center = (100,512))
bird_surface = pygame.transform.flip(bird_surface,False,True)
'''
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

gameOverSurface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
gameOverRect = gameOverSurface.get_rect(center = (288,512))

flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
deathSound = pygame.mixer.Sound('sound/sfx_hit.wav')
scoreSound = pygame.mixer.Sound('sound/sfx_point.wav')
scoreSoundCountdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                bird_movement = 0
                bird_movement -= 10
                flapSound.play()
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                score = 0
                pipe_list.clear()
                birdRect.center = (100,512)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
        else:
            birdIndex = 0

        bird_surface,birdRect = bird_animation()

    wn.blit(bg_surface,(0,0))

    if gameActive:

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        birdRect.centery += bird_movement
        wn.blit(rotated_bird,birdRect)
        gameActive = check_collision(pipe_list)
        floor_x_pos -= 1
        
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)


        score += 0.01
        scoreDisplay('main_game')
        scoreSoundCountdown  -= 1
        if scoreSoundCountdown <= 0:
            scoreSound.play()
            scoreSoundCountdown = 100
            
    else:
        wn.blit(gameOverSurface,gameOverRect)
        highScore = updateScore(score,highScore)
        scoreDisplay('game_over')
    
    
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    wn.blit(floor_surface,(floor_x_pos,900))

    pygame.display.update()
    clock.tick(120)