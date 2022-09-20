import random
import collections
import pandas as pd

def assist():
    game_count = 5
    word_bank = fetch_word_bank()
    
    while game_count >= 0:
        guess, possible_words = choose_word(word_bank)
        print("Try:", guess, "\n(possibile words remaining: ", possible_words, ")\n")
        user_guess = input("Gussed word:")
        user_feedback = input("Feedback (0 is grey, 1 is yellow, 2 is green. E.g. 00122)\n:")
        process_feedback(user_feedback, user_guess, word_bank)
        game_count -= 1

        
    
    print("Attempt exceeded")


def fetch_word_bank():
    word_bank = pd.read_csv('words.csv')
    return word_bank

def choose_word(word_bank):
    return random.choice(word_bank['words'].tolist()), len(word_bank)


GREY = '0'
YELLOW = '1'
GREEN = '2'
def process_feedback(feedback, guess, word_bank):
    duplicate = set([item for item, count in collections.Counter(guess).items() if count > 1])

    print(duplicate)
    for position, feedback_letter in enumerate(feedback):
        guessed_letter = guess[position]
        
        print(guessed_letter)
        if feedback_letter == GREY:
            if guessed_letter in duplicate:
                continue
            index = word_bank[word_bank['words'].str.contains(guessed_letter)].index
            word_bank.drop(index, inplace=True)
            print('remaining words', len(word_bank))
        
        elif feedback_letter == GREEN:
            index = word_bank[word_bank['words'].str[position] != guessed_letter].index
            word_bank.drop(index, inplace=True)
            print('remaining words', len(word_bank))

        elif feedback_letter == YELLOW:
            index = word_bank[word_bank['words'].str[position] == guessed_letter].index
            word_bank.drop(index, inplace=True)
            

            index = word_bank[~word_bank['words'].str.contains(guessed_letter)].index
            word_bank.drop(index, inplace=True)
            print('remaining words', len(word_bank))
        else:
            raise InvalidUserFeedback()
    

class InvalidUserFeedback(Exception):
    pass

def playground():
    word_bank = fetch_word_bank()
    feedback = '00112'
    guess = 'stale'
    process_feedback(feedback, guess, word_bank)
    print(choose_word(word_bank))



if __name__ == '__main__':
    # playground()
    assist()