#  Created by btrif Trif on 10-03-2023 , 10:23 AM.

# ONLY for REFERENCE : This script was made to establish the logic of the game

# Guess the 5-letter word from the website :
# https://www.nytimes.com/games/wordle/index.html


from utils import current_session_local, process_filtered_result_into_set, get_word_regex, exclude_letters_from_word_helper, \
    exact_letter_positions_helper, exclude_letter_positions_helper

if __name__ == '__main__':
    # 1.  First Guess
    word_expression1 = "%o%e%a"
    regex_word_result1 = get_word_regex(current_session_local, word_expression1)

    filtered_words1 = process_filtered_result_into_set(regex_word_result1)
    # print(filtered_words1)

    # 2. Second Guess ( possibly that we have some letters )
    word_expression2 = "%e%"
    regex_word_result2 = get_word_regex(current_session_local, word_expression2)
    filtered_words2 = process_filtered_result_into_set(regex_word_result2)

    # 3. Exclude the following letters:
    letters = {'o', 'm', 'g', 'a'}
    result3 = exclude_letters_from_word_helper(filtered_words2, letters)
    print(f"result3: {len(result3)} \n{result3}")

    # 4. Positions
    positions = {3: 'e'}
    non_positions = {0: ['e'], 2: ['e'], 4: ['r']}
    result41 = exact_letter_positions_helper(result3, positions)
    result42 = exclude_letter_positions_helper(result41, non_positions)
    print(f"result41: {len(result41)} \n{result41}")
    print(f"result42: {len(result42)} \n{result42}")

    letters2 = {'i', 'd' }
    result43 = exclude_letters_from_word_helper(result42, letters2)
    print(f"result43: {len(result43)} \n{result43}")

    # 5. Repeat :
    positions5 = {0: 'r', 1: 'e',3: 'e'}
    exclude_letters5 = {'s', 't'}
    result51 = exclude_letters_from_word_helper(result43, exclude_letters5)
    print(f"result51: {len(result51)} \n{result51}")
    result52 = exact_letter_positions_helper(result51, positions5)
    print(f"result52: {len(result52)} \n{result52}")

    # 6. Repeat :
    positions6 = positions5.copy() ; positions6[4]= 'l'
    exclude_letters6 = {'p'}
    result61 = exact_letter_positions_helper(result52, positions6)
    print(f"result61: {len(result61)} \n{result61}")
    result62 = exclude_letters_from_word_helper(result61, exclude_letters6)
    print(f"result62: {len(result62)} \n{result62}")

    #TODO: @2023.03.10, 18:37 : Must put everything within a while loop and take input from console


