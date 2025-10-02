# -*- coding: utf-8 -*-
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

coins = 500
spin_cost = 10

# Using emojis for slot machine symbols
symbols = ["🍒", "🍋", "🍉", "⭐", "💎", "7"]
symbol_weights = [0.5, 0.3, 2.5, 0.15, 0.07, 0.03]
symbol_rewards = {
    "🍒": 20,
    "🍋": 40,
    "🍉": 60,
    "⭐": 80,
    "💎": 120,
    "7": 200
}
jackpot_mult = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (76, 175, 80)
ORANGE = (255, 152, 0)
BLUE = (33, 150, 243)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (244, 67, 54)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.enabled = True
        self.hover = False
        
    def draw(self, screen, font):
        color = self.color if self.enabled else DARK_GRAY
        if self.hover and self.enabled:
            # Lighten color on hover
            color = tuple(min(c + 30, 255) for c in color)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, self.text_color if self.enabled else LIGHT_GRAY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled and self.rect.collidepoint(event.pos):
                return True
        return False

class SlotMachineGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Slot Machine - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Load fonts - try to use system emoji fonts
        self.emoji_font = self.load_emoji_font(72)
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 24)
        
        # Game state
        self.coins = coins
        self.mult = 2
        self.tempcoins = 0
        self.last_reward = 0
        
        # Animation state
        self.spinning = False
        self.spin_count = 0
        self.spin_delay = 0
        self.final_result = []
        
        # Current display
        self.current_symbols = ["🍒", "🍋", "🍉"]
        self.message = "Press SPIN to start!"
        
        # Create buttons
        self.spin_button = Button(300, 400, 200, 50, "SPIN", GREEN)
        self.mult_button = Button(300, 460, 200, 50, "Try Multiplier", ORANGE)
        self.mult_button.enabled = False
        self.take_button = Button(300, 520, 200, 50, "Take Winnings", BLUE)
        self.take_button.enabled = False
        
        self.running = True
    
    def load_emoji_font(self, size):
        """Try to load an emoji-compatible font for Windows, Linux, and macOS"""
        import os
        import platform
        
        emoji_fonts = []
        
        # Windows fonts
        if platform.system() == "Windows":
            emoji_fonts.extend([
                "segoeuiemoji",  # Windows emoji font (works great on Windows 11!)
                "seguiemj",
                "Arial"
            ])
        
        # Linux fonts (absolute paths)
        elif platform.system() == "Linux":
            emoji_fonts.extend([
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ])
        
        # macOS fonts
        elif platform.system() == "Darwin":
            emoji_fonts.extend([
                "Apple Color Emoji",
                "/System/Library/Fonts/Apple Color Emoji.ttc"
            ])
        
        # Try each font
        for font_path in emoji_fonts:
            try:
                # Check if it's an absolute path or font name
                if os.path.exists(font_path) if os.path.isabs(font_path) else True:
                    font = pygame.font.SysFont(font_path, size) if not os.path.isabs(font_path) else pygame.font.Font(font_path, size)
                    # Test if it can render an emoji
                    test = font.render("🍒", True, WHITE)
                    print(f"✓ Successfully loaded emoji font: {font_path}")
                    return font
            except Exception as e:
                continue
        
        # Final fallback
        print("⚠ Using default font (emojis may not display correctly)")
        return pygame.font.Font(None, size)
    
    def weighted_choice(self, n=1):
        return random.choices(symbols, weights=symbol_weights, k=n)
    
    def start_spin(self):
        if self.coins < spin_cost:
            self.message = "Game Over! Not enough coins."
            self.spin_button.enabled = False
            return
        
        self.coins -= spin_cost
        self.spinning = True
        self.spin_count = 0
        self.spin_delay = 0
        self.final_result = self.weighted_choice(3)
        self.spin_button.enabled = False
    
    def update_spin_animation(self):
        if not self.spinning:
            return
        
        self.spin_delay += 1
        if self.spin_delay >= 5:  # Change symbols every 5 frames
            self.spin_delay = 0
            self.spin_count += 1
            
            if self.spin_count < 15:
                self.current_symbols = self.weighted_choice(3)
            else:
                self.current_symbols = self.final_result
                self.spinning = False
                self.check_win()
    
    def check_win(self):
        if self.current_symbols[0] == self.current_symbols[1] == self.current_symbols[2]:
            symbol = self.current_symbols[0]
            if symbol == "7":
                reward = symbol_rewards[symbol] * jackpot_mult
                self.message = "🎉 JACKPOT! Try multiplier or take winnings?"
            else:
                reward = symbol_rewards[symbol]
                self.message = f"You won {reward} coins! Try multiplier?"
            
            self.last_reward = reward
            self.tempcoins = reward
            self.coins += reward
            self.mult_button.enabled = True
            self.take_button.enabled = True
        else:
            self.message = "You lost! Try again!"
            self.mult_button.enabled = False
            self.take_button.enabled = False
            self.spin_button.enabled = True
    
    def start_multiplier(self):
        self.coins -= self.tempcoins
        rel = self.weighted_choice(2)
        self.current_symbols = [rel[0], rel[1], ""]
        
        if rel[0] == rel[1]:
            self.tempcoins = int(self.last_reward * self.mult)
            self.message = f"Win! Potential: {self.tempcoins} coins. Continue or take?"
            self.mult_button.text = "Continue (x2)"
            self.mult_button.enabled = True
            self.take_button.enabled = True
            self.mult += 2
        else:
            self.message = "Lost the multiplier round!"
            self.mult_button.enabled = False
            self.mult_button.text = "Try Multiplier"
            self.take_button.enabled = False
            self.spin_button.enabled = True
            self.mult = 2
            self.tempcoins = 0
            self.current_symbols = ["🍒", "🍋", "🍉"]
    
    def take_winnings(self):
        self.coins += self.tempcoins
        self.message = f"You took {self.tempcoins} coins! Great choice!"
        self.mult_button.enabled = False
        self.mult_button.text = "Try Multiplier"
        self.take_button.enabled = False
        self.spin_button.enabled = True
        self.mult = 2
        self.tempcoins = 0
        self.current_symbols = ["🍒", "🍋", "🍉"]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.spin_button.handle_event(event) and not self.spinning:
                self.start_spin()
            
            if self.mult_button.handle_event(event):
                self.start_multiplier()
            
            if self.take_button.handle_event(event):
                self.take_winnings()
    
    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        # Draw title
        title = self.title_font.render("🎰 SLOT MACHINE 🎰", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Draw coins
        coins_text = self.text_font.render(f"Coins: {self.coins}", True, WHITE)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(coins_text, coins_rect)
        
        # Draw slot machine display (with box)
        slot_rect = pygame.Rect(150, 140, 500, 120)
        pygame.draw.rect(self.screen, WHITE, slot_rect, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, slot_rect, 4, border_radius=15)
        
        # Draw symbols
        symbol_spacing = 500 // 3
        for i, symbol in enumerate(self.current_symbols):
            if symbol:  # Only draw if symbol exists
                symbol_surf = self.emoji_font.render(symbol, True, BLACK)
                symbol_rect = symbol_surf.get_rect(center=(150 + symbol_spacing // 2 + i * symbol_spacing, 200))
                self.screen.blit(symbol_surf, symbol_rect)
        
        # Draw message
        msg_surf = self.text_font.render(self.message, True, WHITE)
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(msg_surf, msg_rect)
        
        # Draw buttons
        self.spin_button.draw(self.screen, self.button_font)
        self.mult_button.draw(self.screen, self.button_font)
        self.take_button.draw(self.screen, self.button_font)
        
        # Draw multiplier info
        if self.mult > 2:
            mult_text = self.text_font.render(f"Multiplier: {self.mult}x", True, ORANGE)
            mult_rect = mult_text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            self.screen.blit(mult_text, mult_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update_spin_animation()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SlotMachineGame()
    game.run()
