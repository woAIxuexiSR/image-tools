import figuregen
from figuregen.util import image
import simpleimageio as sio
import numpy as np

# settings

VERTICAL = True
DEGREE = -20
LINE_WIDTH_PT = 0.5
LINE_COLOR = (102, 204, 255)

# images

def load_image(path):
    img = sio.read(path)[:,:,:3]
    return image.lin_to_srgb(img)

ref = load_image("data/living-ref.exr")
noisy = load_image("data/living-noisy.exr")
noisy_ = load_image("data/living-noisy+.exr")

images = [ref, noisy, noisy_]
weights = [0.8, 0.5, 0.7]

# create split image, don't change this part

split_image = image.SplitImage(
    images, vertical=VERTICAL, degree=DEGREE, weights=weights)

grid = figuregen.Grid(num_rows=1, num_cols=1)
grid[0, 0].set_image(figuregen.PNG(split_image.get_image()))
grid[0, 0].draw_lines(split_image.get_start_positions(),
                      split_image.get_end_positions(),
                      linewidth_pt=LINE_WIDTH_PT, color=LINE_COLOR)

figuregen.figure([[grid]], width_cm=18, filename="example/split.pdf")