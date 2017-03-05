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
# Inventory

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
    saveInventory(inv, INVENTORY_FILE)
