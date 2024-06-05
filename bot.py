import telebot
from game import word_generation, compare_word
from utils import create_keyboard
from telebot.types import Message
from typing import List, Dict
import os

token = '7327679974:AAEMHBPM0ao2__YNkvGgQP3e2sJHDkh4snE'
bot=telebot.TeleBot(token)
players = {}
available_lengths = [5,6,15]
available_attempt_count = [4,5,6,7,8,20]

words : Dict[int, List[str]] = {}
for len_word in available_lengths:
    with open(os.path.join("words",f"len_{len_word}.txt"),'r',encoding='utf-8') as file:
        words[len_word] = file.readlines()
        print(len_word)
        for index, word in enumerate(words[len_word]):
            words[len_word][index] = word[:-1]



def is_start_game_message(message: Message):
    return message.text in ["Начать игру", "Cыграть еще раз"]
def is_setings_message(message: Message):
    return message.text == "Настройка сложности"
def is_help_message(message: Message):
    return message.text == "Помощь/Правила"
def is_set_len_word(message: Message):
    return message.text =="Настроить длину слова"

@bot.message_handler(commands=['start']) 
def handle_start(message: Message):
    players[str(message.from_user.id)] = {
        "len_word": 5,
        "attempt_count": 6,
    }
    bot.send_message(
        message.from_user.id, 
        f"Привет, {message.from_user.first_name}!\nЭто Guess Word - телеграмм бот, в котором можно попробовать свои силы в угадывании слов!"
        )
    main_menu(message)

def main_menu(message: Message):
    bot.send_message(
        message.from_user.id, 
        'Выбери один из пуктов меню',
        reply_markup=create_keyboard(["Начать игру","Настройка сложности","Помощь/Правила"])
    )

@bot.message_handler(func=is_start_game_message)
def start_game(message: Message):
    players[str(message.from_user.id)]['word'] = word_generation(words[players[str(message.from_user.id)]["len_word"]])
    print(message.from_user.id,players[str(message.from_user.id)]['word'])
    players[str(message.from_user.id)]['attempts'] = players[str(message.from_user.id)]["attempt_count"]
    bot.send_message(
        message.from_user.id,
        f"Попробуй угадать слово из {players[str(message.from_user.id)]["len_word"]} букв. У тебя есть {players[str(message.from_user.id)]["attempts"]} попыток!",
        reply_markup=None
    )
    bot.register_next_step_handler(message, play)
    
def play(message: Message):
    if len(message.text) != players[str(message.from_user.id)]["len_word"]:
        bot.send_message(
            message.from_user.id,
            "Неверная длина слова"
            )
        print('error')
        bot.register_next_step_handler(message, play)
        return

    word_correction = compare_word(players[str(message.from_user.id)]['word'], message.text)
    bot.send_message(
        message.from_user.id,
        word_correction,
        parse_mode="MarkdownV2"
    )


    if word_correction == "".join(f"`{letter}`" for letter in message.text):
        bot.send_message(
            message.from_user.id,
            "Ты победил!",
            reply_markup=create_keyboard(["Cыграть еще раз","Настройка сложности","Помощь/Правила"])
        )
        return
    players[str(message.from_user.id)]["attempts"] -= 1
    if players[str(message.from_user.id)]["attempts"] > 0:
        bot.register_next_step_handler(message, play)
    else:
        bot.send_message(
            message.from_user.id,
            f"Ты проиграл!, было загадано слово {players[str(message.from_user.id)]['word']}",
            reply_markup=create_keyboard(["Cыграть еще раз","Настройка сложности","Помощь/Правила"])
        )

@bot.message_handler(func=is_setings_message)
def setings_menu(message: Message):
    bot.send_message(
        message.from_user.id,
        "Настройки игрового процесса",
        reply_markup=create_keyboard(["Настроить длину слова", "Настроить кол-во попыток","Назад"]))
    bot.register_next_step_handler(message, settings_change)

def settings_change(message: Message):
    if message.text == "Настроить длину слова":
        bot.send_message(
        message.from_user.id,
        "Выберите длину из предложенных варианов",
        reply_markup=create_keyboard(list(map(str,available_lengths)))
        )
        bot.register_next_step_handler(message, set_len_word)
    elif message.text == "Настроить кол-во попыток":
        bot.send_message(
        message.from_user.id,
        "Выберите кол-во попыток из предложенных варианов",
        reply_markup=create_keyboard(list(map(str,available_attempt_count)))
        )
        bot.register_next_step_handler(message, set_attempt_count)
    elif message.text == "Назад":
        main_menu(message)

def set_len_word(message: Message):
    try:
        if int(message.text) in available_lengths:
            players[str(message.from_user.id)]["len_word"] = int(message.text)
    except Exception as e:
        print(e)
    finally:
        setings_menu(message)

def set_attempt_count(message: Message):
    try:
        if int(message.text) in available_attempt_count:
            players[str(message.from_user.id)]["attempt_count"] = int(message.text)
    except Exception as e:
        print(e)
    finally:
        setings_menu(message)


bot.polling()