#well ye sb coad chat gpt k h mujhe na ata'
import math
import time
import os

# Function to clear the screen (cross-platform)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to draw the heart
def heart():
    for y in range(15, -15, -1):
        line = ''
        for x in range(-30, 30):
            formula = ((x * 0.05)**2 + (y * 0.1)**2 - 1)**3 - (x * 0.05)**2 * (y * 0.1)**3
            if formula <= 0:
                line += '❤️'
            else:
                line += '  '
        print(line)

# Animate the heart (pulse effect)
for i in range(100):
    clear()
    heart()
    print("\n      💖 I Love Python 💖\n")
    time.sleep(0.2)
