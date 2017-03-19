from __future__ import print_function
import os
import sys
from mereo.inventory import Inventory


# -----------------------------------------------------------------------------
# I/O

def fullPath(fileName):
    return os.path.join('/Users/farleyj/Desktop/Bernard/', fileName)


# -----------------------------------------------------------------------------
# Inventory -> SVG

def encodeColor(key, part):
    rgb = [255, 16, 16]
    rgb[0] -= ORDER.index(key) + 1
    rgb[1] -= (part['y'] / 30)
    rgb[2] -= (part['z'] / 30)

    asHex = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return asHex


# -----------------------------------------------------------------------------
# Main

def zyyz(key, part):
    if key == 'lower-arm-left' and part['z'] == 270:
        return True

    if key == 'upper-arm-left' and part['z'] == 270:
        return True

    if key == 'hand-left' and part['z'] == 270:
        return True

    if key == 'shoulder-left' and part['z'] == 0:
        return True

    return False


if __name__ == "__main__":
    inventoryPath = fullPath('inventory.json')

    inv = Inventory().\
        updateFromSvg(fullPath('Bernard Z0.svg')).\
        updateFromSvg(fullPath('Bernard Z270.svg')).\
        updateFromSvg(fullPath('Bernard Z0 - Left Arms Y0.svg')).\
        quantize().\
        save(fullPath('inv-fluent.json')).\
        writeSvg(fullPath('inv-fluent.svg'))

    left_arm = inv.select(zyyz).translate(786 - 809, 2).\
        save(fullPath('left_arm.json')).\
        writeSvg(fullPath('left_arm.svg'))
