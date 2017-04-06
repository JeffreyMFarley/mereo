from __future__ import print_function
from mereo import ORDER
from mereo.inventory import Inventory
from mereo.part import Part
from svgpathtools import parse_path, Path, Line, CubicBezier


def _delta(a, b, step, gaps):
    d = float(b - a) / float(gaps)
    return a + d * step


def _deltaPoints(a, b, step, gap):
    points = []
    for i in range(len(a)):
        x = _delta(a[i].real, b[i].real, step, gap)
        y = _delta(a[i].imag, b[i].imag, step, gap)
        points.append(complex(x, y))
    return points


def generateInBetweens(poseA, poseB, steps):
    inv = Inventory()

    # make pairs
    pairs = []
    for key in ORDER:
        if key in poseA.inv and key in poseB.inv:
            partA = poseA.inv[key]
            partB = poseB.inv[key]

            if len(partA) != 1 or len(partB) != 1:
                print('Too many parts {0} - A: {1} B: {2}'.format(
                    key, partA.keys(), partB.keys()
                ))
                continue

            pairs.append((key, partA.values()[0], partB.values()[0]))

    # If there are 3 steps, there are 4 gaps between start and finish
    # |------1------2------3------|
    gaps = steps + 1

    # process pairs
    for key, a, b in pairs:
        pathA = parse_path(a['d'])
        pathB = parse_path(b['d'])

        if len(pathA) != len(pathB):
            print('Unmatched segments {0} - A: {1} B: {2}'.format(
                key, pathA, pathB
            ))
            continue

        for step in range(1, gaps):
            newPath = Path()
            for i in range(len(pathA)):
                segA = pathA[i]
                segB = pathB[i]

                if isinstance(segA, Line):
                    points = _deltaPoints(
                        [segA.start, segA.end],
                        [segB.start, segB.end],
                        step, gaps
                    )
                    newPath.append(Line(*points))

                elif isinstance(segA, CubicBezier):
                    points = _deltaPoints(
                        [segA.start, segA.control1, segA.control2, segA.end],
                        [segB.start, segB.control1, segB.control2, segB.end],
                        step, gaps
                    )
                    newPath.append(CubicBezier(*points))

            newPart = Part(newPath.d())
            newPart['x'] = int(_delta(a['x'], b['x'], step, gaps))
            newPart['y'] = int(_delta(a['y'], b['y'], step, gaps))
            newPart['z'] = int(_delta(a['z'], b['z'], step, gaps))

            inv.addPart(key, newPart)
            print(key, step, newPart)

    return inv
