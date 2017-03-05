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


# -----------------------------------------------------------------------------
# Inventory Operations

def quantizeAll(inventory):
    for key, parts in inventory.items():
        print(key)
        for part in parts:
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

def writeSvg(entries):
    from svgpathtools import wsvg
    # wsvg(paths,
    #      attributes=attributes,
    #      svg_attributes=svg_attributes,
    #      filename='/Users/farleyj/Desktop/output.svg')
    pass

# -----------------------------------------------------------------------------
# Main

if __name__ == "__main__":
    inv = loadInventory(INVENTORY_FILE)
    updateFromSvg(inv, INPUT_SVG)
    quantizeAll(inv)
    saveInventory(inv, INVENTORY_FILE)
