<div align="center">

# 🎰 PySlot

### A Modern Slot Machine Game

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-00A400?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)](https://github.com)

*A cross-platform slot machine game with rich emoji graphics and smooth 60 FPS animations*

[Features](#features) • [Installation](#installation) • [How to Play](#how-to-play) • [Troubleshooting](#troubleshooting) •
[Win Lines](WIN_LINES.md)

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
pip install pygame

# On Linux, install emoji fonts (recommended)
sudo apt install fonts-noto-color-emoji fonts-symbola

# Run the game (fullscreen)
python3 slotmachine.py
```

> 💡 **Pro Tip**: Start with 1-2 lines and low bets to learn the game!

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

- **+ / - Buttons**: Adjust bet per line (1-10 coins) and active lines (1-9)
- **SPIN Button** or **SPACE**: Start the spin
- **X Button** or **ESC**: Exit fullscreen mode
- **Total Bet**: Bet per line × Number of lines

### 💎 Payout Table

Wins require **3+ matching symbols** in a row from left to right:

| Symbol | Base Value | 3 Match | 4 Match | 5 Match |
|:------:|:----------:|:-------:|:-------:|:-------:|
| 🍒 Cherry | 5 | 15 | 20 | 25 |
| 🍋 Lemon | 10 | 30 | 40 | 50 |
| 🍉 Melon | 15 | 45 | 60 | 75 |
| ⭐ Star | 25 | 75 | 100 | 125 |
| 💎 Diamond | 50 | 150 | 200 | 250 |
| 7️⃣ Seven | 100 | 300 | 400 | **500** |

*Win amount = Base value × Bet per line × Number of matches*

### 📈 Win Lines
Direct documentation how to [Win Lines](WIN_LINES.md).

Play up to **9 different win lines**:
1. Middle row (horizontal)
2. Top row (horizontal)
3. Bottom row (horizontal)
4. V-shape
5. Inverted V-shape
6. Diagonal down stairs
7. Diagonal up stairs
8. Zig-zag pattern
9. Zag-zig pattern

Win lines are **color-coded** and **animated** when you win!



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
