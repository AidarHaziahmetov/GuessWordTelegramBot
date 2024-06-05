import json
import logging
import time  # noqa: F401
from typing import Dict, List
import os
import requests  # noqa: F401
from telebot.types import ReplyKeyboardMarkup

logging.basicConfig(
    filename="logs/logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    filemode="w",
)


def load_data(path: str) -> dict:
    """
    Загружает данные из json по переданному пути и возвращает
    преобразованные данные в виде словаря.

    Если json по переданному
    пути не найден или его структура некорректна, то возвращает
    пустой словарь.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logging.debug(f"Не найден файл по пути: {path}")
        return {}


def save_data(data: dict, path: str) -> None:
    """
    Сохраняет переданный словарь в json по переданному пути.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        logging.info(f"Данные '{data}' сохранены в {path}")


def create_keyboard(buttons: list[str | int]) -> ReplyKeyboardMarkup:
    """
    Создает объект клавиатуры для бота по переданному списку строк.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def load_words(available_lengths: List[int]) -> Dict[int, List[str]]:
    words: Dict[int, List[str]] = {}
    for len_word in available_lengths:
        with open(
            os.path.join("words", f"len_{len_word}.txt"), "r", encoding="utf-8"
        ) as file:
            words[len_word] = file.readlines()
            print(len_word)
            for index, word in enumerate(words[len_word]):
                words[len_word][index] = word[:-1]
    return words
