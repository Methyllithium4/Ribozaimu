from dataclasses import dataclass


@dataclass
class Reaction:
    text: str
    face: str = "idle"
    duration: float = 3.0
    priority: int = 1