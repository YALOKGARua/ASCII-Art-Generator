import sys
import time
import math
import random
from PIL import Image
import os
ASCII_CHARS = "@#$%&*+=-:. "
def pixel_to_ansi(r, g, b):
    r = min(int(r * 2.2), 255)
    g = min(int(g * 2.2), 255)
    b = min(int(b * 2.2), 255)
    return f"\033[38;2;{r};{g};{b}m"
def image_to_ascii_dynamic(path, width=100, colored=True, interval=0.016):
    img = Image.open(path)
    img = img.convert("RGB")
    w, h = img.size
    aspect_ratio = h / w
    new_height = int(aspect_ratio * width * 0.55)
    img = img.resize((width, new_height))
    pixels = list(img.getdata())
    grays = [int(0.299*r + 0.587*g + 0.114*b) for (r, g, b) in pixels]
    print("\033[2J", end="")
    t0 = time.time()
    n = len(ASCII_CHARS)
    random_phases = [random.uniform(0, 2*math.pi) for _ in range(len(pixels))]
    try:
        while True:
            t = time.time() - t0
            ascii_str = ""
            for i, ((r, g, b), gray) in enumerate(zip(pixels, grays)):
                idx = gray * (n-1) // 255
                phase = (i % width) * 0.15 + (i // width) * 0.2 + random_phases[i]
                wave = math.sin(t * 4 + phase)
                f = 0.5 + 0.5 * wave
                idx_low = max(idx - 1, 0)
                idx_high = min(idx + 1, n-1)
                idx_interp = int(round(idx_low * (1-f) + idx_high * f))
                char = ASCII_CHARS[idx_interp]
                if colored:
                    ascii_str += f"{pixel_to_ansi(r, g, b)}{char}\033[0m"
                else:
                    ascii_str += char
                if (i + 1) % width == 0:
                    ascii_str += "\n"
            print("\033[?25l\033[H" + ascii_str, end="", flush=True)
            time.sleep(interval)
    finally:
        print("\033[?25h", end="")
def main():
    if len(sys.argv) < 2:
        print("Usage: python art.py path_to_image")
        input("Press Enter to exit...")
        return
    path = sys.argv[1]
    image_to_ascii_dynamic(path, width=100, colored=True, interval=0.016)
if __name__ == "__main__":
    main()