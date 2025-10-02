# PySlot - Slot Machine Game

A cross-platform slot machine game built with Python and Pygame, featuring rich emoji graphics and smooth animations.

## Features

- **Modern Graphics**: Smooth 60 FPS gameplay with polished UI elements
- **Six Unique Symbols**: Cherry (🍒), Lemon (🍋), Melon (🍉), Star (⭐), Diamond (💎), and Lucky Seven (7️⃣)
- **Multiplier System**: Risk your winnings for a chance to double them
- **Interactive UI**: Responsive buttons with hover effects and visual feedback
- **Cross-Platform**: Full support for Windows, Linux, and macOS
- **Emoji Support**: Native emoji rendering with fallback font handling

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

### Windows

1. **Install Python**:
   ```bash
   # Download from python.org or use Windows Package Manager
   winget install Python.Python.3.12
   ```

2. **Install Pygame**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python slotmachine_pygame.py
   ```

> **Note**: Windows 11 includes excellent emoji support via the Segoe UI Emoji font.

### Linux (Ubuntu/Debian)

1. **Install Python and pip**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install Pygame**:
   ```bash
   pip3 install pygame
   ```

3. **Install emoji font support**:
   ```bash
   sudo apt install fonts-noto-color-emoji
   fc-cache -f -v
   ```

4. **Run the game**:
   ```bash
   python3 slotmachine_pygame.py
   ```

### macOS

1. **Install Python** (requires Homebrew):
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

## How to Play

### Basic Gameplay

1. You start with **500 coins**
2. Click **SPIN** to play (costs 10 coins per spin)
3. Match 3 identical symbols to win

### Payout Table

| Symbol | Name | Standard Win | Jackpot Win |
|--------|------|--------------|-------------|
| 🍒 | Cherry | 20 coins | - |
| 🍋 | Lemon | 40 coins | - |
| 🍉 | Melon | 60 coins | - |
| ⭐ | Star | 80 coins | - |
| 💎 | Diamond | 120 coins | - |
| 7️⃣ | Seven | 200 coins | 400 coins |

### Multiplier Round

After a winning spin, you can:
- **Try Multiplier**: Risk your winnings for a chance to double them
- **Take Winnings**: Secure your coins and return to the main game

During the multiplier round:
- Match 2 symbols to double your winnings and continue
- Fail to match and lose all pending winnings

## Technical Comparison

### Tkinter vs Pygame Implementation

| Feature | Tkinter Version | Pygame Version |
|---------|----------------|----------------|
| **Windows Emoji Support** | Inconsistent | Excellent |
| **Linux Emoji Support** | Poor | Good |
| **Animation Quality** | Basic | Smooth (60 FPS) |
| **Graphics Rendering** | Simple | Modern |
| **Performance** | Moderate | Excellent |
| **File** | `slotmachine.py` | `slotmachine_pygame.py` |

### Why Pygame is Recommended

**Tkinter Limitations**:
- Relies on older Tk rendering engine
- Limited Unicode and emoji font support on Linux
- Restricted custom font file loading capabilities

**Pygame Advantages**:
- Utilizes SDL_ttf for modern font rendering
- Direct access to system-level emoji fonts
- Superior cross-platform compatibility
- Enhanced graphics performance and smoother animations

## Troubleshooting

### Emojis Display as Boxes

**Windows**:
Ensure you're running Windows 10 version 1803 or later, or Windows 11:
```bash
winver
```

**Linux**:
Install emoji font packages:
```bash
sudo apt install fonts-noto-color-emoji fonts-symbola
fc-cache -fv
```

### Module Import Error

If you encounter `ModuleNotFoundError: No module named 'pygame'`:
```bash
# Windows
pip install pygame

# Linux/macOS
pip3 install pygame
```

### Game Window Not Appearing

- Verify Pygame installation:
  ```bash
  python -c "import pygame; print(pygame.version.ver)"
  ```
- Ensure you have a display environment (not running over SSH without X11 forwarding)
- Check for error messages in the console output

## Project Structure

```
PySlot/
├── slotmachine_pygame.py    # Pygame version (recommended)
├── slotmachine.py           # Tkinter version (legacy)
├── slotmachine.py.bak       # Backup of original implementation
└── README.md                # Documentation
```

## Implementation Notes

### Font Rendering

The game automatically detects your operating system and loads the appropriate emoji font:
- **Windows**: Segoe UI Emoji (native support)
- **Linux**: Noto Color Emoji (requires installation)
- **macOS**: Apple Color Emoji (native support)

Font loading messages are displayed in the console for debugging purposes.

### Performance

The Pygame version runs at a locked 60 FPS, providing smooth animations and responsive user input handling.

## License

This project is free to use and modify for personal and commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**PySlot** - A modern slot machine game experience built with Python.
