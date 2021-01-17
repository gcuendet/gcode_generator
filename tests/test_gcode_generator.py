import numpy as np
from gcode_generator.cad import *
from matplotlib import pyplot as plt


def test_canvas_init():
    canvas = Canvas()
    assert canvas.xmax > canvas.xmin
    assert canvas.ymax > canvas.ymin


def test_canvas_downsample_image_to_fit_height():
    img = np.zeros((1200, 1600), dtype=np.uint8)
    canvas = Canvas()
    scaled_img = canvas.scale_image_to_fit(img)

    assert scaled_img.shape[0] == 900
    assert scaled_img.shape[1] == 1200


def test_canvas_downsample_image_to_fit_width():
    img = np.zeros((480, 4800), dtype=np.uint8)
    canvas = Canvas()
    scaled_img = canvas.scale_image_to_fit(img)

    assert scaled_img.shape[0] == 360
    assert scaled_img.shape[1] == 3600


def test_canvas_upsample_image_to_fit_height():
    img = np.zeros((450, 450), dtype=np.uint8)
    canvas = Canvas()
    scaled_img = canvas.scale_image_to_fit(img)

    assert scaled_img.shape[0] == 900
    assert scaled_img.shape[1] == 900


def test_canvas_upsample_image_to_fit_width():
    img = np.zeros((200, 1200), dtype=np.uint8)
    canvas = Canvas()
    scaled_img = canvas.scale_image_to_fit(img)

    assert scaled_img.shape[0] == 600
    assert scaled_img.shape[1] == 3600


def test_compute_n_contours():
    arr = np.ones((160, 120), dtype=np.bool)
    square_top_left = (70, 50)
    square_bottom_right = (90, 70)
    arr[
        square_top_left[0] : square_bottom_right[0],
        square_top_left[1] : square_bottom_right[1],
    ] = 0

    n_contours = 1
    paths = compute_n_contours(arr, n_contours, 0.2, 0.5)

    assert len(paths) == n_contours

    # Check that each vertex of the contour is whitin the square
    for i in range(len(paths)):
        for k in paths[i]:
            print(k)
            assert k[0] >= square_top_left[1]
            assert k[0] <= square_bottom_right[1]
            assert k[1] >= square_top_left[0]
            assert k[1] <= square_bottom_right[0]


def test_end_to_end():
    arr = np.ones((120, 160), dtype=np.bool)
    arr[90:110, 10:40] = 0

    n_contours = 1
    canvas = Canvas()
    arr = canvas.scale_image_to_fit(arr)
    plt.imshow(arr)

    print(arr.shape)
    paths = compute_n_contours(arr, n_contours, 0.2, 0.5)
    print(paths)
    for i in range(len(paths)):
        xs, ys = zip(*paths[i])
        plt.plot(xs, ys)
    plt.show()
    gcode = write_gcode(paths, canvas)
    print(gcode)
