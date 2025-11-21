# filename: heart_terminal.py
# Usage:
#   pip install colorama   # (only if on Windows; Linux/macOS terminals usually support ANSI)
#   python heart_terminal.py

import math
import time
import os
import sys

# Try to enable colors on Windows
try:
    import colorama
    colorama.init()
except Exception:
    pass

ESC = "\033["
RESET = ESC + "0m"
HIDE_CURSOR = ESC + "?25l"
SHOW_CURSOR = ESC + "?25h"

def clear():
    # cross-platform clear
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write(ESC + "2J" + ESC + "H")

def heart_points(width=60, height=24, scale=1.0):
    """Generate a 2D grid of points: True where the heart exists."""
    points = []
    for j in range(height):
        row = []
        for i in range(width):
            # map grid to coordinate space centered at (0,0)
            x = (i - width/2) / (width/2) * 1.5 / scale
            y = (j - height/2) / (height/2) * -1.5 / scale  # flip y for correct orientation

            # classic heart implicit equation:
            # (x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0 is inside the heart
            val = (x*x + y*y - 1)**3 - x*x * y**3
            row.append(val <= 0)
        points.append(row)
    return points

def colored(text, color_code):
    return f"{ESC}{color_code}m{text}{RESET}"

def render(points, pulse=0.0):
    h = len(points)
    w = len(points[0]) if h else 0
    out_lines = []
    for j in range(h):
        line = []
        for i in range(w):
            if points[j][i]:
                # vary brightness/size with pulse and position for nicer look
                brightness = 1.0 + 0.25 * math.sin(pulse + (i + j) * 0.05)
                # choose character based on brightness
                if brightness > 1.18:
                    ch = "❤"
                elif brightness > 1.02:
                    ch = "♥"
                else:
                    ch = "❤"
                # Use red background + bright foreground for a bold heart
                # 31 = red fg, 91 = bright red fg; we'll pick depending on brightness
                color = "91" if brightness > 1.1 else "31"
                line.append(colored(ch, color))
            else:
                line.append(" ")  # keep spacing
        out_lines.append("".join(line))
    return "\n".join(out_lines)

def main():
    width = 64
    height = 28
    scale = 1.0

    points = heart_points(width=width, height=height, scale=scale)

    try:
        sys.stdout.write(HIDE_CURSOR)
        for t in range(10000):
            pulse = t * 0.18
            clear()
            print(render(points, pulse=pulse))
            # Add a little message below
            print()
            print("    " + colored("Dil se ❤️", "93"))  # 93 = bright yellow
            time.sleep(0.08)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
