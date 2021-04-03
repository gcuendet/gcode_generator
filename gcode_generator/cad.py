import numpy as np
from scipy.signal.signaltools import fftconvolve
from scipy.interpolate import RectBivariateSpline
from .legacy import (
    evaluate_state,
    sort_segments,
    vectorize_toolpaths,
    RuleTable,
    CAStates,
)


class Canvas:
    def __init__(self):
        """
        x [mm] in [0, 140]
        y [mm] in [-30, 30]
        x [1/10 degrees] in [0, 3600]
        y [1/10 degrees] in [-450, 450] 
        """
        self.xmin = 0  # 1/10 degrees
        self.xmax = 1800  # 1/10 degrees
        self.ymin = -450  # 1/10 degrees
        self.ymax = 450  # 1/10 degrees
        self.xmin_mm = 0  # mm
        self.xmax_mm = 60  # mm
        self.ymin_mm = -25  # mm
        self.ymax_mm = 25  # mm
        # pixel per mm
        # assumes a sphere
        self.ppmm = (self.xmax - self.xmin) / (self.xmax_mm - self.xmin_mm)

    def scale_image_to_fit(self, image):
        assert image.ndim == 2

        im_w = image.shape[1]
        im_h = image.shape[0]
        canvas_w = self.xmax - self.xmin
        canvas_h = self.ymax - self.ymin
        scale = min(float(canvas_w) / im_w, float(canvas_h) / im_h)

        scaled_w = int(np.floor(im_w * scale))
        scaled_h = int(np.floor(im_h * scale))
        spline_order_x = 1
        spline_order_y = 1
        smoothing = 0
        if scale > 1:
            # We are upsampling
            pass
        else:
            # We are downsampling
            smoothing = 0.9  # Tune that value
        interp = RectBivariateSpline(
            np.arange(im_h), np.arange(im_w), image, kx=1, ky=1, s=0
        )
        return (
            interp(
                np.linspace(0, im_h, num=scaled_h, endpoint=False),
                np.linspace(0, im_w, num=scaled_w, endpoint=False),
            )
            >= 0.5
        )


def get_kernel(
    contour: int = 1,
    ppmm: float = 1.0,
    tool_diameter: float = 0.03,
    tool_overlap: float = 0.5,
):
    """ Given the tool diameter, compute a kernel to extract contours """
    tool_radius_mm = tool_diameter / 2.0

    kernel_radius_mm = tool_radius_mm + contour * tool_overlap * tool_diameter
    kernel_radius = 1 + int(ppmm * kernel_radius_mm)
    print("ppmm = ", ppmm)
    print("kernel_radius [mm] = ", kernel_radius_mm)
    print("kernel_radius [-]  = ", kernel_radius)

    kx = 1 + np.outer(np.ones((2 * kernel_radius, 1)), np.arange(2 * kernel_radius))
    ky = 1 + np.outer(np.arange(2 * kernel_radius), np.ones((1, 2 * kernel_radius)))
    k = (
        ((kx - kernel_radius) ** 2 + (ky - kernel_radius) ** 2) < kernel_radius ** 2
    ).astype("uint32")

    return k


def compute_n_contours(
    arr: np.array,
    contours_count: int = 1,
    tool_diameter: float = 0.03,
    tool_overlap: float = 0.5,
):
    """ Given a binary array, compute the contours
    
    Parameters:
    -----------
    arr: np.array
        Binary image.
        Caution: Foreground (black) is 0 and background (white) is 1!
    """
    canvas = Canvas()
    r = RuleTable()
    paths = []
    for contour in range(contours_count):
        kernel = get_kernel(contour, canvas.ppmm, tool_diameter, tool_overlap)
        interior = arr.astype("uint32")
        conv = fftconvolve(interior, kernel, mode="same")
        conv = np.where(conv > 0.01, 1, 0)
        conv_array = conv + (conv != 1) * arr

        state = evaluate_state(conv_array)
        toolpath = r.table[state]
        tool_array = toolpath + (toolpath == 0) * conv_array
        new_paths = vectorize_toolpaths(tool_array)
        if len(new_paths) == 0:
            break
        paths.extend(new_paths)
    return paths


def write_gcode(contours, canvas, pen_up=100, pen_down=125, feedrate=775.0):
    gcode = """;---------------------------------------------------------------
;Start of sheet header
;metric
G21
;zero all axes
G92 X0 Y0 Z0
;End of sheet header\n"""
    dxy = 0
    xold = 0
    yold = 0
    #
    # follow toolpaths CCW, for CW tool motion
    #
    sorted_segments = sort_segments(contours)
    units = 1.0
    for segment in range(len(sorted_segments)):
        x = units * (canvas.xmin + (sorted_segments[segment][0][0] + 0.5))
        y = units * (canvas.ymax - sorted_segments[segment][0][1] + 0.5)
        gcode += ";Pen Up\nM300 S{}\n".format(pen_up)
        gcode += "G4 P120\n"
        gcode += "G1 X{:.4f} Y{:.4f} F{}\n".format(x, y, feedrate)  # rapid motion
        gcode += ";Pen Down\nM300 S{}\n".format(pen_down)  # linear motion
        gcode += "G4 P120\n"
        dxy += np.sqrt((xold - x) ** 2 + (yold - y) ** 2)
        xold = x
        yold = y
        for vertex in range(1, len(sorted_segments[segment])):
            x = units * (canvas.xmin + (sorted_segments[segment][vertex][0] + 0.5))
            y = units * (canvas.ymax - sorted_segments[segment][vertex][1] + 0.5)
            gcode += "G1 X{:.4f} Y{:.4f} F{}\n".format(x, y, feedrate)
            dxy += np.sqrt((xold - x) ** 2 + (yold - y) ** 2)
            xold = x
            yold = y
    gcode += """;Start of sheet footer.
;Pen Up
M300 S{}
;wait 120ms
G4 P120
;go to position for retrieving platform -- increase Z to Z25 or similar if you have trouble avoiding tool
G0 X0 Y0 Z15 F{feedrate}
;wait 300ms
G4 P300
;return to start position of current sheet
G0 Z0 F{feedrate}

;wait 300ms
G4 P300
;disengage drives
M18
;End of sheet footer
;---------------------------------------------------------------
""".format(
        pen_up, feedrate=feedrate
    )
    print("Path length: %f" % dxy)
    return gcode
