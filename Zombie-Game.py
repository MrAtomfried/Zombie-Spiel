import pygame
import sys

pygame.init()
wallpaper = pygame.image.load("Grafics/Background.jpg")
screen = pygame.display.set_mode([1920, 1080])
clock = pygame.time.Clock()
pygame.display.set_caption("PyGame Test")

attack_left = pygame.image.load("Grafics/angriffLinks.png")
attack_right = pygame.image.load("Grafics/angriffRechts.png")
jump = pygame.image.load("Grafics/sprung.png")
walk_right = [pygame.image.load("Grafics/rechts1.png"), pygame.image.load("Grafics/rechts2.png"), pygame.image.load("Grafics/rechts3.png"), pygame.image.load("Grafics/rechts4.png"), pygame.image.load("Grafics/rechts5.png"), pygame.image.load("Grafics/rechts6.png"), pygame.image.load("Grafics/rechts7.png"), pygame.image.load("Grafics/rechts8.png")]
walk_left = [pygame.image.load("Grafics/links1.png"), pygame.image.load("Grafics/links2.png"), pygame.image.load("Grafics/links3.png"), pygame.image.load("Grafics/links4.png"), pygame.image.load("Grafics/links5.png"), pygame.image.load("Grafics/links6.png"), pygame.image.load("Grafics/links7.png"), pygame.image.load("Grafics/links8.png")]
jump_sound = pygame.mixer.Sound("Sounds/sprung.wav")
victory_sound = pygame.mixer.Sound("Sounds/robosieg.wav")
lost_sound = pygame.mixer.Sound("Sounds/robotod.wav")
vitory = pygame.image.load("Grafics/Sieg.png")
lost = pygame.image.load("Grafics/verloren.png")


