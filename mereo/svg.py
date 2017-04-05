from mereo import ORDER
from svgpathtools import wsvg, parse_path


def encodeColor(key, part):
    rgb = [255, 24, 24]
    rgb[0] -= ORDER.index(key) + 1
    rgb[1] -= (part['y'] / 15)
    rgb[2] -= (part['z'] / 15)

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

    def _tryGetGrids(self):
        return self.inventory.xMajor, self.inventory.yMajor

    # -------------------------------------------------------------------------
    # Fluent Methods

    def clear(self):
        self.paths = []
        self.attributes = []
        self.svg_attributes = {
            'size': ('2000', '1800')
        }
        return self

    def showGrid(self):
        majorStyle = {
            'stroke-width': 2,
            'stroke':  '#999999',
            'fill': 'none',
            'opacity': .3
        }
        minorStyle = {
            'stroke-width': 1,
            'stroke':  '#999999',
            'fill': 'none',
            'opacity': .3
        }

        xMajor, yMajor = self._tryGetGrids()
        tics = 5

        s = ''
        for x in xMajor:
            s += 'M {0},{1} L{0},{2} '.format(x, yMajor[0], yMajor[-1])
        for y in yMajor:
            s += 'M {1},{0} L{2},{0} '.format(y, xMajor[0], xMajor[-1])
        self._add(s, majorStyle)

        s = ''
        for i in range(len(xMajor) - 1):
            dx = float(xMajor[i+1] - xMajor[i]) / tics
            for xx in range(1, tics):
                s += 'M {0},{1} L{0},{2} '.format(
                    xx * dx + xMajor[i], yMajor[0], yMajor[-1]
                )
        for i in range(len(yMajor) - 1):
            dy = float(yMajor[i+1] - yMajor[i]) / tics
            for yy in range(1, tics):
                s += 'M {1},{0} L{2},{0} '.format(
                    yy * dy + yMajor[i], xMajor[0], xMajor[-1]
                )

        self._add(s, minorStyle)

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
