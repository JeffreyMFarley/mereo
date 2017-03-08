from __future__ import print_function
import os
import sys


# -----------------------------------------------------------------------------
# I/O

def fullPath(fileName):
    return os.path.join('/Users/farleyj/Desktop/Bernard/', fileName)


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

ORDER = [
    'head',
    'eye-left', 'eye-right',
    'nose', 'mouth',
    'hair',
    'head-cover',
    'shoulder-right', 'shoulder-left',
    'upper-arm-right', 'upper-arm-left',
    'hips',
    'upper-leg-right', 'upper-leg-left',
    'lower-leg-right', 'lower-leg-left',
    'foot-right', 'foot-left',
    'trunk',
    'lower-arm-right', 'lower-arm-left',
    'hand-right', 'hand-left'
]


def quantizeAll(inventory):
    for key in ORDER:
        if key in inventory:
            print(key)
            for part in inventory[key]:
                quantize(part)
                toConsole(part)


# -----------------------------------------------------------------------------
# Inventory I/O

def loadInventory(filename):
    import json
    from collections import defaultdict
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except IOError:
        # no such file, create an empty dictionary
        return defaultdict(list)


def saveInventory(inventory, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(inventory, f, sort_keys=True, indent=2,
                  separators=(',', ': '))


# -----------------------------------------------------------------------------
# Inventory -> SVG

def encodeColor(key, part):
    rgb = [255, 16, 16]
    rgb[0] -= ORDER.index(key) + 1
    rgb[1] -= (part['y'] / 30)
    rgb[2] -= (part['z'] / 30)

    asHex = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return asHex


def writeSvg(subset, filename):
    from svgpathtools import wsvg, parse_path

    paths = []
    attributes = []
    svg_attributes = {
        'width': 2000,
        'height': 1800
    }

    for key in ORDER:
        if key in subset:
            for part in subset[key]:
                path = parse_path(part['d'])
                paths.append(path)
                att = {
                    'id': key + annotation(part),
                    'stroke-width': 2,
                    'stroke': encodeColor(key, part),
                    'fill': 'none',
                    'opacity': 1
                }
                attributes.append(att)

    wsvg(paths, attributes=attributes, svg_attributes=svg_attributes,
         filename=filename)


# -----------------------------------------------------------------------------
# Actions

def createInventory(inventoryPath, svgPath, quantize=True):
    from collections import defaultdict
    inv = defaultdict(list)
    updateFromSvg(inv, svgPath)
    if quantize:
        quantizeAll(inv)
    saveInventory(inv, inventoryPath)


def updateInventory(inventoryPath, svgPath, quantize=True):
    inv = loadInventory(inventoryPath)
    updateFromSvg(inv, svgPath)
    if quantize:
        quantizeAll(inv)
    saveInventory(inv, inventoryPath)


def drawInventory(inventoryPath, svgPath):
    inv = loadInventory(inventoryPath)
    # TODO select parts
    writeSvg(inv, svgPath)

# -----------------------------------------------------------------------------
# Main

if __name__ == "__main__":
    inventoryPath = fullPath('inventory.json')