class player:
    def __init__(self,x,y,speed,width,height,jumpvar,direction,right_step,left_step):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.jumpvar = jumpvar
        self.direction = direction
        self.right_step = right_step
        self.left_step = left_step
        self.jump = False
        self.last = [1,0]
        self.ok = True
    def run(self,list):
        if list[0]:
            self.x += self.speed
            self.direction = [0,1,0,0]
            self.right_step += 1
        if list[1]:
            self.x -= self.speed
            self.direction = [1,0,0,0]
            self.left_step += 1
    def reset_steps(self):
        self.left_step = 0
        self.right_step = 0
    def stand(self):
        self.direction = [0,0,1,0]
        self.reset_steps()
    def jump_set(self):
        if self.jumpvar == -16:
            self.jump = True
            self.jumpvar = 15
            pygame.mixer.Sound.play(jump_sound)
    def jumping(self):
        if self.jump:
            self.direction = [0,0,0,1]
            if self.jumpvar >= -15:
                n = 1
                if self.jumpvar < 0:
                    n = -1
                self.y -= (self.jumpvar ** 2) * 0.17 * n
                self.jumpvar -= 1
            else:
                self.jump = False
    def player_draw(self):
        if self.right_step == 63:
            self.right_step = 0
        if self.left_step == 63:
            self.left_step = 0
        if self.direction[0]:
            screen.blit(walk_left[self.left_step // 8], (self.x, self.y))
            self.last = [1,0]
        if self.direction[1]:
            screen.blit(walk_right[self.right_step // 8], (self.x, self.y))
            self.last = [0,1]
        if self.direction[2]:
            if self.last[0]:
                screen.blit(attack_left, (self.x, self.y))
            else:
                screen.blit(attack_right, (self.x, self.y))
        if self.direction[3]:
            screen.blit(jump, (self.x, self.y))

class bullet:
    def __init__(self, player_x, player_y, bullet_direction, radius, color, speed):
        self.x = player_x
        self.y = player_y
        if bullet_direction[0]:
            self.x += 5
            self.speed = -1 * speed
        if bullet_direction[1]:
            self.x += 92
            self.speed = speed
        self.y += 84
        self.radius = radius
        self.color = color
    def moving(self):
        self.x += self.speed
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

class zombie:
    def __init__(self,x,y,speed,width,height,direction,xMin,xMax):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.direction = direction
        self.right_step = 0
        self.left_step = 0
        self.xMin = xMin
        self.xMax = xMax
        self.lifes = 6
        self.left_list = pygame.image.load("Grafics/l1.png"), pygame.image.load("Grafics/l2.png"), pygame.image.load("Grafics/l3.png"), pygame.image.load("Grafics/l4.png"), pygame.image.load("Grafics/l5.png"), pygame.image.load("Grafics/l6.png"), pygame.image.load("Grafics/l7.png"), pygame.image.load("Grafics/l8.png")
        self.right_list = pygame.image.load("Grafics/r1.png"), pygame.image.load("Grafics/r2.png"), pygame.image.load("Grafics/r3.png"), pygame.image.load("Grafics/r4.png"), pygame.image.load("Grafics/r5.png"), pygame.image.load("Grafics/r6.png"), pygame.image.load("Grafics/r7.png"), pygame.image.load("Grafics/r8.png")
        self.full = pygame.image.load("Grafics/voll.png")
        self.half = pygame.image.load("Grafics/halb.png")
        self.empty = pygame.image.load("Grafics/leer.png")

    def hearts(self):
        if self.lifes >= 2:
            screen.blit(self.full, (507, 15))
        if self.lifes >= 4:
            screen.blit(self.full, (569, 15))
        if self.lifes == 6:
            screen.blit(self.full, (631, 15))

        if self.lifes == 1:
            screen.blit(self.half, (507, 15))
        elif self.lifes == 3:
            screen.blit(self.half, (569, 15))
        elif self.lifes == 5:
            screen.blit(self.half, (631, 15))

        if self.lifes <= 0:
            screen.blit(self.empty, (507, 15))
        if self.lifes <= 2:
            screen.blit(self.empty, (569, 15))
        if self.lifes <= 4:
            screen.blit(self.empty, (631, 15))

    def zombie_draw(self):
        if self.right_step == 63:
            self.right_step = 0
        if self.left_step == 63:
            self.left_step = 0

        if self.direction[0]:
            screen.blit(self.left_list[self.left_step // 8], (self.x, self.y))
        if self.direction[1]:
            screen.blit(self.right_list[self.right_step // 8], (self.x, self.y))

    def running(self):
        self.x += self.speed
        if self.speed > 0:
            self.direction = [0,1]
            self.right_step += 1
        if self.speed < 0:
            self.direction = [1,0]
            self.left_step += 1

    def change(self):
        if self.x > self.xMax:
            self.speed *= -1
        elif self.x < self.xMin:
            self.speed *= -1
        self.running()

def draw():
    screen.blit(wallpaper, (0, 0))
    for b in bullets:
        b.draw()
    player_one.player_draw()
    zombie_one.zombie_draw()
    zombie_one.hearts()
    if winning:
        screen.blit(vitory, (0,0))
    elif losing:
        screen.blit(lost, (0,0))
    pygame.display.update()

def bullet_handle():
    global bullets
    for b in bullets:
        if b.x >= 0 and b.x <= 1920:
            b.moving()
        else:
            bullets.remove(b)

def collision():
    global bullets, losing, winning, go
    zombie_rect = pygame.Rect(zombie_one.x + 18, zombie_one.y + 24, zombie_one.width - 36, zombie_one.height - 24)
    playerRect =  pygame.Rect(player_one.x + 18, player_one.y + 36, player_one.width - 36, player_one.height - 36)
    for b in bullets:
        bullet_rect = pygame.Rect(b.x - b.radius, b.y - b.radius, b.radius*2, b.radius*2)
        if zombie_rect.colliderect((bullet_rect)):
            bullets.remove(b)
            zombie_one.lifes -= 1
            if zombie_one.lifes <= 0 and not losing:
                winning = True
                pygame.mixer.Sound.play(victory_sound)
                go = False

    if zombie_rect.colliderect(playerRect):
        losing = True
        winning = False
        pygame.mixer.Sound.play(lost_sound)
        go = False

leftWall = pygame.draw.rect(screen, (0,0,0), (0, 0, 2, 1080,), 0)
rightWall = pygame.draw.rect(screen, (0,0,0), (1919, 0, 2, 1080,), 0)
player_one = player(300, 810, 4, 96, 128, -16, [0,0,1,0],0,0)
zombie_one = zombie(1200, 810, 5 ,96, 128, [0,0], 40, 1850)
losing = False
winning = False
bullets = []
go = True

while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    playerRect = pygame.Rect(player_one.x,player_one.y,96,128)
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a] and not playerRect.colliderect(leftWall):
        player_one.run([0,1])
    elif pressed[pygame.K_d] and not playerRect.colliderect(rightWall):
        player_one.run([1,0])
    else:
        player_one.stand()

    if pressed[pygame.K_w]:
        player_one.jump_set()
    player_one.jumping()

    if pressed[pygame.K_SPACE]:
        if len(bullets) <= 0 and player_one.ok:
            bullets.append(bullet(round(player_one.x), (player_one.y), player_one.last, 8, (0,0,0), 7))
        player_one.ok = False

    if not pressed[pygame.K_SPACE]:
        player_one.ok = True

    bullet_handle()
    zombie_one.change()
    collision()
    draw()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    draw()