<div align="center">

### A Modern Slot Machine Game

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-00A400?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)](https://github.com)

*A cross-platform slot machine game with rich emoji graphics and smooth 60 FPS animations*

[Features](#features) • [Installation](#installation) • [How to Play](#how-to-play) • [Troubleshooting](#troubleshooting) •

### Platform Support
 🌐 **Cross-platform** support (Windows, Linux, macOS)

🔤 **Native emoji rendering** with automatic font detection

🖱️ **Interactive controls** - keyboard and mouse supportlot

</div>

---

## ✨ Features

- � **5-Reel, 4-Row** professional slot machine layout
- 📊 **9 Win Lines** with animated line indicators
- 💰 **Line-based multipliers** - bet on 1-9 lines
- 🎨 **Fullscreen mode** with smooth 60 FPS animations
- 🌈 **Animated win lines** with color-coded payouts
- � **Six unique symbols** with progressive reel stops
- ⚡ **Sequential reel animation** - reels stop one by one
- 🖱️ **Interactive controls** - adjust lines and bet amounts
- 🌐 **Cross-platform** support (Windows, Linux, macOS)
- � **Native emoji rendering** with automatic font detection

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Azreyo/PySlot.git
cd PySlot

# Install dependencies
pip install pygame numpy

# On Linux, install emoji fonts (recommended)
sudo apt install fonts-noto-color-emoji fonts-symbola

# Run the game (fullscreen)
python3 slotmachine.py
```

> 💡 **Pro Tips**: 
> - Start with 1-2 lines and low bets to learn the game!
> - Build win streaks for multiplier bonuses
> - Use the ► arrow to access spacious bet configuration
> - Look for scatter symbols (🌟) to trigger free spins!

<details>
<summary><b>Platform-Specific Instructions</b></summary>

### Windows
```bash
pip install pygame
python slotmachine.py
```

### Linux (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip fonts-noto fonts-dejavu
pip3 install pygame

# Run
python3 slotmachine.py
```

> **Note**: Pygame doesn't support color emoji fonts. The game uses Noto Sans or DejaVu Sans which provide basic emoji rendering on Linux.

### macOS
```bash
brew install python3
pip3 install pygame
python3 slotmachine.py
```

</details>

## 🎮 How to Play

### Basic Controls

- **SPIN Button** or **SPACE**: Start the spin
- **► Arrow Button** (left side): Open bet configuration screen
- **Lines +/- Buttons**: Adjust active lines (1-9)
- **X Button** or **ESC**: Exit game or return from bet config
- **Total Bet**: Bet per line × Number of lines

### 💳 Bet Configuration Screen

Click the **► arrow button** on the left side to access the spacious bet configuration screen:

- **Basic Controls**: Fine-tune bet with +/- buttons (1-100 coins)
- **Quick Controls**: 
  - **MIN**: Set to minimum bet (1 coin)
  - **÷2**: Halve current bet
  - **×2**: Double current bet
  - **MAX**: Set to maximum bet (100 coins)
- **Preset Buttons**: Instantly set bet to 1, 5, 10, 25, 50, or 100 coins
- **◄ BACK**: Return to main game with smooth animation

### 🔥 Multiplier System

Build win streaks to increase your multiplier:
- **3 wins in a row**: 2x multiplier
- **5 wins in a row**: 3x multiplier
- **7 wins in a row**: 5x multiplier
- **10+ wins in a row**: 10x multiplier! 🚀

*Lose a spin and your streak resets*

### 🎁 Free Spins Bonus

Land **3 or more scatter symbols (🌟)** anywhere on the reels to trigger free spins:
- **3 scatters**: 5 free spins
- **4 scatters**: 8 free spins
- **5 scatters**: 11 free spins

During free spins, you don't pay for spins but can still win big!

### 💎 Payout Table

Wins require **3+ matching symbols** in a row from left to right on active paylines:

| Symbol | Name | Base Value | 3 Match | 4 Match | 5 Match |
|:------:|:----:|:----------:|:-------:|:-------:|:-------:|
| 🍒 | Cherry | 5 | 15 | 20 | 25 |
| 🍋 | Lemon | 10 | 30 | 40 | 50 |
| � | Orange | 12 | 36 | 48 | 60 |
| 🍇 | Grapes | 15 | 45 | 60 | 75 |
| �🍉 | Watermelon | 18 | 54 | 72 | 90 |
| 🔔 | Bell | 20 | 60 | 80 | 100 |
| ⭐ | Star | 25 | 75 | 100 | 125 |
| 💰 | Money Bag | 30 | 90 | 120 | 150 |
| 👑 | Crown | 40 | 120 | 160 | 200 |
| 💎 | Diamond | 50 | 150 | 200 | 250 |
| 🎰 | Slot Machine | 75 | 225 | 300 | 375 |
| 7️⃣ | Lucky Seven | 100 | 300 | 400 | **500** |

**Special Symbol:**
- 🌟 **Scatter**: Triggers free spins (3+ anywhere on reels)

*Win amount = Base value × Bet per line × Multiplier*

### 📈 Win Lines

Play up to **9 different win lines** with rainbow-colored animations:

1. **Middle Row** - Straight across the center
2. **Top Row** - Straight across the top
3. **Bottom Row** - Straight across the bottom
4. **V-Shape** - Down from top corners, up at center
5. **Inverted V** - Up from bottom corners, down at center
6. **Diagonal Stairs Down** - Descending from top-left to bottom-right
7. **Diagonal Stairs Up** - Ascending from bottom-left to top-right
8. **Zig-Zag** - Alternating up and down pattern
9. **Zag-Zig** - Alternating down and up pattern

Win lines feature:
- 🌈 **Rainbow colors** - Each line has unique vibrant colors
- ✨ **Pulsing animations** - Winning lines glow and pulse
- 🎆 **Particle effects** - Celebration particles along win lines


## 🔧 Troubleshooting

<details>
<summary><b>Emojis show as rectangles/boxes on Linux</b></summary>

**Why**: Pygame doesn't support color emoji fonts (like Noto Color Emoji). It needs regular fonts with emoji glyph support.

**Solution**: Install compatible fonts
```bash
sudo apt install fonts-noto fonts-dejavu fonts-symbola
fc-cache -fv
```

The game will automatically detect and use the best available font. Check the console output when starting the game to see which font was loaded.
</details>

<details>
<summary><b>ModuleNotFoundError: pygame</b></summary>

```bash
pip install pygame
```
</details>

<details>
<summary><b>Game window doesn't appear</b></summary>

Verify installation:
```bash
python -c "import pygame; print(pygame.version.ver)"
```
</details>

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

<div align="center">

**Made with ❤️ using Python & Pygame**

⭐ Star this repo if you like it!

</div>
