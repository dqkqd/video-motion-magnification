import numpy as np
import cv2

def rgb2ycc(im):
    
    y = im[:,:,0] * 0.114 + im[:,:,1] * 0.587 + im[:,:,2] * 0.299
    cr = (im[:,:,2] - y ) * 0.713 + 128
    cb = (im[:,:,0] - y ) * 0.564 + 128

    return y, cr, cb

def ycc2rgb(out, cr, cb):
    rgbIm = np.zeros( (out.shape[0], out.shape[1], 3 ))
    rgbIm[:,:,1] = (out - 0.714 * (cr - 128) - 0.344 * (cb - 128)).astype(int)
    rgbIm[:,:,2] = (out + 1.403 * (cr - 128)).astype(int)
    rgbIm[:,:,0] = (out + 1.773 * (cb - 128)).astype(int)
    return rgbIm

def scale_range(w, h, threshold):
    new_w = w
    new_h = h
    scale = 1

    while new_w * new_h > threshold:
        new_w /= 2
        new_h /= 2
        scale *= 2

    return scale
