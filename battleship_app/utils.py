
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
NUMBERS = list(range(1, 11))
BOATS =  {
    'carrier': 5,
    'battleship': 4,
    'cruiser': 3,
    'submarine': 3,
    'destroyer': 2
}


def get_new_game():
    game = {
        'player1': {
            'in': False,
            'ready': False,
            'turn': True,
            'remain': 17,
            'board': {
                ch: {
                    i: {
                        'id': f'{ch}|{i}|none',
                        'fill': 'none',  # or 'fill' (controls css)
                        'is_hit': 'none',  # or 'is_hit'
                        'is_miss': 'none'  # or 'is_miss'
                    } for i in NUMBERS
                } for ch in LETTERS
            },
            'attack': {
                ch: {
                    i: {
                        'id': f'{ch}|{i}|none',
                        'fill': 'none',  # or 'show' or 'remain'
                        'has_hit': 'none',  # or 'has_hit'
                        'has_miss': 'none',  # or 'has_miss'
                    } for i in NUMBERS
                } for ch in LETTERS
            },
            'attacks': [],
            'boats': {boat: {} for boat in BOATS},
            'sunk': []
        },
        'player2': {
            'in': False,
            'ready': False,
            'turn': False,
            'remain': 17,
            'board': {
                ch: {
                    i: {
                        'id': f'{ch}|{i}|none',
                        'fill': 'none',  # or 'fill'
                        'is_hit': 'none',  # or 'is_hit'
                        'is_miss': 'none'  # or 'is_miss'
                    } for i in NUMBERS
                } for ch in LETTERS
            },
            'attack': {
                ch: {
                    i: {
                        'id': f'{ch}|{i}|none',
                        'fill': 'none',  # or 'show' or 'remain'
                        'has_hit': 'none',  # or 'has_hit'
                        'has_miss': 'none',  # or 'has_miss'
                    } for i in NUMBERS
                } for ch in LETTERS
            },
            'attacks': [],
            'boats': {boat: {} for boat in BOATS},
            'sunk': []
        },
        'winner': None,
        'gameover': False
    }
    return game

