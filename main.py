import random

# Not supported: Double letters (yet), Triple letters (ever).

WORD_LOG_LIMIT = 50
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def get_words(file):
    """Collects a list of all five letter words."""
    words = []
    f = open(file, "r")
    for line in f:
        if is_eligible(line):
            words.append(line.replace("\n", "")
    return words

def is_eligible(word):
    """A word is eligible if five letters and contains no more than two of a letter."""
    if len(word) != 6: # Include newline char.
        return False
    for letter in word:
        if word.count(letter) > 1:
            return False
    return True

def create_letter_frequency_table(word_list):
    """Determines the frequency of letters in all remaining valid words."""
    frequency_dict = {}
    for letter in ALPHABET:
        frequency_dict[letter] = 0
    for word in word_list:
        for letter in word:
            if letter in ALPHABET:
                frequency_dict[letter] = frequency_dict[letter] + 1
    return frequency_dict

def find_best_word(word_list, frequency_dict):
    """Finds the best word out of the remaining words.
    Best word is defined by the word with letters that occur most frequently
    in the remaining words."""
    best_word = ''
    max_score = 0
    for word in word_list:
        score = 0
        for letter in word:
            score += frequency_dict[letter]
        if score > max_score:
            best_word = word
    return best_word

def filter_word_list(guess_results, word_list, word_guess):
    """Repeatedly filter the word list with information gained."""
    print(f"DEBUG: {len(word_list)} words at start of filter.")
    if len(word_list) < WORD_LOG_LIMIT:
        print(word_list)
    for i in range(len(guess_results)):
        if guess_results[i] == 'green': # Letter in word & correct position
            word_list = filter_green(word_list, word_guess[i], i)
        if guess_results[i] == 'gold': # Letter in incorrect position
            word_list = filter_gold(word_list, word_guess[i], i)
        if guess_results[i] == 'grey': # Letter not in word
            word_list = filter_grey(word_list, word_guess[i])
        print(f"DEBUG: {len(word_list)} words remain.")
        if len(word_list) < WORD_LOG_LIMIT:
            print(word_list)

def filter_green(word_list, letter, index):
    """Return all words with the letter in position."""
    filtered_word_list = []
    for word in word_list:
        if word[index] == letter:
            filtered_word_list += word
    return filtered_word_list

def filter_gold(word_list, letter, index):
    """Return all words with the letter not in position but present."""
    filtered_word_list = []
    for word in word_list:
        if letter in word and word[index] != letter:
            filtered_word_list += word
    return filtered_word_list

def filter_grey(word_list, letter):
    """Return all words that don't contain the letter."""
    filtered_word_list = []
    for word in word_list:
        if letter not in word:
            filtered_word_list += word
    return filtered_word_list

def return_guess_result(word_guess, secret_word):
    """Return a list of green, gold, or grey results for a word guess."""
    guess_result = []
    for i in range(len(word_guess)):
        if word_guess[i] == secret_word[i]:
            guess_result.append("green")
        elif word_guess[i] != secret_word[i] and word_guess[i] not in secret_word:
            guess_result.append("grey")
        else:
            guess_result.append("gold")
    return guess_result

def play_game(word_list):
    """Have the computer play a game of Wordle against itself."""
    secret_word = random.choice(word_list)
    guesses = 1
    print(f"{len(word_list)} contained in word list.")
    while guesses < 7:
        frequency_dict = create_letter_frequency_table(word_list)
        word_guess = find_best_word(word_list, frequency_dict)
        print(f"Word guess is {word_guess.upper()}")
        guess_result = return_guess_result(word_guess, secret_word)
        print(f"Result was {guess_result}")
        if guess_result.count("green") == 5:
            print("The computer guessed correctly! The game is over!")
            return
        print("Filtering words for next guess.")
        word_list = filter_word(guess_result, word_list, word_guess)
        print(f"{len(word_list)} words remain.")
        guesses += 1
    print(f"The computer had {len(word_list)} words remaining and lost. The game is over.")
    return
        
starting_word_list = get_words("words_alpha.txt")
for i in range(10):
    play_game(starting_word_list)
