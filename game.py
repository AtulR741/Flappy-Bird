import pygame
import random

# parameters

PASS_REWARD = 1
CRASH_PENALTY = -1

# constants
width, height = 1000, 700
score = 0

birdWidth = 100
birdPosition = (200, 300)

pipeWidth = 100
pipeGap = 200

pipesGap = 250

maxDifference = 350

minHeight = 500
maxHeight = 200

gravity = 0.5
scrollSpeed = 2
jump = -10

pipes = []
birdY = birdPosition[1]
birdSpeed = 0
nextPipe = 0

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)

bird = pygame.transform.scale(pygame.image.load('bird.png'), (birdWidth, birdWidth))
birdRect = bird.get_rect()
pipes = []

def get_state():
        x = (pipes[nextPipe][0] - birdPosition[0])
        y = (pipes[nextPipe][1] - birdY)
        state = [
            x - 0.5*pipeWidth,
            x + 0.5*pipeWidth,
            y - 0.5*pipeGap,
            y + 0.5*pipeGap,
            birdSpeed
        ]

        return state

def addPipe(pipes):
    if pipes[-1][0] <= width - pipesGap + 0.5*pipeWidth:
        gapX = pipesGap
        gapY = random.random() * maxDifference * 2 - maxDifference
        y = max(min(pipes[-1][1] + gapY, minHeight), maxHeight)
        newPipe = [pipes[-1][0] + gapX, y]
        pipes.append(newPipe)

def init():
    global birdY, birdSpeed, pipes, birdRect, nextPipe, score
    score = 0
    birdY = birdPosition[1]
    birdSpeed = 0

    pipes = [[400, 300]]

    birdRect.centery = birdY
    nextPipe = 0

def clamp(min, max, val):
    if val < min:
        return min
    elif val > max:
        return max
    return val

def collision():
    global pipes
    for i in range(2):
        closestX = clamp(pipes[i][0] - 0.5*pipeWidth, pipes[i][0] + 0.5*pipeWidth, birdPosition[0])
        #upper rectangle
        closestY = clamp(0, pipes[i][1] - 0.5*pipeGap, birdY)
        dx, dy = closestX - birdPosition[0], closestY - birdY
        if dx**2 + dy**2 < 0.25*birdWidth:
            return True
        #lower rectangle
        closestY = clamp(pipes[i][1] + 0.5*pipeGap, height, birdY)
        dy = closestY - birdY
        if dx**2 + dy**2 < 0.25*birdWidth:
            return True
    return False

def play_step(move, record):
    global birdSpeed, birdY, pipes, nextPipe, score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                move[1] = 1

    reward = 0
    if birdY - 0.5*birdWidth >= pipes[nextPipe][1] - 0.5*pipeGap and birdY + 0.5*birdWidth <= pipes[nextPipe][1] + 0.5*pipeGap:
        reward = 0.5
    done = False

    # action
    if move[1]:
        birdSpeed = jump

    # position
    birdY += birdSpeed

    # gravity
    birdSpeed += gravity

    # scroll
    for i in range(len(pipes)):
        pipes[i][0] -= scrollSpeed

    # add pipe
    addPipe(pipes)

    # delete front pipe
    if pipes[0][0] + 0.5*pipeWidth < 0:
        pipes.pop(0)
        nextPipe -= 1

    # collision detection
    if birdY - 0.5*birdWidth < 0 or birdY + 0.5*birdWidth > height:
        reward = CRASH_PENALTY*2
        done = True
    elif collision(): 
        reward = CRASH_PENALTY
        done = True
    
    # passing a pipe
    if pipes[nextPipe][0] + 0.5*pipeWidth < birdPosition[0]:
        score += 1
        nextPipe += 1
        reward = PASS_REWARD
    
    # draw
    screen.fill('CYAN')
    for i in range(len(pipes)):
        #upper pipe
        image = pygame.transform.scale(pygame.image.load('pipe2.png'), (pipeWidth, 0.75*height))
        imageRect = image.get_rect(midbottom = (pipes[i][0], pipes[i][1] - 0.5*pipeGap))
        screen.blit(image, imageRect)
        # lower pipe
        image = pygame.transform.scale(pygame.image.load('pipe1.png'), (pipeWidth, 0.75*height))
        imageRect = image.get_rect(midtop = (pipes[i][0], pipes[i][1] + 0.5*pipeGap))
        screen.blit(image, imageRect)
    birdRect.center = (birdPosition[0], birdY)
    screen.blit(bird, birdRect)

    text = font.render(f'Score : {score}', False, 'RED')
    textRect = text.get_rect(midleft = (10, 20))
    screen.blit(text, textRect)

    text = font.render(f'HI : {record}', False, 'BLUE')
    textRect = text.get_rect(midright = (990, 20))
    screen.blit(text, textRect)

    # 60 fps
    pygame.display.update()
    clock.tick(60)

    return score, reward, done