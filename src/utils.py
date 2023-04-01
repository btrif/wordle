#  Created by btrif Trif on 09-03-2023 , 1:05 PM.
import os
import re
import string
from typing import Union

from sqlalchemy.orm import Session, sessionmaker

from database import db_engine, DB_URL
from models import WordleModel

this_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
current_session_local = this_session()


def get_word(
        db: Session,
        word: str
        ):
    return db.query(WordleModel).filter(WordleModel.word == word).first()


def get_all_words_query(
        db: Session,
        ):
    return db.query(WordleModel).all()


def get_word_regex(
        db: Session,
        expression: str
        ):
    # return db.query(WordleModel).filter(WordleModel.word.op('REGEXP')('%pa%') ).all()
    return db.query(WordleModel).filter(WordleModel.word.like(expression)).all()


def process_query_result_into_set(query_result: list):
    '''Translates the query result into a set of words where we will use string filtering methods '''
    matched_words = set()
    for count, wrd in enumerate(query_result):
        # print(f"{count + 1}.    {wrd.word}")
        matched_words.add(wrd.word)
    return matched_words


def only_words_containing_letters_filter(word_set: set, letters: set) -> set:
    ''' Filter: Returns the set of words which contains only letters
        Example:     letters = {'a', 'n', 't'} . Returns only words containing these letters.      '''
    words_with = set()
    for word in word_set:
        diff_letters = letters - set(word)
        if not diff_letters:
            words_with.add(word)
    return words_with


def exclude_letters_from_word_filter(letters: set, words_set: set) -> set:
    ''' Filter : Take an entire words_set and exclude words with do not contain letters'''
    new_set = set()
    for word in words_set:
        if not set(word) & letters:
            new_set.add(word)
    return new_set


def exact_letter_positions_filter(words_set: set, positions: dict):
    '''Filter : Matches the exact position of letters within word and retains only those words.
            positions = {3: 'e'}'''
    filtered_set = set()
    for word in words_set:

        bool_set = {True if word[pos] == letter else False for pos, letter in positions.items()}
        if False not in bool_set:
            filtered_set.add(word)
    return filtered_set


def exclude_letter_positions_filter(non_positions: dict, words_set: set) ->set :
    ''' It takes the words_Set and uses the wrong positions letters to exclude the words which have those letters.
    Example : Taking the word_set : ['brook', 'broth', 'grook', 'grout', 'troth', 'trout']. Now we choose the letter
     o to exclude from position 3: It will result in the reduced set :    ['broth', 'grout', 'troth', 'trout']
     because letter o was marked as not being at position 3. thus the words ['brook',  'grook'] will be excluded.

    non_positions = {0: ['e'], 2: ['e'], 4: ['r','d']} '''
    excluded_set = set()
    for word in words_set:
        bools_set = set()
        for position, letter_list in non_positions.items():
            excluded_letters_at_position = {True if word[position] == letter else False for letter in letter_list}
            bools_set |= excluded_letters_at_position
        if True not in bools_set:
            excluded_set.add(word)
    return excluded_set


def process_input_letter_digit_into_dictionary(word_letters: list) -> dict:
    non_positions = dict()
    for elem in word_letters:
        digit = int(elem[1])
        if digit not in non_positions:
            non_positions[digit] = []
        non_positions[digit].append(elem[0])
    return non_positions


def update_dictionary_of_non_positions(all_excluded: dict, new_excluded: dict) -> dict:
    ''' Adds a new letter to a position of excluded letters.
    :param all_excluded: looks like [ 0: ['a', 'b', 'e'], 2 : ['r', 't', 'q']  ]
    :param new_excluded:    looks like : [ 0: ['a', 'b', 'e'], 2 : ['r', 't', 'q']  ]
    :return:
    '''
    for d, letters in new_excluded.items():
        if d not in all_excluded:
            all_excluded[d] = []
        for letter in letters:
            if letter not in all_excluded[d]:
                all_excluded[d].append(letter)

    return all_excluded


def process_exact_matches(exact_pos: list) -> dict:
    '''

    :param exact_pos: looks like ['e3', 'p4', 'r2']
    :return:
    '''
    exact_matches = dict()
    for elem in exact_pos:
        digit = int(elem[1])
        exact_matches[digit] = elem[0]
    return exact_matches

def words_containing_given_letter(letter:str, all_words_set: set) -> Union[set] :
    words_with_letter = set()
    for word in all_words_set:
        if letter in word:
            words_with_letter.add(word)
    return words_with_letter



class Colors:
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main2 class
    i.e. colors.bold
    '''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        lightgreen = '\33[102m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        yellow = '\33[103m'
        iceberg = '\33[106m'
        white = '\33[107m'


if __name__ == '__main__':

    print(os.getcwd())

    if not os.path.isfile(DB_URL):
        raise Exception("\033[91m Database does NOT exists !")

    all_words = get_all_words_query(current_session_local)
    print(all_words)


class Score():
    def __init__(self, all_words):
        self.all_words = all_words
        self.letter_scores = self.all_letters_score()


    def all_letters_score(self) -> dict:
        ''' The letter score represents in how many words a given letter is present. It must be only present,
        it does not  count if that letter is repeated in that word'''
        most_letters = dict()
        for letter in string.ascii_lowercase:
            words_with_letter = words_containing_given_letter(letter, self.all_words)
            how_many = len(words_with_letter)
            # print(f"{letter}.   {how_many}    {words_with_letter}")
            most_letters[letter] = how_many

        return most_letters     # return sorted(most_letters.items(), key=lambda x: x[1], reverse=True)


    def word_score(self, word: str) -> int:
        '''Computes the score of the word by summing how many times the letters appear in all the words.
        thus we have a non-normalized probability of appearance'''
        score = 0
        for letter in set(word):
            score += self.letter_scores[letter]
        return score


    def all_words_score(self) -> dict:
        ''' a dictionary containing the score for all the words in the set '''
        words_score = dict()
        for word in self.all_words:
            words_score[word] = self.word_score(word)

        return sorted(words_score.items(), key=lambda x: x[1], reverse=False)




if __name__ == '__main__':
    query_words = get_all_words_query(current_session_local)  # query DB SQLite3
    all_words_set = process_query_result_into_set(query_words)  # Store all 5-letter words in a set

    score = Score(all_words_set)
    sorted_most_letters = score.letter_scores
    print(f"\nmost_letters: \n{sorted_most_letters}")

    five_letters = ['e', 'a', 'o', 's', 't' ]
    word5 = all_words_set.copy()
    for letter in five_letters :
        word5 = words_containing_given_letter(letter, word5)

    print(f"\nwords with most probability : {word5}")


    print(f"word score ")
    print(f" yogas   {score.word_score('yogas')}")
    print(f" stoae   {score.word_score('stoae')}")

    print(score.all_words_score())



