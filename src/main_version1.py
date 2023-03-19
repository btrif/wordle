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

from utils import get_all_words_query, only_words_containing_letters_helper
import re

letter_digit_pattern = "[a-z][0-4](,[a-z][0-4])*"  # matches : e3    or     e3,g4,k2  ...


def include_letters(all_included_letters, all_words_set):
    print("\n---- LETTERS IN WORD , either in good or wrong position ----")
    print(f"currently we have the letters :  {all_included_letters} ")
    matched_letters = input(" letters must be separated by comma, Eg: a,b,c :    ")
    # Input check :
    matched_letters = set(string.ascii_lowercase) & set(
            matched_letters.split(',')
            )  # this excludes non-letter characters
    all_included_letters |= set(matched_letters)
    all_words_set = only_words_containing_letters_helper(all_words_set, all_included_letters)
    print(f"{all_included_letters}")
    print(
            f"\nWORDS: \n{all_words_set}   \n\nThere are {len(all_words_set)} words containing letters "
            f"{all_included_letters} "
            f"... "
            f"\n"
            )
    return all_included_letters, all_words_set


def exclude_letters(all_excluded_letters, all_words_set):
    print("\n---- EXCLUDE LETTERS  ----")
    print(f"currently EXCLUDED letters :  {all_excluded_letters} ")
    excluded_letters = input("( letters must be separated by comma, Eg: a,b,c ) : ")
    # Input check :
    excluded_letters = set(string.ascii_lowercase) & set(
            excluded_letters.split(',')
            )  # this excludes non-letter characters
    all_excluded_letters |= set(excluded_letters)
    all_words_set = exclude_letters_from_word_helper(all_words_set, all_excluded_letters)
    print(f"{all_excluded_letters}")
    print(
            f"\nWORDS: \n{all_words_set}   \n\nThere are {len(all_words_set)} words without letters "
            f"{all_excluded_letters} "
            f"... \n"
            )
    return (all_excluded_letters, all_words_set)


def wrong_position_letters(all_wrong_positions, all_words_set):
    '''

    :param all_wrong_positions:
    :param all_words_set:
    :return:
    '''
    check_input_non_positions = False
    while not check_input_non_positions:
        print("\n---- LETTERS IN WRONG POSITION ----")
        print(f"Currently we have : {all_wrong_positions}")
        print('If you do not have any matched letters ( good or bad) press Y ')
        non_positions = input("\nFound letters which are not in a good position. Example: e3,p4 : ")
        if non_positions == 'Y':
            break
        print(f"non_positions: {non_positions}")

        check_input_non_positions = re.match(letter_digit_pattern, non_positions)
    if check_input_non_positions:
        non_positions = process_input_letter_digit_into_dictionary(non_positions.split(','))
        all_wrong_positions = update_dictionary_of_non_positions(all_wrong_positions, non_positions)
        print(f"all_non_positions : {all_wrong_positions}")

        all_words_set = exclude_letter_positions_helper(all_words_set, all_wrong_positions)
        print(
                f"\nWORDS: \n{all_words_set}   \n\nThere are {len(all_words_set)} words without non_positions "
                f"{all_wrong_positions} ... \n"
                )

    return (all_wrong_positions, all_words_set)


def correct_position_letters(all_exact_positions, all_words_set):
    check_input_exact_positions = False
    while not check_input_exact_positions:
        print("\n---- LETTERS IN EXACT POSITION ----")
        print(f"Currently we have : {all_exact_positions}")
        exact_positions = input("Example: e3,p4. If you do not have any EXACT letters  press Y :  ")

        if exact_positions == 'Y':
            break
        print(f"exact_positions : {exact_positions}")
        check_input_exact_positions = re.match(letter_digit_pattern, exact_positions)
    if check_input_exact_positions:
        exact_positions = exact_positions.split(',')
        exact_positions = process_exact_matches(exact_positions)

        all_exact_positions.update(exact_positions)
        print(f"{all_exact_positions}")

        all_words_set = exact_letter_positions_helper(all_words_set, all_exact_positions)
        print(
                f"\nWORDS: \n{all_words_set}   \n\nThere are {len(all_words_set)} words with exact positions "
                f"{all_exact_positions} ... \n"
                )
    return all_exact_positions, all_words_set


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


if __name__ == '__main__':

    query_words = get_all_words_query(current_session_local)
    all_words_set = process_filtered_result_into_set(query_words)

    word = 'word initialization'
    while len(word) != 5:
        word  = input(Colors.fg.lightgrey + 'Enter a 5-letter word: ' + Colors.reset)

    all_included_letters = set()  # Letters which are present within word
    all_excluded_letters = set()  # Letters which are not present within word
    all_wrong_positions = dict()  # Letters which are present in word but are not at the correct position
    all_exact_positions = dict()  # Letters which are in the exact position

    while True:
        print_options()

        case = 'initialization of the options loop'
        while case not in {'I', 'E', 'W', 'C', 'F'}:
            case = input("Please choose an option from I, E, W, C, F : ")

            ### CASE 1.  Letters which are within word, either green or yellow ( either good or bad position )
            if case == 'I':
                all_included_letters, all_words_set = include_letters(all_included_letters, all_words_set)

            ### CASE 2.     Exclude the following letters from word :
            if case == 'E':
                all_excluded_letters, all_words_set = exclude_letters(all_excluded_letters, all_words_set)

            ### CASE 3.    Letters which are not in good position :
            if case == 'W':
                all_wrong_positions, all_words_set = wrong_position_letters(all_wrong_positions, all_words_set)

            ### CASE 4.    Letters in EXACT position:
            if case == 'C':
                all_exact_positions, all_words_set = correct_position_letters(all_exact_positions, all_words_set)

        ### CASE 5.     Finish
        if case == 'F' :
            print("\n\nDO YOU KNOW the word ?")
            print("If YES, type the name of the word :   ")
            word = input()
            if word in all_words_set:
                print("\n\nC O N G R A T U L A T I O N S   ! ! !")
                print("you found the word : " + Colors.bg.black + Colors.fg.yellow + word + Colors.reset)
                break

    print("\nAnd the word is : " + Colors.bg.purple + word + Colors.reset )

