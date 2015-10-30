import re
from django import forms
from .constants import WIKIBRACKETS
from .utils import balanced_brackets


def wiki(value):
    def verify(match):
        token, trail = match.groups()
        if len(token) > 150:
            raise forms.ValidationError("Seems like you've entered "
                                        "some bad [[ brackets ]]")
    if not balanced_brackets(value):
        raise forms.ValidationError("Left bracket count doesn't "
                                    "match right bracket count")
    re.sub('%s(.*?)' % WIKIBRACKETS, verify, value)
    return value
