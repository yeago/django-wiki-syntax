from wikisyntax.constants import LEFTBRACKET, RIGHTBRACKET


def balanced_brackets(value):
    len_lbrack = len([i for i in value.split(LEFTBRACKET)])
    len_rbrack = len([i for i in value.split(RIGHTBRACKET)])
    if len_lbrack != len_rbrack:
        return False
    return True
