import figuregen
from figuregen.util import image
from figuregen.util.image import Cropbox
import simpleimageio as sio
from metrics import compute_metric


scene_names = ["Living Room", "Test"]
method_names = ["Noisy", "Noisy+", "Darker", "Reference"]
metric_name = "MAPE"

# reference, *[method list]
img_path = [
    [
        "data/living-ref.exr",
        "data/living-noisy.exr",
        "data/living-noisy+.exr",
        "data/living-darker.exr",
        "data/living-ref.exr",
    ],
    [
        "data/living-ref.exr",
        "data/living-noisy.exr",
        "data/living-noisy+.exr",
        "data/living-darker.exr",
        "data/living-ref.exr",
    ],
]

crops = [
    [
        Cropbox(top=320, left=380, height=64, width=64, scale=1),
        Cropbox(top=350, left=660, height=96, width=96, scale=1)
    ],
    [
        Cropbox(top=460, left=180, height=96, width=96, scale=1),
        Cropbox(top=155, left=1070, height=96, width=96, scale=1)
    ],
]
CROPS_COLOR = [(102, 204, 255), (0, 200, 100)]

TITLE_BACKGROUND_COLOR = (255, 255, 255)
ROW_TITLE_FONT_SIZE = 10
COL_TITLE_FONT_SIZE = 8
ERR_TITLE_FONT_SIZE = 7
ROW_TITLE_SIZE = 5
COL_TITLE_SIZE = 4
ERR_TITLE_SIZE = 3

# don't change this part


def prepare_image(img):
    # maybe do some processing here, e.g. padding, etc.
    return image.lin_to_srgb(img)


def draw_scene(scene_idx):

    # load image and compute errors

    ref_img = sio.read(img_path[scene_idx][0])
    method_imgs = [sio.read(p) for p in img_path[scene_idx][1:]]

    errors = [
        compute_metric(method_img, ref_img, metric_name)
        for method_img in method_imgs
    ]
    crop_errors = [
        [
            compute_metric(crop.crop(method_img),
                           crop.crop(ref_img), metric_name)
            for method_img in method_imgs
        ]
        for crop in crops[scene_idx]
    ]

    ref_img = prepare_image(ref_img)
    method_imgs = [prepare_image(img) for img in method_imgs]

    # generate ref grid

    ref_grid = figuregen.Grid(num_rows=1, num_cols=1)
    ref_grid[0, 0].set_image(figuregen.PNG(ref_img))
    ref_grid.set_title("left", scene_names[scene_idx])
    ref_grid.layout.titles[figuregen.LEFT] = figuregen.TextFieldLayout(
        size=ROW_TITLE_SIZE, offset=0, rotation=90,
        fontsize=ROW_TITLE_FONT_SIZE,
        background_colors=TITLE_BACKGROUND_COLOR)
    for crop_idx in range(len(crops[scene_idx])):
        crop = crops[scene_idx][crop_idx]
        ref_grid[0, 0].set_marker(
            crop.marker_pos, crop.marker_size, color=CROPS_COLOR[crop_idx])
    ref_grid.layout.set_padding(right=1.0)

    # generate methods grid

    row_num, col_num = len(crops[scene_idx]), len(method_names)
    methods_grid = figuregen.Grid(num_rows=row_num, num_cols=col_num)
    for row in range(row_num):
        for col in range(col_num):
            img = crops[scene_idx][row].crop(method_imgs[col])
            methods_grid[row, col].set_image(figuregen.PNG(img))
            methods_grid[row, col].set_frame(
                linewidth=1, color=CROPS_COLOR[row])
            if method_names[col] == "Reference":
                continue
            methods_grid[row, col].set_label(f"{crop_errors[row][col]:.3f}",
                                             pos="bottom_right", width_mm=8, height_mm=3, offset_mm=[0, 0],
                                             fontsize=6, txt_color=(255, 255, 255), bg_color=None)
    error_strings = []
    for i, method_name in enumerate(method_names):
        if method_name == "Reference":
            error_strings.append(metric_name)
        else:
            error_strings.append(f"{errors[i]:.3f}")
    methods_grid.set_col_titles("bottom", error_strings)
    methods_grid.layout.column_titles[figuregen.BOTTOM] = figuregen.TextFieldLayout(
        size=ERR_TITLE_SIZE, offset=0, fontsize=ERR_TITLE_FONT_SIZE,
        background_colors=TITLE_BACKGROUND_COLOR)
    methods_grid.layout.set_padding(right=1.0)

    # add first title and padding ref grid

    if scene_idx == 0:
        methods_grid.set_col_titles("top", method_names)
        methods_grid.layout.column_titles[figuregen.TOP] = figuregen.TextFieldLayout(
            size=COL_TITLE_SIZE, offset=0, fontsize=COL_TITLE_FONT_SIZE,
            background_colors=TITLE_BACKGROUND_COLOR)
        padding_size = methods_grid.layout.column_titles[figuregen.TOP].size + \
            methods_grid.layout.column_titles[figuregen.TOP].offset
        ref_grid.layout.padding[figuregen.TOP] = padding_size

    padding_size = methods_grid.layout.column_titles[figuregen.BOTTOM].size + \
        methods_grid.layout.column_titles[figuregen.BOTTOM].offset
    ref_grid.layout.padding[figuregen.BOTTOM] = padding_size

    return [ref_grid, methods_grid]


grid = [draw_scene(i) for i in range(len(scene_names))]

figuregen.figure(grid, width_cm=18., filename="example/crop.pdf")
