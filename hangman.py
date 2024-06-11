from typing import List
import requests
import random

is_running = True

url = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(url)

words = response.text.splitlines()
random_word = random.choice(
    [word for word in words if len(word) >= 10 and len(word) <= 15]
)
keyword = [char for char in random_word]
print(random_word)
indexes_of_found_letters = set()
number_of_attempts = 10
attempts_icon = "❤︎ "


def check_letter(word: str, letter: str) -> List[int]:
    global number_of_attempts

    if not letter.isalpha() or len(letter) != 1:
        raise ValueError("Input must be a single letter")

    if letter not in word:
        number_of_attempts -= 1

    index_list_of_matched_letters = [
        index for index, char in enumerate(word) if char == letter
    ]
    return index_list_of_matched_letters


def show_result() -> None:
    result = " ".join(
        [
            random_word[i] if i in indexes_of_found_letters else "_"
            for i in range(len(random_word))
        ]
    )
    return print(result)


def show_rest_of_attempts() -> None:
    return print(attempts_icon * number_of_attempts)


def close_game():
    global is_running
    is_running = False


while is_running:
    show_result()
    show_rest_of_attempts()
    user_input = input("Guess the letter: ").lower()

    try:
        indexes_of_found_letters.update(
            map(lambda index: index, check_letter(random_word, user_input))
        )
    except ValueError as e:
        print(e)
    finally:
        if len(indexes_of_found_letters) == len(keyword):
            print("You win!")
            close_game()

        if number_of_attempts <= 0:
            print("You lose!")
            close_game()
