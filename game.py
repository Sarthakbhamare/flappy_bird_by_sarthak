import pygame
import random
from head_controls import HeadController

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 512))
        self.clock = pygame.time.Clock()

        # Load and scale game assets
        self.bird = pygame.transform.scale(pygame.image.load('assets/images/bird_img.png').convert_alpha(), (40, 28))
        self.background = pygame.transform.scale(pygame.image.load('assets/images/bg_img.jpg').convert_alpha(), (800, 512))
        self.pipe_top = pygame.transform.scale(pygame.image.load('assets/images/pipe_img.png').convert_alpha(), (50, 300))
        self.pipe_bottom = pygame.transform.scale(pygame.image.load('assets/images/pipe2.img.png').convert_alpha(), (50, 300))

        # Initial bird position and gravity
        self.bird_x = 50
        self.bird_y = 250
        self.bird_movement = 0
        self.gravity = 0.15  # Slower fall

        # Pipe settings
        self.pipe_gap = 200  # Gap between pipes
        self.pipe_velocity = 2 # Pipe speed
        self.pipe_list = []
        self.pipe_timer = pygame.USEREVENT
        pygame.time.set_timer(self.pipe_timer, 1500)  # Pipes spawn every 1.4 seconds

        # Buttons
        self.restart_button = pygame.Rect(250, 350, 300, 50)
        self.quit_button = pygame.Rect(250, 420, 300, 50)
        self.pause_button = pygame.Rect(250, 420, 300, 50)

        # Game variables
        self.head_controller = HeadController()
        self.score = 0
        self.passed_pipe = False
        self.font = pygame.font.SysFont('Arial', 30)
        self.game_over = False
        self.paused = False

    def spawn_pipe(self):
        pipe_height = random.randint(180, 320)
        pipe_top_y = pipe_height - self.pipe_top.get_height()
        pipe_bottom_y = pipe_height + self.pipe_gap
        pipe_x = 800  # Pipes spawn off-screen

        self.pipe_list.append([pipe_x, pipe_top_y, pipe_bottom_y])

    def move_pipes(self):
        """Move pipes and remove off-screen ones."""
        for pipe in self.pipe_list:
            pipe[0] -= self.pipe_velocity

        if self.pipe_list and self.pipe_list[0][0] < -self.pipe_top.get_width():
            self.pipe_list.pop(0)

    def check_collision(self):
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, self.bird.get_width(), self.bird.get_height())

        for pipe in self.pipe_list:
            pipe_top_rect = pygame.Rect(pipe[0], pipe[1], self.pipe_top.get_width(), self.pipe_top.get_height())
            pipe_bottom_rect = pygame.Rect(pipe[0], pipe[2], self.pipe_bottom.get_width(), self.pipe_bottom.get_height())

            if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
                return True

        if self.bird_y <= 0 or self.bird_y >= 512 - self.bird.get_height():
            return True

        return False

    def update_score(self):
        for pipe in self.pipe_list:
            if pipe[0] + self.pipe_top.get_width() < self.bird_x and not self.passed_pipe:
                self.score += 1
                self.passed_pipe = True
            if pipe[0] + self.pipe_top.get_width() >= self.bird_x:
                self.passed_pipe = False

    def display_game_over(self):
        text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (300, 200))
        self.screen.blit(score_text, (300, 250))

        # Draw buttons with formatting
        pygame.draw.rect(self.screen, (0, 255, 0), self.restart_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button, border_radius=10)

        # Add text to buttons
        restart_text = self.font.render("Restart", True, (0, 0, 0))
        quit_text = self.font.render("Quit", True, (0, 0, 0))
        self.screen.blit(restart_text, (self.restart_button.x + 100, self.restart_button.y + 10))
        self.screen.blit(quit_text, (self.quit_button.x + 130, self.quit_button.y + 10))

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def handle_buttons(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.restart_button.collidepoint(mouse_pos):
                self.restart_game()
            elif self.quit_button.collidepoint(mouse_pos):
                pygame.quit()
                return

    def run_game(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == self.pipe_timer and not self.game_over and not self.paused:
                    self.spawn_pipe()
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.handle_buttons(event)

            if not self.game_over and not self.paused:
                movement_direction = self.head_controller.get_head_movement()

                if movement_direction == 'up':
                    self.bird_movement = -4
                elif movement_direction == 'down':
                    self.bird_movement = 3
                else:
                    self.bird_movement += self.gravity

                self.bird_y += self.bird_movement

                self.move_pipes()
                if self.check_collision():
                    self.game_over = True

                self.update_score()

            self.screen.blit(self.bird, (self.bird_x, self.bird_y))
            for pipe in self.pipe_list:
                self.screen.blit(self.pipe_top, (pipe[0], pipe[1]))
                self.screen.blit(self.pipe_bottom, (pipe[0], pipe[2]))

            self.display_score()

            if self.game_over:
                self.display_game_over()

            pygame.display.update()
            self.clock.tick(30)

    def restart_game(self):
        """Restart the game by resetting variables."""
        self.bird_y = 250
        self.bird_movement = 0
        self.pipe_list = []
        self.score = 0
        self.game_over = False

        pygame.time.set_timer(self.pipe_timer, 1400)

# For testing purposes
if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run_game()
