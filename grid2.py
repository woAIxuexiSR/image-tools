import figuregen
from figuregen.util import image
import simpleimageio as sio
import numpy as np
import matplotlib.pyplot as plt

# settings

NROWS, NCOLS = 2, 3
ROW_PADDING = 1.0
COL_PADDING = 1.0
TITLE_BACKGROUND_COLOR = (255, 255, 255)
ROW_TITLE_FONT_SIZE = 12
COL_TITLE_FONT_SIZE = 12
ROW_TITLE_SIZE = 5
COL_TITLE_SIZE = 5

# images

BLUE = np.array([94, 163, 188])
GREEN = np.array([5, 142, 78])
ORANGE = np.array([186, 98, 82])

img_blue = np.tile(BLUE / 255., (32, 64, 1))
img_green = np.tile(GREEN / 255., (32, 64, 1))
img_orange = np.tile(ORANGE / 255., (32, 64, 1))
# exr_img = image.lin_to_srgb(sio.read("data/living-ref.exr"))

images = [
    [figuregen.PNG(img_blue), figuregen.PNG(
        img_green), figuregen.PNG(img_orange)],
    [figuregen.PNG(1 - img_blue), figuregen.PNG(1 - img_green),
     figuregen.PNG(1 - img_orange)],
]

row_titles = ["Original", "Negative"]
col_titles = ["Blue", "Green", "Orange"]

# labels

USE_LABELS = True
LABEL_POSITION = "bottom_right"
LABEL_FONT_SIZE = 8
LABEL_TEXT_COLOR = (255, 255, 255)
LABEL_BACKGROUND_COLOR = None

labels = [
    [None, "B", "C"],
    ["", "E", "F"],
]

# create grid, don't change this part


def generate_image(row, col):

    image_grid = figuregen.Grid(num_rows=1, num_cols=1)
    image_grid[0, 0].set_image(images[row][col])

    if row == 0:
        image_grid.set_title("top", col_titles[col])
        image_grid.layout.titles[figuregen.TOP] = figuregen.TextFieldLayout(
            size=COL_TITLE_SIZE, offset=0, fontsize=COL_TITLE_FONT_SIZE,
            background_colors=TITLE_BACKGROUND_COLOR)
    if col == 0:
        image_grid.set_title("left", row_titles[row])
        image_grid.layout.titles[figuregen.LEFT] = figuregen.TextFieldLayout(
            size=ROW_TITLE_SIZE, offset=0, rotation=90,
            fontsize=ROW_TITLE_FONT_SIZE,
            background_colors=TITLE_BACKGROUND_COLOR)

    if USE_LABELS and labels[row][col]:
        image_grid[0, 0].set_label(
            labels[row][col], pos=LABEL_POSITION,
            width_mm=10, height_mm=5,
            fontsize=LABEL_FONT_SIZE,
            txt_color=LABEL_TEXT_COLOR,
            bg_color=LABEL_BACKGROUND_COLOR)

    image_grid.layout.set_padding(bottom=ROW_PADDING)
    image_grid.layout.set_padding(right=COL_PADDING)

    return image_grid


grid = []

for row in range(NROWS):
    row_grid = []
    for col in range(NCOLS):
        row_grid.append(generate_image(row, col))
    grid.append(row_grid)

figuregen.figure(grid, width_cm=18., filename="example/grid2.pdf",
                 backend=figuregen.PdfBackend(preamble_lines=[
                     '\\usepackage[T1]{fontenc}',
                     '\\usepackage{libertine}',
                 ]))
