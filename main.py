import pygame
import os
import random
import time


# Init and create window
pygame.init()
win_height = 400
win_width = 800
win = pygame.display.set_mode((win_width, win_height))

# Load and Size Images
idle = []
for frame in range(0, 8):
    idle.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Idle_"+str(frame)+".png")))

idle_left = []
for frame in range(0, 8):
    idle_left.append(pygame.transform.flip(idle[frame], True, False))
right = []
for frame in range(0, 10):
    right.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Run_"+str(frame)+".png")))

left = []
for frame in range(0, 10):
    left.append(pygame.transform.flip(right[frame], True, False))

jump_right = []
for frame in range(0, 3):
    jump_right.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Jump_"+str(frame)+".png")))

jump_left = []
for frame in range(0, 3):
    jump_left.append(pygame.transform.flip(jump_right[frame], True, False))

attack_right = []
for frame in range(0,6):
    attack_right.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Attack1_" + str(frame) + ".png")))

attack_left = []
for frame in range(0,6):
    attack_left.append(pygame.transform.flip(attack_right[frame], True, False))

hurt_right = []
for frame in range(0, 3):
    hurt_right.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Hurt_" + str(frame) + ".png")))

hurt_left = []
for frame in range(0, 3):
    hurt_left.append(pygame.transform.flip(hurt_right[frame], True, False))

death_right = []
for frame in range(0, 10):
    death_right.append(pygame.image.load(os.path.join("Hero_Sprites", "HeroKnight_Death_" + str(frame) + ".png")))

death_left = []
for frame in range(0, 10):
    death_left.append(pygame.transform.flip(death_right[frame], True, False))

# background
bg = pygame.transform.scale(pygame.image.load('Background_Images/Background.png'), (win_width, win_height))

# enemy animations
left_enemy = []
for frame in range(1, 9):
    left_enemy.append(pygame.image.load(os.path.join("Enemy_Sprites/Bringer-of-Death_Walk_" + str(frame) + ".png")))

right_enemy = []
for frame in range(0, 8):
    right_enemy.append(pygame.transform.flip(left_enemy[frame], True, False))

left_enemy_hurt = []
for frame in range(1, 4):
    left_enemy_hurt.append(pygame.image.load(os.path.join("Enemy_Sprites/Bringer-of-Death_Hurt_" + str(frame) + ".png")))

left_enemy_death = []
for frame in range(1, 11):
    left_enemy_death.append(pygame.image.load(os.path.join("Enemy_Sprites/Bringer-of-Death_Death_" + str(frame) + ".png")))

left_enemy_attack = []
for frame in range(1, 11):
    left_enemy_attack.append(pygame.image.load(os.path.join("Enemy_Sprites/Bringer-of-Death_Attack_" + str(frame) + ".png")))

