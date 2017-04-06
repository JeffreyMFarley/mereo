import os
from mereo.in_betweens import generateInBetweens
from mereo.inventory import Inventory
from mereo.svg import Svg


# -----------------------------------------------------------------------------
# I/O

def fullPath(fileName):
    return os.path.join('/Users/farleyj/Desktop/Bernard/', fileName)


# -----------------------------------------------------------------------------
# Main

pose_neutral = [
    'foot-left',
    'foot-right',
    'hand-left_z270',
    'hand-right_z90',
    'hips',
    'lower-arm-left_z270',
    'lower-arm-right_z90',
    'lower-leg-left',
    'lower-leg-right',
    'shoulder-left',
    'shoulder-right',
    'trunk',
    'upper-arm-left_z270',
    'upper-arm-right_z90',
    'upper-leg-left',
    'upper-leg-right'
]

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

    inv = Inventory().load(inventoryPath).\
        selectPose(pose_neutral + pose_z270)

    parts = generateInBetweens(
        inv.selectPose(pose_neutral), inv.selectPose(pose_z270), 1
    )

    inv.merge(parts)

    svg = Svg(inv).showGrid().\
        showParts().\
        write(fullPath('foo.svg'))
    # inv.snap(8)
    # svg.clear().showGrid().\
    #     showParts().\
    #     write(fullPath('bar.svg'))
    # inv.save(fullPath('tighten.json'))
