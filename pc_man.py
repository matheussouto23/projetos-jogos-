import pygame
import random

# Configurações iniciais
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)  # Cor para as frutas

# Classes
class PacMan:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.size = 20
        self.lives = 3
        self.powered_up = False
        self.score = 0
        self.power_up_time = 0  # Tempo para o poder

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def activate_power_up(self):
        self.powered_up = True
        self.power_up_time = pygame.time.get_ticks()  # Marca o tempo atual

    def update(self):
        # Verifica se o tempo de poder expirou
        if self.powered_up and pygame.time.get_ticks() - self.power_up_time > 6000:  # 6 segundos
            self.powered_up = False

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 20
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  # Direção inicial
        self.speed = 2  # Velocidade base
        self.color = color

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        # Lógica para mudar a direção ao atingir as bordas da tela
        if self.x <= 0 or self.x >= WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.y <= 0 or self.y >= HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Pellet:
    def __init__(self, x, y, power=False):
        self.x = x
        self.y = y
        self.size = 5
        self.power = power  # Indica se é uma super pastilha

    def draw(self):
        color = WHITE if not self.power else (255, 165, 0)  # Laranja para super pastilha
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10

    def draw(self):
        pygame.draw.circle(screen, PURPLE, (self.x, self.y), self.size)

# Inicialização
pacman = PacMan()
ghosts = [Ghost(100, 100, RED)]  # Inicia com um fantasma
pellets = [Pellet(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(20)]  # Pastilhas normais
super_pellets = [Pellet(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), power=True) for _ in range(3)]  # Super pastilhas
fruits = []  # Lista de frutas

# Variáveis de controle de fase
pellet_threshold = 20  # Número de pastilhas para aumentar a dificuldade
current_level = 1  # Nível atual
ghosts_speed_increment = 1  # Incremento na velocidade dos fantasmas

# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do Pac-Man
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        pacman.move(5, 0)
    if keys[pygame.K_UP]:
        pacman.move(0, -5)
    if keys[pygame.K_DOWN]:
        pacman.move(0, 5)

    # Atualização e desenho dos pellets
    for pellet in pellets[:]:
        if (pacman.x - pellet.x)**2 + (pacman.y - pellet.y)**2 < (pacman.size + pellet.size)**2:
            pacman.score += 10  # Pontuação por pastilhas normais
            pellets.remove(pellet)

    for sp in super_pellets[:]:
        if (pacman.x - sp.x)**2 + (pacman.y - sp.y)**2 < (pacman.size + sp.size)**2:
            pacman.powered_up = True  # Ativa o efeito da super pastilha
            pacman.score += 50  # Pontuação por super pastilha
            super_pellets.remove(sp)

    # Adicionar frutas aleatórias
    if random.randint(1, 50) == 1:  # Chance de spawn de frutas
        fruits.append(Fruit(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)))

    for fruit in fruits[:]:
        if (pacman.x - fruit.x)**2 + (pacman.y - fruit.y)**2 < (pacman.size + fruit.size)**2:
            pacman.activate_power_up()  # Ativa a habilidade de vencer fantasmas
            pacman.score += 30  # Pontuação por fruta
            fruits.remove(fruit)

    # Atualização e desenho dos fantasmas
    for ghost in ghosts:
        ghost.move()
        ghost.draw()
        
        # Verificação de colisão com o Pac-Man
        if (pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2 < (pacman.size + ghost.size)**2:
            if pacman.powered_up:
                # Pac-Man come o fantasma
                ghosts.remove(ghost)  # Remove o fantasma
            else:
                # Pac-Man perde uma vida
                pacman.lives -= 1
                if pacman.lives <= 0:
                    print("Game Over!")
                    running = False
                else:
                    # Reposicionar Pac-Man após a morte
                    pacman.x, pacman.y = 50, 50  # Reseta a posição do Pac-Man

    # Atualiza o estado do Pac-Man (para ver se o poder expirou)
    pacman.update()

    # Desenhar pacman, pellets e frutas
    pacman.draw()
    for pellet in pellets:
        pellet.draw()
    for sp in super_pellets:
        sp.draw()
    for fruit in fruits:
        fruit.draw()

    # Exibir informações do jogo
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f'Lives: {pacman.lives}', True, (255, 255, 255))
    score_text = font.render(f'Score: {pacman.score}', True, (255, 255, 255))
    level_text = font.render(f'Level: {current_level}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))

    # Verificação para aumentar a dificuldade
    if pacman.score >= pellet_threshold * current_level:
        # Aumentar a dificuldade: adicionar um novo fantasma e aumentar a velocidade dos fantasmas
        ghosts.append(Ghost(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), RED))
        for ghost in ghosts:
            ghost.speed += ghosts_speed_increment  # Aumenta a velocidade dos fantasmas
        current_level += 1  # Avança para o próximo nível
        pellet_threshold += 20  # Aumenta o limite de pastilhas para o próximo nível

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
import pygame
import random