# Hero Class
class Hero:
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = True
        self.face = True # true = right and false = left
        self.jump = False
        self.jump_count = True
        self.attack = False
        self.attack_count = True
        self.alive = True
        self.health = 5
        self.death_count = False
        self.hit = False
        self.hit_count = False
        self.stepIndex = 0
    def hero_sound(self):
        attack_sound = pygame.mixer.Sound('Sounds/Super-Short-Transition-Whoosh-A-www.fesliyanstudios.com.mp3')
        jump_sound = pygame.mixer.Sound('Sounds/mixkit-player-jumping-in-a-video-game-2043.wav')
        hero_death_sound = pygame.mixer.Sound('Sounds/female-sad-tragic-ambience-74919.mp3')
        if self.health <= 0:
            hero_death_sound.play()
        if self.attack:
            attack_sound.play()
        if self.jump:
            jump_sound.play()
    def move_hero(self, userinput):
        if self.hit is True:
            pass
        else:
            if userinput[pygame.K_RIGHT]:
                self.x += self.velx
                self.face_right = True
                self.face_left = False
                self.face = True
            elif userinput[pygame.K_LEFT]:
                self.x -= self.velx
                self.face_right = False
                self.face_left = True
                self.face = False
            else:
                self.face_right = False
                self.face_left = False
            if self.jump is False and userinput[pygame.K_UP]:
                self.jump = True
                self.hero_sound()
            if self.jump is True:
                self.y -= self.vely*1.5
                self.vely -= 1
                if self.vely < -10:
                    self.jump = False
                    self.jump_count = True
                    self.vely = 10
            if userinput[pygame.K_SPACE] and self.attack is False:
                self.attack = True
                self.hero_sound()
                for enemy in enemies:
                    if (self.x < (enemy.x + 110)) and (self.x >= enemy.x-10):
                        enemy.health -= 1
                        enemy.hit = True
                        enemy.enemy_sound()

    def draw(self, win):
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.hit is True:
            if self.health <= 0:
                self.hero_sound()
                if self.death_count is False:
                    self.stepIndex = 0
                    self.death_count = True
                if self.face is True:
                    win.blit(death_right[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    time.sleep(.25)
                    if self.stepIndex >= 9:
                        self.alive = False
                        self.death_count = False
                else:
                    win.blit(death_left[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    time.sleep(.25)
                    if self.stepIndex >= 9:
                        self.alive = False
                        self.death_count = False
            else:
                if self.hit_count is False:
                    self.stepIndex = 0
                    self.hit_count = True
                if self.face is True and self.hit_count is True:
                    if self.stepIndex >= 3:
                        self.stepIndex = 0
                        self.hit_count = False
                        self.hit = False
                    win.blit(hurt_right[self.stepIndex], (self.x, self.y))
                    pygame.time.delay(10)
                    self.stepIndex += 1
                elif self.face is False and self.hit_count is True:
                    if self.stepIndex >= 3:
                        self.stepIndex = 0
                        self.hit_count = False
                        self.hit = False
                    win.blit(hurt_left[self.stepIndex], (self.x, self.y))
                    pygame.time.delay(10)
                    self.stepIndex += 1
        elif self.face_right and self.jump is False and self.hit is False:
            win.blit(right[self.stepIndex], (self.x, self.y))
            pygame.time.delay(10)
            self.stepIndex += 1
        elif self.face_left and self.jump is False and self.hit is False:
            win.blit(left[self.stepIndex], (self.x, self.y))
            pygame.time.delay(10)
            self.stepIndex += 1
        elif self.attack is False and self.jump is False and self.hit is False:
            if self.face is True:
                if self.stepIndex >= 8:
                    self.stepIndex = 0
                win.blit(idle[self.stepIndex], (self.x, self.y))
                pygame.time.delay(15)
                self.stepIndex += 1
            elif self.face is False:
                if self.stepIndex >= 8:
                    self.stepIndex = 0
                win.blit(idle_left[self.stepIndex], (self.x, self.y))
                pygame.time.delay(15)
                self.stepIndex += 1
        if self.jump and self.attack is False and self.hit is False:
            if self.face is True:
                if self.jump_count is True:
                    if self.stepIndex >= 3:
                        self.stepIndex = 0
                        self.jump_count = False
                    win.blit(jump_right[self.stepIndex], (self.x, self.y))
                    pygame.time.delay(15)
                    self.stepIndex += 1
                else:
                    win.blit(jump_right[2], (self.x, self.y))
            elif self.face is False:
                if self.jump_count is True:
                    if self.stepIndex >= 3:
                        self.stepIndex = 0
                        self.jump_count = False
                    win.blit(jump_left[self.stepIndex], (self.x, self.y))
                    pygame.time.delay(15)
                    self.stepIndex += 1
                else:
                    win.blit(jump_left[2], (self.x, self.y))
        if self.attack:
            if self.attack_count:
                self.stepIndex = 0
                self.attack_count = False
            if self.face is True and self.stepIndex <= 5:
                win.blit(attack_right[self.stepIndex], (self.x, self.y))
                pygame.time.delay(25)
                self.stepIndex += 1
            elif self.face is False and self.stepIndex <= 5:
                win.blit(attack_left[self.stepIndex], (self.x, self.y))
                pygame.time.delay(25)
                self.stepIndex += 1
            if self.stepIndex >= 6:
                self.attack = False
                self.attack_count = True

# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = 2
        self.vely = 10
        self.health = 3
        self.hit = False
        self.hit_count = False
        self.alive = True
        self.face_right = True
        self.face_left = True
        self.face = True  # true = right and false = left
        self.attack = False
        self.attack_count = True
        self.gameover_var = False
        self.stepIndex = 0
    def enemy_sound(self):
        enemy_hurt_sound = pygame.mixer.Sound('Sounds/mixkit-monster-hiss-1964.wav')
        enemy_death_sound = pygame.mixer.Sound('Sounds/mixkit-monster-wraith-passing-by-1979.wav')
        enemy_attack_sound = pygame.mixer.Sound('Sounds/mixkit-short-fire-whoosh-1345.wav')
        if self.health <= 0:
            enemy_death_sound.play()
        elif self.attack is True:
            enemy_attack_sound.play()
        else:
            enemy_hurt_sound.play()
    def gameover(self):
        for enemy in enemies:
            enemy.gameover_var = True
    def move_Enemy(self):
        if (player.x < (self.x + 110)) and (player.x >= self.x-10):
            self.attack = True
            self.enemy_sound()
        if self.x > -150:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
            self.face = False
    def draw(self, win):
        if self.gameover_var is False:
            if self.stepIndex >= 8 and self.hit is False and self.attack is False:
                self.stepIndex = 0
            if self.hit is False:
                if self.attack is True:
                    if self.attack_count is True:
                        self.stepIndex = 0
                        self.attack_count = False
                    if self.stepIndex >= len(left_enemy_attack):
                        self.stepIndex = 0
                    win.blit(left_enemy_attack[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    if self.stepIndex >= 10:
                        if (player.x < (self.x + 110)) and (player.x >= self.x - 10):
                            player.health -= 1
                            player.hit = True
                            if player.health <= 0:
                                self.gameover()
                        self.attack_count = True
                        self.attack = False
                else:
                    win.blit(left_enemy[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    self.move_Enemy()
            else:
                if self.hit_count is False:
                    self.stepIndex = 0
                    self.hit_count = True
                elif self.health <= 0:
                    win.blit(left_enemy_death[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    if self.stepIndex >= 10:
                        self.hit_count = False
                        self.hit = False
                        self.alive = False
                else:
                    win.blit(left_enemy_hurt[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                    if self.stepIndex >= 3:
                        self.hit_count = False
                        self.hit = False

# Draw Game
def draw_game():
    win.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    if player.alive is True:
        player.draw(win)
        for enemy in enemies:
            if enemy.alive is False:
                enemies.remove(enemy)
            enemy.draw(win)
    else:
        win.blit(game_over, (150, -50))
        if player.face:
            win.blit(death_right[9],(player.x, player.y))
        else:
            win.blit(death_left[9], (player.x, player.y))
    pygame.time.delay(30)
    pygame.display.update()

# instansiate player
player = Hero(250,315)
enemies = []

# Main Loop
run = True
start_time = False
start_ticks = pygame.time.get_ticks()
timestamp = 0.0
spawn_timer = random.uniform(.5, 6)
pygame.mixer.init()
pygame.mixer.music.load("Sounds/15. Terra Feminarum OST - Kalevala.mp3")
game_over = pygame.image.load(os.path.join("Background_Images/gameover-removebg-preview.png"))
while run:
    seconds = (pygame.time.get_ticks()-start_ticks)/1000
    if start_time is False:
        pygame.mixer.music.play(-1, 0.0)
        timestamp = seconds
        start_time = True
    # Quit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.mixer.music.stop()
    # input
    userinput = pygame.key.get_pressed()

    # movement
    player.move_hero(userinput)
    # spawn enemies
    if len(enemies) <= 0:
        Enemy_spawn = Enemy(700, 280)
        enemies.append(Enemy_spawn)
    else:
        if player.health >= 1:
            if seconds >= float(timestamp + spawn_timer):
                timestamp = seconds
                Enemy_spawn = Enemy(700, 280)
                enemies.append(Enemy_spawn)
                spawn_timer = random.uniform(.5, 6)
        else:
            pygame.mixer.music.stop()
    # Draw Game in Window
    draw_game()
