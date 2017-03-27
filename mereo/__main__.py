import os
from mereo.inventory import Inventory


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
    if part['y'] == 0:
        return True

    return False


if __name__ == "__main__":
    inventoryPath = fullPath('inventory.json')

    # inv = Inventory().\
    #     updateFromSvg(fullPath('Bernard Z0.svg')).\
    #     updateFromSvg(fullPath('Bernard Z270.svg')).\
    #     quantize()

    # left_arm = Inventory().\
    #     updateFromSvg(fullPath('Bernard Z0 - Left Arms Y0.svg')).\
    #     quantize().\
    #     translate(786 - 809, 2)

    # inv.merge(left_arm).\
    #     save(inventoryPath).\
    #     select(anatomical).\
    #     writeSvg(fullPath('ready.svg'))

    inv = Inventory().load(inventoryPath).\
        selectPose(pose_z0 + pose_z270).\
        writeSvg(fullPath('ready.svg'))

    inv = Inventory().load(inventoryPath).\
        select(anatomical).\
        writeSvg(fullPath('quantized0.svg'))
