from dataclasses import dataclass

@dataclass(frozen=True)
class Outcome():
    name: str
    odds: int

    def win_amount(self, amount: float) -> float:
        return self.odds * amount

    def __eq__(self, other) -> bool:
        return self.name == other.name
    
    def __ne__(self, other) -> bool:
        return self.name != other.name

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return f"{self.name} {self.odds}:1"
    
    def __repr__(self) -> str:
        return f"Outcome(name=\'{self.name}\', odds={self.odds})"
