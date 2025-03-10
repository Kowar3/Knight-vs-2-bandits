import random
import pygame
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

sirina_ekrana = 800
visina_ekrana = 550

screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
pygame.display.set_caption("Battle")

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90

attack = False
potion = False
target = None
clicked = False
potion_effect = 15
game_over = 0  

font = pygame.font.Font("freesansbold.ttf", 26)

red = (255, 0, 0)
green = (0, 255, 0)

pozadina_ekrana = pygame.image.load("img/Background/background.png").convert_alpha()

pozadina_panela = pygame.image.load("img/Icons/panel.png").convert_alpha()
mac_slika = pygame.image.load("img/Icons/sword.png").convert_alpha()

slika_potiona = pygame.image.load("img/Icons/potion.png")

pobeda_img = pygame.image.load("img/Icons/victory.png")
poraz_img = pygame.image.load("img/Icons/defeat.png")

restart_slika = pygame.image.load("img/Icons/restart.png")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(pozadina_ekrana, (0, 0))

def draw_panel():
    screen.blit(pozadina_panela, (0, visina_ekrana - 150))

    draw_text(f"{knight.name} HP: {knight.hp}", font, red, 100, visina_ekrana - 150 + 20)
    for count, i in enumerate(bandit_list):
        draw_text(f"{i.name} HP: {i.hp}", font, red, 550, visina_ekrana - 150 + 20 + count * 60)

class Fighter():

    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        # 0:Idle, 1:Attack, 2:Hurt, 3:Dead
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f"img/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f"img/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        animation_cooldown = 100

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            if self.frame_index == len(self.animation_list[self.action]) - 1:
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()
            else:
                self.frame_index += 1

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        damage = self.strength + random.randint(-5, 5)
        target.hp -= damage
        target.hurt()
        if target.hp < 1:
            target.death()
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):

    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

knight = Fighter(200, 260, "Knight", 40, 10, 3)

bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_healt_bar = HealthBar(100, visina_ekrana - 150 + 50, knight.hp, knight.max_hp)
bandit1_healt_bar = HealthBar(550, visina_ekrana - 150 + 50, bandit1.hp, bandit1.max_hp)
bandit2_healt_bar = HealthBar(550, visina_ekrana - 150 + 110, bandit2.hp, bandit2.max_hp)

potion_button = button.Button(screen, 100, visina_ekrana - 150 + 70, slika_potiona, 64, 64)

restart_button = button.Button(screen, 330, 120, restart_slika, 120, 30)

running = True

while running:

    clock.tick(fps)

    draw_bg()
    draw_panel()

    knight.update()
    knight.draw()

    knight_healt_bar.draw(knight.hp)
    bandit1_healt_bar.draw(bandit1.hp)
    bandit2_healt_bar.draw(bandit2.hp)

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    damage_text_group.update()
    damage_text_group.draw(screen)

    attack = False
    potion = False
    target = None
    pygame.mouse.set_visible(True)

    pos = pygame.mouse.get_pos()

    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(mac_slika, pos)
            if clicked and bandit.alive:
                attack = True
                target = bandit_list[count]

    if potion_button.draw():
        potion = True
    draw_text(str(knight.potions), font, red, 147, visina_ekrana - 150 + 73)

    if game_over == 0:
        if knight.alive:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    if attack and target is not None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    if potion:
                        if knight.potions > 0:
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            heal_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(heal_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        for count, bandit in enumerate(bandit_list):
            if current_fighter == count + 2:
                if bandit.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        if (bandit.hp / bandit.max_hp) < 0.5:
                            if bandit.potions > 0:
                                if bandit.max_hp - bandit.hp < potion_effect:
                                    heal_amount = bandit.max_hp - bandit.hp
                                else:
                                    heal_amount = potion_effect
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                heal_text = DamageText(bandit.rect.centerx, bandit.rect.centery, str(heal_amount),
                                                       green)
                                damage_text_group.add(heal_text)
                                current_fighter += 1
                                action_cooldown = 0
                                continue
                        bandit.attack(knight)
                        current_fighter += 1
                        action_cooldown = 0
                else:
                    current_fighter += 1

        if current_fighter > total_fighters:
            current_fighter = 1

    alive_bandits = 0

    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1

    if alive_bandits == 0:
        game_over = 1

    if game_over != 0:
        if game_over == 1:
            screen.blit(pobeda_img, (250, 50))
        else:
            screen.blit(poraz_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()