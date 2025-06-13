import pygame
import pymunk
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Kolory
BACKGROUND = (30, 30, 30)
PLAYER = (255, 255, 255)
ENEMY = (255, 0, 0)
MAP = (15, 15, 15)

# Ustawienia fizyki
space = pymunk.Space()
space.gravity = (0, 0)

# Gracz
player_width = 50
player_height = 50
player_speed = 200000

# Przeciwnik
default_enemy_width = 50
default_enemy_height = 50
default_enemy_speed = 100000

class Enemy:
    def __init__(self, screen_width, space, enemy_width=50, enemy_height=50, enemy_speed=100000):
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.enemy_speed = enemy_speed

        # setting random position
        x_pos = random.randint(0, screen_width - enemy_width)
        y_pos = -enemy_height
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (enemy_width, enemy_height)))
        self.body.position = (x_pos, y_pos)
        self.shape = pymunk.Poly.create_box(self.body, (enemy_width, enemy_height))
        self.shape.density = 0.1
        self.shape.friction = 5
        space.add(self.body, self.shape)

enemies: list[Enemy] = []

# Funkcja tworząca obiekt gracza
def create_player(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (player_width, player_height)))  # Ciało
    body.position = (x, y)
    shape = pymunk.Poly.create_box(body, (player_width, player_height))  # Kształt
    shape.density = 0.1
    shape.friction = 3
    space.add(body, shape)
    return body

player_body = create_player(screen_width // 2, screen_height - player_height - 10)


# Ustawienia zegara
clock = pygame.time.Clock()
score = 0


# Funkcja do sprawdzania kolizji
def check_collision():
    if(player_body.position.y > screen_height - player_height + 5): 
        return True # to oznacza, że gracz został dotknięty przeciwnikiem ale kolizja się nie zarejestrowała
    for i in range(len(enemies)-1, -1, -1):
        if player_body.position.get_distance(enemies[i].body.position) < (player_width / 2 + enemies[i].enemy_width / 2):
            return True
        if(enemies[i].body.position.y > screen_height - enemies[i].enemy_height):
            global score 
            score += 1
            space.remove(enemies[i].body, enemies[i].shape)
            enemies.pop(i)
    return False


# Funkcja do rysowania obiektów
def draw_objects():
    # player
    pygame.draw.rect(screen, PLAYER, (player_body.position.x - player_width / 2,
                                     player_body.position.y - player_height / 2,
                                     player_width, player_height))

    # enemies
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY, (enemy.body.position.x - enemy.enemy_width / 2,
                                       enemy.body.position.y - enemy.enemy_height / 2,
                                       enemy.enemy_width, enemy.enemy_height))
        
    # map
    pygame.draw.rect(screen, MAP, (0,
                                    screen_height-35,
                                    screen_width, 35))
    mapbody_left = pymunk.Body(0, 0, pymunk.Body.STATIC)
    mapbody_left.position = (-5, screen_height/2)
    space.add(mapbody_left, pymunk.Poly.create_box(mapbody_left, (10, screen_height)))
    mapbody_right = pymunk.Body(0, 0, pymunk.Body.STATIC)
    mapbody_right.position = (screen_width+5, screen_height/2)
    space.add(mapbody_right, pymunk.Poly.create_box(mapbody_right, (10, screen_height)))


# Główna pętla gry
running = True
while running:
    screen.fill(BACKGROUND)

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruch gracza za pomocą strzałek
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_body.apply_force_at_local_point((-player_speed, 0))  # lewo
    if keys[pygame.K_RIGHT]:
        player_body.apply_force_at_local_point((player_speed, 0))   # prawo

    # Generowanie nowych przeciwników i nadawanie im prędkości
    if random.randint(1, 100) <= 4:
        enemies.append(Enemy(screen_width, space, default_enemy_width, default_enemy_height, default_enemy_speed))
    for i in range(len(enemies)):
        enemies[i].body.apply_force_at_local_point((0, enemies[i].enemy_speed))

    

    # Sprawdzanie kolizji
    if check_collision():
        running = False  # Zatrzymanie gry w przypadku kolizji

    # Rysowanie obiektów na ekranie
    draw_objects()

    # Wyświetlanie wyniku
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Wynik: {score}", True, PLAYER)
    screen.blit(score_text, (10, 10))

    # Odświeżenie ekranu
    pygame.display.update()

    # Ustawienie liczby klatek na sekundę
    clock.tick(60)

    # Aktualizacja fizyki
    space.step(1 / 60.0)

# Zakończenie gry
pygame.quit()