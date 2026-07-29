# 🧮 Calculator (CLI Based → GUI Evolved)

> "This is my first project, made to learn and apply the basics of programming."

A calculator project that started as a simple command-line tool and evolved into a fully animated, Windows-style desktop application — built entirely in Python as a learning journey.

---

## 🚀 Technologies Used

- **Python** — core logic and application structure
- **customtkinter** — modern, rounded, themeable GUI components
- **math** (standard library) — trigonometric and scientific functions

---

## 📌 Project Phases

### Phase 1 — The Beginning (CLI Calculator)
A simple terminal-based calculator to practice fundamentals.

| Function | What it does |
|---|---|
| Addition | Adds two numbers |
| Subtraction | Subtracts two numbers, supports negative/float results |
| Multiplication | Multiplies two numbers |
| Division | Divides two numbers |
| Clear | Clears all the content |

📄 File: `Calulator (CLI Based).py`

---

### Phase 2 — Going Graphical (GUI Calculator)
Rebuilt as a desktop app using `tkinter`, styled after the Windows Calculator — buttons, a display screen, dark theme.

---

### Phase 3 — Modern & Animated
Upgraded to `customtkinter` for a modern rounded UI, then layered in smooth custom animations:

- 🖱️ **Resizable window** — drag to resize like any real desktop app
- ✨ **Button press glow animation** — buttons flash softly when clicked
- 🔤 **Display entry animation** — numbers glow in as you type
- 🎉 **Dramatic "pop" animation on `=`** — a bounce + color shimmer reveal for the result
- 🧪 **Scientific mode** — a hidden panel that *slides open* to reveal trig functions, keeping the home screen clean

---

### Phase 4 — Feature Complete (Current)
Added the core features every standard calculator (like Windows Calculator) needs:

| Feature | Description |
|---|---|
| **⌫ Backspace** | Deletes the last entered character instead of clearing everything |
| **Memory (MC / MR / M+ / M-)** | Store a number, recall it, or add/subtract from it |
| **√ Square Root** | Calculates the square root of the current value |
| **x² Square** | Squares the current value |
| **1/x Reciprocal** | Calculates the reciprocal of the current value |
| **Scientific Functions** | `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `sec`, `csc`, `cot` |
| **Leading-zero fix** | Correctly handles inputs like `100 + 02` without crashing |

---

## 🖥️ How to Run

1. Make sure Python is installed on your system.
2. Install the one required dependency:
   ```bash
   pip install customtkinter
   ```
3. Run the app:
   ```bash
   python calculator_animated_v4.py
   ```

---

## 🗺️ Roadmap / What's Next

- [ ] Calculation history panel (slide-in, same style as the scientific panel)
- [ ] Keyboard input support (type instead of click)
- [ ] Light/Dark mode toggle switch
- [ ] Sound effects on button press
- [ ] Package into a standalone `.exe` with a custom icon

---

## 👤 Author

**8BitKrishna**
First programming project — built step by step while learning Python, GUI development, and animation logic.

---

## 📄 License

This project is open for learning purposes. Feel free to explore, fork, and build on top of it.
