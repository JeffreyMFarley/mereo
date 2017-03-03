from __future__ import print_function
import os
import sys

if __name__ == "__main__":
    from svgpathtools import svg2paths2, wsvg
    paths, attributes, svg_attributes = svg2paths2(
        '/Users/farleyj/Desktop/Bernard.svg'
    )

    for x in paths:
        print(x)

    for a in attributes:
        print(a)

    for sa in svg_attributes:
        print(sa)

    wsvg(paths,
         attributes=attributes,
         svg_attributes=svg_attributes,
         filename='/Users/farleyj/Desktop/output.svg')
