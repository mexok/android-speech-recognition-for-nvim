from enum import Enum


def map_hjkl(word: str) -> str:
    if word == 'links':
        return 'h'
    elif word == 'runter' or word == 'unter':
        return 'j'
    elif word == 'hoch':
        return 'k'
    elif word == 'rechts':
        return 'l'
    else:
        return ''


KEY_VISUAL_MODE = "markiere"
ADDITIONAL_KEY_VISUAL_LINE_MODE = "zeile"
ADDITIONAL_KEY_VISUAL_BLOCK_MODE = "blog"


KEY_BACK = "hinten"
KEY_FRONT = "vorne"
KEY_APPEND = "danach"
KEY_ABOVE = "darüber"
KEY_BELOW = "darunter"

def is_key_insert(word: str) -> bool:
    return word == 'einfügen'


def is_key_delete(word: str) -> bool:
    return word == 'lösche' or word == 'löschen'


def is_key_copy(word: str) -> bool:
    return word == 'kopiere' or word == 'kopieren'


KEY_AGAIN = "noch"
ADDITIONAL_KEY_AGAIN = "mal"

KEY_ESCAPE = "fertig"


class MapCharModifier(Enum):
    NONE = 'none'
    GREAT = 'great'
    CURVED = 'curved'
    SQUARED = 'squared'
    BRACKET = 'bracket'


def map_char(word: str, map_char_modifier: MapCharModifier) -> str:
    s = set(['anton', 'blau', 'chor', 'dora', 'emil', 'emir', 'friedrich',
             'gustav', 'heinrich', 'ida', 'julius', 'konrad', 'ludwig',
             'martha', 'nordpol', 'otto', 'paula', 'quelle', 'richard',
             'siegfried', 'theodor', 'ulrich', 'viktor', 'wilhelm', 'xaver',
             'y', 'yipsilon', 'zeppelin'
    ])
    if word in s:
        if map_char_modifier is MapCharModifier.GREAT:
            return word[0].upper()
        return word[0]
    elif word == 'doppel':
        return ':'
    elif word == 'komma':
        return ','
    elif word == 'semikolon':
        return ';'
    elif word == 'punkt':
        return '.'
    elif word == 'klammern':
        return _get_bracket_open(map_char_modifier=map_char_modifier)
    elif word == 'auf':
        return _get_bracket_open(map_char_modifier=map_char_modifier)
    elif word == 'zu':
        return _get_bracket_close(map_char_modifier=map_char_modifier)

    return ''


def _get_bracket_open(map_char_modifier: MapCharModifier) -> str:
    if map_char_modifier is MapCharModifier.CURVED:
        return '{'
    elif map_char_modifier is MapCharModifier.SQUARED:
        return '['
    else:
        return '('


def _get_bracket_close(map_char_modifier: MapCharModifier) -> str:
    if map_char_modifier is MapCharModifier.CURVED:
        return '}'
    elif map_char_modifier is MapCharModifier.SQUARED:
        return ']'
    else:
        return ')'


def get_map_char_modifier(word: str) -> MapCharModifier:
    if word == 'groß' or word == 'große' or word == 'großer':
        return MapCharModifier.GREAT
    elif word == 'geschwungene':
        return MapCharModifier.CURVED
    elif word == 'eckige':
        return MapCharModifier.SQUARED
    elif word == 'klammer':
        return MapCharModifier.BRACKET
    else:
        return MapCharModifier.NONE


def is_key_remove(word: str) -> bool:
   return word == 'entferne' or word == 'entfernen'

