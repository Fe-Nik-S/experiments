

from const import PATH_TO_IMG, OUTPUT_IMG
from utils import save_as
from PIL import Image


def main():
    pil_im = Image.open(PATH_TO_IMG).convert("L")
    save_as(pil_im, OUTPUT_IMG, "png")


if __name__ == "__main__":
    main()
