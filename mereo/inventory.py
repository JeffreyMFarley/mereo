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
    # Properties

    @property
    def xMajor(self):
        return [
            141, 245, 349, 452, 556, 660, 764, 868, 972, 1076, 1180, 1284,
            1388, 1492, 1596, 1700, 1804, 1908
        ]

    @property
    def yMajor(self):
        return [
            100, 204, 308, 412, 516, 620, 724, 828, 932, 1036, 1140, 1244, 1348
        ]

    # -------------------------------------------------------------------------
    # Non-fluent methods

    def addPart(self, key, part):
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
                    instance.addPart(key, part)
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
                self.addPart(tokens[0], part)

        return self

    # -------------------------------------------------------------------------
    # Predicate Logic

    def select(self, fn):
        clone = Inventory()
        for key, part in self:
            if fn(key, part):
                clone.addPart(key, part)
        return clone

    def selectPose(self, partList):
        clone = Inventory()
        for key, part in self:
            if key + part.ID in partList:
                clone.addPart(key, part)
        return clone

    # -------------------------------------------------------------------------
    # Actions

    def merge(self, other):
        for key, part in other:
            self.addPart(key, part)
        return self

    def quantize(self):
        for _, part in self:
            part.quantize()
        return self

    def snap(self, threshold):
        from hew import KDTree

        tics = 5

        xcells = list(self.xMajor)
        for i in range(len(self.xMajor) - 1):
            dx = float(self.xMajor[i+1] - self.xMajor[i]) / tics
            for xx in range(1, tics):
                xcells.append(xx * dx + self.xMajor[i])

        ycells = list(self.yMajor)
        for i in range(len(self.yMajor) - 1):
            dy = float(self.yMajor[i+1] - self.yMajor[i]) / tics
            for yy in range(1, tics):
                ycells.append(yy * dy + self.yMajor[i])

        pairs = []
        for x in xcells:
            for y in ycells:
                pairs.append(([x, y], []))

        tree = KDTree(pairs)

        for key, part in self:
            part.snap(tree, threshold)

        return self

    def toConsole(self):
        for key in ORDER:
            if key in self.inv:
                print(key)
                for part in self.inv[key].values():
                    part.toConsole()
        return self

    def translate(self, x, y):
        for _, part in self:
            part.translate(x, y)
        return self
