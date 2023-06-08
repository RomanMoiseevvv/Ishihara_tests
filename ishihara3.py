import math
import random
import sys
import os
import sys

from PIL import Image, ImageDraw

SOURCE_PATCH = "fonts"
RESULT_PATH = "test5"
GEN_COUNT = 1

try:
    from scipy.spatial import cKDTree as KDTree
    import numpy as np
    IMPORTED_SCIPY = True
except ImportError:
    IMPORTED_SCIPY = False

BACKGROUND = (255, 255, 255)
TOTAL_CIRCLES = 1500

color = lambda c: ((c >> 16) & 255, (c >> 8) & 255, c & 255)
if sys.argv[1]:
    COLOR_THEAM = int(sys.argv[1] ) % 5
else: 
    COLOR_THEAM = 1

TYPE = COLOR_THEAM if COLOR_THEAM <= 3 else 3

#   type 1
if COLOR_THEAM == 1:
    COLORS_ON = [
        color(0xF9BB82), color(0xEBA170), color(0xFCCD84)
    ]
    COLORS_OFF = [
        color(0x9CA594), color(0xACB4A5), color(0xBBB964),
        color(0xD7DAAA), color(0xE5D57D), color(0xD1D6AF)
    ]

# type 2
elif COLOR_THEAM == 2:
    COLORS_ON = [
        color(0xb6b87c), color(0xe3da73), color(0xb0ab60)
    ]
    COLORS_OFF = [
        color(0xef845a), color(0xffc68c), color(0xef845a),
    ]

# type 3
elif COLOR_THEAM == 3:
    COLORS_ON = [
        color(0xf79087), color(0xf26969), color(0xd8859d),\
        color(0xf79087)
    ]
    COLORS_OFF = [
        color(0x5a4e46), color(0x7b6b63), color(0x9c9c84),
    ]

# type 3 too
elif COLOR_THEAM == 4:
    COLORS_ON = [
        color(0xb6b87c), color(0xe3da73), color(0xb0ab60)
    ]
    COLORS_OFF = [
        color(0xef845a), color(0xffc68c), color(0xef845a),\
        color(0xfff36b), color(0xffbd52)
    ]


def generate_circle(image_width, image_height, min_diameter, max_diameter):
    radius = random.triangular(min_diameter, max_diameter,
                               max_diameter * 0.8 + min_diameter * 0.2) / 2

    angle = random.uniform(0, math.pi * 2)
    distance_from_center = random.uniform(0, image_width * 0.48 - radius)
    x = image_width  * 0.5 + math.cos(angle) * distance_from_center
    y = image_height * 0.5 + math.sin(angle) * distance_from_center

    return x, y, radius


def overlaps_motive(image, par):
    (x, y, r) = par
    points_x = [x, x, x, x-r, x+r, x-r*0.93, x-r*0.93, x+r*0.93, x+r*0.93]
    points_y = [y, y-r, y+r, y, y, y+r*0.93, y-r*0.93, y+r*0.93, y-r*0.93]

    for xy in zip(points_x, points_y):
        try:
            if image.getpixel(xy)[:3] != BACKGROUND:
                return True
        except IndexError:
            print ("Exept gen")
            return False
        except TypeError:
            print ("second exept gen")
            return False

    return False


def circle_intersection(par1, par2):
    (x1, y1, r1) = par1
    (x2, y2, r2) = par2
    return (x2 - x1)**2 + (y2 - y1)**2 < (r2 + r1)**2


def circle_draw(draw_image, image, par):
    (x, y, r) = par
    fill_colors = COLORS_ON if overlaps_motive(image, (x, y, r)) else COLORS_OFF
    fill_color = random.choice(fill_colors)

    draw_image.ellipse((x - r, y - r, x + r, y + r),
                       fill=fill_color,
                       outline=fill_color)


def gen_test(name,gen_n = 0):
	'''
	Generate Ishihara test card
	from file name.png to name+gen_n+.png
	'''
    image = Image.open(os.path.join(SOURCE_PATCH,name + ".png"))
    image2 = Image.new('RGB', image.size, BACKGROUND)
    draw_image = ImageDraw.Draw(image2)

    width, height = image.size

    min_diameter = (width + height) / 200
    max_diameter = (width + height) / 75

    circle = generate_circle(width, height, min_diameter, max_diameter)
    circles = [circle]

    circle_draw(draw_image, image, circle)

    try:
        for i in range(TOTAL_CIRCLES):
            tries = 0
            if IMPORTED_SCIPY:
                kdtree = KDTree([(x, y) for (x, y, _) in circles])
                while True:
                    circle = generate_circle(width, height, min_diameter, max_diameter)
                    elements, indexes = kdtree.query([(circle[0], circle[1])], k=12)
                    for element, index in zip(elements[0], indexes[0]):
                        if not np.isinf(element) and circle_intersection(circle, circles[index]):
                            break
                    else:
                        break
                    tries += 1
            else:
                while any(circle_intersection(circle, circle2) for circle2 in circles):
                    tries += 1
                    circle = generate_circle(width, height, min_diameter, max_diameter)

            #print ('{}/{} {}'.format(i, TOTAL_CIRCLES, tries) )

            circles.append(circle)
            circle_draw(draw_image, image, circle)
    except (KeyboardInterrupt, SystemExit):
        pass

    name =  name + "theme_" + str(COLOR_THEAM) + " type_" + str(TYPE) + ".png"
    image2.save(os.path.join(RESULT_PATH , name ) , "PNG")
    print ("Generate " + name +" succesfully" )

def main():
    files = os.listdir(SOURCE_PATCH)
    if not os.path.isdir(RESULT_PATH):
        os.mkdir(RESULT_PATH)
    count = 0
    for filename in files:
        name,ext = os.path.splitext(filename)
        if ext == ".png":
            for i in range(GEN_COUNT):
                gen_test(name,i)
            count += 1 
            print("not more than " +str( len(files) - count ) + " files left" )
    print("Generate test success")

if __name__ == '__main__':
    main()
