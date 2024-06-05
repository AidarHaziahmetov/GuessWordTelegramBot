import telebot
from game import word_generation, compare_word
from entities import Player
from menu import Menu
from utils import create_keyboard, load_words
from telebot.types import Message
from typing import List, Dict  # noqa: F401
import os  # noqa: F401

token = "7327679974:AAEMHBPM0ao2__YNkvGgQP3e2sJHDkh4snE"
bot = telebot.TeleBot(token)
players: Dict[str, Player] = {}
available_lengths = [4, 5, 6, 7, 8]
available_attempt_count = [5, 6, 7, 8]

words = load_words(available_lengths)


def is_start_game_message(message: Message):
    return message.text in ["Начать игру", "Cыграть еще раз"]


def is_setings_message(message: Message):
    return message.text == "Настройка сложности"


def is_help_message(message: Message):
    return message.text == "Помощь/Правила"


def is_set_len_word(message: Message):
    return message.text == "Настроить длину слова"


@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    players[str(message.from_user.id)] = Player(message.from_user.first_name)
    bot.send_message(
        message.from_user.id,
        f"Привет, {message.from_user.first_name}!\nЭто Guess Word - телеграмм бот, в котором можно попробовать свои силы в угадывании слов!",
        reply_markup=create_keyboard(Menu[Player.location]["avalible_steps"]),
    )


@bot.message_handler()
def main_meneger(message: Message):
    if players[str(message.from_user.id)].location == "Настроить длину слова" and message.text != "Назад↩":
        if int(message.text) in available_lengths:
            players[str(message.from_user.id)].len_word = int(message.text)
            bot.send_message(
                str(message.from_user.id),
                f"Вы успешно установили длину слова на {int(message.text)}",
            )
    elif players[str(message.from_user.id)].location == "Настроить кол-во попыток" and message.text != "Назад↩":
        if int(message.text) in available_attempt_count:
            players[str(message.from_user.id)].attempt_count = int(message.text)
            bot.send_message(
                str(message.from_user.id),
                f"Вы успешно установили кол-во попыток на {int(message.text)}",
            )
    elif players[str(message.from_user.id)].location == "Играть🕹" and message.text != "Назад↩":
        if message.text == "Cыграть еще раз":
            players[str(message.from_user.id)].not_win = True
            players[str(message.from_user.id)].word = word_generation(words[players[str(message.from_user.id)].len_word])
            players[str(message.from_user.id)].attempts_left = players[str(message.from_user.id)].attempt_count
            bot.send_message(
                        message.from_user.id,
                        Menu[players[str(message.from_user.id)].location]["messege"].format(
                            len_word=players[str(message.from_user.id)].len_word,
                            attempt_count=players[str(message.from_user.id)].attempts_left),
                        reply_markup=create_keyboard(Menu[players[str(message.from_user.id)].location]["avalible_steps"])
                    )
        elif players[str(message.from_user.id)].attempts_left > 0:
            if players[str(message.from_user.id)].not_win:
                if len(message.text) != players[str(message.from_user.id)].len_word:
                    bot.send_message(message.from_user.id, "Неверная длина слова")
                    print("error")
                else:
                    word_correction = compare_word(
                        players[str(message.from_user.id)].word, message.text.lower()
                    )
                    print(players[str(message.from_user.id)].word)
                    players[str(message.from_user.id)].attempts_left -= 1
                    bot.send_message(message.from_user.id, word_correction, parse_mode="MarkdownV2")
                    if word_correction == "".join(f"`{letter}`" for letter in message.text):
                        players[str(message.from_user.id)].not_win = False
                        bot.send_message(
                        message.from_user.id,
                        "Ты победил!",
                        reply_markup=create_keyboard(["Cыграть еще раз","Назад↩"])
                        )
                    elif players[str(message.from_user.id)].attempts_left <= 0:
                        players[str(message.from_user.id)].not_win = True
                        bot.send_message(
                            message.from_user.id,
                            f"Ты проиграл!, было загадано слово {players[str(message.from_user.id)].word}",
                            reply_markup=create_keyboard(["Cыграть еще раз","Назад↩"]),
                            )
            else:
                bot.send_message(
                    message.from_user.id,
                    "Выбери пункт из меню",
                    reply_markup=create_keyboard(["Cыграть еще раз","Назад↩"])
                    )     
        else:
            bot.send_message(
                    message.from_user.id,
                    "Выбери пункт из меню",
                    reply_markup=create_keyboard(["Cыграть еще раз","Назад↩"])
                    )  
    elif message.text in Menu[players[str(message.from_user.id)].location]["avalible_steps"]:
        if message.text == "Назад↩":
            for location, steps in Menu.items():
                if players[str(message.from_user.id)].location in steps["avalible_steps"]:
                    players[str(message.from_user.id)].location = location
                    bot.send_message(
                        message.from_user.id,
                        Menu[players[str(message.from_user.id)].location]["messege"],
                        reply_markup=create_keyboard(Menu[location]["avalible_steps"]),
                        parse_mode="MarkdownV2"
                    )
        elif message.text == "Играть🕹":
            players[str(message.from_user.id)].location = message.text
            players[str(message.from_user.id)].word = word_generation(words[players[str(message.from_user.id)].len_word])
            players[str(message.from_user.id)].attempts_left = players[str(message.from_user.id)].attempt_count
            bot.send_message(
                        message.from_user.id,
                        Menu[players[str(message.from_user.id)].location]["messege"].format(
                            len_word=players[str(message.from_user.id)].len_word,
                            attempt_count=players[str(message.from_user.id)].attempts_left),
                        reply_markup=create_keyboard(Menu[players[str(message.from_user.id)].location]["avalible_steps"])
                    )
        elif players[str(message.from_user.id)].location in ["Настроить длину слова","Настроить кол-во попыток"]:
            pass
        else:
            players[str(message.from_user.id)].location = message.text
            bot.send_message(
                        message.from_user.id,
                        Menu[players[str(message.from_user.id)].location]["messege"],
                        reply_markup=create_keyboard(Menu[players[str(message.from_user.id)].location]["avalible_steps"]),
                        parse_mode="MarkdownV2"
                    )

    else:
        bot.send_message(
            message.from_user.id,
            "Выбери пункт из меню"
        )
    


bot.polling()
