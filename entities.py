from dataclasses import dataclass


@dataclass
class Player:
    first_name: str
    game: str = "Guess Word"
    location: str = "Главное меню"
    attempt_count: int = 6
    attempts_left: int = 6
    len_word: int = 5
    word: str = ""
    not_win: bool = True
