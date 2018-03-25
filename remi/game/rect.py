#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


class Rect(object):
    def __init__(self, position, size):
        self.x = position[0]
        self.y = position[1]
        self.w = size[0]
        self.h = size[1]

    def __str__(self):
        return '%s, %s, %s, %s' % (self.x, self.y, self.w, self.h)

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h
    
    @property
    def centerx(self):
        return self.x + (self.w / 2)

    @property
    def centery(self):
        return self.y + (self.h / 2)

    @property
    def center(self):
        return (self.centerx, self.centery)

    @property
    def size(self):
        return (self.w, self.h)

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w
    
    @property
    def topleft(self):
        return (self.left, self.top)

    @property
    def bottomleft(self):
        return (self.left, self.bottom)

    @property
    def topright(self):
        return (self.right, self.top)

    @property
    def bottomright(self):
        return (self.right, self.bottom)

    @property
    def midtop(self):
        return (self.centerx, self.top)

    @property
    def midleft(self):
        return (self.left, self.centery)

    @property
    def midbottom(self):
        return (self.centerx, self.bottom)

    @property
    def midright(self):
        return (self.right, self.centery)
