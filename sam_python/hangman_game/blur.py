"""
File: blur.py
-------------------------------
This file shows the original image first,
smiley-face.png, and then compare to its
blurred image. The blur algorithm uses the
average RGB values of a pixel's nearest neighbors
"""

from simpleimage import SimpleImage


def blur(img):
    """
    :param img:
    :return:
    """
    new_img = SimpleImage.blank(img.width, img.height)
    color1 = []
    color2 = []
    color3 = []
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.get_pixel(x, y)
            blank_pixel = new_img.get_pixel(x, y)
            for n in range(-1, 2):
                for m in range(-1, 2):
                    if img.width > x+n >= 0 and img.height > y+m >= 0:
                        a_pixel = img.get_pixel(x+n, y+m)
                        blank_pixel.red += a_pixel.red
                        color1.append(a_pixel.red)
                        color2.append(a_pixel.green)
                        color3.append(a_pixel.blue)
            blank_pixel.red = (sum(color1) - pixel.red) // (len(color1) - 1)
            blank_pixel.green = (sum(color2) - pixel.green) // (len(color2) - 1)
            blank_pixel.blue = (sum(color3) - pixel.blue) // (len(color3) - 1)
            color1 = []
            color2 = []
            color3 = []
    return new_img


def main():
    """
    TODO:
    """
    old_img = SimpleImage("images/smiley-face.png")
    old_img.show()

    blurred_img = blur(old_img)
    for i in range(3):
        blurred_img = blur(blurred_img)
    blurred_img.show()


if __name__ == '__main__':
    main()
