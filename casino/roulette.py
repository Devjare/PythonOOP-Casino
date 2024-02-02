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
        return self.name == other.name

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

    def __init__(self):
        pass


class BinBuilder:
    def __init__(self):
        pass

    def buildBins(self, wheel: Wheel) -> None:
        # Build straights
        self.wheel: Wheel = wheel
        self.build_straight_bets()
        self.build_split_bets()

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

            n = 3 * r + 2  # Column one
            outcome = Outcome(f"Split {n}-{n+1}", Game.SPLIT_BET)
            self.wheel.add_outcome(n, outcome)
            self.wheel.add_outcome(n + 1, outcome)
