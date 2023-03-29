#  Created by btrif Trif on 11-03-2023 , 4:50 PM.

# Guess the 5-letter word from the website :
# https://www.nytimes.com/games/wordle/index.html


#########################################
#                   W  O  R  D  L  E       G  A  M  E                       #
#########################################
import string

from utils import current_session_local, process_query_result_into_set, \
    exclude_letters_from_word_filter, \
    exact_letter_positions_filter, exclude_letter_positions_filter, Colors, only_words_containing_letters_filter

from utils import get_all_words_query
from dataclasses import dataclass

@dataclass
class WordCharacteristics():
    all_words_set : set                                 # {'tuple', 'maybe', 'later'}
    all_excluded_letters : set                      #{ 'a', 'b', 'c'}
    word_letters : set                                  #{ 'a', 'b', 'c'}
    all_correct_position_letters : dict          # Dict : { 4: 'e', 1:  'r', 2: 'i' }
    all_wrong_position_letters : dict           # Dict:  {4: ['e'], 1: ['e', 'r'], 2: ['i']}




def print_all_words_set(all_exact_positions, all_wrong_positions, all_excluded_letters, all_words_set):
    print(f"\nAll the words available with :\n {all_words_set}")
    print(f"all_exact_positions: {all_exact_positions}")
    print(f"all_wrong_positions: {all_wrong_positions}")
    print(f"all_excluded_letters: {all_excluded_letters}")



def add_exact_position(letter: str, position: int, all_correct_position_letters: dict) -> dict:
    ''' Adds a letter to a correct position
    '''
    all_correct_position_letters[position] = letter
    return all_correct_position_letters


def add_wrong_position(letter: str, position: int, all_wrong_position_letters: dict) -> dict:
    ''' Adds a letter to a wrong position
    all_wrong_position_letters = { 0:["a","t","y"], 2:["s","n"] , 4:["u"] }

    '''
    if position not in all_wrong_position_letters:
        all_wrong_position_letters[position] = []
    all_wrong_position_letters[position].append(letter)

    return all_wrong_position_letters


def print_remaining_words(all_excluded_letters, all_correct_position_letters, all_wrong_position_letters, word_letters, all_words_set):
    print(f"\nWORDS: \n{sorted(all_words_set)}")
    print("There are " + Colors.bold + Colors.bg.yellow + f"{len(all_words_set)}" + Colors.reset + " words with conditions: ")
    print(f"word_letters : {word_letters}")
    print(f"excluded_letters : {all_excluded_letters}")
    print(f"correct_position_letters : {all_correct_position_letters}")
    print(f"wrong_position_letters : {all_wrong_position_letters}")


def print_inclusion_exclusion(letter):
    print("\nPress ENTER to continue or ... Press ")
    print(
            Colors.bold + Colors.fg.lightblue + "E" + Colors.reset + " to EXCLUDE or " +
            Colors.fg.lightblue + Colors.bold + "I" + Colors.reset + " to INCLUDE the letter" + Colors.reset + " " +
            Colors.fg.blue + Colors.bold + letter + Colors.reset + ": ",
            end=""
            )


def print_inclusion_good_or_bad_position():
    print("\nPress ENTER to continue or ... Press")
    print(
        Colors.bold + Colors.fg.lightblue + "C" + Colors.reset + " for CORRECT or " + Colors.bold +
        Colors.fg.lightblue + "W" + Colors.reset + " for WRONG the letter " + Colors.bold + Colors.fg.lightblue +
        letter + Colors.reset + " on position " + Colors.bold + Colors.fg.lightblue + str(position) + Colors.reset + " : ", end=""
        )


def correct_or_wrong_position_letter_dialog(letter, position, all_correct_position_letters, all_wrong_position_letters, all_words_set):
    if position in all_correct_position_letters :
        if all_correct_position_letters[position] == letter :
            pass
    else :
        correct_wrong_position_choice = False
        while correct_wrong_position_choice not in {"C", "W", ""}:
            print_inclusion_good_or_bad_position()
            correct_wrong_position_choice = input()

            ### CORRECT Position
            if correct_wrong_position_choice == 'C':
                # If we have the correct position there is no need for INPUT
                all_correct_position_letters = add_exact_position(
                        letter, position, all_correct_position_letters
                        )
                all_words_set = exact_letter_positions_filter(all_words_set, all_correct_position_letters)

            ### WRONG Position
            if correct_wrong_position_choice == 'W':
                all_wrong_position_letters = add_wrong_position(
                        letter, position, all_wrong_position_letters
                        )
                all_words_set = exclude_letter_positions_filter(all_wrong_position_letters, all_words_set)

    return all_words_set, all_correct_position_letters, all_wrong_position_letters



def inclusion_exclusion_letter_dialog(letter, position, all_excluded_letters, all_correct_position_letters, word_letters, all_wrong_position_letters, all_words_set):
    ''' Dialog for Inclusion / Exclusion of letter'''

    inclusion_exclusion_choice = False
    while inclusion_exclusion_choice not in {"I", "E", ""}:
        print_inclusion_exclusion(letter)
        inclusion_exclusion_choice = input()

        ### EXCLUDE letter
        if inclusion_exclusion_choice == "E":
            all_excluded_letters.add(letter)
            all_words_set = exclude_letters_from_word_filter(all_excluded_letters, all_words_set)
            print(f'all_excluded_letters : {all_excluded_letters}')

        ### INCLUDE letter
        elif inclusion_exclusion_choice == "I":
            word_letters.add(letter)
            # Filter only words which contain the already found word letters.
            all_words_set = only_words_containing_letters_filter(all_words_set, word_letters)
            all_words_set, all_correct_position_letters, all_wrong_position_letters = \
                correct_or_wrong_position_letter_dialog(
                        letter,
                        position,
                        all_correct_position_letters,
                        all_wrong_position_letters,
                        all_words_set
                        )

    return all_excluded_letters, all_correct_position_letters, word_letters, all_wrong_position_letters, all_words_set



