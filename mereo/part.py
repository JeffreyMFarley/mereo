from __future__ import print_function
from svgpathtools import parse_path, Path, Line, CubicBezier


def formatPoint(point):
    return '{0:10.3f}, {1:10.3f}'.format(point.real, point.imag)


class Part(dict):
    """implemented as a fluent interface"""

    # -------------------------------------------------------------------------
    # Customization Methods

    def __init__(self, d):
        self['d'] = d
        self['x'] = 0
        self['y'] = 0
        self['z'] = 0
        self['other'] = ''

    def __repr__(self):
        return 'Part(\'%s\')' % self['d']

    def __str__(self):
        return ', '.join([
            '{}={}'.format(k, self[k]) for k in ['x', 'y', 'z', 'other']
        ])

    # -------------------------------------------------------------------------
    # Properties

    @property
    def ID(self):
        s = '_'.join([
            '{}{}'.format(k, self[k]) for k in ['x', 'y', 'z'] if self[k]
        ])

        if self['other']:
            s += '_' + self['other'] if s else self['other']

        return '_' + s if s else ''

    @ID.setter
    def ID(self, tokens):
        for token in tokens:
            for dim in ['x', 'y', 'z']:
                if dim in token:
                    try:
                        self[dim] = int(token[1:])
                    except:
                        self['other'] = token
        return self

    # -------------------------------------------------------------------------
    # Actions

    def quantize(self):
        path = parse_path(self['d'])
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
                    complex(
                        round(seg.control1.real), round(seg.control1.imag)
                    ),
                    complex(
                        round(seg.control2.real), round(seg.control2.imag)
                    ),
                    complex(round(seg.end.real), round(seg.end.imag))
                )
                newPath.append(newSeg)

        self['d'] = newPath.d()
        return self

    def snap(self, tree, threshold):
        def process(points):
            for i, p in enumerate(points):
                best, _, dist = tree.nearest_neighbor([p.real, p.imag])

                if dist < threshold:
                    points[i] = complex(best[0], best[1])
            return points

        path = parse_path(self['d'])
        newPath = Path()
        for seg in path:
            points = process([seg.start, seg.end])

            if isinstance(seg, Line):
                newSeg = Line(*points)
                newPath.append(newSeg)

            elif isinstance(seg, CubicBezier):
                newSeg = CubicBezier(
                    points[0], seg.control1, seg.control2, points[1]
                )
                newPath.append(newSeg)

        self['d'] = newPath.d()
        return self

    def toConsole(self):
        print('\t', self)
        path = parse_path(self['d'])
        for seg in path:
            if isinstance(seg, Line):
                print('\t\tLine',
                      formatPoint(seg.start),
                      ' ' * 22,
                      ' ' * 22,
                      formatPoint(seg.end))
            elif isinstance(seg, CubicBezier):
                print('\t\tCubB',
                      formatPoint(seg.start),
                      formatPoint(seg.control1),
                      formatPoint(seg.control2),
                      formatPoint(seg.end))
            else:
                raise TypeError("seg must be a path segment.")

        return self

    def translate(self, x, y):
        path = parse_path(self['d'])
        newPath = path.translated(complex(x, y))
        self['d'] = newPath.d()
        return self
