import os
from mereo.inventory import Inventory
from mereo.svg import Svg


# -----------------------------------------------------------------------------
# I/O

def fullPath(fileName):
    return os.path.join('/Users/farleyj/Desktop/Bernard/', fileName)


# -----------------------------------------------------------------------------
# Main

pose_z0 = [
    'foot-left',
    'foot-right',
    'hand-left_y90_splayed',
    'hand-right_z90',
    'hips',
    'lower-arm-left_y90',
    'lower-arm-right_z90',
    'lower-leg-left',
    'lower-leg-right',
    'shoulder-left_y90',
    'shoulder-right',
    'trunk',
    'upper-arm-left_y90',
    'upper-arm-right_z90',
    'upper-leg-left',
    'upper-leg-right'
]

pose_z270 = [
    'foot-left_z270',
    'hips_z270',
    'lower-arm-left_z180',
    'lower-leg-left_z270',
    'shoulder-left_z270',
    'trunk_z270',
    'upper-arm-left_z180',
    'upper-leg-left_z270'
]


def anatomical(key, part):
    if part['y'] == 0 and part['z'] == 0:
        return True

    return False


if __name__ == "__main__":
    inventoryPath = fullPath('inventory.json')

    # inv = Inventory().\
    #     updateFromSvg(fullPath('bar.svg')).\
    #     quantize().\
    #     translate(786 - 809, 2).\
    #     selectPose(pose_z0).\
    #     save(fullPath('foo.json')).\

    inv = Inventory().load(inventoryPath).\
        select(anatomical)

    svg = Svg(inv).showGrid().\
        write(fullPath('step0.svg')).\
        showBoundingBoxes().\
        write(fullPath('step1.svg')).\
        showParts().\
        write(fullPath('step2.svg')).\
        clear().\
        showParts().\
        write(fullPath('step3.svg'))
