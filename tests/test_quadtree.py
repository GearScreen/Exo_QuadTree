import sys, os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from src import QuadTree, TkQuadTree


def test_sample():
    filename = "files/quadtree.txt"
    q = QuadTree.fromFile(filename)
    assert q.depth == 4


def test_single():
    filename = "files/quadtree_easy.txt"
    q = QuadTree.fromFile(filename)
    assert q.depth == 1


def test_custom():
    quadTree = QuadTree.fromString("[[0,1,0,0],0,0,0]")
    # quadTree = QuadTree.fromString("[1,0,1,0]")
    # print(quadTree)
    # print("Depth :", quadTree.depth)
    # TkQuadTree(quadTree).draw(test_draw)
    TkQuadTree(quadTree).paint()


def test_Tk():
    filename = "files/quadtree.txt"
    q = QuadTree.fromFile(filename)
    TkQuadTree(q).paint()


def test_draw_start(quadTree_drawer):
    quadTree_drawer.drawCell(500, 500, 50)
    quadTree_drawer.drawCell(0, 0, 50)
    quadTree_drawer.drawCell(50, 0, 50, "red")
    quadTree_drawer.drawCell(0, 50, 50, "green")


def test_draw(quadTree_drawer):
    # Draw Cells
    quadTree_drawer.drawCell(0, 0, 200)

    # Draw Quadrant Grid
    half_size = quadTree_drawer.half_size
    quadTree_drawer.drawQuadrantGrid(0, 0, half_size)
    quadTree_drawer.drawQuadrantGrid(0, 0, 200)
    quadTree_drawer.drawQuadrantGrid(half_size, 0, 200)


# print(sys.getrecursionlimit())
# sys.setrecursionlimit(2000)

# test_single()
# test_custom()
# test_sample()
test_Tk()