# Configurações iniciais
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Classes
class PacMan:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.size = 20
        self.lives = 3
        self.powered_up = False
        self.score = 0

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 20
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  # Direção inicial
        self.color = color
        self.speed = 2  # Velocidade base

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        # Lógica para mudar a direção ao atingir as bordas da tela
        if self.x <= 0 or self.x >= WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.y <= 0 or self.y >= HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Pellet:
    def __init__(self, x, y, power=False):
        self.x = x
        self.y = y
        self.size = 5
        self.power = power  # Indica se é uma super pastilha

    def draw(self):
        color = WHITE if not self.power else (255, 165, 0)  # Laranja para super pastilha
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

# Inicialização
pacman = PacMan()
ghosts = [Ghost(100, 100, RED), Ghost(300, 100, (0, 0, 255)), Ghost(200, 200, (255, 192, 203))]  # Fantasmas coloridos
pellets = [Pellet(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(20)]  # Pastilhas normais
super_pellets = [Pellet(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), power=True) for _ in range(3)]  # Super pastilhas

# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do Pac-Man (simples)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        pacman.move(5, 0)
    if keys[pygame.K_UP]:
        pacman.move(0, -5)
    if keys[pygame.K_DOWN]:
        pacman.move(0, 5)

    # Atualização e desenho dos pellets
    for pellet in pellets[:]:  # Copiar a lista para evitar problemas ao remover
        if (pacman.x - pellet.x)**2 + (pacman.y - pellet.y)**2 < (pacman.size + pellet.size)**2:
            pacman.score += 10  # Pontuação por pastilhas normais
            pellets.remove(pellet)

    for sp in super_pellets[:]:
        if (pacman.x - sp.x)**2 + (pacman.y - sp.y)**2 < (pacman.size + sp.size)**2:
            pacman.powered_up = True  # Ativa o efeito da super pastilha
            pacman.score += 50  # Pontuação por super pastilha
            super_pellets.remove(sp)

    # Atualização e desenho dos fantasmas
    for ghost in ghosts:
        ghost.move()
        ghost.draw()
        
        # Verificação de colisão com o Pac-Man
        if (pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2 < (pacman.size + ghost.size)**2:
            if pacman.powered_up:
                # Pac-Man come o fantasma
                ghosts.remove(ghost)  # Remove o fantasma
            else:
                # Pac-Man perde uma vida
                pacman.lives -= 1
                if pacman.lives <= 0:
                    print("Game Over!")
                    running = False

    # Desenhar pacman e pellets
    pacman.draw()
    for pellet in pellets:
        pellet.draw()
    for sp in super_pellets:
        sp.draw()

    # Exibir informações do jogo
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f'Lives: {pacman.lives}', True, (255, 255, 255))
    score_text = font.render(f'Score: {pacman.score}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 40))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
