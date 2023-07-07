from PIL import Image, ImageDraw

from math import sqrt
from time import time
import sys
from Color import Color
from utils import *
from os import mkdir

from resizeimage import resizeimage

# sys.path.append("..")
# import screen


# colors = [
#     Color(0, 0, 0),
#     Color(255, 255, 255)
# ]

"""todo: read color palette from json files + convert hex to rgb"""
colors = [

    Color(0, 0, 0),
    Color(255, 0, 0),
    Color(255, 255, 0),
    Color(255, 128, 0),
    Color(0, 255, 0),
    Color(0, 0, 255),
    Color(255, 255, 255),
]


def render(image: Image):
    """put all pixel data inside a 2d array for faster operations"""


    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            color = Color(pixel[0], pixel[1], pixel[2])
            new_color = nearest_color(color)
            distance_error = Color(color.r - new_color.r,
                                   color.g - new_color.g, color.b - new_color.b)

            draw = ImageDraw.Draw(image)
            draw.point((x, y), (new_color.r, new_color.g, new_color.b))

            if (x+1 < image.width and y+1 < image.height):
                """ugly Floyd–Steinberg dithering

                https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

                todo: find a way to do each step on one line
                """
                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x+1, y))),
                    color_multiplication(7/16, distance_error))

                draw.point((x+1, y), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x-1, y+1))),
                    color_multiplication(3/16, distance_error))

                draw.point((x-1, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x, y+1))),
                    color_multiplication(5/16, distance_error))

                draw.point((x, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x+1, y+1))),
                    color_multiplication(1/16, distance_error))

                draw.point((x+1, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

    try:
        image.save(f"/home/pi/MagicBox/pic/{sys.argv[2]}/{sys.argv[3]}.gif")
        #export = sys.argv[2] + ".gif"
        #screen.EPaper.Update(export)

    except FileNotFoundError:
        print("Out folder not found, creating it...")
        mkdir("./out")
        image.save("./out/" + str(time()) + ".gif")


def nearest_color(old_color: Color):
    """change the current color to the nearest color available"""

    new_color = colors[0]
    min_distance = distance(old_color, colors[0])

    for color in colors:
        new_distance = distance(color, old_color)

        if (new_distance < min_distance):
            new_color = color
            min_distance = new_distance

    return new_color


def distance(first_color: Color, second_color: Color):
    """return the distance between 2 colors"""
    return sqrt((first_color.r - second_color.r) ** 2 + (first_color.g - second_color.g) ** 2 + (first_color.b - second_color.b) ** 2)


def resize_proportionally(ratio, max_v, min_v):
    new_height = max_v
    new_width = int(ratio * new_height)
    if new_width < min_v: new_width = min_v

    return (new_width, new_height)




def start():
    """render the image with the provided image"""
    try:

        width = 640
        height = 400
        with Image.open(sys.argv[1]) as image:
            if image.width < image.height:
                width = 400
                height = 640

            ratio = image.width / image.height
    
            # vertical small picture handler    
            if image.width < 400 and image.height < 640:
                new_size = resize_proportionally(ratio, 640, 400)
                image = image.resize(new_size)

            if image.width < 640 and image.height < 400:
                new_size = resize_proportionally(ratio, 400, 640)
                image = image.resize(new_size)


            croped = resizeimage.resize_cover(image, [width, height])    
            data = render(croped)

    except IndexError:
        """if an image is not specified return an error"""
        print("Missing argument")


if __name__ == "__main__":
    start()
