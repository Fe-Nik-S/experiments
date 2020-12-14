

from const import PATH_TO_IMG, OUTPUT_IMG
from utils import save_as, make_thumbnail
from PIL import Image


def main():
    pil_im = Image.open(PATH_TO_IMG)
    thumbnail = make_thumbnail(pil_im, 256, 128)
    save_as(pil_im, OUTPUT_IMG, "png")


if __name__ == "__main__":
    main()
