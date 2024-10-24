#! /usr/bin/env python3

"""
Use constraint satisfaction problem framework (csp.py) to solve SEND+MORE=MONEY
cryptographic puzzle.
"""

# code taken from David Kopec's "Classic Computer Science Problems in Python"

from typing import Dict, List, Optional

from csp import Constraint, CSP


class SendMoreMoneyConstraint(Constraint[str, int]):
    """ Class for constraint to satisfy requirement of csp.py """

    def __init__(self, letters: List[str]) -> None:
        """ Initialize Constraint """
        super().__init__(letters)
        self.letters: List[str] = letters

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        """ Determine if we've satisfied the constraint and found solution """
        # if there are duplicate values, then its' not a solution
        if len(set(assignment.values())) < len(assignment):
            return False

        # if all variables have been assigned, check if it adds correctly
        if len(assignment) == len(self.letters):
            s: int = assignment["S"]
            e: int = assignment["E"]
            n: int = assignment["N"]
            d: int = assignment["D"]
            m: int = assignment["M"]
            o: int = assignment["O"]
            r: int = assignment["R"]
            y: int = assignment["Y"]

            send: int = s*1000 + e*100 + n*10 + d
            more: int = m*1000 + o*100 + r*10 + e
            money: int = m*10000 + o*1000 + n*100 + e*10 + y

            return send + more == money

        return True  # no conflict


def main():
    """ Let's get this party started """

    letters: List[str] = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    possible_digits: Dict[str, List[int]] = {}
    for letter in letters:
        possible_digits[letter] = list(range(0, 10))
    possible_digits["M"] = [1]  # So we don't get answers starting with a zero
    csp: CSP[str, int] = CSP(letters, possible_digits)
    csp.add_constraint(SendMoreMoneyConstraint(letters))
    solution: Optional[Dict[str, int]] = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        print(solution)


if __name__ == "__main__":
    main()
