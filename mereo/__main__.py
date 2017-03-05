from __future__ import print_function
import os
import sys


def extractAnnotations(entry, annotations):
    for annot in annotations:
        for dim in ['x', 'y', 'z']:
            if dim in annot:
                try:
                    entry[dim] = int(annot[1:])
                except:
                    entry['other'] = annot


def buildInventory(attributes):
    from collections import defaultdict

    r = defaultdict(list)
    for i, a in enumerate(attributes):
        if 'id' in a:
            annotations = a['id'].split('_')
            entry = {
                'd': a['d'],
                'x': 0,
                'y': 0,
                'z': 0,
                'other': ''
            }

            extractAnnotations(entry, annotations[1:])
            r[annotations[0]].append(entry)

    return r


if __name__ == "__main__":
    from svgpathtools import svg2paths2, wsvg
    import json

    _, attributes, _ = svg2paths2(
        '/Users/farleyj/Desktop/Bernard.svg'
    )

    inventory = buildInventory(attributes)

    with open('/Users/farleyj/Desktop/inventory.json', 'w') as f:
        json.dump(inventory, f, sort_keys=True, indent=2,
                  separators=(',', ': '))

    # wsvg(paths,
    #      attributes=attributes,
    #      svg_attributes=svg_attributes,
    #      filename='/Users/farleyj/Desktop/output.svg')
