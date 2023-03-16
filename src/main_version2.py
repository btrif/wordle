#  Created by btrif Trif on 11-03-2023 , 4:50 PM.

# Guess the 5-letter word from the website :
# https://www.nytimes.com/games/wordle/index.html


#########################################
#                   W  O  R  D  L  E       G  A  M  E                       #
#########################################
import string

from utils import current_session_local, process_filtered_result_into_set, \
    exclude_letters_from_word_helper, \
    exact_letter_positions_helper, exclude_letter_positions_helper, Colors, process_exact_matches, \
    process_input_letter_digit_into_dictionary, update_dictionary_of_non_positions

from utils import get_all_words_query, only_words_containing_letters
import re

letter_digit_pattern = "[a-z][0-4](,[a-z][0-4])*"  # matches : e3    or     e3,g4,k2  ...


def exclude_letters(all_excluded_letters: set, all_words_set: set) -> set:
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


def filter_large_word_set_with_wrong_position_letters(all_wrong_positions: dict, all_words_set: set) -> set:
    '''
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
    '''     Example : all_correct_position_letters = { 0:"t", 2 : "f", 3 :"e" }
    '''
    print("\n---- LETTERS IN EXACT POSITION ----")
    print(f"Currently we have : {all_exact_positions}")

    all_words_set = exact_letter_positions_helper(all_words_set, all_exact_positions)
    print(
            f"\nWORDS: \n{sorted(all_words_set)}   \n\nThere are {len(all_words_set)} words with exact positions "
            f"{all_exact_positions} ... \n"
            )
    return all_words_set


def add_exact_position(letter: str, position: int, all_correct_position_letters: dict):
    '''
    Example : all_correct_position_letters = { 0:"t", 2 : "f", 3 :"e" }
    :param letter:
    :param position:
    :param all_correct_position_letters:
    :return:
    '''
    all_correct_position_letters[position] = letter
    return all_correct_position_letters


def add_wrong_position(letter: str, position: int, all_wrong_position_letters: dict):
    '''
    all_wrong_position_letters = { 0:["a","t","y"], 2:["s","n"] , 4:["u"] }

    :param letter:
    :param position:
    :param all_wrong_position_letters:
    :return:
    '''
    if position not in all_wrong_position_letters:
        all_wrong_position_letters[position] = []
    all_wrong_position_letters[position].append(letter)

    return all_wrong_position_letters


def print_options():
    ### OPTIONS :
    print("\n" + Colors.bg.iceberg + "You have the following options :" + Colors.reset)
    print(
            Colors.bg.yellow + "Press " + Colors.fg.blue + Colors.bg.lightgreen + "I" + Colors.fg.black +
            Colors.bg.yellow + " to INCLUDE letters" + Colors.reset,
            end='; '
            )
    print(
            Colors.bg.yellow + "Press " + Colors.fg.blue + Colors.bg.lightgreen + "E" + Colors.fg.black +
            Colors.bg.yellow + " to EXCLUDE letters" + Colors.reset
            )
    print(
            Colors.bg.yellow + "Press " + Colors.fg.blue + Colors.bg.lightgreen + "W" + Colors.fg.black +
            Colors.bg.yellow + " to for WRONG position letters" + Colors.reset,
            end='; '
            )
    print(
            Colors.bg.yellow + "Press " + Colors.fg.blue + Colors.bg.lightgreen + "C" + Colors.fg.black +
            Colors.bg.yellow + " to for EXACT position letters" + Colors.reset
            )
    print(
            Colors.bg.yellow + "Press " + Colors.fg.blue + Colors.bg.lightgreen + "F" + Colors.fg.black +
            Colors.bg.yellow + " if you know the word and you want to finish" + Colors.reset
            )


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
            letter + Colors.reset + " on position " + Colors.bold + Colors.fg.lightblue + str(
                position
                ) + Colors.reset + " : "
            )


if __name__ == '__main__':

    query_words = get_all_words_query(current_session_local)  # query DB SQLite3
    all_words_set = process_filtered_result_into_set(query_words)  # Store all 5-letter words in a set
    print(all_words_set)
    all_excluded_letters = set()
    all_correct_position_letters = dict()            # Data structure : { 4: 'e', 1:  'r', 2: 'i' }
    all_wrong_position_letters = dict()             #                       {4: ['e'], 1: ['e', 'r'], 2: ['i']}
    word_letters = set()

    for choice in range(1, 8):
        if choice == 7:  # Did not find the word in 6 tries
            print("\n" + Colors.bg.red + "You lost. You exhausted all the 6 tries." + Colors.reset)

        word = 'word initialization'
        while word not in all_words_set:
            word = input(
                    "\n" + Colors.bg.black + Colors.fg.lightcyan + str(choice) + '.  Enter a valid 5-letter word: ' + Colors.reset
                    )

        for position, letter in enumerate(word):
            # We check if it is necessary to process the current letter
            if (letter not in all_excluded_letters or position not in all_correct_position_letters or letter not in
                    all_wrong_position_letters[position]):
                print("pos: " + str(position)  + ".  letter: " + Colors.fg.green +Colors.bold + letter + Colors.reset +
                      "  from word " + Colors.bg.yellow+Colors.underline+ word + Colors.reset)

                # CASE in which we already have the letter but it is in WRONG position
                # if letter in word_letters :
                #     if position not in all_wrong_position_letters :
                #         all_wrong_position_letters[position] = []
                #     if letter not in all_wrong_position_letters[position] :
                #         print("As we already have this letter we only need its position :")
                #         all_wrong_position_letters = add_wrong_position(
                #                 letter, position, all_wrong_position_letters
                #                 )
                #         all_words_set = filter_large_word_set_with_wrong_position_letters(
                #                 all_wrong_position_letters, all_words_set
                #                 )
                #
                # else :
                inclusion_exclusion_choice = False
                while inclusion_exclusion_choice not in {"I", "E", ""}:
                    print_inclusion_exclusion(letter)
                    inclusion_exclusion_choice = input()

                    ### EXCLUDE letter
                    if inclusion_exclusion_choice == "E":
                        all_excluded_letters.add(letter)
                        all_words_set = exclude_letters(all_excluded_letters, all_words_set)
                        print(f'all_excluded_letters : {all_excluded_letters}')

                    ### INCLUDE letter
                    elif inclusion_exclusion_choice == "I":
                        word_letters.add(letter)


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

        word_guess = input(
            "Press " + Colors.fg.lightblue + "ENTER to continue " + Colors.reset + Colors.fg.lightred +
            "or type the word if you want to finish: " + Colors.reset
            )
        if word_guess in all_words_set:
            print("\n\nC O N G R A T U L A T I O N S   ! ! !")
            print("you found the word : " + Colors.bg.black + Colors.fg.yellow + word_guess + Colors.reset)
            break
