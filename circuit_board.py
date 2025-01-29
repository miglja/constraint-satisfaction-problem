#! /usr/bin/env python3

# code adapted from word search in David Kopec's "Classic Computer Science 
# Problems in Python"

from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase

from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids

class GridLocation(NamedTuple): 
    row: int
    column: int

class Rectangle:
    counter = 0

    def __init__(self, rows: int, cols: int):
        Rectangle.counter += 1
        self.id = Rectangle.counter
        self.rows = rows
        self.cols = cols

    def __hash__(self):
        return hash((self.id, self.rows, self.cols))

    def __eq__(self, other):
        return (self.id, self.rows, self.cols) == (other.id, other.rows, other.cols)

def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [["O" for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

def generate_domain(rect: List[List[int]], grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    rect_height: int = rect.rows
    rect_width: int = rect.cols

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + rect_width)
            rows: range = range(row, row + rect_height)
            if col + rect_width <= width and row + rect_height <= height:
                domain.append([GridLocation(c,r) for r in rows for c in columns])
                if not (rect_height == rect_width):
                    domain.append([GridLocation(r,c) for r in rows for c in columns])
    return domain

class CircuitBoardConstraint(Constraint[Rectangle, List[GridLocation]]):
    def __init__(self, rects: List[Rectangle]) -> None:
        super().__init__(rects)
        self.rects: List[Rectangle] = rects

    def satisfied(self, assignment: Dict[Rectangle, List[GridLocation]]) -> bool:
        # if there are any duplicate grid locations, then there is an overlap
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)

def main():
    grid: Grid = generate_grid(9,9)
    rects: List[Rectangle] = [Rectangle(2,5),
                              Rectangle(4,4),
                              Rectangle(3,3),
                              Rectangle(2,2),
                              Rectangle(6,1)
                             ]
    """
    grid:  Grid = generate_grid(3,3)
    rects: List[Rectangle] = [Rectangle(2,1), Rectangle(2,2)]
    """
    locations: Dict[Rectangle, List[List[GridLocation]]] = {}

    for rect in rects:
        locations[rect] = generate_domain(rect, grid)

    csp: CSP[str, List[GridLocation]] = CSP(rects, locations)
    csp.add_constraint(CircuitBoardConstraint(rects))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        for rect, grid_locations in solution.items():
           for loc in grid_locations:
                (row, col) = (loc.row, loc.column)
                grid[row][col] = str(rect.id)

        display_grid(grid)

if __name__ == "__main__":
    main()
