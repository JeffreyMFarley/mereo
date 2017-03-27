from mereo import ORDER
from mereo.part import Part


def encodeColor(key, part):
    rgb = [255, 16, 16]
    rgb[0] -= ORDER.index(key) + 1
    rgb[1] -= (part['y'] / 30)
    rgb[2] -= (part['z'] / 30)

    asHex = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return asHex


class Inventory(object):
    """implemented as a fluent interface"""

    # -------------------------------------------------------------------------
    # Customization Methods

    def __init__(self):
        from collections import defaultdict
        self.inv = defaultdict(dict)

    def __len__(self):
        return len(self.inv)

    def __iter__(self):
        for key in ORDER:
            if key in self.inv:
                for part in self.inv[key].values():
                    yield key, part

    # -------------------------------------------------------------------------
    # Non-fluent methods

    def _mergePart(self, key, part):
        self.inv[key][part.ID] = part

    # -------------------------------------------------------------------------
    # I/O

    @staticmethod
    def load(filename):
        instance = Inventory()

        import json
        try:
            with open(filename, 'r') as f:
                d = json.load(f)
            for k, v in d.items():
                instance.inv[k] = v
        except IOError:
            pass

        return instance

    def save(self, filename):
        import json
        with open(filename, 'w') as f:
            json.dump(self.inv, f, sort_keys=True, indent=2,
                      separators=(',', ': '))
        return self

    # -------------------------------------------------------------------------
    # SVG I/O

    def updateFromSvg(self, filename):
        from svgpathtools import svg2paths2

        _, attributes, _ = svg2paths2(filename)

        for i, a in enumerate(attributes):
            if 'id' in a:
                tokens = a['id'].split('_')
                part = Part(a['d'])
                part.ID = tokens[1:]
                self._mergePart(tokens[0], part)

        return self

    def writeSvg(self, filename):
        from svgpathtools import wsvg, parse_path

        paths = []
        attributes = []
        svg_attributes = {
            'width': 2000,
            'height': 1800
        }

        for key, part in self:
            path = parse_path(part['d'])
            paths.append(path)
            att = {
                'id': key + part.ID,
                'stroke-width': 2,
                'stroke':  encodeColor(key, part),
                'fill': 'none',
                'opacity': 1
            }
            attributes.append(att)

        wsvg(paths, attributes=attributes, svg_attributes=svg_attributes,
             filename=filename)

        return self

    # -------------------------------------------------------------------------
    # Predicate Logic

    def select(self, fn):
        clone = Inventory()
        for key, part in self:
            if fn(key, part):
                clone.inv[key].append(part)
        return clone

    # -------------------------------------------------------------------------
    # Actions

    def merge(self, other):
        for key, part in other:
            self._mergePart(key, part)
        return self

    def quantize(self):
        for _, part in self:
            part.quantize()
        return self

    def toConsole(self):
        for key in ORDER:
            if key in self.inv:
                print(key)
                for part in self.inv[key]:
                    part.toConsole()
        return self

    def translate(self, x, y):
        for _, part in self:
            part.translate(x, y)
        return self
