import tkinter as tk
import random

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo de Plataforma Estilo Super Mario")
        self.canvas = tk.Canvas(master, width=800, height=400, bg="skyblue")
        self.canvas.pack()

        self.character = self.canvas.create_rectangle(50, 300, 100, 350, fill="red")
        self.platforms = []
        self.coins = []
        self.enemies = []

        self.gravity = 1
        self.is_jumping = False
        self.jump_speed = 15
        self.character_speed = 5
        self.character_y_velocity = 0
        self.score = 0

        self.create_platforms()
        self.create_coins()
        self.create_enemies()

        self.master.bind("<KeyPress>", self.on_key_press)

        self.update_game()

    def create_platforms(self):
        for i in range(5):
            x = random.randint(100, 700)
            y = random.randint(100, 350)
            platform = self.canvas.create_rectangle(x, y, x + 100, y + 10, fill="green")
            self.platforms.append(platform)

    def create_coins(self):
        for _ in range(10):
            x = random.randint(50, 750)
            y = random.randint(50, 350)
            coin = self.canvas.create_oval(x, y, x + 20, y + 20, fill="yellow")
            self.coins.append(coin)

    def create_enemies(self):
        for _ in range(3):
            x = random.randint(200, 600)
            y = random.randint(200, 350)
            enemy = self.canvas.create_rectangle(x, y, x + 30, y + 30, fill="black")
            self.enemies.append(enemy)

    def on_key_press(self, event):
        if event.keysym == "Left":
            self.move_character(-self.character_speed)
        elif event.keysym == "Right":
            self.move_character(self.character_speed)
        elif event.keysym == "space":
            if not self.is_jumping:
                self.is_jumping = True
                self.character_y_velocity = self.jump_speed

    def move_character(self, dx):
        self.canvas.move(self.character, dx, 0)
        self.check_platform_collision()

    def update_game(self):
        if self.is_jumping:
            self.character_y_velocity -= self.gravity
            self.canvas.move(self.character, 0, -self.character_y_velocity)
            if self.character_y_velocity <= 0:
                self.is_jumping = False
                self.character_y_velocity = 0

        self.check_platform_collision()
        self.check_collision_with_coins()
        self.check_collision_with_enemies()

        self.master.after(20, self.update_game)

    def check_platform_collision(self):
        character_coords = self.canvas.coords(self.character)
        character_bottom = character_coords[3]

        for platform in self.platforms:
            platform_coords = self.canvas.coords(platform)
            platform_top = platform_coords[1]
            if character_bottom >= platform_top and character_coords[0] >= platform_coords[0] and character_coords[2] <= platform_coords[2]:
                self.is_jumping = False
                self.character_y_velocity = 0
                self.canvas.move(self.character, 0, platform_top - character_bottom)

    def check_collision_with_coins(self):
        character_coords = self.canvas.coords(self.character)
        for coin in self.coins:
            coin_coords = self.canvas.coords(coin)
            if character_coords[0] < coin_coords[2] and character_coords[2] > coin_coords[0] and character_coords[1] < coin_coords[3] and character_coords[3] > coin_coords[1]:
                self.canvas.delete(coin)
                self.coins.remove(coin)
                self.score += 1
                print(f"Score: {self.score}")

    def check_collision_with_enemies(self):
        character_coords = self.canvas.coords(self.character)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy)
            if character_coords[0] < enemy_coords[2] and character_coords[2] > enemy_coords[0] and character_coords[1] < enemy_coords[3] and character_coords[3] > enemy_coords[1]:
                print("Game Over!")
                self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
