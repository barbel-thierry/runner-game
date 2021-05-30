import random

from kivy.core.window import Window

from tree import Tree


def outer_trees(trees, tree_size):
    if len(trees) < 10:
        for i in range(random.randint(0, 2)):
            (x, y) = tree_size
            trees.append(
                Tree(
                    pos=(random.randint(-x, Window.width), random.randint(-y * 3, -y)),
                    size=tree_size,
                    alpha=0
                )
            )


def nearest_to_furthest(trees):
    sorted(trees, key=lambda tree: tree.pos[1], reverse=True)


def move_backward(trees, tree_size, pace):
    for tree in trees:
        (x, y) = tree.pos
        y += pace
        if y > Window.height:
            trees.remove(tree)
            tree.alpha = 0
            return
        tree.pos = (x, y)
        tree.alpha = 1
    outer_trees(trees, tree_size)
    nearest_to_furthest(trees)


def move_laterally(trees, pace):
    for tree in trees:
        (x, y) = tree.pos
        x += pace
        if x < -tree.size[0]:
            x = Window.width
        elif x > Window.width:
            x = -tree.size[0]
        tree.pos = (x, y)


def has_collide(trees):
    for tree in trees:
        (x, y) = tree.pos
        (size_x, size_y) = tree.size
        if x < int(Window.width / 2) < x + size_x and -50 < y < 0:
            return True
    return False
