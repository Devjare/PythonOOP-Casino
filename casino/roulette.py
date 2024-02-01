"""
    Roulette classes definitions.

    .. code-block:: python

        Outcome(name: str, odds: int)
        Bin(frozenset: Outcomes)
"""

from collections.abc import Iterable

from dataclasses import dataclass

@dataclass(frozen=True)
class Outcome():
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
    def __init__(self, outcomes: Iterable[Outcome]) -> None:
        self.outcomes = frozenset(outcomes)
