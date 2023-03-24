#  Created by btrif Trif on 11-03-2023 , 4:50 PM.

# Guess the 5-letter word from the website :
# https://www.nytimes.com/games/wordle/index.html


#########################################
#                   W  O  R  D  L  E       G  A  M  E                       #
#########################################
import string

from utils import current_session_local, process_filtered_result_into_set, \
    exclude_letters_from_word_helper, \
    exact_letter_positions_helper, exclude_letter_positions_helper, Colors, only_words_containing_letters_helper

from utils import get_all_words_query


def filter_exclude_letters(all_excluded_letters: set, all_words_set: set) -> set:
    print("\n---- EXCLUDE LETTERS  ----")
    print(f"currently EXCLUDED letters :  {all_excluded_letters} ")

    all_words_set = exclude_letters_from_word_helper(all_words_set, all_excluded_letters)
    print(f"{all_excluded_letters}")
    print(
            f"\nWORDS: \n{sorted(all_words_set)}   \n\nThere are {len(all_words_set)} words without letters "
            f"{all_excluded_letters} "
            f"... \n"
            )
    return all_words_set


def print_all_words_set(all_words_set, all_exact_positions, all_wrong_positions, all_excluded_letters):
    print(f"\nAll the words available with :\n {all_words_set}")
    print(f"all_exact_positions: {all_exact_positions}")
    print(f"all_wrong_positions: {all_wrong_positions}")
    print(f"all_excluded_letters: {all_excluded_letters}")


def filter_large_word_set_with_wrong_position_letters(all_wrong_positions: dict, all_words_set: set) -> set:
    '''  Given the wrong positions letters removes the words which have letters in those positions
    all_wrong_position_letters = { 0:["a","t","y"], 2:["s","n"] , 4:["u"] }
    '''
    print("\n---- LETTERS IN WRONG POSITION ----")
    print(f"Currently we have wrong_positions : {all_wrong_positions}")

    all_words_set = exclude_letter_positions_helper(all_words_set, all_wrong_positions)
    print(
            f"\nWORDS: \n{sorted(all_words_set)}   "
            f"\n\nThere are {len(all_words_set)} words with letters in WRONG positions {all_wrong_positions}"
            )

    return all_words_set


def filter_large_word_set_with_correct_position_letters(all_exact_positions: dict, all_words_set: set) -> set:
    ''' Given the word letter exact positions returns the set with words which contain the given letters
        in that exact position
        Example : all_correct_position_letters = { 0:"t", 2 : "f", 3 :"e" }
    '''
    print("\n---- LETTERS IN EXACT POSITION ----")
    print(f"Currently we have : {all_exact_positions}")

    all_words_set = exact_letter_positions_helper(all_words_set, all_exact_positions)
    print(
            f"\nWORDS: \n{sorted(all_words_set)}   \n\nThere are {len(all_words_set)} words with exact positions "
            f"{all_exact_positions} ... \n"
            )
    return all_words_set


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


def correct_or_wrong_position_letter_dialog(letter, position, all_words_set, all_correct_position_letters, all_wrong_position_letters):
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
                all_words_set = filter_large_word_set_with_correct_position_letters(
                        all_correct_position_letters, all_words_set
                        )

            ### WRONG Position
            if correct_wrong_position_choice == 'W':
                all_wrong_position_letters = add_wrong_position(
                        letter, position, all_wrong_position_letters
                        )
                all_words_set = filter_large_word_set_with_wrong_position_letters(
                        all_wrong_position_letters, all_words_set
                        )

    return all_words_set, all_correct_position_letters, all_wrong_position_letters


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
            found_word = str(list(*args)[0])
            print(f"----- {check_words_function.__name__}: end -----")
            print("\n\n" + Colors.bg.lightgreen + "C O N G R A T U L A T I O N S   ! ! !"+Colors.reset)
            print("you found the word : " + Colors.bg.black + Colors.fg.yellow + found_word + Colors.reset)
        return check_words_function(*args)
    return wrapper



@contratulations_finish_decorator
def check_only_one_word_remaining(all_words: set) -> bool:
    '''checks if we have a single word remaining in the all_words_set '''
    if len(all_words) == 1 :
        return True
    return False


if __name__ == '__main__':

    query_words = get_all_words_query(current_session_local)  # query DB SQLite3
    all_words_set = process_filtered_result_into_set(query_words)  # Store all 5-letter words in a set
    # Word characteristics TODO : To put in a DataClass
    all_excluded_letters = set()                    #{ 'a', 'b', 'c'}
    all_correct_position_letters = dict()       # Dict : { 4: 'e', 1:  'r', 2: 'i' }
    all_wrong_position_letters = dict()     # Dict:  {4: ['e'], 1: ['e', 'r'], 2: ['i']}
    word_letters = set()

    for choice in range(1, 8):
        # Fail Ending,   Did not find the word in 6 tries
        if choice == 7:
            print("\n" + Colors.bg.red + "You lost. You exhausted all the 6 tries." + Colors.reset)

        # Happy Ending, the word was found
        if check_only_one_word_remaining(all_words_set) :
            break

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
                        print_all_words_set(all_words_set, all_correct_position_letters, all_wrong_position_letters, all_excluded_letters)

                    else :
                        print("Letter ", letter, "is already within word. So we need only to establish its position")
                        all_words_set, all_correct_position_letters, all_wrong_position_letters =  correct_or_wrong_position_letter_dialog(
                                letter,
                                position,
                                all_words_set,
                                all_correct_position_letters,
                                all_wrong_position_letters
                                )
                else :  #TODO Inclusion-Exclusion Function Dialog
                    inclusion_exclusion_choice = False
                    while inclusion_exclusion_choice not in {"I", "E", ""}:
                        print_inclusion_exclusion(letter)
                        inclusion_exclusion_choice = input()

                        ### EXCLUDE letter
                        if inclusion_exclusion_choice == "E":
                            all_excluded_letters.add(letter)
                            all_words_set = filter_exclude_letters(all_excluded_letters, all_words_set)
                            print(f'all_excluded_letters : {all_excluded_letters}')

                        ### INCLUDE letter
                        elif inclusion_exclusion_choice == "I":
                            word_letters.add(letter)
                            # Filter only words which contain the already found word letters.
                            all_words_set = only_words_containing_letters_helper(all_words_set, word_letters)
                            all_words_set, all_correct_position_letters, all_wrong_position_letters =  correct_or_wrong_position_letter_dialog(
                                    letter,
                                    position,
                                    all_words_set,
                                    all_correct_position_letters,
                                    all_wrong_position_letters
                                    )

