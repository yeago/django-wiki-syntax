from django.contrib.markup.templatetags.markup import markdown
from django.utils.safestring import mark_safe

def wikisafe_markdown(value, lsafety=None, rsafety=None):
    lsafety = lsafety or 'LBRACK666' # Some unlikely nonsense
    rsafety = rsafety or 'RBRACK666' # Some unlikely nonsense
    value = value.replace('[[', lsafety).replace(']]', rsafety)
    value = markdown(value)
    value = value.replace(lsafety, '[[').replace(rsafety, ']]')
    return mark_safe(value)