def check_only_one_position_left_for_letter(letter:str, all_correct_position_letters:dict, all_wrong_position_letters:dict ) -> bool:
    ''' It will  In the case in which we have a letter which has only one remaining option, it will automatically
    place it in the right place. Examples will help understand better the situations:
    Example 1:  position=2, letter=r  , all_correct_position_letters = { 0:'e'}, all_wrong_position_letters = { 1: ['x', 'r'], 3:['r'], 4:['r'] }
    In this case it is clear that letter 'r' is not at 0 as it is occupied already by 'e'. We also have the wrong positions of : 1, 3, 4.
    this means that the only remaining available place for letter 'r' is at position 2
    :returns : True, if only one position is left. False otherwise
    '''

    # Returns all the positions in which a letter is not already an exact match
    positions_available = set(range(5)) - { pos for pos, letter in all_correct_position_letters.items() if letter in string.ascii_lowercase }
    # Returns the set of all the positions in which letter is excluded
    excluded_positions = { pos for pos, letters_list in all_wrong_position_letters.items()  for l in letters_list if l ==letter }

    if len(positions_available - excluded_positions) == 1 :
        return True

    return False



def contratulations_finish_decorator(check_words_function):
    def wrapper(*args):
        if check_words_function(*args) :
            found_word, tries = list(args)
            print("\n\n" + Colors.bg.lightgreen + "C O N G R A T U L A T I O N S   ! ! !"+Colors.reset)
            print("you found the word : " + Colors.bg.black + Colors.fg.yellow + list(found_word)[0] + Colors.reset + f" in {tries} tries" )
        return check_words_function(*args)
    return wrapper



@contratulations_finish_decorator
def check_only_one_word_remaining(all_words: set, choice: int) -> bool:
    '''checks if we have a single word remaining in the all_words_set '''
    if len(all_words) == 1 :
        return True
    return False


if __name__ == '__main__':

    query_words = get_all_words_query(current_session_local)  # query DB SQLite3
    all_words_set = process_query_result_into_set(query_words)  # Store all 5-letter words in a set
    # Word characteristics
    word_letters = set()                            #{ 'a', 'b', 'c'}
    all_excluded_letters = set()                    #{ 'a', 'b', 'c'}
    all_correct_position_letters = dict()       # Dict : { 4: 'e', 1:  'r', 2: 'i' }
    all_wrong_position_letters = dict()     # Dict:  {4: ['e'], 1: ['e', 'r'], 2: ['i']}

    for choice in range(1, 8):
        # Fail Ending,   Did not find the word in 6 tries
        if choice == 7:
            print("\n" + Colors.bg.red + "You lost. You exhausted all the 6 tries." + Colors.reset)

        # Happy Ending, the word was found
        if check_only_one_word_remaining(all_words_set, choice) :
            break

        print_remaining_words(all_excluded_letters, all_correct_position_letters, all_wrong_position_letters, word_letters, all_words_set)

        word = 'word initialization'
        while word not in all_words_set:
            word = input(
                    "\n" + Colors.bg.black + Colors.fg.lightcyan + str(
                        choice
                        ) + '.  Enter a valid 5-letter word:' + Colors.reset +' '
                    )

        for position, letter in enumerate(word):
            # We check if it is necessary to process the current letter
            if (letter not in all_excluded_letters or position not in all_correct_position_letters or letter not in
                    all_wrong_position_letters[position]):
                print(
                    "pos: " + str(position) + ".  letter: " + Colors.fg.yellow + Colors.bg.blue + Colors.bold + letter + Colors.reset +
                    "  from word " + Colors.bg.yellow + Colors.underline + word + Colors.reset
                    )

                if letter in word_letters:
                    # No need to write its position if we can deduce it from what we have.
                    if check_only_one_position_left_for_letter(letter, all_correct_position_letters, all_wrong_position_letters):
                        all_correct_position_letters = add_exact_position(letter , position, all_correct_position_letters)
                        print_all_words_set(all_correct_position_letters, all_wrong_position_letters, all_excluded_letters, all_words_set)

                    else :      # Correct / Wrong Position Letter Dialog
                        print("\nLetter ", letter, "is already within word. So we need only to establish its position")
                        all_words_set, all_correct_position_letters, all_wrong_position_letters =  \
                            correct_or_wrong_position_letter_dialog(letter,
                                                                    position,
                                                                    all_correct_position_letters,
                                                                    all_wrong_position_letters,
                                                                    all_words_set)
                else :  # Inclusion/ Exclusion Function Dialog
                    all_excluded_letters, all_correct_position_letters, word_letters, all_wrong_position_letters, all_words_set = \
                        inclusion_exclusion_letter_dialog(
                                letter, position, all_excluded_letters, all_correct_position_letters, word_letters,
                                all_wrong_position_letters, all_words_set
                                )
