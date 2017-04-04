from mereo import ORDER
from svgpathtools import wsvg, parse_path


def encodeColor(key, part):
    rgb = [255, 16, 16]
    rgb[0] -= ORDER.index(key) + 1
    rgb[1] -= (part['y'] / 30)
    rgb[2] -= (part['z'] / 30)

    asHex = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return asHex


class Svg(object):
    """implemented as a fluent interface"""

    # -------------------------------------------------------------------------
    # Customization Methods

    def __init__(self, inventory):
        self.inventory = inventory
        self.clear()

    # -------------------------------------------------------------------------
    # Non-fluent methods

    def _add(self, pathAsString, attribute):
        self.paths.append(parse_path(pathAsString))
        self.attributes.append(attribute)

    # -------------------------------------------------------------------------
    # Fluent Methods

    def clear(self):
        self.paths = []
        self.attributes = []
        self.svg_attributes = {
            'width': 2000,
            'height': 1800
        }
        return self

    def showGrid(self):
        style = {
            'stroke-width': 1,
            'stroke':  '#330033',
            'fill': 'none',
            'opacity': .3
        }

        xMajor = [
            142, 245, 348, 451, 554, 658, 762, 866, 970, 1074, 1179, 1283,
            1386, 1490, 1594, 1697, 1802, 1905
        ]
        yMajor = [
            100, 203, 306, 409, 512, 616, 720, 824, 928, 1032, 1137, 1241,
            1344
        ]

        s = ''
        for x in xMajor:
            s += 'M {0},{1} L{0},{2} '.format(x, yMajor[0], yMajor[-1])

        self._add(s, style)

        s = ''
        for y in yMajor:
            s += 'M {1},{0} L{2},{0} '.format(y, xMajor[0], xMajor[-1])

        self._add(s, style)

        return self

    def showBoundingBoxes(self):
        style = {
            'stroke-width': 2,
            'stroke':  '#0000ff',
            'fill': 'none',
            'opacity': .5
        }

        for key, part in self.inventory:
            path = parse_path(part['d'])
            x0, x1, y0, y1 = path.bbox()
            s = 'M{0},{1} L{0},{3} L{2},{3} L{2},{1} Z'.format(x0, y0, x1, y1)
            self._add(s, style)

        return self

    def showParts(self):
        for key, part in self.inventory:
            att = {
                'id': key + part.ID,
                'stroke-width': 2,
                'stroke':  encodeColor(key, part),
                'fill': 'none',
                'opacity': 1
            }
            self._add(part['d'], att)

        return self

    def write(self, filename):
        wsvg(self.paths,
             attributes=self.attributes,
             svg_attributes=self.svg_attributes,
             filename=filename)

        return self
