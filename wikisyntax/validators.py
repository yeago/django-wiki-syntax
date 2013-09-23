import re
from django import forms
from .constants import WIKIBRACKETS

def wiki(value):
    def verify(match):
        token, trail = match.groups()
        if len(token) > 250:
            raise forms.ValidationError("Seems like you've entered some bad [[ brackets ]]")
    re.sub('%s(.*?)' % WIKIBRACKETS, verify, value)
    return value

