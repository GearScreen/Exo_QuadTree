from __future__ import annotations
from src import utils
import tkinter as tk
from tkinter import Canvas


def remove_char(string: str, pos: int) -> str:
    """Removes a character from a string at a given position"""
    return string[:pos] + string[pos + 1 :]


class QuadTree:
    NB_NODES: int = 4

    def __init__(
        self,
        list_rep: list | None,
        tl: bool | QuadTree,
        tr: bool | QuadTree,
        br: bool | QuadTree,
        bl: bool | QuadTree,
    ):
        self.list_rep = list_rep
        self.quadrants = [tl, tr, br, bl]
        self._depth = 1
        # self.find_depth()

    def __str__(self) -> str:
        def quadrant_str(base_str: str, quadrant: bool | QuadTree) -> str:
            return f"\n{base_str} {quadrant}"

        return f"Quad Tree :{quadrant_str("Top Left:", self.quadrants[1])}{quadrant_str("Top Right:", self.quadrants[2])}{quadrant_str("Bottom Right:", self.quadrants[3])}{quadrant_str("Bottom Left:", self.quadrants[4])}\n"

    def fullInfo(self) -> str:
        """Detailed information about the quadtree"""
        return f"QuadTree Infos : \nList Representation {self.list_rep} \nDepth = {self.depth} \nValues = {self}"

    @property
    def depth(self) -> int:
        """Recursion depth of the quadtree"""
        return self._depth

    @depth.setter
    def depth(self, value: int):
        """Set Depth of the Quadtree"""
        self._depth = value

    def find_depth(self):
        """Find the depth of a quadtree from its list representation"""
        depth = 1

    @staticmethod
    def fromString(tree_str: str) -> QuadTree:
        """Generates a Quadtree from a string representation"""
        clean_tree = QuadTree.flatten_tree(tree_str)
        iterator = enumerate(clean_tree)  # iter(clean_tree)

        # Start Building QuadTree
        print("\n Building QuadTree... Using :", clean_tree)
        quadTree = [4]
        depth = 1

        # Check each quadrant (4)
        for quadrant in range(0, 4):
            (index, current_char) = iterator.__next__()
            sub_tree_count = 1
            # print("Reading Tree Char :", current_char)
            if current_char == "0" or current_char == "1":
                print(f"Quadrant {quadrant} -> Bool Value Found :", current_char)
                quadTree.append(int(current_char))
            elif current_char == "[":
                # print("Sub-Tree at :", index)
                sub_tree = [current_char]
                n_sub_tree_count = 0
                sub_tree_count += 1
                if sub_tree_count > depth:
                    depth = sub_tree_count
                # Build Sub-Tree
                while current_char != "]" or n_sub_tree_count > 0:
                    (index, current_char) = iterator.__next__()
                    sub_tree.append(current_char)
                    # Count nested sub-trees
                    if current_char == "[":
                        print("N-Sub-Tree found at :", index)
                        n_sub_tree_count += 1
                        sub_tree_count += 1
                        if sub_tree_count > depth:
                            depth = sub_tree_count
                        # if n_sub_tree_count + 1 > depth:
                        # depth = n_sub_tree_count + 1
                    elif current_char == "]" and n_sub_tree_count > 0:
                        current_char = ""  # Avoid counting the closing bracket
                        n_sub_tree_count -= 1
                        sub_tree_count -= 1
                # sub_tree.append(current_char)
                sub_tree_str = "".join(sub_tree)
                print(f"Quadrant {quadrant} -> Sub-Tree Found :", sub_tree_str)
                quadTree.append(QuadTree.fromString(sub_tree_str))

        print(f" QuadTree Built : {quadTree}\n Depth : {depth}\n")
        result = QuadTree(
            clean_tree, quadTree[1], quadTree[2], quadTree[3], quadTree[4]
        )
        result.depth = depth
        return result

    def flatten_tree(tree_str: str) -> str:
        """Flattens quadtree string"""
        # print("Input tree :", tree_str)
        # utils.print_all_chars(clean_tree)
        flattened = (
            tree_str.replace(" ", "")
            .replace("\n", "")
            .replace("\t", "")
            .replace(",", "")
        )
        # utils.print_all_chars(clean_tree)
        left_clean = remove_char(flattened, 0)
        clean_tree = remove_char(left_clean, len(left_clean) - 1)
        return clean_tree

    @staticmethod
    def fromFile(filename: str) -> QuadTree:
        """Open a given file, containing a textual representation of a list"""
        with open(filename, "r") as f:
            content = f.read()
        return QuadTree.fromString(content)

    @staticmethod
    def fromList(data: list) -> QuadTree:
        """Generates a Quadtree from a list representation"""
        pass


