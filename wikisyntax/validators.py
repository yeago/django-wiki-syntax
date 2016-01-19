from django import forms
from .constants import LEFTBRACKET, RIGHTBRACKET


def brackets(value):
    left_open = prev = None
    trail_token = token = []
    for char in value or '':
        trail_token.append(char)
        if not prev:
            prev = char
            continue

        if left_open:
            token.append(char)

        if prev + char == LEFTBRACKET:
            if left_open:
                raise forms.ValidationError("Bad brackets near '%s'" % "".join(trail_token))
            left_open = True

        if prev + char == RIGHTBRACKET:
            if not left_open:
                raise forms.ValidationError("Bad brackets near '%s'" % "".join(trail_token))
            token = []
            left_open = False

        if token and len(token) > 250:
            raise forms.ValidationError("Bad brackets near '%s'" % "".join(trail_token))

        trail_token = trail_token[-250:]

        prev = char

    if left_open:
        raise forms.ValidationError("Bad brackets near '%s'" % "".join(trail_token))
    return value
