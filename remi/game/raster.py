#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from PIL import Image


class RasterImage(object):
    data = ''
    width = 0
    height = 0


def load_image(image_file):
    image = Image.open(image_file)
    data = image.tobytes()
    data = [ord(b) for b in data]
    result = RasterImage()
    result.width = image.width
    result.height = image.height
    result.data = repr(data)
    return result


def draw(image, canvas, position):
    canvas.draw('''var canvas = document.getElementById('%s');
var ctx = canvas.getContext('2d');
var image = ctx.createImageData(%s, %s);
image.data.set(new Uint8ClampedArray(%s));
ctx.putImageData(image, %s, %s);''' % (
    canvas.id,
    image.width, image.height, image.data,
    position[0], position[1]
    ))
