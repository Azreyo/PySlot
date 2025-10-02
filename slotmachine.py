#!/usr/bin/env python3
import pygame
import random
import sys
import os
import platform
import subprocess

# Initialize Pygame
pygame.init()

# Get display info for fullscreen
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
FPS = 60

# Game constants
REELS = 5
ROWS = 4
coins = 1000
spin_cost = 20

# Slot symbols with weights
symbols = ["🍒", "🍋", "🍉", "⭐", "💎", "7️⃣"]
symbol_weights = [30, 25, 20, 15, 8, 2]
symbol_rewards = {
    "🍒": 5,
    "🍋": 10,
    "🍉": 15,
    "⭐": 25,
    "💎": 50,
    "7️⃣": 100
}

# Win lines
WIN_LINES = [
    [1, 1, 1, 1, 1],  # Middle line
    [0, 0, 0, 0, 0],  # Top line
    [2, 2, 2, 2, 2],  # Bottom line
    [0, 1, 2, 1, 0],  # V shape
    [2, 1, 0, 1, 2],  # Inverse V
    [0, 0, 1, 2, 2],  # Down stairs
    [2, 2, 1, 0, 0],  # Up stairs
    [1, 0, 1, 2, 1],  # Zig-zag
    [1, 2, 1, 0, 1],  # Zag-zig
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (76, 175, 80)
DARK_GREEN = (56, 142, 60)
ORANGE = (255, 152, 0)
BLUE = (33, 150, 243)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (244, 67, 54)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
SLOT_BG = (40, 44, 52)
REEL_BG = (240, 240, 245)
PURPLE = (156, 39, 176)
CYAN = (0, 188, 212)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.enabled = True
        self.hover = False
        self.font_size = font_size
        
    def draw(self, screen, font):
        color = self.color if self.enabled else DARK_GRAY
        if self.hover and self.enabled:
            color = tuple(min(c + 30, 255) for c in color)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=15)
        
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("🎰 PySlot - Professional Slot Machine")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.emoji_font = self.load_emoji_font(int(SCREEN_HEIGHT * 0.08))
        self.title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.06))
        self.text_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
        self.button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.035))
        self.small_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.025))
        
        # Game state
        self.coins = coins
        self.bet_per_line = 1
        self.lines = 9
        self.total_bet = 0
        
        # Slot state - 5 reels x 4 rows
        self.reels = [[random.choice(symbols) for _ in range(ROWS)] for _ in range(REELS)]
        self.display_reels = [[random.choice(symbols) for _ in range(ROWS + 6)] for _ in range(REELS)]
        
        # Animation state
        self.spinning = False
        self.reel_spinning = [False] * REELS
        self.reel_offset = [0] * REELS
        self.reel_speed = [0] * REELS
        self.reel_stop_time = [0] * REELS
        self.spin_time = 0
        
        # Win state
        self.winning_lines = []
        self.win_animation_timer = 0
        self.win_flash = 0
        self.total_win = 0
        
        self.message = "Select lines and press SPIN!"
        
        # Calculate UI positions
        self.calculate_layout()
        
        # Create buttons
        btn_width = SCREEN_WIDTH * 0.15
        btn_height = SCREEN_HEIGHT * 0.08
        btn_y = SCREEN_HEIGHT * 0.85
        btn_spacing = SCREEN_WIDTH * 0.02
        
        center_x = SCREEN_WIDTH // 2
        self.spin_button = Button(
            center_x - btn_width // 2, btn_y,
            btn_width, btn_height, "SPIN", GREEN
        )
        
        self.lines_down = Button(
            center_x - btn_width * 1.8, btn_y,
            btn_width * 0.4, btn_height, "-", BLUE
        )
        self.lines_up = Button(
            center_x - btn_width * 1.3, btn_y,
            btn_width * 0.4, btn_height, "+", BLUE
        )
        
        self.bet_down = Button(
            center_x + btn_width * 0.9, btn_y,
            btn_width * 0.4, btn_height, "-", ORANGE
        )
        self.bet_up = Button(
            center_x + btn_width * 1.4, btn_y,
            btn_width * 0.4, btn_height, "+", ORANGE
        )
        
        # Exit button (X in corner)
        exit_size = int(SCREEN_HEIGHT * 0.06)
        self.exit_button = Button(
            SCREEN_WIDTH - exit_size - 20, 20,
            exit_size, exit_size, "✕", RED, WHITE, int(SCREEN_HEIGHT * 0.045)
        )
        
        self.running = True
    
    def calculate_layout(self):
        """Calculate reel positions and sizes"""
        # Machine area
        machine_margin = SCREEN_WIDTH * 0.1
        self.machine_width = SCREEN_WIDTH - 2 * machine_margin
        self.machine_height = SCREEN_HEIGHT * 0.65
        self.machine_x = machine_margin
        self.machine_y = SCREEN_HEIGHT * 0.15
        
        # Reel dimensions
        reel_margin = self.machine_width * 0.02
        total_reel_width = self.machine_width - 2 * reel_margin
        self.reel_spacing = total_reel_width * 0.02
        self.reel_width = (total_reel_width - self.reel_spacing * (REELS - 1)) / REELS
        self.reel_height = self.machine_height * 0.85
        
        self.symbol_height = self.reel_height / ROWS
        
        # Calculate reel positions
        self.reel_positions = []
        for i in range(REELS):
            x = self.machine_x + reel_margin + i * (self.reel_width + self.reel_spacing)
            y = self.machine_y + self.machine_height * 0.08
            self.reel_positions.append((x, y))
    
    def load_emoji_font(self, size):
        """Load emoji font for Linux"""
        import os
        import platform
        import subprocess
        
        emoji_fonts = []
        
        if platform.system() == "Windows":
            emoji_fonts.extend(["segoeuiemoji", "seguiemj", "Arial"])
        elif platform.system() == "Linux":
            try:
                result = subprocess.run(['fc-list', ':family=Noto Color Emoji', 'file'],
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0 and result.stdout:
                    font_path = result.stdout.split(':')[0].strip()
                    if font_path and os.path.exists(font_path):
                        emoji_fonts.append(font_path)
            except Exception as e:
                pass
            
            emoji_fonts.extend([
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                "Symbola",
                "/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf",
                "Noto Sans Symbols2",
                "/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf",
            ])
        elif platform.system() == "Darwin":
            emoji_fonts.extend(["Apple Color Emoji"])
        
        for font_path in emoji_fonts:
            try:
                if os.path.isabs(font_path):
                    if os.path.exists(font_path):
                        font = pygame.font.Font(font_path, size)
                        print(f"✓ Loaded emoji font: {font_path}")
                        return font
                else:
                    font = pygame.font.SysFont(font_path, size)
                    print(f"✓ Loaded emoji font: {font_path}")
                    return font
            except:
                continue
        
        print("⚠ Using default font")
        return pygame.font.Font(None, size)
    
    def start_spin(self):
        if self.spinning:
            return
        
        self.total_bet = self.bet_per_line * self.lines
        
        if self.coins < self.total_bet:
            self.message = "Not enough coins!"
            return
        
        self.coins -= self.total_bet
        self.spinning = True
        self.winning_lines = []
        self.total_win = 0
        
        # Start all reels
        self.reel_spinning = [True] * REELS
        self.reel_offset = [0] * REELS
        self.reel_speed = [30] * REELS
        self.spin_time = 0
        
        # Set stop times
        for i in range(REELS):
            self.reel_stop_time[i] = 60 + i * 15
        
        # Generate result
        for reel in range(REELS):
            for row in range(ROWS):
                self.reels[reel][row] = random.choices(symbols, weights=symbol_weights, k=1)[0]
        
        self.message = "Spinning..."
    
    def update_spin_animation(self):
        if not self.spinning:
            if self.win_animation_timer > 0:
                self.win_animation_timer -= 1
                self.win_flash = (self.win_flash + 1) % 30
            return
        
        self.spin_time += 1
        all_stopped = True
        
        for i in range(REELS):
            if self.reel_spinning[i]:
                all_stopped = False
                
                # Move reel
                self.reel_offset[i] += self.reel_speed[i]
                
                # Cycle symbols
                if self.reel_offset[i] >= self.symbol_height:
                    self.reel_offset[i] = 0
                    self.display_reels[i].pop(0)
                    self.display_reels[i].append(random.choices(symbols, weights=symbol_weights, k=1)[0])
                
                # Check if should stop
                if self.spin_time >= self.reel_stop_time[i]:
                    self.reel_speed[i] = max(5, self.reel_speed[i] - 3)
                    
                    if self.reel_speed[i] <= 5 and self.reel_offset[i] < 5:
                        self.reel_spinning[i] = False
                        self.reel_offset[i] = 0
                        # Set final symbols
                        for row in range(ROWS):
                            self.display_reels[i][row] = self.reels[i][row]
        
        if all_stopped:
            self.spinning = False
            self.check_wins()
    
    def check_wins(self):
        """Check for winning lines"""
        self.winning_lines = []
        self.total_win = 0
        
        for line_idx in range(self.lines):
            line = WIN_LINES[line_idx]
            symbols_on_line = [self.reels[reel][line[reel]] for reel in range(REELS)]
            
            # Check for matches
            first_symbol = symbols_on_line[0]
            match_count = 1
            
            for i in range(1, REELS):
                if symbols_on_line[i] == first_symbol:
                    match_count += 1
                else:
                    break
            
            if match_count >= 3:
                win_amount = symbol_rewards[first_symbol] * self.bet_per_line * match_count
                self.total_win += win_amount
                self.winning_lines.append({
                    'line_idx': line_idx,
                    'line': line,
                    'symbol': first_symbol,
                    'count': match_count,
                    'win': win_amount
                })
        
        if self.total_win > 0:
            self.coins += self.total_win
            self.message = f"WIN! {self.total_win} coins on {len(self.winning_lines)} line(s)!"
            self.win_animation_timer = 180
            self.win_flash = 0
        else:
            self.message = "No win. Try again!"
        
        self.spin_button.enabled = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.spinning:
                    self.start_spin()
            
            if self.exit_button.handle_event(event):
                self.running = False
            
            if self.spin_button.handle_event(event) and not self.spinning:
                self.start_spin()
            
            if not self.spinning:
                if self.lines_up.handle_event(event):
                    self.lines = min(9, self.lines + 1)
                if self.lines_down.handle_event(event):
                    self.lines = max(1, self.lines - 1)
                if self.bet_up.handle_event(event):
                    self.bet_per_line = min(10, self.bet_per_line + 1)
                if self.bet_down.handle_event(event):
                    self.bet_per_line = max(1, self.bet_per_line - 1)
    
    def draw(self):
        # Background gradient
        for y in range(SCREEN_HEIGHT):
            color_val = int(25 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(self.screen, (color_val, color_val + 5, color_val + 10), (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title = self.title_font.render("🎰 PYSLOT CASINO 🎰", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.05))
        title_shadow = self.title_font.render("🎰 PYSLOT CASINO 🎰", True, BLACK)
        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)
        
        # Coins display
        coins_bg = pygame.Rect(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.05)
        pygame.draw.rect(self.screen, BLACK, coins_bg, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, coins_bg, 3, border_radius=10)
        coins_text = self.text_font.render(f"💰 {self.coins}", True, GOLD)
        coins_rect = coins_text.get_rect(center=coins_bg.center)
        self.screen.blit(coins_text, coins_rect)
        
        # Bet display
        bet_bg = pygame.Rect(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.05)
        pygame.draw.rect(self.screen, BLACK, bet_bg, border_radius=10)
        pygame.draw.rect(self.screen, ORANGE, bet_bg, 3, border_radius=10)
        bet_text = self.small_font.render(f"Bet: {self.bet_per_line} × {self.lines} = {self.bet_per_line * self.lines}", True, WHITE)
        bet_rect = bet_text.get_rect(center=bet_bg.center)
        self.screen.blit(bet_text, bet_rect)
        
        # Machine body
        machine_rect = pygame.Rect(self.machine_x, self.machine_y, self.machine_width, self.machine_height)
        pygame.draw.rect(self.screen, DARK_RED, machine_rect, border_radius=20)
        pygame.draw.rect(self.screen, GOLD, machine_rect, 6, border_radius=20)
        
        # Inner panel
        panel_rect = machine_rect.inflate(-40, -40)
        pygame.draw.rect(self.screen, SLOT_BG, panel_rect, border_radius=15)
        
        # Draw reels
        self.draw_reels()
        
        # Draw win lines
        if self.winning_lines and self.win_animation_timer > 0:
            self.draw_win_lines()
        
        # Message
        msg_bg = pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.75, SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.06)
        pygame.draw.rect(self.screen, BLACK, msg_bg, border_radius=10)
        msg_color = GOLD if self.total_win > 0 else WHITE
        msg_text = self.text_font.render(self.message, True, msg_color)
        msg_rect = msg_text.get_rect(center=msg_bg.center)
        self.screen.blit(msg_text, msg_rect)
        
        # Buttons
        self.spin_button.draw(self.screen, self.button_font)
        
        # Lines controls
        lines_label = self.small_font.render(f"Lines: {self.lines}", True, WHITE)
        lines_x = self.lines_down.rect.centerx + (self.lines_up.rect.centerx - self.lines_down.rect.centerx) // 2
        self.screen.blit(lines_label, (lines_x - lines_label.get_width() // 2, self.lines_down.rect.y - 30))
        self.lines_down.draw(self.screen, self.button_font)
        self.lines_up.draw(self.screen, self.button_font)
        
        # Bet controls
        bet_label = self.small_font.render(f"Bet: {self.bet_per_line}", True, WHITE)
        bet_x = self.bet_down.rect.centerx + (self.bet_up.rect.centerx - self.bet_down.rect.centerx) // 2
        self.screen.blit(bet_label, (bet_x - bet_label.get_width() // 2, self.bet_down.rect.y - 30))
        self.bet_down.draw(self.screen, self.button_font)
        self.bet_up.draw(self.screen, self.button_font)
        
        # Exit button
        self.exit_button.draw(self.screen, self.button_font)
        
        # Instructions
        inst_text = self.small_font.render("SPACE to spin | ESC to exit", True, LIGHT_GRAY)
        self.screen.blit(inst_text, (20, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
    
    def draw_reels(self):
        """Draw all reels with symbols"""
        for reel_idx in range(REELS):
            x, y = self.reel_positions[reel_idx]
            
            # Reel background
            reel_rect = pygame.Rect(x, y, self.reel_width, self.reel_height)
            pygame.draw.rect(self.screen, REEL_BG, reel_rect, border_radius=10)
            pygame.draw.rect(self.screen, DARK_GRAY, reel_rect, 3, border_radius=10)
            
            # Clip to reel area
            clip_rect = pygame.Rect(x + 5, y + 5, self.reel_width - 10, self.reel_height - 10)
            self.screen.set_clip(clip_rect)
            
            # Draw symbols
            for row in range(ROWS + 2):
                symbol_y = y + row * self.symbol_height - self.reel_offset[reel_idx]
                
                if self.reel_spinning[reel_idx]:
                    symbol = self.display_reels[reel_idx][row % len(self.display_reels[reel_idx])]
                else:
                    if row < ROWS:
                        symbol = self.reels[reel_idx][row]
                    else:
                        continue
                
                symbol_surf = self.emoji_font.render(symbol, True, BLACK)
                symbol_rect = symbol_surf.get_rect(center=(x + self.reel_width // 2, symbol_y + self.symbol_height // 2))
                self.screen.blit(symbol_surf, symbol_rect)
            
            self.screen.set_clip(None)
            
            # Reel number
            reel_num = self.small_font.render(f"{reel_idx + 1}", True, WHITE)
            self.screen.blit(reel_num, (x + 5, y - 25))
    
    def draw_win_lines(self):
        """Draw animated win lines"""
        if self.win_flash < 15:
            alpha = 180
        else:
            alpha = 100
        
        line_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        colors = [GOLD, CYAN, PURPLE, GREEN, ORANGE, RED, BLUE, WHITE, (255, 105, 180)]
        
        for win_info in self.winning_lines:
            line = win_info['line']
            line_idx = win_info['line_idx']
            match_count = win_info['count']
            
            color = colors[line_idx % len(colors)]
            color_alpha = (*color, alpha)
            
            points = []
            for reel in range(match_count):
                x, y = self.reel_positions[reel]
                row = line[reel]
                point_x = x + self.reel_width // 2
                point_y = y + row * self.symbol_height + self.symbol_height // 2
                points.append((point_x, point_y))
            
            if len(points) >= 2:
                pygame.draw.lines(line_surface, color_alpha, False, points, 8)
                for point in points:
                    pygame.draw.circle(line_surface, color_alpha, point, 15)
        
        self.screen.blit(line_surface, (0, 0))
    
    def run(self):
        print("=" * 60)
        print("🎰 PySlot - Professional Casino Slot Machine")
        print("=" * 60)
        print("✓ Game started in fullscreen mode")
        print("=" * 60)
        
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
