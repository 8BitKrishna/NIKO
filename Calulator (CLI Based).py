"""
Calculator App (Animated / Modern UI) - v4 (Windows-style features)
-----------------------------------------------------------------------
New in this version:
  - Backspace (deletes last character instead of clearing everything)
  - Memory functions: MC (clear), MR (recall), M+ (add), M- (subtract)
  - sqrt (square root), square (x squared), reciprocal (1/x)

Install requirement (run once in your terminal):
    pip install customtkinter
"""

import re
import math
import customtkinter as ctk

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FONT_DISPLAY = ("Segoe UI", 44, "bold")
FONT_BTN = ("Segoe UI", 18)
FONT_SMALL_BTN = ("Segoe UI", 14)
FONT_SCI_BTN = ("Segoe UI", 13)

NUM_BTN_COLOR = "#2b2b2b"
NUM_BTN_HOVER = "#3d3d3d"
NUM_BTN_FLASH = "#6e6e6e"

OP_BTN_COLOR = "#ff9500"
OP_BTN_HOVER = "#ffb347"
OP_BTN_FLASH = "#ffe0ad"

CLEAR_BTN_COLOR = "#d64545"
CLEAR_BTN_HOVER = "#e57373"

EQUAL_BTN_COLOR = "#0a84ff"
EQUAL_BTN_HOVER = "#4da3ff"

SCI_BTN_COLOR = "#1f6f5c"
SCI_BTN_HOVER = "#2b9c80"

MEM_BTN_COLOR = "#3a3a52"
MEM_BTN_HOVER = "#4d4d6e"

EXTRA_BTN_COLOR = "#333333"
EXTRA_BTN_HOVER = "#474747"

DISPLAY_DEFAULT_FG = "#ffffff"
DISPLAY_ACCENT = "#5ac8fa"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, int(c))) for c in rgb])


def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))


def ease_out(t):
    return 1 - (1 - t) ** 3


def sanitize_expression(expr):
    return re.sub(r'(?<!\d)0+(?=\d)', '', expr)


