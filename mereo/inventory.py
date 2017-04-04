from mereo import ORDER
from mereo.part import Part


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
            for key, parts in d.items():
                for pid, a in parts.items():
                    tokens = pid.split('_')
                    part = Part(a['d'])
                    part.ID = tokens
                    instance._mergePart(key, part)
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

    # -------------------------------------------------------------------------
    # Predicate Logic

    def select(self, fn):
        clone = Inventory()
        for key, part in self:
            if fn(key, part):
                clone._mergePart(key, part)
        return clone

    def selectPose(self, partList):
        clone = Inventory()
        for key, part in self:
            if key + part.ID in partList:
                clone._mergePart(key, part)
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
