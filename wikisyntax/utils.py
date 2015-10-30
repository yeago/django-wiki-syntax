from wikisyntax.constants import LEFTBRACKET, RIGHTBRACKET


def balanced_brackets(value):
    len_lbrack = len(value.split(LEFTBRACKET))
    len_rbrack = len(value.split(RIGHTBRACKET))
    if len_lbrack != len_rbrack:
        return False
    return True
