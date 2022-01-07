import random


def GenMap(add_block, materials):
    material = random.choice(list(materials.values()))
    n = 2 ** 5  # 1/2 width and height of world
    s = 1  # step size
    y = 0  # initial y height
    for x in range(-n, n + 1, s):
        print(x)
        for z in range(-n, n + 1, s):
            for y1 in range(-n * 2, 0, s):
                # create a layer stone a grass everywhere.
                add_block((x, y1, z), material, immediate=False)
