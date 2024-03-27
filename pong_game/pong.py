# Import necessary modules and classes from pygame
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_UP, K_DOWN, K_RETURN, KEYDOWN, KEYUP
from pong_game.ball import Ball
from pong_game.paddle import Paddle
from pong_game.scrolling_background import ScrollingBackground


# Function to handle the escape option in the game menu
def handle_escape_option(selected_option):
    options = ['Continue', 'Main Menu', 'Quit to Desktop']
    return options[selected_option]


# Function to add font to the game
def add_font(self, size=50, font_family='assets\\font\ARCADECLASSIC.TTF'):
    self.font = pygame.font.Font(font_family, size)
    return self.font


# Main class representing the Pong game
class PongGame:
    def __init__(self):
        pygame.init()  # Initialize pygame
        info_object = pygame.display.Info()  # Get display information
        pygame.display.set_caption("Project19-Pong")  # Set the window title
        add_font(self)  # Add font to the game
        # Initialize various game parameters
        self.player2_paddle = Paddle
        self.player1_paddle = Paddle
        self.ball = Ball
        self.level_screen_background = ''
        self.pc_difficulty = 0
        self.pc_paddle_speed = 0
        self.paddle_speed = 0
        self.ball_speed = 0
        self.paddle_height = 0
        self.paddle_width = 0
        self.ball_radius = 0
        self.base_width, self.base_height = 1920, 1080
        self.aspect_ratio = self.base_width / self.base_height
        self.width, self.height = info_object.current_w, info_object.current_h
        self.screen = pygame.display.set_mode((self.width, int(self.width / self.aspect_ratio)), pygame.FULLSCREEN)
        self.continues = 2
        self.lives = 3
        self.player2_score = 0
        self.player1_score = 0
        self.escape_dialog_visible = False  # Flag to track if the escape dialog is visible
        self.white = (255, 255, 255)
        self.hover_color = (100, 100, 100)
        self.black = (0, 0, 0)
        self.level = 1
        self.levels = 2
        # Load sounds and background images
        self.bounce_sound = pygame.mixer.Sound('assets\sounds\\bounce.wav')
        self.victory_sound = pygame.mixer.Sound('assets\sounds\player_wins.wav')
        self.score_point_sound = pygame.mixer.Sound('assets\sounds\point_scored.wav')
        self.level1_background = 'assets\images\level1_background_image.png'
        self.level2_background = 'assets\images\level2_background_image.png'
        self.scroll_speed = 5
        self.background_scroller = ScrollingBackground(self.screen, self.level1_background, self.scroll_speed)
        # Define positions for menu options
        options = ['Continue', 'Main Menu', 'Quit to Desktop']
        self.option_positions = [
            (self.width // 2 - add_font(self).render(option, True, (255, 255, 255)).get_width() // 2,
             self.height // 2 - len(options) * add_font(self).get_height() // 2 + i * 60)
            for i, option in enumerate(options)]

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load('assets\images\sprites.png').convert_alpha()

        # Define the rectangle area of the sprite you want (x, y, width, height)
        self.sprite_ball = pygame.Rect(100, 0, 50, 50)  # Adjust these values to your sprite's position and size
        self.sprite_player1_paddle = pygame.Rect(10, 10, 30, 130)
        self.sprite_player2_paddle = pygame.Rect(70, 10, 30, 130)

        # Load background music
        pygame.mixer.music.load('assets\sounds\\background.wav')

        pygame.mixer.music.set_volume(0.5)

    def run_game(self):
        self.run_menu()  # Start the game by running the menu screen

    # Method to run the main menu
    def run_menu(self):
        mode_selected = False
        mode = None

        while not mode_selected:
            self.screen.fill(self.black)  # Fill screen with black color

            # Display game title within a black container with a pixelated white border
            title_container_rect = pygame.Rect(self.screen.get_width() // 4, 50, self.screen.get_width() // 2, 150)
            pygame.draw.rect(self.screen, self.black, title_container_rect)
            pygame.draw.rect(self.screen, self.white, title_container_rect, 5, border_radius=0)

            # Render and position game title
            title_text = add_font(self, 100).render("Pong 19", True, self.white)
            title_x = title_container_rect.centerx - title_text.get_width() // 2
            title_y = title_container_rect.centery - title_text.get_height() // 2
            title_pos = (title_x, title_y)
            self.screen.blit(title_text, title_pos)

            # Render and position menu options
            mode_text_line1 = add_font(self).render("Select Mode", True, self.white)
            mode_text_line2 = add_font(self).render("1 Player", True, self.white)
            mode_text_line3 = add_font(self).render("2 Players", True, self.white)
            quit_text = add_font(self).render("Quit", True, self.white)
            screen_center_x = self.screen.get_width() // 2
            screen_center_y = self.screen.get_height() // 2
            mode_text_line1_pos = (screen_center_x - mode_text_line1.get_width() // 2 - 80, screen_center_y - 50)
            mode_text_line2_pos = (screen_center_x - mode_text_line2.get_width() // 2 - 120, screen_center_y + 50)
            mode_text_line3_pos = (screen_center_x - mode_text_line3.get_width() // 2 - 105, screen_center_y + 100)
            quit_text_pos = (screen_center_x - quit_text.get_width() // 2 - 165, screen_center_y + 150)

            rect_line2 = mode_text_line2.get_rect(topleft=mode_text_line2_pos)
            rect_line3 = mode_text_line3.get_rect(topleft=mode_text_line3_pos)
            rect_quit = quit_text.get_rect(topleft=quit_text_pos)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if rect_line2.collidepoint(mouse_x, mouse_y):
                mode_text_line2 = add_font(self).render("1 Player", True, self.hover_color)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif rect_line3.collidepoint(mouse_x, mouse_y):
                mode_text_line3 = add_font(self).render("2 Players", True, self.hover_color)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif rect_quit.collidepoint(mouse_x, mouse_y):
                quit_text = add_font(self).render("Quit", True, self.hover_color)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            self.screen.blit(mode_text_line1, mode_text_line1_pos)
            self.screen.blit(mode_text_line2, mode_text_line2_pos)
            self.screen.blit(mode_text_line3, mode_text_line3_pos)
            self.screen.blit(quit_text, quit_text_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_line2.collidepoint(mouse_x, mouse_y):
                        mode = "1P"
                        mode_selected = True
                    elif rect_line3.collidepoint(mouse_x, mouse_y):
                        mode = "2P"
                        mode_selected = True  # Set mode to 2 players and indicate mode selected
                    elif rect_quit.collidepoint(mouse_x, mouse_y):
                        pygame.quit()  # Quit the game when "Quit" is clicked

        # Reset the level before running levels again
        self.level = 1
        self.run_levels(mode)

    def run_levels(self, game_mode):
        while self.level <= self.levels:
            self.run_level(game_mode)

        # Check if all levels are completed
        if self.level > self.levels:
            self.lives = 3
            self.continues = 2
            self.display_credits()  # Display credits when all levels are completed

    def run_level(self, game_mode):
        if self.level == 1:
            self.level_screen_background = self.level1_background
            self.ball_radius = 15
            self.paddle_width = 15
            self.paddle_height = 200
            self.ball_speed = 14
            self.paddle_speed = 14
            self.pc_paddle_speed = 16
            self.pc_difficulty = 0.7
        elif self.level == 2:
            self.level_screen_background = self.level2_background

        self.background_scroller = ScrollingBackground(self.screen, self.level_screen_background, self.scroll_speed)
        self.ball = Ball(self.width // 2, self.height // 2, 25)
        self.player1_paddle = Paddle(0, (self.height - 130) // 2, 30, 130)
        self.player2_paddle = Paddle(self.width - 15, (self.height - 130) // 2, 30, 130)
        self.player1_score = 0
        self.player2_score = 0

        pygame.mixer.music.load('assets\sounds\\background.wav')
        pygame.mixer.music.play(-1)

        # Display the level indicator screen
        if game_mode == "1P":
            self.display_level_indicator()  # Display level indicator screen in 1 player mode
        # Start the countdown after displaying the level indicator
        self.reset_ball()
        self.play_countdown_sound()

        while self.lives >= 0:
            self.run_game_loop(game_mode)

    def show_game_over_logo(self):
        game_over_text = add_font(self, 100).render("Game Over", True, self.white)

        # Calculate the position to center the "Game Over" text
        game_over_x = self.screen.get_width() // 2 - game_over_text.get_width() // 2
        game_over_y = self.screen.get_height() // 2 - game_over_text.get_height() // 2

        game_over_pos = (game_over_x, game_over_y)

        # Draw a black background for the container
        pygame.draw.rect(self.screen, self.black, (game_over_x - 5, game_over_y - 5,
                                                   game_over_text.get_width() + 10, game_over_text.get_height() + 10))

        self.screen.blit(game_over_text, game_over_pos)
        pygame.display.flip()

    def show_game_over_dialog(self):
        options = ['Continue', 'Main Menu']
        selected_option = 0

        while True:
            for i, option in enumerate(options):
                if i == 0 and self.continues > 0:
                    option_text = add_font(self).render(f'Continue   {self.continues - 1}   left', True, self.white)
                else:
                    text_color = self.hover_color if i == selected_option else self.white
                    option_text = add_font(self).render(option, True, text_color)

                option_pos = (
                    self.width // 2 - option_text.get_width() // 2,
                    self.height // 2 - len(options) * option_text.get_height() // 2 + i * 60
                )
                self.screen.blit(option_text, option_pos)

            pygame.display.flip()

            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == K_RETURN:
                        if selected_option == 0:
                            self.continues -= 1   # Decrement continues if "Continue" is selected
                            return selected_option
                        elif selected_option == 1:
                            return selected_option

            pygame.event.pump()

    def display_level_indicator(self):
        level_indicator_text = add_font(self, 100).render(f"Level {self.level}", True, self.white)

        # Calculate the position to center the level indicator
        level_indicator_x = self.screen.get_width() // 2 - level_indicator_text.get_width() // 2
        level_indicator_y = self.screen.get_height() // 2 - level_indicator_text.get_height() // 2

        level_indicator_pos = (level_indicator_x, level_indicator_y)

        self.screen.fill(self.black)
        self.screen.blit(level_indicator_text, level_indicator_pos)
        pygame.display.flip()

        pygame.time.wait(3000)  # Wait for 2 seconds before starting the countdown

    def run_game_loop(self, game_mode):
        clock = pygame.time.Clock()
        running = True

        background_x = 0

        while running:
            self.screen.fill(self.black)

            # Draw scrolling background
            self.background_scroller.scroll_background()

            # Handle events here
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.show_escape_dialog()

            keys = pygame.key.get_pressed()
            self.move_paddles(keys, game_mode)
            if game_mode == "1P":
                self.move_computer_paddle()
            self.ball.rect.x += self.ball.dx
            self.ball.rect.y += self.ball.dy
            self.check_ball_collisions()
            running = self.check_ball_out_of_bounds(game_mode)
            self.draw_paddles_ball()
            self.display_scores(game_mode)

            background_x -= 1

            if background_x <= -self.width:
                background_x = 0

            pygame.display.flip()
            clock.tick(60)

        self.display_winner()
        pygame.time.wait(2000)

    def draw_paddles_ball(self):
        self.screen.blit(self.sprite_sheet, self.ball.rect.center, self.sprite_ball)
        self.screen.blit(self.sprite_sheet, self.player1_paddle.rect, self.sprite_player1_paddle)
        self.screen.blit(self.sprite_sheet, self.player2_paddle.rect, self.sprite_player2_paddle)

    def display_scores(self, game_mode):
        score_text = add_font(self).render(f"{self.player1_score}     {self.player2_score}", True, self.white)
        self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))

        if game_mode == "1P":
            lives_text = add_font(self).render(f"Lives {self.lives}", True, self.white)
            # Display lives indicator on the top left
            self.screen.blit(lives_text, (10, 10))

    def handle_events(self):
        keys = pygame.key.get_pressed()  # Get the state of all keys

        if keys[K_ESCAPE]:
            self.show_escape_dialog()

    # Add the following method to display the escape dialogue
    def show_escape_dialog(self):
        options = ['Continue', 'Main Menu', 'Quit to Desktop']
        selected_option = 0  # Index of the selected option

        while True:
            for i, option in enumerate(options):
                text_color = self.hover_color if i == selected_option else self.white
                option_text = add_font(self).render(option, True, text_color)
                option_pos = (self.width // 2 - option_text.get_width() // 2,
                              self.height // 2 - len(options) * option_text.get_height() // 2 + i * 60)
                self.screen.blit(option_text, option_pos)

            pygame.display.flip()

            pygame.time.delay(100)  # Add a small delay to prevent rapid key presses

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check for mouse clicks
            if mouse_pressed[0]:  # Left mouse button
                for i, option_pos in enumerate(self.option_positions):
                    x, y = option_pos
                    option_rect = pygame.Rect(x, y, option_text.get_width(), option_text.get_height())
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        selected_option = i
                        self.handle_escape_option(selected_option)
                        # Toggle the visibility of the escape dialogue
                        self.escape_dialog_visible = not self.escape_dialog_visible
                        break  # Exit the loop after handling the mouse click

            if keys[K_UP]:
                selected_option = (selected_option - 1) % len(options)
            elif keys[K_DOWN]:
                selected_option = (selected_option + 1) % len(options)
            elif keys[K_RETURN]:  # Use the Enter key to select an option
                self.handle_escape_option(selected_option)
                # Toggle the visibility of the escape dialogue
                self.escape_dialog_visible = not self.escape_dialog_visible
                break  # Exit the loop after handling Enter key

            # Toggle the visibility of the escape dialogue when the Escape key is pressed
            elif keys[K_ESCAPE]:
                self.escape_dialog_visible = not self.escape_dialog_visible
                break  # Exit the loop after toggling escape dialog visibility

            # Check if the dialogue should be visible
            if self.escape_dialog_visible:
                pygame.draw.rect(self.screen, self.black,
                                 (self.width // 4, self.height // 4, self.width // 2, self.height // 2))
                pygame.draw.rect(self.screen, self.white,
                                 (self.width // 4, self.height // 4, self.width // 2, self.height // 2), 5,
                                 border_radius=0)
                pygame.display.flip()

            # Ensure that the event queue is processed during the loop
            pygame.event.pump()

    # Add the following method to handle the selected escape option
    def handle_escape_option(self, selected_option):
        if selected_option == 0:  # Continue
            pass  # Add the code to resume the game
        elif selected_option == 1:  # Main Menu
            self.run_menu()
        elif selected_option == 2:  # Quit to Desktop
            pygame.quit()

    def move_paddles(self, keys, game_mode):
        if game_mode == "1P":
            if keys[pygame.K_w]:
                self.player1_paddle.move(-self.paddle_speed)
            if keys[pygame.K_s]:
                self.player1_paddle.move(self.paddle_speed)
        elif game_mode == "2P":
            if keys[pygame.K_w]:
                self.player1_paddle.move(-self.paddle_speed)
            if keys[pygame.K_s]:
                self.player1_paddle.move(self.paddle_speed)
            if keys[pygame.K_UP]:
                self.player2_paddle.move(-self.paddle_speed)
            if keys[pygame.K_DOWN]:
                self.player2_paddle.move(self.paddle_speed)

    def move_computer_paddle(self):
        if self.ball.dx > 0:
            if self.player2_paddle.rect.centery < self.ball.rect.centery:
                self.player2_paddle.move(self.pc_paddle_speed * self.pc_difficulty)
            elif self.player2_paddle.rect.centery > self.ball.rect.centery:
                self.player2_paddle.move(-self.pc_paddle_speed * self.pc_difficulty)

    def check_ball_collisions(self):
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.dy = -self.ball.dy
            self.bounce_sound.play()

        if self.ball.rect.colliderect(self.player1_paddle.rect) or self.ball.rect.colliderect(self.player2_paddle.rect):
            self.ball.dx = -self.ball.dx
            self.bounce_sound.play()

    def check_ball_out_of_bounds(self, game_mode):
        point_scored = False

        if self.ball.rect.left <= 0:
            self.player2_score += 1
            point_scored = True
        elif self.ball.rect.right >= self.width:
            self.player1_score += 1
            point_scored = True

        if point_scored:
            # Stop the background music
            pygame.mixer.music.stop()
            # Play the score point sound
            self.score_point_sound.play()
            # Wait for the score point sound to finish
            while pygame.mixer.get_busy():
                continue

            if game_mode == '2P':
                self.handle_2_player_game_mode()
            else:
                self.handle_1_player_game_mode()

        return True

    def handle_1_player_game_mode(self):
        if self.player1_score >= 6:
            self.display_winner()
            self.player1_score = 0
            self.player2_score = 0
            pygame.time.wait(2000)
            self.level += 1
            self.run_levels('1P')
        elif self.player2_score >= 6:
            self.display_winner()
            self.player1_score = 0
            self.player2_score = 0
            pygame.time.wait(2000)
            self.lives -= 1
            self.display_scores('1P')
            if self.lives == 0:
                self.handle_game_over()
            else:
                self.play_countdown_sound()
                self.reset_ball()

        else:
            self.play_countdown_sound()
            self.reset_ball()
        pygame.mixer.music.play(-1)

    def handle_2_player_game_mode(self):
        if self.player1_score >= 6 or self.player2_score >= 6:
            self.display_winner()
            pygame.time.wait(2000)
            self.show_game_over_logo()
            pygame.time.wait(5000)
            self.handle_escape_option(1)
        self.play_countdown_sound()
        self.reset_ball()
        pygame.mixer.music.play(-1)

    def handle_game_over(self):
        if self.continues == 1:
            self.show_game_over_logo()
            pygame.time.wait(5000)
            self.lives = 3
            self.continues = 2
            self.handle_escape_option(1)
        continue_option = self.show_game_over_dialog()
        if continue_option == 0:  # Continue
            self.lives = 3
            self.reset_ball()
            self.play_countdown_sound()
        elif continue_option == 1:  # Main Menu
            self.run_menu()
        elif continue_option == 2:  # Quit to Desktop
            pygame.quit()
            return  # Return from the method if quitting to desktop

    def update_and_draw_background(self):
        # Redraw the background
        self.screen.fill(self.black)
        self.background_scroller.scroll_background()
        self.display_scores(None)
        pygame.display.flip()

    def play_countdown_sound(self):
        countdown_sound = pygame.mixer.Sound('assets\sounds\countdown-sound.wav')
        countdown_sound.play()

        # Temporarily disable background scrolling
        self.background_scroller.scrolling_enabled = False

        for i in range(3, 0, -1):
            self.update_and_draw_background()

            lives_text = add_font(self).render(f"Lives {self.lives}", True, self.white)
            self.screen.blit(lives_text, (10, 10))

            # Display countdown in the middle of the screen
            countdown_text = add_font(self).render(str(i), True, self.white)
            countdown_rect = countdown_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(countdown_text, countdown_rect.topleft)

            ball_rect = self.ball.rect
            ball_rect.center = (self.width // 2, self.height // 3)

            self.player1_paddle = Paddle(0, (self.height - 130) // 2, 30, 130)
            self.player2_paddle = Paddle(self.width - 15, (self.height - 130) // 2, 30, 130)
            self.screen.blit(self.sprite_sheet, ball_rect.center, self.sprite_ball)
            self.screen.blit(self.sprite_sheet, self.player1_paddle.rect, self.sprite_player1_paddle)
            self.screen.blit(self.sprite_sheet, self.player2_paddle.rect, self.sprite_player2_paddle)

            pygame.display.flip()

            pygame.time.wait(1000)  # Wait for 1 second

        # Re-enable background scrolling
        self.background_scroller.scrolling_enabled = True
        pygame.time.wait(1000)  # Wait for 1 second after the countdown

    def reset_ball(self):
        self.ball = Ball(self.width // 2, self.height // 3, self.ball_radius)

    def display_credits(self):
        credit_lines = [
            "Thank you for playing!",
            "Game developed by",
            "..."
            "Music Credits Song Name",
            "Composer Composer Name",
            "Graphics Graphic Designer Name"
        ]

        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        line_spacing = 50

        rendered_lines = []

        for idx, line in enumerate(credit_lines):
            rendered_line = add_font(self).render(line, True, self.white)
            pos = (screen_center_x - rendered_line.get_width() // 2, screen_center_y - 250 + idx * line_spacing)
            rendered_lines.append((rendered_line, pos))

        self.screen.fill(self.black)

        for rendered_line, pos in rendered_lines:
            self.screen.blit(rendered_line, pos)

        pygame.display.flip()

        pygame.mixer.music.load('assets\sounds\credits_song.mp3')
        pygame.mixer.music.play()

        pygame.time.wait(15000)
        pygame.mixer.music.stop()  # Stop the music

        self.run_menu()

    def display_winner(self):
        winner_text = add_font(self).render(f"Player 1 Wins!" if self.player1_score >= 6 else "Player 2 Wins!", True,
                                            self.white)
        self.screen.blit(winner_text, (
            self.width // 2 - winner_text.get_width() // 2, self.height // 5 - winner_text.get_height() // 2))
        pygame.display.flip()


if __name__ == "__main__":
    pong_game = PongGame()
    pong_game.run_game()
    pygame.quit()
