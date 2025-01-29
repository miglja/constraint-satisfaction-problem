#! /usr/bin/env python3

# code adapted from word search in David Kopec's "Classic Computer Science 
# Problems in Python"

from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase

from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids

class GridLocation(NamedTuple): 
    contents: str
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    entry = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                entry = []
                for i, c in enumerate(columns):
                    entry.append(GridLocation(word[i], row, c))
                domain.append(entry)
                #domain.append([GridLocation(row, c) for c in columns])
                # diagonal towards bottom right
                if row + length <= height:
                    entry = []
                    for i, r in enumerate(rows):
                        entry.append(GridLocation(word[i], r, col+(r-row)))
                    domain.append(entry)
                    #domain.append([GridLocation(r, col + (r-row)) for r in rows])

            if row + length <= height:
                # top to bottom
                entry = []
                for i, r in enumerate(rows):
                    entry.append(GridLocation(word[i], r, col))
                domain.append(entry)
                # domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col - length >= 0:
                    entry = []
                    for i, r in enumerate(rows):
                        entry.append(GridLocation(word[i], r, col-(r-row)))
                    domain.append(entry)
                    # domain.append([GridLocation(r, col - (r-row)) for r in rows])
    return domain

class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicate grid locations, then there is an overlap
        all_locations = []
        for values in assignment.values():
            for locs in values:
                all_locations.append(locs)
        # all_locations = [locs for values in assignment.values() for locs in values]
        for (position, location) in enumerate(all_locations):
            for match in all_locations[(position+1):]:
                if location.row == match.row and location.column == match.column and location.contents != match.contents:
                    return False
        return True

def main():
    grid: Grid = generate_grid(9,9)
    data: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    # data: List[str] = ["matthew", "joe", "mary", "sarah", "sally"]
    words: List[str] = list(map(lambda word: word if choice([True, False]) else word[::-1], data))
    """
    grid: Grid = generate_grid(2,2)
    words: List[str] = ["bo", "ma", "bm"]
    """

    locations: Dict[str, List[List[GridLocation]]] = {}

    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            # random reverse half the time
            # if choice([True, False]):
            #    grid_locations.reverse()

            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = letter

        display_grid(grid)

if __name__ == "__main__":
    main()
