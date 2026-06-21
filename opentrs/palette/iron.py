import numpy as np


def render_iron(temp, minimum, maximum):

    t = (temp - minimum) / (maximum - minimum)
    t = np.clip(t, 0, 1)

    r = np.clip(255 * (t ** 1.5), 0, 255)
    g = np.clip(255 * (t ** 0.7), 0, 255)
    b = np.clip(255 * (1 - t) ** 2, 0, 255)

    return np.stack([r, g, b], axis=-1).astype(np.uint8)