from __future__ import print_function
import os
import sys

INPUT_SVG = '/Users/farleyj/Desktop/Bernard.svg'
INVENTORY_FILE = '/Users/farleyj/Desktop/inventory.json'


# -----------------------------------------------------------------------------
# SVG -> Inventory

def extractAnnotations(part, annotations):
    for annot in annotations:
        for dim in ['x', 'y', 'z']:
            if dim in annot:
                try:
                    part[dim] = int(annot[1:])
                except:
                    part['other'] = annot


def updateFromSvg(inventory, filename):
    from svgpathtools import svg2paths2

    _, attributes, _ = svg2paths2(filename)

    for i, a in enumerate(attributes):
        if 'id' in a:
            annotations = a['id'].split('_')
            part = {
                'd': a['d'],
                'x': 0,
                'y': 0,
                'z': 0,
                'other': ''
            }

            extractAnnotations(part, annotations[1:])
            inventory[annotations[0]].append(part)

    return inventory


# -----------------------------------------------------------------------------
# Part Operations

def formatPoint(point):
    return '{0:10.3f}, {1:10.3f}'.format(point.real, point.imag)


def annotation(part):
    s = '_'.join([
        '{}{}'.format(k, part[k]) for k in ['x', 'y', 'z'] if part[k]
    ])

    if part['other']:
        s += '_' + part['other'] if s else part['other']

    return '_' + s if s else ''


def name(part):
    return ', '.join([
        '{}={}'.format(k, part[k]) for k in ['x', 'y', 'z', 'other']
    ])


def toConsole(part):
    from svgpathtools import parse_path, Line, CubicBezier

    print(name(part))
    path = parse_path(part['d'])
    for seg in path:
        if isinstance(seg, Line):
            print('\tLine',
                  formatPoint(seg.start),
                  ' ' * 22,
                  ' ' * 22,
                  formatPoint(seg.end))
        elif isinstance(seg, CubicBezier):
            print('\tCubB',
                  formatPoint(seg.start),
                  formatPoint(seg.control1),
                  formatPoint(seg.control2),
                  formatPoint(seg.end))
        else:
            raise TypeError("seg must be a path segment.")


def quantize(part):
    from svgpathtools import parse_path, Path, Line, CubicBezier

    path = parse_path(part['d'])
    newPath = Path()
    for seg in path:
        if isinstance(seg, Line):
            newSeg = Line(
                complex(round(seg.start.real), round(seg.start.imag)),
                complex(round(seg.end.real), round(seg.end.imag))
            )
            newPath.append(newSeg)

        elif isinstance(seg, CubicBezier):
            newSeg = CubicBezier(
                complex(round(seg.start.real), round(seg.start.imag)),
                complex(round(seg.control1.real), round(seg.control1.imag)),
                complex(round(seg.control2.real), round(seg.control2.imag)),
                complex(round(seg.end.real), round(seg.end.imag))
            )
            newPath.append(newSeg)

    part['d'] = newPath.d()


# -----------------------------------------------------------------------------
# Inventory Operations

def quantizeAll(inventory):
    for key, parts in inventory.items():
        print(key)
        for part in parts:
            quantize(part)
            toConsole(part)


# -----------------------------------------------------------------------------
# Inventory I/O

def loadInventory(filename):
    from collections import defaultdict
    return defaultdict(list)


def saveInventory(inventory, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(inventory, f, sort_keys=True, indent=2,
                  separators=(',', ': '))


# -----------------------------------------------------------------------------
# Inventory -> SVG

def writeSvg(subset, filename):
    from svgpathtools import wsvg, parse_path

    paths = []
    attributes = []

    for key, parts in subset.items():
        for part in parts:
            path = parse_path(part['d'])
            paths.append(path)
            att = {
                'id': key + annotation(part),
                'stroke-width': 2,
                'stroke': '#ff0000',
                'fill': 'none',
                'opacity': 1
            }
            attributes.append(att)

    wsvg(paths, attributes=attributes, filename=filename)

# -----------------------------------------------------------------------------
# Main

if __name__ == "__main__":
    inv = loadInventory(INVENTORY_FILE)
    updateFromSvg(inv, INPUT_SVG)
    quantizeAll(inv)
    saveInventory(inv, INVENTORY_FILE)
    writeSvg(inv, '/Users/farleyj/Desktop/output.svg')
