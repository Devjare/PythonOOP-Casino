"""
    Roulette classes definitions.

    .. code-block:: python

        Outcome(name: str, odds: int)
        Bin(frozenset: Outcomes)
"""

import random

from dataclasses import dataclass
from typing import List, Tuple

from collections.abc import Iterable


@dataclass(frozen=True)
class Outcome:
    """Outcome class

    Attributes:
        name (str): Name of the outcome.
        odds (int): Odds corresponding to the outcome.
    """

    name: str
    odds: int

    def win_amount(self, amount: float) -> float:
        """Compute the winning amount based on the `Bet`s and the corresponding `odds`.

        Args:
            amount (float): Amount assigned to the `Bet`.

        Returns:
            float: Total won amount = amount * odds.
        """
        return self.odds * amount

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.odds == other.odds

    def __ne__(self, other) -> bool:
        return self.name != other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name:s} {self.odds:d}:1"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__:s}(name={self.name!r}, odds={self.odds!r})"


# Extending (inhereting) from frozensets prevents from setting a custom type for the frozen set.
# Decision choice: Wrapping the frozen set to allow things suchs as validation of objects
# with custom iterable typing
class Bin:
    def __init__(self, outcomes: Iterable[Outcome] | None = None) -> None:
        # If not none, then empty set
        self.outcomes = set(outcomes if outcomes else ())

    def __eq__(self, bin):
        return self.outcomes == bin.outcomes

    def __contains__(self, outcome):
        return outcome in self.outcomes


class Wheel:
    """Wheel class

    Attributes:
        bins (Tuple): Tuple containing the 38 bins.
        rng (Callable): Random number generator object.
    """

    def __init__(self):
        self.bins: Tuple[Bin, ...] = tuple(Bin() for _ in range(38))
        self.rng = random.Random()

    def add_outcome(self, number: int, outcome: Outcome) -> None:
        bin = self.bins[number]
        bin.outcomes.add(outcome)

    def choose(self):
        return self.rng.choice(self.bins)

    def get(self, number: int):
        return self.bins[number]


class Game:
    STRAIGHT_BET = 35
    STREET_BET = 11
    SPLIT_BET = 17
    CORNER_BET = 8
    LINE_BET = 5
    DOZEN_BET = 2
    COLUMN_BET = 2
    OUTSIDE_BET = 1
    FIVE_BET = 6


    def __init__(self):
        pass


class BinBuilder:
    def __init__(self, wheel: Wheel):
        self.wheel: Wheel = wheel

    def build_bins(self, wheel: Wheel) -> None:
        self.build_straight_bets()
        self.build_split_bets()
        self.build_street_bets()
        self.build_line_bets()
        self.build_corner_bets()
        self.build_dozen_bets()
        self.build_column_bets()
        self.build_outside_bets()
        self.build_five_bet()

    def build_straight_bets(self):
        for i in range(1, 37):
            self.wheel.add_outcome(i, Outcome(f"Bin no. {i}", Game.STRAIGHT_BET))

        # Add bets for 0, and 00
        self.wheel.add_outcome(0, Outcome("Bin no. 0", Game.STRAIGHT_BET))
        self.wheel.add_outcome(37, Outcome("Bin no. 00", Game.STRAIGHT_BET))

    def build_split_bets(self):
        for r in range(12):
            n = 3 * r + 1  # Column one
            outcome = Outcome(f"Split {n}-{n+1}", Game.SPLIT_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n + 1, outcome)

            n = 3 * r + 2  # Column two
            outcome = Outcome(f"Split {n}-{n+1}", Game.SPLIT_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n + 1, outcome)
        
        for n in range(1, 34):
            outcome = Outcome(f"Split {n}-{n+3}", Game.SPLIT_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n+3, outcome)


    def build_street_bets(self):
        for r in range(12):
            n = 3 * r + 1
            outcome = Outcome(f"Street {n}-{n+1}-{n+2}", Game.STREET_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n + 1, outcome)
            self.wheel.add_outcome(n + 2, outcome)
    
    def build_corner_bets(self):
        for r in range(12):
            n = 3 * r + 1
            outcome = Outcome(f"Corner {n}-{n+1}-{n+3}-{n+4}", Game.CORNER_BET)
            self.wheel.add_outcome(n,outcome)
            self.wheel.add_outcome(n+1,outcome)
            self.wheel.add_outcome(n+3,outcome)
            self.wheel.add_outcome(n+4,outcome)
    
    def build_line_bets(self):
        for r in range(11):
            n = 3 * r + 1
            outcome = Outcome(f"Line {n}-{n+1}-{n+2}-{n+3}-{n+4}-{n+5}", Game.LINE_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n+1, outcome)
            self.wheel.add_outcome(n+2, outcome)
            self.wheel.add_outcome(n+3, outcome)
            self.wheel.add_outcome(n+4, outcome)
            self.wheel.add_outcome(n+5, outcome)
    
    def build_dozen_bets(self):
        for d in range(3):
            outcome = Outcome(f"Dozen {d+1}", Game.DOZEN_BET)
            for m in range(12):
                self.wheel.add_outcome(12*d+m+1, outcome)
    
    def build_column_bets(self):
        for c in range(3):
            outcome = Outcome(f"Column {c+1}", Game.COLUMN_BET)
            for r in range(12):
                self.wheel.add_outcome(3*r+c+1, outcome)

    
    def build_outside_bets(self):
        """
        Even-Money or 'Outside' bets.
        """
        red = Outcome("Red", Game.OUTSIDE_BET)
        black = Outcome("Black", Game.OUTSIDE_BET)
        even = Outcome("Event", Game.OUTSIDE_BET)
        odd = Outcome("Odd", Game.OUTSIDE_BET)
        low = Outcome("Low", Game.OUTSIDE_BET)
        high = Outcome("High", Game.OUTSIDE_BET)
            
        reds = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        for n in range(1, 37):
            self.wheel.add_outcome(n, low if n < 19 else high)
            self.wheel.add_outcome(n, even if n % 2 == 0 else odd)
            self.wheel.add_outcome(n, red if n in reds else black)
                
    def build_five_bet(self):
        """
        Five bet.
        """
        outcome = Outcome("Five", Game.FIVE_BET)
        self.wheel.add_outcome(0, outcome)
        self.wheel.add_outcome(37, outcome)
        self.wheel.add_outcome(1, outcome)
        self.wheel.add_outcome(2, outcome)
        self.wheel.add_outcome(3, outcome)