def format_number(value):
    """Turns 5.0 into '5' but keeps 5.25 as '5.25' - avoids ugly '.0' everywhere."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 6))


class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("380x760")
        self.minsize(340, 620)
        self.resizable(True, True)

        self.expression = ""
        self.memory = 0.0
        self.sci_open = False
        self.sci_panel_height = 220

        self._display_anim_gen = 0
        self._panel_anim_gen = 0

        self.grid_rowconfigure(0, weight=0)   # display
        self.grid_rowconfigure(1, weight=0)   # memory row
        self.grid_rowconfigure(2, weight=0)   # extra functions row (sqrt, x^2, 1/x, backspace)
        self.grid_rowconfigure(3, weight=1)   # main number grid
        self.grid_rowconfigure(4, weight=0)   # scientific toggle
        self.grid_rowconfigure(5, weight=0)   # scientific panel
        self.grid_columnconfigure(0, weight=1)

        self._build_display()
        self._build_memory_row()
        self._build_extra_row()
        self._build_main_buttons()
        self._build_toggle()
        self._build_sci_panel()

    # ==================================================================
    # DISPLAY
    # ==================================================================
    def _build_display(self):
        self.display_var = ctk.StringVar(value="0")
        self.display = ctk.CTkLabel(
            self, textvariable=self.display_var, font=FONT_DISPLAY,
            anchor="e", text_color=DISPLAY_DEFAULT_FG,
        )
        self.display.grid(row=0, column=0, sticky="nsew", padx=20, pady=(25, 5))

    # ==================================================================
    # MEMORY ROW (MC, MR, M+, M-)
    # ==================================================================
    def _build_memory_row(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 0))
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        mem_buttons = [
            ("MC", 0, self.memory_clear),
            ("MR", 1, self.memory_recall),
            ("M+", 2, self.memory_add),
            ("M-", 3, self.memory_subtract),
        ]
        self.mem_buttons_widgets = []
        for (label, col, action) in mem_buttons:
            b = ctk.CTkButton(
                frame, text=label, font=FONT_SMALL_BTN, fg_color=MEM_BTN_COLOR,
                hover_color=MEM_BTN_HOVER, corner_radius=14, height=32,
                command=action,
            )
            b.grid(row=0, column=col, sticky="ew", padx=4, pady=4)
            self.mem_buttons_widgets.append(b)

    # ==================================================================
    # EXTRA FUNCTIONS ROW (sqrt, square, reciprocal, backspace)
    # ==================================================================
    def _build_extra_row(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 0))
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        extra_buttons = [
            ("√", 0, self.apply_sqrt),
            ("x²", 1, self.apply_square),
            ("1/x", 2, self.apply_reciprocal),
            ("⌫", 3, self.backspace),
        ]
        for (label, col, action) in extra_buttons:
            b = ctk.CTkButton(
                frame, text=label, font=FONT_SMALL_BTN, fg_color=EXTRA_BTN_COLOR,
                hover_color=EXTRA_BTN_HOVER, corner_radius=14, height=32,
                command=action,
            )
            b.grid(row=0, column=col, sticky="ew", padx=4, pady=4)

    # ==================================================================
    # MAIN BUTTON GRID
    # ==================================================================
    def _build_main_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=5)

        for i in range(5):
            frame.rowconfigure(i, weight=1)
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        buttons = [
            ("C", 0, 0, 1, CLEAR_BTN_COLOR, CLEAR_BTN_HOVER, CLEAR_BTN_HOVER),
            ("+/-", 0, 1, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("%", 0, 2, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("/", 0, 3, 1, OP_BTN_COLOR, OP_BTN_HOVER, OP_BTN_FLASH),

            ("7", 1, 0, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("8", 1, 1, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("9", 1, 2, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("*", 1, 3, 1, OP_BTN_COLOR, OP_BTN_HOVER, OP_BTN_FLASH),

            ("4", 2, 0, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("5", 2, 1, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("6", 2, 2, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("-", 2, 3, 1, OP_BTN_COLOR, OP_BTN_HOVER, OP_BTN_FLASH),

            ("1", 3, 0, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("2", 3, 1, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("3", 3, 2, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("+", 3, 3, 1, OP_BTN_COLOR, OP_BTN_HOVER, OP_BTN_FLASH),

            ("0", 4, 0, 2, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            (".", 4, 2, 1, NUM_BTN_COLOR, NUM_BTN_HOVER, NUM_BTN_FLASH),
            ("=", 4, 3, 1, EQUAL_BTN_COLOR, EQUAL_BTN_HOVER, EQUAL_BTN_HOVER),
        ]

        for (text, row, col, colspan, color, hover, flash) in buttons:
            btn = ctk.CTkButton(
                frame, text=text, font=FONT_BTN, fg_color=color,
                hover_color=hover, corner_radius=20,
            )
            btn.configure(command=lambda t=text, c=color, f=flash, b=btn: self.on_button_click(t, c, f, b))
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=6, pady=6)

    # ==================================================================
    # SCIENTIFIC TOGGLE ARROW
    # ==================================================================
    def _build_toggle(self):
        self.toggle_btn = ctk.CTkButton(
            self, text="▾  Scientific", font=("Segoe UI", 13),
            fg_color="transparent", hover_color="#2b2b2b", text_color="#b8bec4",
            height=28, command=self.toggle_sci_panel,
        )
        self.toggle_btn.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 2))

    # ==================================================================
    # SCIENTIFIC PANEL
    # ==================================================================
    def _build_sci_panel(self):
        self.sci_container = ctk.CTkFrame(self, height=0, fg_color="transparent")
        self.sci_container.grid(row=5, column=0, sticky="ew", padx=15, pady=(0, 10))
        self.sci_container.grid_propagate(False)

        inner = ctk.CTkFrame(self.sci_container, fg_color="transparent")
        inner.pack(fill="both", expand=True)

        def sec(d):
            return 1 / math.cos(math.radians(d))

        def csc(d):
            return 1 / math.sin(math.radians(d))

        def cot(d):
            return 1 / math.tan(math.radians(d))

        sci_buttons = [
            ("sin", 0, 0, "trig", math.sin), ("cos", 0, 1, "trig", math.cos), ("tan", 0, 2, "trig", math.tan),
            ("asin", 1, 0, "inv_trig", math.asin), ("acos", 1, 1, "inv_trig", math.acos), ("atan", 1, 2, "inv_trig", math.atan),
            ("sinh", 2, 0, "plain", math.sinh), ("cosh", 2, 1, "plain", math.cosh), ("tanh", 2, 2, "plain", math.tanh),
            ("sec", 3, 0, "deg_direct", sec), ("csc", 3, 1, "deg_direct", csc), ("cot", 3, 2, "deg_direct", cot),
        ]

        for i in range(4):
            inner.rowconfigure(i, weight=1)
        for i in range(3):
            inner.columnconfigure(i, weight=1)

        for (label, row, col, kind, func) in sci_buttons:
            b = ctk.CTkButton(
                inner, text=label, font=FONT_SCI_BTN, fg_color=SCI_BTN_COLOR,
                hover_color=SCI_BTN_HOVER, corner_radius=16,
                command=lambda f=func, k=kind: self.apply_trig(f, k),
            )
            b.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def toggle_sci_panel(self):
        self.sci_open = not self.sci_open
        self.toggle_btn.configure(text=("▴  Scientific" if self.sci_open else "▾  Scientific"))
        target = self.sci_panel_height if self.sci_open else 0
        self._animate_panel_height(target)

    def _animate_panel_height(self, target, steps=14, delay=12):
        self._panel_anim_gen += 1
        gen = self._panel_anim_gen
        start = self.sci_container.cget("height")

        def step(i=0):
            if gen != self._panel_anim_gen:
                return
            try:
                eased = ease_out(i / steps)
                self.sci_container.configure(height=int(start + (target - start) * eased))
                if i < steps:
                    self.after(delay, lambda: step(i + 1))
                else:
                    self.sci_container.configure(height=target)
            except Exception as e:
                print("[panel animation warning]", e)

        step()
        self.after(steps * delay + 100, lambda: self._force_panel_height(gen, target))

    def _force_panel_height(self, gen, target):
        if gen == self._panel_anim_gen:
            try:
                self.sci_container.configure(height=target)
            except Exception:
                pass

    # ==================================================================
    # BUTTON PRESS ANIMATION
    # ==================================================================
    def _flash_button(self, btn, base_color, flash_color, steps=4, delay=12):
        gen = getattr(btn, "_flash_gen", 0) + 1
        btn._flash_gen = gen

        def go(i, c_from, c_to, next_fn):
            if btn._flash_gen != gen:
                return
            try:
                btn.configure(fg_color=lerp_color(c_from, c_to, i / steps))
                if i < steps:
                    self.after(delay, lambda: go(i + 1, c_from, c_to, next_fn))
                elif next_fn:
                    next_fn()
            except Exception as e:
                print("[button animation warning]", e)

        go(0, base_color, flash_color, lambda: go(0, flash_color, base_color, None))
        self.after(steps * delay * 2 + 80, lambda: self._force_button_color(btn, gen, base_color))

    def _force_button_color(self, btn, gen, base_color):
        if btn._flash_gen == gen:
            try:
                btn.configure(fg_color=base_color)
            except Exception:
                pass

    # ==================================================================
    # DISPLAY ANIMATIONS
    # ==================================================================
    def _flash_display_text(self, steps=4, delay=12):
        self._display_anim_gen += 1
        gen = self._display_anim_gen

        def go(i, c_from, c_to, next_fn):
            if gen != self._display_anim_gen:
                return
            try:
                self.display.configure(text_color=lerp_color(c_from, c_to, i / steps))
                if i < steps:
                    self.after(delay, lambda: go(i + 1, c_from, c_to, next_fn))
                elif next_fn:
                    next_fn()
            except Exception as e:
                print("[display animation warning]", e)

        go(0, DISPLAY_DEFAULT_FG, DISPLAY_ACCENT, lambda: go(0, DISPLAY_ACCENT, DISPLAY_DEFAULT_FG, None))
        self.after(steps * delay * 2 + 80, lambda: self._force_display_color(gen))

    def _quick_flash(self, color, steps=4, delay=12):
        self._display_anim_gen += 1
        gen = self._display_anim_gen

        def go(i, c_from, c_to, next_fn):
            if gen != self._display_anim_gen:
                return
            try:
                self.display.configure(text_color=lerp_color(c_from, c_to, i / steps))
                if i < steps:
                    self.after(delay, lambda: go(i + 1, c_from, c_to, next_fn))
                elif next_fn:
                    next_fn()
            except Exception as e:
                print("[display animation warning]", e)

        go(0, DISPLAY_DEFAULT_FG, color, lambda: go(0, color, DISPLAY_DEFAULT_FG, None))
        self.after(steps * delay * 2 + 80, lambda: self._force_display_color(gen))

    def _pop_equals_result(self, steps=4, delay=22):
        self._display_anim_gen += 1
        gen = self._display_anim_gen
        sizes = [44, 50, 46, 44]
        colors = [DISPLAY_ACCENT, "#8fe3ff", DISPLAY_DEFAULT_FG, DISPLAY_DEFAULT_FG]

        def run(i=0):
            if gen != self._display_anim_gen:
                return
            try:
                if i < len(sizes):
                    self.display.configure(font=("Segoe UI", sizes[i], "bold"), text_color=colors[i])
                    self.after(delay, lambda: run(i + 1))
                else:
                    self._force_display_color(gen)
            except Exception as e:
                print("[equals animation warning]", e)

        run()
        self.after(len(sizes) * delay + 100, lambda: self._force_display_color(gen))

    def _force_display_color(self, gen):
        if gen == self._display_anim_gen:
            try:
                self.display.configure(font=FONT_DISPLAY, text_color=DISPLAY_DEFAULT_FG)
            except Exception:
                pass

    # ==================================================================
    # LOGIC - number pad / operators
    # ==================================================================
    def on_button_click(self, key, base_color, flash_color, btn=None):
        if key == "C":
            self._clear_expression()
            self._quick_flash("#e57373")

        elif key == "=":
            self.calculate()
            self._pop_equals_result()

        elif key == "+/-":
            self.toggle_sign()
            self._flash_display_text()

        elif key == "%":
            self.apply_percent()
            self._flash_display_text()

        else:
            self.expression += key
            self.display_var.set(self.expression)
            self._flash_display_text()

        if btn is not None:
            self._flash_button(btn, base_color, flash_color)

    def _clear_expression(self):
        self.expression = ""
        self.display_var.set("0")

    def calculate(self):
        try:
            clean_expr = sanitize_expression(self.expression)
            result = eval(clean_expr)
            self.display_var.set(str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def toggle_sign(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression)

    def apply_percent(self):
        try:
            clean_expr = sanitize_expression(self.expression)
            value = eval(clean_expr) / 100
            self.expression = str(value)
            self.display_var.set(self.expression)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def apply_trig(self, func, kind):
        try:
            clean_expr = sanitize_expression(self.expression) if self.expression else "0"
            value = eval(clean_expr)

            if kind == "trig":
                result = func(math.radians(value))
            elif kind == "inv_trig":
                result = math.degrees(func(value))
            else:
                result = func(value)

            self.expression = str(round(result, 6))
            self.display_var.set(self.expression)
            self._pop_equals_result()
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    # ==================================================================
    # NEW: BACKSPACE
    # ==================================================================
    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        self._flash_display_text()

    # ==================================================================
    # NEW: MEMORY FUNCTIONS
    # ==================================================================
    def _current_value(self):
        clean_expr = sanitize_expression(self.expression) if self.expression else "0"
        return eval(clean_expr)

    def memory_clear(self):
        self.memory = 0.0
        self._quick_flash("#8888ff")

    def memory_recall(self):
        self.expression = format_number(self.memory)
        self.display_var.set(self.expression)
        self._flash_display_text()

    def memory_add(self):
        try:
            self.memory += self._current_value()
            self._quick_flash("#8888ff")
        except Exception:
            self.display_var.set("Error")

    def memory_subtract(self):
        try:
            self.memory -= self._current_value()
            self._quick_flash("#8888ff")
        except Exception:
            self.display_var.set("Error")

    # ==================================================================
    # NEW: sqrt / square / reciprocal
    # ==================================================================
    def apply_sqrt(self):
        try:
            value = self._current_value()
            if value < 0:
                raise ValueError("negative")
            result = math.sqrt(value)
            self.expression = format_number(round(result, 6))
            self.display_var.set(self.expression)
            self._pop_equals_result()
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def apply_square(self):
        try:
            value = self._current_value()
            result = value ** 2
            self.expression = format_number(round(result, 6))
            self.display_var.set(self.expression)
            self._pop_equals_result()
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def apply_reciprocal(self):
        try:
            value = self._current_value()
            result = 1 / value
            self.expression = format_number(round(result, 6))
            self.display_var.set(self.expression)
            self._pop_equals_result()
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()