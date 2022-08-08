# import libraries
import pygame
import random

# initialize pygame
pygame.init()

# constant variables
width = 1000
height = 600
font_Small = pygame.font.Font("freesansbold.ttf", 20)
font_Big = pygame.font.Font("freesansbold.ttf", 32)
font_Medium = pygame.font.Font("freesansbold.ttf", 27)
gravity = 1
max_Platforms = 10
background = [135, 206, 235]
red = [255, 0, 0]
green = [0, 200, 0]
black = [0, 0, 0]
scroll_Speed = 1

# game window
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Test Platformer")
icon = pygame.image.load("gameIcon.png").convert_alpha()
pygame.display.set_icon(icon)

# platform class
class Platform():

    def __init__(self, x=50, y=height / 2):
        self.rect = pygame.Rect(x, y, 100, 5)

    def getPlatformRect(self):
        return self.rect

# game variables
score = 0
# create platform instances
platform_List = [Platform()]
for i in range(1, max_Platforms):
    # platforms staying in bounds
    if platform_List[i-1].getPlatformRect().y - 100 < -height + 5:
        platform_List.append(Platform(platform_List[i - 1].getPlatformRect().x + random.randint(115, 200),
                                      platform_List[i - 1].getPlatformRect().y + random.randint(0, 100)))
    elif platform_List[i-1].getPlatformRect().y + 100 > height - 5:
        platform_List.append(Platform(platform_List[i - 1].getPlatformRect().x + random.randint(115, 200),
                                      platform_List[i - 1].getPlatformRect().y + random.randint(-100, 0)))
    else:
        platform_List.append(Platform(platform_List[i-1].getPlatformRect().x + random.randint(115, 200),
                                  platform_List[i-1].getPlatformRect().y + random.randint(-100, 100)))
y_Change = 0
x_Change = 0
active = False
game_Over = False
flip = False
moveLeft = False
moveRight = False
highScore = 0

# player class
class Player():
    def __init__(self, x, y):
        self.icon = pygame.transform.scale(icon, (28,28))
        self.width = 18
        self.height = 28
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)

    def playerFunc(self):
        screen.blit(pygame.transform.flip(self.icon, flip, False), (self.rect.x - 4, self.rect.y - 1))
        pygame.draw.rect(screen, black, self.rect, 1)

    def getRect(self):
        return self.rect

# create player instance
player = Player(50, 0)

# text function
def draw_Text(text, font, colour, x, y):
    text = font.render(text, True, colour)
    screen.blit(text, (x,y))

def platformFunc():
    for plat in platform_List:
        pygame.draw.rect(screen, black, plat.getPlatformRect())

# screen initialization
running = True
while running:
    pygame.time.Clock().tick(60)
    screen.fill(background)

    # start screen/game reset
    if not active:
        if game_Over:
            draw_Text("Game Over", font_Big, red, 340, 200)
            draw_Text("Score: " + str(score), font_Medium, green, 340, 240)
            draw_Text("High Score: " + str(highScore), font_Medium, green, 340, 280)
            draw_Text("Press Space to Retry", font_Small, black, 340, 320)
        else:
            draw_Text("Press Space to Start", font_Big, black, 340, 50)
        player = Player(50, 0)
        player.rect.bottom = platform_List[0].getPlatformRect().centery
        platform_List[0].getPlatformRect().x = 50
        platform_List[0].getPlatformRect().y = height/2
        flip = False
        y_Change = 0
        x_Change = 0
        scroll_Speed = 1

    # quitting/movement controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not active:
            if event.key == pygame.K_SPACE:
                active = True
                score = 0
        elif event.type == pygame.KEYDOWN and active:
            for platform in platform_List:
                if event.key == pygame.K_SPACE and platform.getPlatformRect().colliderect(player.getRect()) \
                        and y_Change == 0:
                    y_Change = 20
            if event.key == pygame.K_RIGHT:
                moveRight = True
                moveLeft = False
            if event.key == pygame.K_LEFT:
                moveLeft = True
                moveRight = False
        if event.type == pygame.KEYUP and active:
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_LEFT:
                moveLeft = False


    if active:
        score += 1
        # player movement
        x_Change = -scroll_Speed
        if moveLeft:
            x_Change = -scroll_Speed - 3
            flip = True
        if moveRight:
            x_Change = 3
            flip = False
        player.rect.y -= y_Change
        player.rect.x += x_Change
        y_Change -= gravity
        # scrolling platforms
        for plat in platform_List:
            plat.getPlatformRect().x -= scroll_Speed
            if plat.getPlatformRect().right < 0:
                platform_List.remove(plat)
                # platforms staying in bounds
                if platform_List[-1].getPlatformRect().y - 100 < 50:
                    platform_List.append(Platform(platform_List[-1].getPlatformRect().x + random.randint(115, 200),
                                                  platform_List[-1].getPlatformRect().y + random.randint(0, 100)))
                elif platform_List[-1].getPlatformRect().y + 100 > height - 10:
                    platform_List.append(Platform(platform_List[-1].getPlatformRect().x + random.randint(115, 200),
                                                  platform_List[-1].getPlatformRect().y + random.randint(-100, 0)))
                else:
                    platform_List.append(Platform(platform_List[-1].getPlatformRect().x + random.randint(115, 200),
                                                  platform_List[-1].getPlatformRect().y + random.randint(-100, 100)))

        # successful platform landing
        for platform in platform_List:
            if platform.getPlatformRect().colliderect(player.getRect()) and y_Change < 0:
                y_Change = 0
                player.rect.bottom = platform.getPlatformRect().centery

        # screen bounds
        if player.getRect().top > height or player.getRect().right < -12:
            active = False
            game_Over = True
            platform_List.clear()
            platform_List = [Platform()]
            for i in range(1, max_Platforms):
                platform_List.append(Platform(platform_List[i - 1].getPlatformRect().x + random.randint(95, 200),
                                          platform_List[i - 1].getPlatformRect().y + random.randint(-100, 100)))
        if player.getRect().x + x_Change >= width - 15:
            x_Change = 0

        # highscore update
        if score > highScore:
            highScore = score

        # score display
        draw_Text("Score: " + str(score), font_Small, green, 800, 50)
        draw_Text("High Score: " + str(highScore), font_Small, green, 800, 75)

        # game speedup
        if score % 1000 == 0 and scroll_Speed <= 5:
            scroll_Speed += 1


    player.playerFunc()
    platformFunc()
    pygame.display.flip()