class TkQuadTree(QuadTree):
    def __init__(self, quadtree, canvas_size=800):
        self.quadtree = quadtree
        self.canvas_size = canvas_size
        self.half_size = canvas_size // 2

    def paint(self):
        """TK representation of a Quadtree"""
        TkQuadTree.draw(
            self, lambda self: TkQuadTree.drawQuadTree(self, 0, 0, self.canvas_size)
        )

    def draw(self, drawFunc):
        """Draw Anything on the TK Canvas"""
        root = tk.Tk()
        root.title("Quadtree Renderer")
        root.geometry("900x900")
        # Create canvas
        self.canvas = tk.Canvas(
            root, width=self.canvas_size, height=self.canvas_size, bg="gray"
        )
        self.canvas.pack(pady=20)

        drawFunc(self)  # Draw Whatever

        self.canvas.pack()
        root.mainloop()

    def drawQuadTree(self, x_start: int, y_start: int, size: int):
        """Logic to draw the Quadtree on the canvas"""
        quadrants = self.quadtree.quadrants
        half_size = size // 2

        def drawQuadrant(self, index):
            quadrant = quadrants[index]
            cell_color = lambda: "White" if quadrant == 1 else "Black"
            x_pos = 0
            y_pos = 0

            match index:
                case 0:  # Top-Left
                    x_pos = x_start
                    y_pos = y_start
                case 1:  # Top-Right
                    x_pos = x_start + half_size
                    y_pos = y_start
                case 2:  # Bottom-Left
                    x_pos = x_start + half_size
                    y_pos = y_start + half_size
                case 3:  # Bottom-Right
                    x_pos = x_start
                    y_pos = y_start + half_size
                case _:
                    pass

            if isinstance(quadrant, int):
                # Quadrant is a leaf
                TkQuadTree.drawCell(
                    self,
                    x_pos,
                    y_pos,
                    half_size,
                    cell_color(),
                )
            elif isinstance(quadrant, QuadTree):
                # Quadrant is a sub-tree
                newDrawer = TkQuadTree(quadrant)
                newDrawer.canvas = self.canvas
                newDrawer.drawQuadTree(x_pos, y_pos, half_size)

        drawQuadrant(self, 0)
        drawQuadrant(self, 1)
        drawQuadrant(self, 2)
        drawQuadrant(self, 3)

        # Draw Grid at the end (on top)
        TkQuadTree.drawQuadrantGrid(self, x_start, y_start, half_size)

    def drawQuadrantGrid(self, x_start: int, y_start: int, size: int):
        """Draws the quadrant grid on the canvas"""
        x_half = x_start + size
        y_half = y_start + size
        # Horizontal
        self.canvas.create_line(
            x_start, y_half, x_start + size * 2, y_half, fill="red", width=2
        )
        # Vertical
        self.canvas.create_line(
            x_half, y_start, x_half, y_start + size * 2, fill="red", width=2
        )

    def drawCell(self, x_start: int, y_start: int, size: int, color: str = "black"):
        """Draw a Quadrant Cell"""
        self.canvas.create_rectangle(
            x_start,
            y_start,
            x_start + size,
            y_start + size,
            fill=color,
            outline="gray",
            width=1,
        )
