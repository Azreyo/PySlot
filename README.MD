# 🎰 Slot Machine Game - Pygame Edition

A colorful slot machine game with emoji support! Works on **Windows 11**, **Linux**, and **macOS**.

## ✨ Features

- 🎨 Beautiful graphics with smooth animations
- 🎰 6 different slot symbols (🍒, 🍋, 🍉, ⭐, 💎, 7)
- 💰 Multiplier system to increase winnings
- 🖱️ Interactive buttons with hover effects
- 🎮 60 FPS smooth gameplay
- 🌈 Cross-platform emoji support

## 📋 Requirements

- Python 3.6 or higher
- Pygame library

## 🚀 Installation & Running

### On Windows 11:

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Or install from Microsoft Store: `winget install Python.Python.3.12`

2. **Install Pygame**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python slotmachine_pygame.py
   ```

**Note**: Windows 11 has excellent emoji support out-of-the-box with the "Segoe UI Emoji" font!

### On Linux (Pop!OS / Ubuntu):

1. **Install Python** (usually pre-installed):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install Pygame**:
   ```bash
   pip3 install pygame
   ```

3. **Install emoji fonts** (for better emoji display):
   ```bash
   sudo apt install fonts-noto-color-emoji
   fc-cache -f -v
   ```

4. **Run the game**:
   ```bash
   python3 slotmachine_pygame.py
   ```

### On macOS:

1. **Install Python**:
   ```bash
   brew install python3
   ```

2. **Install Pygame**:
   ```bash
   pip3 install pygame
   ```

3. **Run the game**:
   ```bash
   python3 slotmachine_pygame.py
   ```

## 🎮 How to Play

1. **Start with 500 coins**
2. **Click "SPIN"** - Costs 10 coins per spin
3. **Match 3 symbols** to win:
   - 🍒 Cherry = 20 coins
   - 🍋 Lemon = 40 coins
   - 🍉 Melon = 60 coins
   - ⭐ Star = 80 coins
   - 💎 Diamond = 120 coins
   - 7️⃣ Seven = 200 coins (JACKPOT = 400!)

4. **After winning**:
   - Click "Try Multiplier" to double your winnings (risky!)
   - Click "Take Winnings" to secure your coins

5. **Multiplier Round**:
   - Match 2 symbols to continue doubling
   - Fail and lose all pending winnings!

## 🆚 Tkinter vs Pygame

| Feature | Tkinter | Pygame |
|---------|---------|--------|
| **Emoji on Windows** | ⚠️ Sometimes works | ✅ Perfect |
| **Emoji on Linux** | ❌ Poor | ✅ Good |
| **Animation** | Basic | Smooth (60 FPS) |
| **Graphics** | Simple | Modern |
| **Performance** | Moderate | Excellent |
| **File Size** | `slotmachine.py` | `slotmachine_pygame.py` |

## 🐛 Troubleshooting

### Emojis show as boxes □:

**Windows**: Make sure you're running Windows 10 1803+ or Windows 11
```bash
# Check Windows version
winver
```

**Linux**: Install emoji fonts
```bash
sudo apt install fonts-noto-color-emoji fonts-symbola
fc-cache -fv
```

### "No module named 'pygame'":
```bash
pip install pygame
# or on Linux:
pip3 install pygame
```

### Game window doesn't appear:
- Check if pygame is properly installed: `python -c "import pygame; print(pygame.version.ver)"`
- Make sure you have a display (not running in SSH without X11)

## 📝 Files

- `slotmachine_pygame.py` - Pygame version (recommended, best emoji support)
- `slotmachine.py` - Tkinter version (simpler, but poor emoji support on Linux)
- `slotmachine.py.bak` - Backup of original tkinter version

## 🎯 Why Pygame is Better for Emojis

**Tkinter Issues**:
- Uses older Tk rendering engine
- Limited Unicode/emoji font support on Linux
- Can't easily load custom font files

**Pygame Advantages**:
- Uses SDL_ttf for modern font rendering
- Direct access to system emoji fonts
- Better cross-platform compatibility
- Smoother graphics and animations

## 💡 Tips

- On Windows 11, emojis will display perfectly with no extra setup!
- On Linux, emojis should work well with the Noto Color Emoji font
- The game auto-detects your OS and loads the best available emoji font
- If emojis don't show, check the console for font loading messages

## 📄 License

Free to use and modify!

---

**Enjoy the game! 🎰🎲💰**
