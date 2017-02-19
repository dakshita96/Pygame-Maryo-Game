import pygame,sys,random
import time

pygame.init()

display_width = 1200
display_height = 600

white = (255,255,255)
black = (0,0,0)

canvas =  pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Maryo")

topScore = 0

clock = pygame.time.Clock()
FPS = 20

menuImage = pygame.image.load("start.png")
menuImageRect = menuImage.get_rect() 
cactusImage = pygame.image.load("cactus_bricks.png")
cactusImageRect = cactusImage.get_rect()
cactusImageRect.centerx = display_width/2
cactusImageRect.centery = -100


fireImage = pygame.image.load("fire_bricks.png")
fireImageRect = fireImage.get_rect()
fireImageRect.centerx = display_width/2
fireImageRect.centery = display_height + 100

flameImage = pygame.image.load("fireball.png")
flameImageRect = flameImage.get_rect()

maryoImage = pygame.image.load("maryo.png")
maryoImageRect = maryoImage.get_rect()

dragonImage = pygame.image.load("dragon.png")
dragonImageRect = dragonImage.get_rect()

gameOverImage = pygame.image.load("end.png")
gameOverRect = gameOverImage.get_rect()

movey = 0

def gameOver():

    gameover = True
    pygame.mixer.music.load("mario_dies.wav")
    pygame.mixer.music.play(1)
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    gameover = False
                    pygame.mixer.music.stop()
                                 
        
        gameOverRect.centerx = (display_width/2)
        gameOverRect.centery = (display_height/2)

        canvas.blit(gameOverImage , gameOverRect)
        pygame.display.update()
        clock.tick(5)
    gameLoop()

font = pygame.font.SysFont(None,25)

class Maryo:
    global movey , gravity , cactusImageRect , fireImageRect
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = maryoImage
        self.imgRect = maryoImageRect
    def move(self):
        self.imgRect.center = self.x , self.y
        canvas.blit(self.img , self.imgRect)
    def update(self):
        if self.imgRect.top < cactusImageRect.bottom:
            gameOver()
        if self.imgRect.bottom > fireImageRect.top:
            gameOver()
            
class Dragon:
    global cactusImageRect , fireImageRect
    up = False
    down = True
    velocity = 10
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = dragonImage
        self.imgRect = dragonImageRect
    def move(self):
        self.imgRect.center = self.x , self.y
        canvas.blit(self.img , self.imgRect)
    def update(self):
        if self.imgRect.top < cactusImageRect.bottom:
            self.up = False
            self.down = True            
        if self.imgRect.bottom > fireImageRect.top:
            self.down = False
            self.up = True
        if self.up:
            self.y -= Dragon.velocity
        if self.down:
            self.y += Dragon.velocity

class Flames:
    global maryoImageRect 
    flameSpeed = 20
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = flameImage
        self.imgRect = flameImageRect
    def move(self):
        self.imgRect.center = self.x , self.y
        canvas.blit(self.img , self.imgRect)

    def update(self):
        self.x -= Flames.flameSpeed
    def collision(self):
        if self.imgRect.left <= maryoImageRect.right and self.imgRect.right >= maryoImageRect.left and ((self.imgRect.top >= maryoImageRect.top and self.imgRect.top <= maryoImageRect.bottom) or (self.imgRect.bottom >= maryoImageRect.top and self.imgRect.bottom <= maryoImageRect.bottom)):
            gameOver()
        
        
def terminate():
    pygame.quit()
    sys.exit()


def main_menu():

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    menu = False

        menuImageRect.centerx = (display_width/2)
        menuImageRect.centery = (display_height/2)

        canvas.blit(menuImage , menuImageRect)
        pygame.display.update()
        clock.tick(5)

def display(msg,color,displace = 25):
    textSurf = font.render(msg, True, color)
    textRect = textSurf.get_rect()
    textRect.centerx = display_width / 2
    textRect.centery = cactusImageRect.bottom + displace
    canvas.blit(textSurf , textRect)


def level(score):
    global cactusImageRect,fireImageRect,cactusImage,fireImage
    if score in range(0,40):
        cactusImageRect.centery = -50
        fireImageRect.centery =  display_height + 50
        canvas.blit(cactusImage, cactusImageRect)
        canvas.blit(fireImage, fireImageRect)
        return 1
    elif score in range(40,100):
        cactusImageRect.centery = 0
        fireImageRect.centery = display_height
        canvas.blit(cactusImage, cactusImageRect)
        canvas.blit(fireImage, fireImageRect)
        return 2
    elif score in range(100,180):
        cactusImageRect.centery = 50
        fireImageRect.centery = display_height - 50
        canvas.blit(cactusImage, cactusImageRect)
        canvas.blit(fireImage, fireImageRect)
        return 3
    elif score >= 180:
        cactusImageRect.centery = 100
        fireImageRect.centery = display_height - 100
        canvas.blit(cactusImage, cactusImageRect)
        canvas.blit(fireImage, fireImageRect)
        return 4
    


def gameLoop():
    global topScore
    direction = "up"
    score = 0
    gravity = False
    speed = 30
    movey = 0
    player = Maryo(50 , display_height/2)
    dragon = Dragon(display_width-70, display_height/2)
    pygame.mixer.music.load("mario_theme.wav")
    pygame.mixer.music.play(-1)

    flameList = []
    flameCounter = 0
    addFlames = 20
    while True:
        canvas.fill(black)
        l = level(score)

        if topScore < score:
            topScore = score

        flameCounter += 1
        
        if flameCounter == addFlames:
            flameCounter = 0
            newFlame = Flames(display_width-50 , dragon.y)
            flameList.append(newFlame)

        for f in flameList:
            f.move()
            f.update()
            f.collision()

            if f.x <= 0:
                del f
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_UP:
                    direction = "up"
                    gravity = False
                    movey -= speed
                    score += 1
                if event.key == pygame.K_DOWN:
                    direction = "down"
                    gravity = False
                    movey +=speed
                    score += 1
            if event.type == pygame.KEYUP:
                if direction == "up" or direction == "down":
                    gravity = True
                    movey = 0
        if gravity:
            movey = 10
                
                
                
        player.y += movey
        player.move()
        player.update()
        dragon.move()
        dragon.update()
        
        display("Score :"+str(score)+"||Top Score:"+str(topScore)+"||Level :"+str(l),white)
        pygame.display.update()
        clock.tick(FPS)
    pygame.mixer.music.stop()

main_menu()
gameLoop()

        

