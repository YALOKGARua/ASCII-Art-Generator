import sys
from PIL import Image

ASCII_CHARS = "@#W$9876543210?!abc;:+=-,._ "

def pixel_to_ansi(r, g, b):
    r = min(int(r * 2.2), 255)
    g = min(int(g * 2.2), 255)
    b = min(int(b * 2.2), 255)
    return f"\033[38;2;{r};{g};{b}m"

def image_to_ascii(path, width=100, colored=True):
    img = Image.open(path)
    img = img.convert("RGB")
    w, h = img.size
    aspect_ratio = h / w
    new_height = int(aspect_ratio * width * 0.55)
    img = img.resize((width, new_height))
    pixels = list(img.getdata())
    ascii_str = ""
    for i, (r, g, b) in enumerate(pixels):
        gray = int(0.299*r + 0.587*g + 0.114*b)
        char = ASCII_CHARS[gray * (len(ASCII_CHARS)-1) // 255]
        if colored:
            ascii_str += f"{pixel_to_ansi(r, g, b)}{char}\033[0m"
        else:
            ascii_str += char
        if (i + 1) % width == 0:
            ascii_str += "\n"
    return ascii_str

def main():
    if len(sys.argv) < 2:
        print("Usage: python art.py path_to_image")
        input("Press Enter to exit...")
        return
    path = sys.argv[1]
    print(image_to_ascii(path, width=100, colored=True))
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
