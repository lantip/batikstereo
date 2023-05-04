# -*- coding: utf-8 -*-
# Forked from:
# https://bitbucket.org/denilsonsa/autostereogram

from __future__ import division, print_function, unicode_literals
from io import BytesIO
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

try:
    from PIL import Image, ImageChops, ImageOps
except ImportError:
    import Image


def random_image(dimensions):
    '''Returns a RGB image filled with random pixels.'''
    # random_integers() returns a 'int64' array
    # But PIL expects a 'uint8' array
    # I also need to swap width and height in numpy
    img = 'PIL.Image.fromarray(r, mode="RGB")'
    return img


def make_stereogram(depthmap_filename, pattern_filename, pattern_width=140, scale=0.125, dir=1, print_warnings=False, debug=False):
    '''Receives a ProgramOptions() instance, and do all the hard work!'''
    # Sanity check
    if(print_warnings
    and round(255 * scale) >= pattern_width
    ):
        print(
            'WARNING! "pattern_width" is too small for current "scale".'
        )
    #depthmap_bytes = BytesIO(depthmap_filename)
    #depthmap_img = Image.open(depthmap_bytes)
    depthmap_img = Image.open(depthmap_filename)
    # Converting to grayscale
    if(print_warnings
    and depthmap_img.mode != 'L'
    ):
        print('Warning! Converting "{0}" to grayscale.'
            .format('fff')
        )
    depthmap_img = depthmap_img.convert('L')
    pattern_img = Image.open(os.path.join(basedir,'static/img/pattern/'+pattern_filename))
    # Creating the output image
    output_img = Image.new('RGB',
        (depthmap_img.size[0] + pattern_width, depthmap_img.size[1])
    )
    # Copying the pattern to the left side of the output image
    y = 0
    while y < output_img.size[1]:
        output_img.paste(pattern_img, (0, y))
        y += pattern_img.size[1]
    # The pixel access objects, with indexes [x,y]
    depth = depthmap_img.load()
    out = output_img.load()
    # Iterating over other pixels to generate the stereogram
    for y in range(0, depthmap_img.size[1]):
        for x in range(0, depthmap_img.size[0]):
            # Find the source pixel
            sx = round(x + dir * scale * depth[x, y])
            if sx < 0:
                # In Python: -3 % 10 => 7
                sx = sx % pattern_width
            if debug:
                print("x,y=%3d,%3d depth=%3d out[%3d,%3d]=out[%3d,%3d]" % (
                    x, y, depth[x, y],
                    x + pattern_width, y,
                    sx, y
                ))
            # Copy the pixel
            out[x + pattern_width, y] = out[sx, y]
        # Fill out any remaining horizontal space.
        # Actually, this loop won't run.
        x += 1
        while x + pattern_width < output_img.size[0]:
            out[x + pattern_width, y] = out[x, y]
            x += 1
    #Show the final image
    output = BytesIO()
    output_img.save(output, format='PNG')
    return output.getvalue()
