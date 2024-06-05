from dataclasses import dataclass


@dataclass
class Player:
    id: str
    game: str = "Guess Word"
    location: str
    attempt_count: int = 6
    attempts_left: int = 6
    len_word: int = 5
