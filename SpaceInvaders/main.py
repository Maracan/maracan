import random
import math
import pygame


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height

        # festlegen Größe des Spielfeldes. Achtung es muss ein Tupel übergeben werden.
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")  # Caption festlegen.
        self.clock = pygame.time.Clock()  # Framerate definieren
        self.running = True
        # Spaceship reinladen auf Startposition
        self.spaceship = Spaceship(self, 370, 515)

        self.score = 0

        # Liste mit Enemies on random positions
        self.enemies = []
        for i in range(12):
            self.enemies.append(
                Enemy(self, random.randint(0, 736), random.randint(30, 130)))

        # Background definieren
        self.background_img = pygame.image.load("./Spaceinvaders/res/star.png")

        while self.running:
            self.clock.tick(60)  # Framerate übergeben
            self.screen.blit(self.background_img, (0, 0))

            # Wenn das event pygame.QUIT ausgelöst wurde - break while Schleife.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Tastatursteuerung - Events keydown
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(-10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(10)
                    # Tastatursteuerung - Bullet feuern
                    if event.key == pygame.K_SPACE:
                        self.spaceship.fire_bullet()

                # Tastatursteuerung - Events Keyup
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(-10)

            # Update Spaceship und Background
            self.spaceship.update()

            # Liste durchgehen und jedes Objekt dessen Wert auf True gesetzt ist > updaten!
            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.is_fired is True:
                        bullet.update()
                    else:
                        # Patrone removen aus der Liste
                        self.spaceship.bullets.remove(bullet)

            # Enemies updaten
            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                # Check if enemy too close
                if enemy.y > 460:
                    for i in self.enemies:
                        i.y = 1000
                    self.print_game_over()
                    break
            self.print_score()
            pygame.display.update()

    def print_game_over(self):
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(go_text, (200, 250))

    def print_score(self):
        score_font = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render(
            "Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))


class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 0

        self.game = game
        self.spaceship_img = pygame.image.load(
            "./Spaceinvaders/res/spr_spaceship.png")
        self.bullets = []  # Liste im die Bullet Objekte zu speichern.

    def fire_bullet(self):
        self.bullets.append(Bullet(self.game, self.x, self.y))
        # Wir greifen damit auf das letzte Element der Liste zu und das ruft die fire() auf.
        self.bullets[len(self.bullets) - 1].fire()

    def move(self, speed):
        # Jedes mal wenn diese Methode aufgerufen wird, wird der Wert change_x um den Wert speed erhöht.
        self.change_x += speed

    # Spaceship malen
    def update(self):
        self.x += self.change_x
        # Spielfeld / Bewegung begrenzen. 800-64px (breite von Spaceship.) Dies hängt mit der blitt methode zusammen.
        if self.x < 0:
            self.x = 0
        elif self.x > 736:
            self.x = 736

        self.game.screen.blit(self.spaceship_img, (self.x, self.y))


class Bullet:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.is_fired = False
        self.bullet_speed = 10
        self.bullet_img = pygame.image.load(
            "./Spaceinvaders/res/spr_patrone.png")

    def fire(self):
        self.is_fired = True

        # Bulletsound
        pygame.mixer.music.load("./Spaceinvaders/res/blaster2.mp3")
        pygame.mixer.music.play()

    def update(self):
        self.y -= self.bullet_speed  # Bewegung Bullet
        if self.y <= 0:  # Bulletobjekt einschränken am oberen Rand
            self.is_fired = False
        self.game.screen.blit(self.bullet_img, (self.x, self.y))


class Enemy:

    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 60
        self.game = game
        self.enemy_img = pygame.image.load(
            "./Spaceinvaders/res/spr_space_enemy.png")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(
                math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))  # Distanzermittlungsformel Bullet / Enemy
            if distance < 35:
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)

    def update(self):
        # Richtungswechsel / Begrenzung an den Seiten / Vorwärtsgang xD
        self.x += self.change_x
        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -5
        elif self.x <= 0:
            self.y += self.change_y
            self.change_x = 5

        self.game.screen.blit(self.enemy_img, (self.x, self.y))


if __name__ == "__main__":
    game = Game(800, 600)
