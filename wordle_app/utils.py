import random


# Get random word from five-words list
def get_word():
    with open('five_words.txt', 'r') as f:
        words = f.readlines()
        word = random.choice(words).replace('\n', '').upper()
    return word


# Resets the game -> app.config['GAME']
def get_new_game():
    word = get_word()
    game = {
        'new': False,
        'word': word,
        'word_idx': {i: ch for i, ch in enumerate(word)},
        'word_list': list(word),
        'row': 0,
        'word_guesses': [],
        'missed_letters': [],
        'guesses': [
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']],
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']],
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']],
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']],
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']],
            [['', 'none'], ['', 'none'], ['', 'none'], ['', 'none'], ['', 'none']]
        ],
        'correct': False,
        'gameover': False
    }
    return game


# Creates regular expression for javascript handler to exclude used input characters
def get_regex(missed_letters):
    all_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    groups = []
    group = []
    for ch in all_letters:
        if ch not in missed_letters:
            group.append(ch)
        else:
            groups.append(group)
            group = []
    if group:
        groups.append(group)

    regex = ''
    for group in groups:
        if group:
            if len(group) > 1:
                text=f'{group[0]}-{group[-1]}'
                regex += text + text.lower()
            else:
                regex += group[0] + group[0].lower()

    regex = f'/[{regex}]+/'
    return regex