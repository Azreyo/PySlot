#!/usr/bin/env python3
import pygame
import random
import sys
import os
import platform
import subprocess
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

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

# Slot symbols with weights (more = appears more often)
symbols = [
    "🍒",  # Cherry - classic slot symbol
    "🍋",  # Lemon - classic fruit
    "🍊",  # Orange - classic fruit
    "🍇",  # Grapes - classic fruit
    "🍉",  # Watermelon - high value fruit
    "🔔",  # Bell - traditional slot symbol
    "⭐",  # Star - medium value
    "💰",  # Money bag - high value
    "💎",  # Diamond - very high value
    "7️⃣",   # Lucky 7 - jackpot symbol
    "�",  # Slot machine - special symbol
    "🎁"   # Gift/Scatter - triggers bonus
]
symbol_weights = [35, 30, 28, 25, 22, 18, 15, 12, 8, 3, 6, 5]
symbol_rewards = {
    "🍒": 5,      # Cherry - lowest
    "🍋": 8,      # Lemon
    "🍊": 10,     # Orange
    "🍇": 12,     # Grapes
    "🍉": 15,     # Watermelon
    "🔔": 20,     # Bell
    "⭐": 30,     # Star
    "💰": 40,     # Money bag
    "💎": 60,     # Diamond
    "7️⃣": 150,    # Lucky 7 - jackpot!
    "🎰": 25,     # Slot machine
    "🎁": 20      # Scatter pays + triggers bonus
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
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 191, 255)
NEON_ORANGE = (255, 140, 0)
NEON_YELLOW = (255, 255, 0)
LIME = (0, 255, 0)
MAGENTA = (255, 0, 255)
ELECTRIC_BLUE = (125, 249, 255)
HOT_PINK = (255, 105, 180)

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
            color = tuple(min(c + 50, 255) for c in color)
        
        # Draw gradient background
        for i in range(int(self.rect.height)):
            progress = i / self.rect.height
            r = int(color[0] * (0.7 + 0.3 * progress))
            g = int(color[1] * (0.7 + 0.3 * progress))
            b = int(color[2] * (0.7 + 0.3 * progress))
            pygame.draw.rect(screen, (r, g, b), 
                           pygame.Rect(self.rect.x, self.rect.y + i, self.rect.width, 1))
        
        # Glowing border
        if self.enabled:
            border_colors = [color, tuple(min(c + 30, 255) for c in color), BLACK]
            for i, bcolor in enumerate(border_colors):
                pygame.draw.rect(screen, bcolor, self.rect.inflate(i*2, i*2), 2, border_radius=15 + i)
        else:
            pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=15)
        
        text_surf = font.render(self.text, True, self.text_color if self.enabled else LIGHT_GRAY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Add glow to enabled buttons
        if self.enabled:
            text_glow = font.render(self.text, True, BLACK)
            screen.blit(text_glow, (text_rect.x + 2, text_rect.y + 2))
        
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
        pygame.display.set_caption("PySlot - Professional Slot Machine")
        self.clock = pygame.time.Clock()
        
        # Initialize sounds
        self.sounds = self.create_sounds()
        
        # Load fonts
        self.emoji_font = self.load_emoji_font(int(SCREEN_HEIGHT * 0.08))
        self.title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.06))
        self.text_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.04))
        self.button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.035))
        self.small_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.025))
        
        # Game state
        self.coins = coins
        self.bet_per_line = 1
        self.min_bet = 1
        self.max_bet = 100  # Increased from 10 to 100
        self.lines = 9
        self.total_bet = 0
        
        # Slot state - 5 reels x 4 rows
        self.reels = [[random.choice(symbols) for _ in range(ROWS + 6)] for _ in range(REELS)]
        
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
        self.particles = []
        self.background_phase = 0
        self.win_particles = []
        
        # Multiplier/Combo system
        self.win_streak = 0
        self.multiplier = 1
        self.max_streak = 0
        
        # Free spins bonus
        self.free_spins = 0
        self.free_spins_active = False
        self.scatter_count = 0
        self.bonus_triggered = False
        self.bonus_animation_timer = 0
        
        # Screen management
        self.screen_state = "main"  # "main" or "bet_config"
        self.transition_progress = 0  # 0 to 1, for smooth animations
        self.transitioning = False
        self.transition_target = "main"
        
        self.message = "Select lines and press SPIN!"
        
        # Calculate UI positions
        self.calculate_layout()
        
        # Create buttons
        btn_width = SCREEN_WIDTH * 0.15
        btn_height = SCREEN_HEIGHT * 0.08
        btn_y = SCREEN_HEIGHT * 0.88  # Moved down slightly
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
        
        # Quick bet control buttons (row above main buttons with more spacing)
        quick_btn_width = SCREEN_WIDTH * 0.11
        quick_btn_height = SCREEN_HEIGHT * 0.055
        quick_btn_y = btn_y - quick_btn_height - 25  # Increased spacing
        
        # Min, Half, Double, Max buttons (with better spacing)
        self.bet_min = Button(
            center_x - quick_btn_width * 2.2, quick_btn_y,
            quick_btn_width * 0.95, quick_btn_height, "MIN", PURPLE
        )
        self.bet_half = Button(
            center_x - quick_btn_width * 1.1, quick_btn_y,
            quick_btn_width * 0.95, quick_btn_height, "÷2", CYAN
        )
        self.bet_double = Button(
            center_x + quick_btn_width * 0.15, quick_btn_y,
            quick_btn_width * 0.95, quick_btn_height, "×2", NEON_ORANGE
        )
        self.bet_max = Button(
            center_x + quick_btn_width * 1.25, quick_btn_y,
            quick_btn_width * 0.95, quick_btn_height, "MAX", NEON_PINK
        )
        
        # Preset bet amount buttons (above quick controls with more spacing)
        preset_btn_width = SCREEN_WIDTH * 0.075
        preset_btn_height = SCREEN_HEIGHT * 0.048
        preset_btn_y = quick_btn_y - preset_btn_height - 20  # Increased spacing
        preset_start_x = center_x - preset_btn_width * 3.2
        
        self.preset_bet_1 = Button(
            preset_start_x, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "1", BLUE
        )
        self.preset_bet_5 = Button(
            preset_start_x + preset_btn_width * 1.05, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "5", BLUE
        )
        self.preset_bet_10 = Button(
            preset_start_x + preset_btn_width * 2.1, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "10", GREEN
        )
        self.preset_bet_25 = Button(
            preset_start_x + preset_btn_width * 3.15, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "25", ORANGE
        )
        self.preset_bet_50 = Button(
            preset_start_x + preset_btn_width * 4.2, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "50", NEON_ORANGE
        )
        self.preset_bet_100 = Button(
            preset_start_x + preset_btn_width * 5.25, preset_btn_y,
            preset_btn_width * 0.9, preset_btn_height, "100", RED
        )
        
        # Exit button (X in corner)
        exit_size = int(SCREEN_HEIGHT * 0.06)
        self.exit_button = Button(
            SCREEN_WIDTH - exit_size - 20, 20,
            exit_size, exit_size, "x", RED, WHITE, int(SCREEN_HEIGHT * 0.045)
        )
        
        # Bet config toggle button (arrow on left side)
        arrow_width = SCREEN_WIDTH * 0.04
        arrow_height = SCREEN_HEIGHT * 0.1
        self.bet_config_button = Button(
            10, SCREEN_HEIGHT // 2 - arrow_height // 2,
            arrow_width, arrow_height, "►", NEON_ORANGE, WHITE, int(SCREEN_HEIGHT * 0.06)
        )
        
        # Back button for bet config screen
        self.back_button = Button(
            SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.05,
            SCREEN_WIDTH * 0.12, SCREEN_HEIGHT * 0.07, "◄ BACK", PURPLE, WHITE, int(SCREEN_HEIGHT * 0.04)
        )
        
        self.running = True
    
    def create_sounds(self):
        """Create simple sound effects using pygame"""
        import numpy as np
        
        sounds = {}
        sample_rate = 22050
        
        try:
            # Spin sound - rising tone
            duration = 0.1
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = np.linspace(200, 400, len(t))
            spin_wave = np.sin(2 * np.pi * frequency * t) * 0.3
            spin_wave = (spin_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((spin_wave, spin_wave))
            sounds['spin'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Reel stop sound - quick beep
            duration = 0.08
            t = np.linspace(0, duration, int(sample_rate * duration))
            stop_wave = np.sin(2 * np.pi * 600 * t) * 0.2 * np.exp(-t * 20)
            stop_wave = (stop_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((stop_wave, stop_wave))
            sounds['stop'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Win sound - happy ascending tones
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration))
            win_wave = np.zeros_like(t)
            for freq in [523, 659, 784, 1047]:  # C, E, G, C (major chord)
                win_wave += np.sin(2 * np.pi * freq * t) * 0.15
            win_wave *= np.exp(-t * 3)  # Fade out
            win_wave = (win_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((win_wave, win_wave))
            sounds['win'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Big win sound - celebration
            duration = 0.8
            t = np.linspace(0, duration, int(sample_rate * duration))
            bigwin_wave = np.zeros_like(t)
            for freq in [523, 659, 784, 1047, 1319]:  # Extended chord
                bigwin_wave += np.sin(2 * np.pi * freq * t) * 0.12
            # Add some sparkle
            bigwin_wave += np.sin(2 * np.pi * 2093 * t) * 0.1 * np.sin(t * 20)
            bigwin_wave *= np.exp(-t * 2)
            bigwin_wave = (bigwin_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((bigwin_wave, bigwin_wave))
            sounds['bigwin'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Button click sound
            duration = 0.05
            t = np.linspace(0, duration, int(sample_rate * duration))
            click_wave = np.sin(2 * np.pi * 800 * t) * 0.2 * np.exp(-t * 50)
            click_wave = (click_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((click_wave, click_wave))
            sounds['click'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Coin sound - metallic ping
            duration = 0.15
            t = np.linspace(0, duration, int(sample_rate * duration))
            coin_wave = np.sin(2 * np.pi * 1200 * t) * 0.2 * np.exp(-t * 15)
            coin_wave += np.sin(2 * np.pi * 1800 * t) * 0.1 * np.exp(-t * 20)
            coin_wave = (coin_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((coin_wave, coin_wave))
            sounds['coin'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Multiplier sound - power up
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration))
            mult_wave = np.zeros_like(t)
            for freq in [440, 554, 659]:  # A, C#, E (ascending)
                mult_wave += np.sin(2 * np.pi * freq * t) * 0.12
            mult_wave *= np.exp(-t * 5)
            mult_wave = (mult_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((mult_wave, mult_wave))
            sounds['multiplier'] = pygame.sndarray.make_sound(stereo_wave)
            
            # Bonus trigger sound - fanfare
            duration = 1.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            bonus_wave = np.zeros_like(t)
            # Triumphant fanfare
            for i, freq in enumerate([523, 659, 784, 1047, 1319]):
                segment = (t >= i*0.15) & (t < (i+1)*0.15)
                bonus_wave += np.sin(2 * np.pi * freq * t) * segment * 0.15
            bonus_wave *= np.exp(-t * 2)
            bonus_wave = (bonus_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((bonus_wave, bonus_wave))
            sounds['bonus'] = pygame.sndarray.make_sound(stereo_wave)
            
            print("✓ Sound effects created successfully")
        except Exception as e:
            print(f"⚠ Could not create sounds: {e}")
            print("  Game will run without sound effects")
            # Create silent sounds as fallback
            silent = np.zeros((100, 2), dtype=np.int16)
            for key in ['spin', 'stop', 'win', 'bigwin', 'click', 'coin', 'multiplier', 'bonus']:
                sounds[key] = pygame.sndarray.make_sound(silent)
        
        return sounds
    
    def calculate_layout(self):
        """Calculate reel positions and sizes"""
        # Machine area
        machine_margin = SCREEN_WIDTH * 0.1
        self.machine_width = SCREEN_WIDTH - 2 * machine_margin
        self.machine_height = SCREEN_HEIGHT * 0.58  # Reduced to make more room for buttons
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
        
        # Check if using free spin or regular spin
        if self.free_spins > 0:
            self.free_spins -= 1
            self.free_spins_active = True
            self.message = f"FREE SPIN! {self.free_spins} remaining"
        else:
            if self.coins < self.total_bet:
                self.message = "Not enough coins!"
                return
            self.coins -= self.total_bet
            self.free_spins_active = False
        
        self.spinning = True
        self.winning_lines = []
        self.total_win = 0
        self.scatter_count = 0
        self.bonus_triggered = False
        
        # Play spin sound
        self.sounds['spin'].play()
        
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
        # Update background animation
        self.background_phase = (self.background_phase + 1) % 360
        
        # Update particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.5  # gravity
            particle['life'] -= 1
            particle['size'] = max(1, particle['size'] - 0.1)
        
        # Update win particles
        self.win_particles = [p for p in self.win_particles if p['life'] > 0]
        for particle in self.win_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['alpha'] = int((particle['life'] / particle['max_life']) * 255)
        
        if not self.spinning:
            if self.win_animation_timer > 0:
                self.win_animation_timer -= 1
                self.win_flash = (self.win_flash + 1) % 20
                
                # Create win particles
                if self.win_animation_timer % 3 == 0 and len(self.winning_lines) > 0:
                    for win_info in self.winning_lines:
                        line = win_info['line']
                        reel = random.randint(0, win_info['count'] - 1)
                        x, y = self.reel_positions[reel]
                        row = line[reel]
                        px = x + self.reel_width // 2
                        py = y + row * self.symbol_height + self.symbol_height // 2
                        
                        for _ in range(2):
                            self.create_win_particle(px, py)
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
                    self.reels[i].pop(0)
                    self.reels[i].append(random.choices(symbols, weights=symbol_weights, k=1)[0])
                
                # Check if should stop
                if self.spin_time >= self.reel_stop_time[i]:
                    self.reel_speed[i] = max(5, self.reel_speed[i] - 3)
                    
                    if self.reel_speed[i] <= 5 and self.reel_offset[i] < 5:
                        self.reel_spinning[i] = False
                        self.reel_offset[i] = 0
                        # Set final symbols
                        for row in range(ROWS):
                            self.reels[i][row] = self.reels[i][row]
                        
                        # Play stop sound
                        self.sounds['stop'].play()
                        
                        # Create particles when reel stops
                        x, y = self.reel_positions[i]
                        for _ in range(10):
                            self.create_particle(x + self.reel_width // 2, y + self.reel_height // 2)
        
        if all_stopped:
            self.spinning = False
            self.check_wins()
    
    def check_wins(self):
        """Check for winning lines"""
        self.winning_lines = []
        self.total_win = 0
        
        # Count scatter symbols (🎁) anywhere on the reels
        self.scatter_count = 0
        for reel in range(REELS):
            for row in range(ROWS):
                if self.reels[reel][row] == "🎁":
                    self.scatter_count += 1
        
        # Check regular win lines
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
        
        # Check for scatter bonus (3+ scatter symbols triggers free spins)
        if self.scatter_count >= 3:
            self.bonus_triggered = True
            bonus_spins = 5 + (self.scatter_count - 3) * 2  # 5 spins for 3 scatters, +2 for each extra
            self.free_spins += bonus_spins
            scatter_win = symbol_rewards["🎁"] * self.scatter_count * self.bet_per_line
            self.total_win += scatter_win
            self.bonus_animation_timer = 120
            # Play bonus sound
            self.sounds['bonus'].play()
        
        if self.total_win > 0:
            # Increase win streak and multiplier
            old_multiplier = self.multiplier
            self.win_streak += 1
            self.max_streak = max(self.max_streak, self.win_streak)
            
            # Calculate multiplier based on streak (caps at 10x)
            if self.win_streak >= 10:
                self.multiplier = 10
            elif self.win_streak >= 7:
                self.multiplier = 5
            elif self.win_streak >= 5:
                self.multiplier = 3
            elif self.win_streak >= 3:
                self.multiplier = 2
            else:
                self.multiplier = 1
            
            # Play multiplier sound when it increases
            if self.multiplier > old_multiplier:
                self.sounds['multiplier'].play()
            
            # Apply multiplier to win (extra bonus during free spins)
            bonus_multiplier = 2 if self.free_spins_active else 1
            final_multiplier = self.multiplier * bonus_multiplier
            final_win = int(self.total_win * final_multiplier)
            
            self.coins += final_win
            
            # Create message
            if self.bonus_triggered:
                self.message = f"🎁 BONUS! {bonus_spins} FREE SPINS! Won {final_win} coins!"
            elif final_multiplier > 1:
                self.message = f"WIN! {final_win} coins ({self.total_win} x{final_multiplier}) - STREAK {self.win_streak}!"
            else:
                self.message = f"WIN! {final_win} coins on {len(self.winning_lines)} line(s)!"
            
            self.win_animation_timer = 180
            self.win_flash = 0
            
            # Play appropriate win sound
            if self.bonus_triggered:
                self.sounds['bigwin'].play()
            elif final_win >= 100 or final_multiplier >= 3:
                self.sounds['bigwin'].play()
            else:
                self.sounds['win'].play()
            
            # Play coin sound
            self.sounds['coin'].play()
            
            # Create celebration particles (more for bigger multipliers)
            particle_count = 50 + (final_multiplier * 10)
            for _ in range(int(particle_count)):
                x = random.randint(int(self.machine_x), int(self.machine_x + self.machine_width))
                y = random.randint(int(self.machine_y), int(self.machine_y + self.machine_height))
                self.create_particle(x, y)
        else:
            # Reset streak on loss
            self.win_streak = 0
            self.multiplier = 1
            self.message = "No win. Try again!"
        
        self.spin_button.enabled = True
    
    def create_particle(self, x, y):
        """Create a celebration particle"""
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-8, 8),
            'vy': random.uniform(-15, -5),
            'life': random.randint(30, 60),
            'size': random.uniform(3, 8),
            'color': random.choice([GOLD, NEON_PINK, NEON_GREEN, NEON_BLUE, CYAN, ORANGE, NEON_YELLOW, MAGENTA])
        }
        self.particles.append(particle)
    
    def create_win_particle(self, x, y):
        """Create a win line particle"""
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(2, 6)
        particle = {
            'x': x,
            'y': y,
            'vx': speed * random.uniform(-1, 1),
            'vy': speed * random.uniform(-1, 1),
            'life': random.randint(20, 40),
            'max_life': 40,
            'size': random.uniform(4, 10),
            'color': random.choice([GOLD, NEON_YELLOW, ORANGE, WHITE, ELECTRIC_BLUE]),
            'alpha': 255
        }
        self.win_particles.append(particle)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.screen_state == "bet_config":
                        # Go back to main screen
                        self.start_transition("main")
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE and not self.spinning and self.screen_state == "main":
                    self.start_spin()
            
            if self.exit_button.handle_event(event):
                self.sounds['click'].play()
                self.running = False
            
            # Bet config toggle button (only visible on main screen)
            if self.screen_state == "main" and not self.transitioning:
                if self.bet_config_button.handle_event(event):
                    self.sounds['click'].play()
                    self.start_transition("bet_config")
            
            # Back button (only visible on bet config screen)
            if self.screen_state == "bet_config" and not self.transitioning:
                if self.back_button.handle_event(event):
                    self.sounds['click'].play()
                    self.start_transition("main")
            
            if self.screen_state == "main":
                if self.spin_button.handle_event(event) and not self.spinning:
                    self.start_spin()
            
            if not self.spinning and self.screen_state == "bet_config":
                # Line controls
                if self.lines_up.handle_event(event):
                    self.sounds['click'].play()
                    self.lines = min(9, self.lines + 1)
                if self.lines_down.handle_event(event):
                    self.sounds['click'].play()
                    self.lines = max(1, self.lines - 1)
                
                # Basic bet controls
                if self.bet_up.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = min(self.max_bet, self.bet_per_line + 1)
                if self.bet_down.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = max(self.min_bet, self.bet_per_line - 1)
                
                # Quick bet controls
                if self.bet_min.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = self.min_bet
                if self.bet_max.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = self.max_bet
                if self.bet_half.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = max(self.min_bet, self.bet_per_line // 2)
                if self.bet_double.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = min(self.max_bet, self.bet_per_line * 2)
                
                # Preset bet buttons
                if self.preset_bet_1.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 1
                if self.preset_bet_5.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 5
                if self.preset_bet_10.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 10
                if self.preset_bet_25.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 25
                if self.preset_bet_50.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 50
                if self.preset_bet_100.handle_event(event):
                    self.sounds['click'].play()
                    self.bet_per_line = 100
    
    def start_transition(self, target_screen):
        """Start screen transition animation"""
        self.transitioning = True
        self.transition_target = target_screen
        self.transition_progress = 0
    
    def update_transition(self):
        """Update transition animation"""
        if not self.transitioning:
            return
        
        # Smooth easing function
        self.transition_progress += 0.08  # Speed of transition
        
        if self.transition_progress >= 1.0:
            self.transition_progress = 1.0
            self.transitioning = False
            self.screen_state = self.transition_target
    
    def draw(self):
        import math
        
        # Animated background gradient
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            phase = self.background_phase / 360.0
            
            r = int(20 + 40 * math.sin(progress * 3.14159 + phase * 2) + 20)
            g = int(25 + 35 * math.sin(progress * 3.14159 + phase * 2 + 2) + 15)
            b = int(35 + 45 * math.sin(progress * 3.14159 + phase * 2 + 4) + 25)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Choose which screen to draw based on state
        if self.screen_state == "main":
            self.draw_main_screen()
        elif self.screen_state == "bet_config":
            self.draw_bet_config_screen()
        
        # Draw transition overlay if transitioning
        if self.transitioning:
            self.draw_transition()
        
        pygame.display.flip()
    
    def draw_main_screen(self):
        """Draw the main game screen"""
        import math
        
        # Title with glow effect
        title_text = "PYSLOT CASINO 🎰"
        title_surf = self.title_font.render(title_text, True, NEON_YELLOW)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.05))
        
        # Glowing title
        title_glow = self.title_font.render(title_text, True, GOLD)
        for offset in [(4, 4), (-4, 4), (4, -4), (-4, -4), (0, 4), (4, 0), (0, -4), (-4, 0)]:
            self.screen.blit(title_glow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        self.screen.blit(title_surf, title_rect)
        
        # Coins display with animated glow
        brightness = int(255 * (0.8 + 0.2 * math.sin(self.background_phase / 10)))
        coin_color = (255, 215, brightness) 
        coins_text = f"Coins: ${self.coins}"
        coins_surf = self.text_font.render(coins_text, True, coin_color)
        self.screen.blit(coins_surf, (SCREEN_WIDTH * 0.02, SCREEN_HEIGHT * 0.12))
        
        # Bet display
        bet_text = f"Total Bet: ${self.bet_per_line * self.lines}"
        bet_surf = self.text_font.render(bet_text, True, NEON_PINK)
        self.screen.blit(bet_surf, (SCREEN_WIDTH * 0.02, SCREEN_HEIGHT * 0.16))
        
        # Multiplier display (when active)
        if self.multiplier > 1:
            mult_text = f"🔥 {self.multiplier}x MULTIPLIER! 🔥"
            mult_surf = self.text_font.render(mult_text, True, NEON_ORANGE)
            mult_glow = self.text_font.render(mult_text, True, ORANGE)
            mult_rect = mult_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.12))
            
            # Glow effect
            for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
                self.screen.blit(mult_glow, (mult_rect.x + offset[0], mult_rect.y + offset[1]))
            self.screen.blit(mult_surf, mult_rect)
        
        # Free spins display
        if self.free_spins > 0:
            free_text = f"🌟 FREE SPINS: {self.free_spins} 🌟"
            free_surf = self.text_font.render(free_text, True, NEON_YELLOW)
            free_glow = self.text_font.render(free_text, True, GOLD)
            free_rect = free_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.16))
            
            # Glow effect
            for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
                self.screen.blit(free_glow, (free_rect.x + offset[0], free_rect.y + offset[1]))
            self.screen.blit(free_surf, free_rect)
        
        # Draw machine frame
        machine_rect = pygame.Rect(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.22, SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.42)
        
        # Machine gradient background
        for i in range(int(machine_rect.height)):
            progress = i / machine_rect.height
            brightness = int(50 + 30 * math.sin(progress * 3.14159))
            pygame.draw.rect(self.screen, (brightness, brightness, brightness + 20),
                           pygame.Rect(machine_rect.x, machine_rect.y + i, machine_rect.width, 1))
        
        # Rainbow border
        for i, color in enumerate([GOLD, ORANGE, NEON_YELLOW, NEON_GREEN]):
            pygame.draw.rect(self.screen, color, machine_rect.inflate(i*4, i*4), 3, border_radius=15 + i*2)
        
        # Draw reels
        self.draw_reels()
        
        # Draw particles
        for particle in self.particles:
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            alpha = int((particle['life'] / 60) * 255)
            pygame.draw.circle(particle_surface, (*particle['color'], alpha), 
                             (int(particle['size']), int(particle['size'])), int(particle['size']))
            self.screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
        
        # Draw win lines
        if self.winning_lines and self.win_animation_timer > 0:
            self.draw_win_lines()
        
        # Draw bonus trigger animation
        if self.bonus_animation_timer > 0:
            self.draw_bonus_animation()
            self.bonus_animation_timer -= 1
        
        # Message with rainbow effect for wins
        msg_bg = pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.74, SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.055)
        
        # Gradient background for message
        if self.total_win > 0 and self.win_animation_timer > 0:
            # Animated gradient for win message
            for i in range(int(msg_bg.height)):
                progress = i / msg_bg.height
                phase = (self.win_flash / 10)
                r = int(100 + 80 * math.sin(progress * 6.28 + phase))
                g = int(50 + 50 * math.sin(progress * 6.28 + phase + 2))
                b = int(0)
                line_rect = pygame.Rect(msg_bg.x, msg_bg.y + i, msg_bg.width, 1)
                pygame.draw.rect(self.screen, (r, g, b), line_rect)
            
            # Glowing border
            for i in range(5):
                border_color = [NEON_YELLOW, GOLD, NEON_ORANGE, ORANGE][i % 4]
                pygame.draw.rect(self.screen, border_color, msg_bg.inflate(i*2, i*2), 2, border_radius=10 + i)
            
            # Pulsing text
            scale = 1.0 + 0.1 * math.sin(self.win_flash / 3)
            msg_color = NEON_YELLOW if self.win_flash % 10 < 5 else GOLD
        else:
            pygame.draw.rect(self.screen, (20, 20, 30), msg_bg, border_radius=10)
            pygame.draw.rect(self.screen, BLUE, msg_bg, 3, border_radius=10)
            msg_color = WHITE
        
        msg_text = self.text_font.render(self.message, True, msg_color)
        msg_rect = msg_text.get_rect(center=msg_bg.center)
        
        # Add glow to win messages
        if self.total_win > 0 and self.win_animation_timer > 0:
            msg_glow = self.text_font.render(self.message, True, ORANGE)
            for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3), (0, 3), (3, 0), (0, -3), (-3, 0)]:
                self.screen.blit(msg_glow, (msg_rect.x + offset[0], msg_rect.y + offset[1]))
        
        self.screen.blit(msg_text, msg_rect)
        
        # Buttons
        self.spin_button.draw(self.screen, self.button_font)
        
        # Lines controls
        lines_label = self.small_font.render(f"Lines: {self.lines}", True, WHITE)
        lines_x = self.lines_down.rect.centerx + (self.lines_up.rect.centerx - self.lines_down.rect.centerx) // 2
        self.screen.blit(lines_label, (lines_x - lines_label.get_width() // 2, self.lines_down.rect.y - 30))
        self.lines_down.draw(self.screen, self.button_font)
        self.lines_up.draw(self.screen, self.button_font)
        
        # Bet configuration arrow button
        self.bet_config_button.draw(self.screen, self.button_font)
        
        # Exit button
        self.exit_button.draw(self.screen, self.button_font)
        
        # Instructions
        inst_text = self.small_font.render("SPACE to spin | ► for bet config | ESC to exit", True, LIGHT_GRAY)
        self.screen.blit(inst_text, (20, SCREEN_HEIGHT - 30))
    
    def draw_bet_config_screen(self):
        """Draw the bet configuration screen"""
        import math
        
        # Title
        title_text = "⚙️ BET CONFIGURATION ⚙️"
        title_surf = self.title_font.render(title_text, True, NEON_YELLOW)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.1))
        
        # Glowing title
        title_glow = self.title_font.render(title_text, True, GOLD)
        for offset in [(4, 4), (-4, 4), (4, -4), (-4, -4)]:
            self.screen.blit(title_glow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        self.screen.blit(title_surf, title_rect)
        
        # Back button
        self.back_button.draw(self.screen, self.button_font)
        
        # Current bet display (large)
        current_bet_text = f"Current Bet Per Line: ${self.bet_per_line}"
        current_bet_surf = self.text_font.render(current_bet_text, True, NEON_PINK)
        current_bet_rect = current_bet_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.2))
        
        # Glowing current bet
        bet_glow = self.text_font.render(current_bet_text, True, MAGENTA)
        for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
            self.screen.blit(bet_glow, (current_bet_rect.x + offset[0], current_bet_rect.y + offset[1]))
        self.screen.blit(current_bet_surf, current_bet_rect)
        
        # Total bet preview
        total_text = f"Total Bet: ${self.bet_per_line * self.lines} ({self.lines} lines)"
        total_surf = self.text_font.render(total_text, True, NEON_GREEN)
        total_rect = total_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.26))
        self.screen.blit(total_surf, total_rect)
        
        # Basic bet controls (larger, centered)
        bet_label = self.small_font.render(f"Bet: {self.bet_per_line}", True, WHITE)
        bet_x = self.bet_down.rect.centerx + (self.bet_up.rect.centerx - self.bet_down.rect.centerx) // 2
        self.screen.blit(bet_label, (bet_x - bet_label.get_width() // 2, self.bet_down.rect.y - 30))
        self.bet_down.draw(self.screen, self.button_font)
        self.bet_up.draw(self.screen, self.button_font)
        
        # Quick bet controls (with more space)
        quick_label = self.small_font.render("Quick Bet Controls:", True, NEON_YELLOW)
        quick_label_rect = quick_label.get_rect(center=(SCREEN_WIDTH // 2, self.bet_min.rect.y - 35))
        self.screen.blit(quick_label, quick_label_rect)
        
        self.bet_min.draw(self.screen, self.small_font)
        self.bet_half.draw(self.screen, self.small_font)
        self.bet_double.draw(self.screen, self.small_font)
        self.bet_max.draw(self.screen, self.small_font)
        
        # Preset bet buttons (nicely spaced)
        preset_label = self.small_font.render("Preset Bet Amounts:", True, NEON_GREEN)
        preset_label_rect = preset_label.get_rect(center=(SCREEN_WIDTH // 2, self.preset_bet_1.rect.y - 35))
        self.screen.blit(preset_label, preset_label_rect)
        
        self.preset_bet_1.draw(self.screen, self.small_font)
        self.preset_bet_5.draw(self.screen, self.small_font)
        self.preset_bet_10.draw(self.screen, self.small_font)
        self.preset_bet_25.draw(self.screen, self.small_font)
        self.preset_bet_50.draw(self.screen, self.small_font)
        self.preset_bet_100.draw(self.screen, self.small_font)
        
        # Instructions
        inst_text = self.small_font.render("Configure your bet | Press ◄ or ESC to return to game", True, LIGHT_GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_transition(self):
        """Draw transition overlay effect"""
        import math
        
        # Calculate transition progress
        t = self.transition_progress
        eased_progress = t * t * (3.0 - 2.0 * t)  # Smoothstep
        
        # Fade overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = int(100 * math.sin(eased_progress * 3.14159))
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))
    
    def draw_reels(self):
        """Draw all reels with symbols"""
        import math
        for reel_idx in range(REELS):
            x, y = self.reel_positions[reel_idx]
            
            # Reel background with gradient
            reel_rect = pygame.Rect(x, y, self.reel_width, self.reel_height)
            
            # Draw gradient for reel
            for i in range(int(self.reel_height)):
                progress = i / self.reel_height
                brightness = int(230 + 25 * math.sin(progress * 3.14159))
                blue_brightness = min(255, brightness + 15)
                pygame.draw.rect(self.screen, (brightness, brightness, blue_brightness), 
                               pygame.Rect(x, y + i, self.reel_width, 1))
            
            # Colorful border with glow
            if self.reel_spinning[reel_idx]:
                # Spinning reel gets animated rainbow border
                color_phase = (self.background_phase + reel_idx * 60) % 360
                border_colors = [
                    NEON_BLUE if color_phase < 120 else NEON_GREEN if color_phase < 240 else NEON_PINK,
                    CYAN,
                    BLUE
                ]
            else:
                border_colors = [GOLD, ORANGE, DARK_GRAY]
            
            for i, color in enumerate(border_colors):
                pygame.draw.rect(self.screen, color, reel_rect.inflate(i*2, i*2), 2, border_radius=10 + i)
            
            # Clip to reel area
            clip_rect = pygame.Rect(x + 5, y + 5, self.reel_width - 10, self.reel_height - 10)
            self.screen.set_clip(clip_rect)
            
            # Draw symbols
            for row in range(ROWS + 2):
                symbol_y = y + row * self.symbol_height - self.reel_offset[reel_idx]
                
                if self.reel_spinning[reel_idx]:
                    symbol = self.reels[reel_idx][row % len(self.reels[reel_idx])]
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
        """Draw animated rainbow win lines with particles"""
        import math
        
        # Pulsing alpha animation
        pulse = math.sin(self.win_flash / 3) * 0.3 + 0.7
        alpha = int(220 * pulse)
        
        line_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Rainbow colors that cycle
        rainbow_colors = [
            NEON_PINK, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, 
            NEON_BLUE, ELECTRIC_BLUE, PURPLE, MAGENTA, HOT_PINK
        ]
        
        for idx, win_info in enumerate(self.winning_lines):
            line = win_info['line']
            line_idx = win_info['line_idx']
            match_count = win_info['count']
            
            # Cycle through rainbow colors with animation
            color_idx = (line_idx + self.win_flash // 4) % len(rainbow_colors)
            color = rainbow_colors[color_idx]
            
            # Calculate line path
            points = []
            for reel in range(match_count):
                x, y = self.reel_positions[reel]
                row = line[reel]
                point_x = x + self.reel_width // 2
                point_y = y + row * self.symbol_height + self.symbol_height // 2
                
                # Add wave effect to points
                wave_offset = math.sin(self.win_flash / 5 + reel * 0.5) * 5
                points.append((point_x, point_y + wave_offset))
            
            if len(points) >= 2:
                # Draw multiple gradient layers for glow effect
                for layer in range(5, 0, -1):
                    layer_alpha = alpha // (6 - layer)
                    layer_width = 4 + layer * 4
                    
                    # Alternate colors for rainbow effect
                    layer_color_idx = (color_idx + layer) % len(rainbow_colors)
                    layer_color = rainbow_colors[layer_color_idx]
                    color_with_alpha = (*layer_color, layer_alpha)
                    
                    pygame.draw.lines(line_surface, color_with_alpha, False, points, layer_width)
                
                # Draw glowing circles at connection points
                for i, point in enumerate(points):
                    # Outer glow
                    for radius in range(25, 5, -4):
                        circle_alpha = alpha // (26 - radius) * 2
                        glow_color_idx = (color_idx + radius // 5) % len(rainbow_colors)
                        glow_color = rainbow_colors[glow_color_idx]
                        circle_color = (*glow_color, min(255, circle_alpha))
                        pygame.draw.circle(line_surface, circle_color, (int(point[0]), int(point[1])), radius)
                    
                    # Bright center
                    pygame.draw.circle(line_surface, (255, 255, 255, alpha), (int(point[0]), int(point[1])), 6)
                    
                    # Sparkle effect
                    if self.win_flash % 8 < 4:
                        sparkle_size = 15 + int(5 * math.sin(self.win_flash / 2))
                        pygame.draw.circle(line_surface, (*NEON_YELLOW, alpha), (int(point[0]), int(point[1])), sparkle_size, 2)
        
        self.screen.blit(line_surface, (0, 0))
        
        # Draw win particles
        for particle in self.win_particles:
            particle_surface = pygame.Surface((int(particle['size']*2), int(particle['size']*2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], particle['alpha']), 
                             (int(particle['size']), int(particle['size'])), int(particle['size']))
            self.screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
    
    def draw_bonus_animation(self):
        """Draw bonus trigger celebration overlay"""
        import math
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Pulsing background
        alpha = int(100 + 50 * math.sin(self.bonus_animation_timer / 5))
        overlay.fill((0, 0, 0, alpha))
        
        # Big "BONUS!" text
        progress = (120 - self.bonus_animation_timer) / 120
        if progress < 0.5:
            # Zoom in
            scale = progress * 2
        else:
            # Slight bounce
            scale = 1.0 + 0.1 * math.sin((progress - 0.5) * 10)
        
        bonus_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.15 * scale))
        
        # Rainbow color cycling
        color_phase = (self.bonus_animation_timer * 10) % 360
        if color_phase < 60:
            text_color = NEON_PINK
        elif color_phase < 120:
            text_color = NEON_ORANGE
        elif color_phase < 180:
            text_color = NEON_YELLOW
        elif color_phase < 240:
            text_color = NEON_GREEN
        elif color_phase < 300:
            text_color = NEON_BLUE
        else:
            text_color = MAGENTA
        
        # Draw "BONUS!" with glow
        bonus_text = "🎁 BONUS! 🎁"
        for offset in range(10, 0, -2):
            glow_alpha = int(150 * (offset / 10))
            glow_color = (*text_color, glow_alpha)
            glow_surf = bonus_font.render(bonus_text, True, text_color)
            glow_surf.set_alpha(glow_alpha)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            overlay.blit(glow_surf, (glow_rect.x + offset, glow_rect.y + offset))
        
        main_text = bonus_font.render(bonus_text, True, WHITE)
        main_rect = main_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        overlay.blit(main_text, main_rect)
        
        # Free spins count
        fs_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.08))
        bonus_spins = 5 + (self.scatter_count - 3) * 2
        fs_text = fs_font.render(f"{bonus_spins} FREE SPINS!", True, NEON_YELLOW)
        fs_rect = fs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        overlay.blit(fs_text, fs_rect)
        
        # Scatter count
        scatter_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
        scatter_text = scatter_font.render(f"({self.scatter_count} Scatters!)", True, NEON_GREEN)
        scatter_rect = scatter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        overlay.blit(scatter_text, scatter_rect)
        
        # Fireworks particles
        if self.bonus_animation_timer % 5 == 0:
            for _ in range(5):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                self.create_particle(x, y)
        
        self.screen.blit(overlay, (0, 0))
    
    def run(self):
        print("=" * 60)
        print("PySlot - Professional Casino Slot Machine")
        print("=" * 60)
        print("✓ Game started in fullscreen mode")
        print("=" * 60)
        
        while self.running:
            self.handle_events()
            self.update_spin_animation()
            self.update_transition()  # Update screen transitions
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SlotMachineGame()
    game.run()
