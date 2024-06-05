import random
from typing import List
def compare_word(word1:str, word2:str)->str:
    res = ''
    for index, letter in enumerate(word1):
        if letter == word2[index]:
            res += f'`{word2[index]}`'
        elif word2[index] in word1:
            res += f'{word2[index]}'
        else:
            res += f'~{word2[index]}~'
    return res

def word_generation(words: List[str]) ->str:
    current_word = random.choice(words)
    return current_word