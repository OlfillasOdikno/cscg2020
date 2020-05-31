from PIL import Image

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Map:

    def __init__(self):
        self.map = []
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)


    def load(self, path):
        im = Image.open(path)
        w, h = im.size
        v= list(map(lambda p: 1 if (p[0]+p[1]+p[2])//3>127 else 0,im.getdata()))
        self.grid = Grid(matrix=[v[i*w:(i+1)*w] for i in range(h)])

    
    def width(self):
        return len(self.map[0])

    def height(self):
        return len(self.map)

    def find_path(self,a,b):
        start = self.grid.node(a[0],a[1])
        end = self.grid.node(b[0],b[1])
        path, runs = self.finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        return path


def test():
    m = Map()
    m.load("static/map.bmp")
    

if __name__ == "__main__":
    test()