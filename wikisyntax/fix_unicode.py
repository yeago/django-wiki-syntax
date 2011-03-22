# If the character doesn't exist in the dictionary, add it as None
# and also return None.  This tells the translate to delete the character
# and makes the next lookup for that character faster.
class XLate(dict):
    def __getitem__(self, c):
        try:
            return dict.__getitem__(self, c)
        except KeyError:
            self[c] = None
            return None

# Define the translation table.  I needed to hammer unicode going to
# NCBI's web services (for Biopython's EUtils package) so I used the
# table defined at
#  http://www.nlm.nih.gov/databases/dtd/medline_character_database.utf8
# This is not as extensive as the original conversion set.
class XLate(dict):
    def __getitem__(self, c):
        try:
            return dict.__getitem__(self, c)
        except KeyError:
            self[c] = None
            return None

# Convert these unicode characters into ASCII
xlate = XLate({
    # The note at the bottom of the page says "the inverted question
    # mark represents a questionable character found as a result of
    # NLM's conversion from its legacy extended EBCDIC character set
    # to UNICODE UTF-8."  I do not use it but leave it here for
    # completeness.
    ord(u"\N{INVERTED QUESTION MARK}"): None,

    ord(u"\N{LATIN CAPITAL LETTER O WITH STROKE}"): u"O",
    ord(u"\N{LATIN SMALL LETTER A WITH GRAVE}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH ACUTE}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH TILDE}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH DIAERESIS}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH RING ABOVE}"): u"a",
    ord(u"\N{LATIN SMALL LETTER C WITH CEDILLA}"): u"c",
    ord(u"\N{LATIN SMALL LETTER E WITH GRAVE}"): u"e",
    ord(u"\N{LATIN SMALL LETTER E WITH ACUTE}"): u"e",
    ord(u"\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}"): u"e",
    ord(u"\N{LATIN SMALL LETTER E WITH DIAERESIS}"): u"e",
    ord(u"\N{LATIN SMALL LETTER I WITH GRAVE}"): u"i",
    ord(u"\N{LATIN SMALL LETTER I WITH ACUTE}"): u"i",
    ord(u"\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}"): u"i",
    ord(u"\N{LATIN SMALL LETTER I WITH DIAERESIS}"): u"i",
    ord(u"\N{LATIN SMALL LETTER N WITH TILDE}"): u"n",
    ord(u"\N{LATIN SMALL LETTER O WITH GRAVE}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH ACUTE}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH TILDE}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH DIAERESIS}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH STROKE}"): u"o",
    ord(u"\N{LATIN SMALL LETTER U WITH GRAVE}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH ACUTE}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH DIAERESIS}"): u"u",
    ord(u"\N{LATIN SMALL LETTER Y WITH ACUTE}"): u"y",
    ord(u"\N{LATIN SMALL LETTER Y WITH DIAERESIS}"): u"y",
    ord(u"\N{LATIN SMALL LETTER A WITH MACRON}"): u"a",
    ord(u"\N{LATIN SMALL LETTER A WITH BREVE}"): u"a",
    ord(u"\N{LATIN SMALL LETTER C WITH ACUTE}"): u"c",
    ord(u"\N{LATIN SMALL LETTER C WITH CIRCUMFLEX}"): u"c",
    ord(u"\N{LATIN SMALL LETTER E WITH MACRON}"): u"e",
    ord(u"\N{LATIN SMALL LETTER E WITH BREVE}"): u"e",
    ord(u"\N{LATIN SMALL LETTER G WITH CIRCUMFLEX}"): u"g",
    ord(u"\N{LATIN SMALL LETTER G WITH BREVE}"): u"g",
    ord(u"\N{LATIN SMALL LETTER G WITH CEDILLA}"): u"g",
    ord(u"\N{LATIN SMALL LETTER H WITH CIRCUMFLEX}"): u"h",
    ord(u"\N{LATIN SMALL LETTER I WITH TILDE}"): u"i",
    ord(u"\N{LATIN SMALL LETTER I WITH MACRON}"): u"i",
    ord(u"\N{LATIN SMALL LETTER I WITH BREVE}"): u"i",
    ord(u"\N{LATIN SMALL LETTER J WITH CIRCUMFLEX}"): u"j",
    ord(u"\N{LATIN SMALL LETTER K WITH CEDILLA}"): u"k",
    ord(u"\N{LATIN SMALL LETTER L WITH ACUTE}"): u"l",
    ord(u"\N{LATIN SMALL LETTER L WITH CEDILLA}"): u"l",
    ord(u"\N{LATIN CAPITAL LETTER L WITH STROKE}"): u"L",
    ord(u"\N{LATIN SMALL LETTER L WITH STROKE}"): u"l",
    ord(u"\N{LATIN SMALL LETTER N WITH ACUTE}"): u"n",
    ord(u"\N{LATIN SMALL LETTER N WITH CEDILLA}"): u"n",
    ord(u"\N{LATIN SMALL LETTER O WITH MACRON}"): u"o",
    ord(u"\N{LATIN SMALL LETTER O WITH BREVE}"): u"o",
    ord(u"\N{LATIN SMALL LETTER R WITH ACUTE}"): u"r",
    ord(u"\N{LATIN SMALL LETTER R WITH CEDILLA}"): u"r",
    ord(u"\N{LATIN SMALL LETTER S WITH ACUTE}"): u"s",
    ord(u"\N{LATIN SMALL LETTER S WITH CIRCUMFLEX}"): u"s",
    ord(u"\N{LATIN SMALL LETTER S WITH CEDILLA}"): u"s",
    ord(u"\N{LATIN SMALL LETTER T WITH CEDILLA}"): u"t",
    ord(u"\N{LATIN SMALL LETTER U WITH TILDE}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH MACRON}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH BREVE}"): u"u",
    ord(u"\N{LATIN SMALL LETTER U WITH RING ABOVE}"): u"u",
    ord(u"\N{LATIN SMALL LETTER W WITH CIRCUMFLEX}"): u"w",
    ord(u"\N{LATIN SMALL LETTER Y WITH CIRCUMFLEX}"): u"y",
    ord(u"\N{LATIN SMALL LETTER Z WITH ACUTE}"): u"z",
    ord(u"\N{LATIN SMALL LETTER W WITH GRAVE}"): u"w",
    ord(u"\N{LATIN SMALL LETTER W WITH ACUTE}"): u"w",
    ord(u"\N{LATIN SMALL LETTER W WITH DIAERESIS}"): u"w",
    ord(u"\N{LATIN SMALL LETTER Y WITH GRAVE}"): u"y",
    })

# These are the ASCII characters NCBI knows about.  Note that I'm
# building one unicode string here, and not a tuple of unicode
# characters.
for c in (u"\N{SPACE}"
          u"\N{EXCLAMATION MARK}"
          u"\N{QUOTATION MARK}"
          u"\N{NUMBER SIGN}"
          u"\N{DOLLAR SIGN}"
          u"\N{PERCENT SIGN}"
          u"\N{AMPERSAND}"
          u"\N{APOSTROPHE}"
          u"\N{LEFT PARENTHESIS}"
          u"\N{RIGHT PARENTHESIS}"
          u"\N{ASTERISK}"
          u"\N{PLUS SIGN}"
          u"\N{COMMA}"
          u"\N{HYPHEN-MINUS}"
          u"\N{FULL STOP}"
          u"\N{SOLIDUS}"
          u"\N{DIGIT ZERO}"
          u"\N{DIGIT ONE}"
          u"\N{DIGIT TWO}"
          u"\N{DIGIT THREE}"
          u"\N{DIGIT FOUR}"
          u"\N{DIGIT FIVE}"
          u"\N{DIGIT SIX}"
          u"\N{DIGIT SEVEN}"
          u"\N{DIGIT EIGHT}"
          u"\N{DIGIT NINE}"
          u"\N{COLON}"
          u"\N{SEMICOLON}"
          u"\N{LESS-THAN SIGN}"
          u"\N{EQUALS SIGN}"
          u"\N{GREATER-THAN SIGN}"
          u"\N{QUESTION MARK}"
          u"\N{COMMERCIAL AT}"
          u"\N{LATIN CAPITAL LETTER A}"
          u"\N{LATIN CAPITAL LETTER B}"
          u"\N{LATIN CAPITAL LETTER C}"
          u"\N{LATIN CAPITAL LETTER D}"
          u"\N{LATIN CAPITAL LETTER E}"
          u"\N{LATIN CAPITAL LETTER F}"
          u"\N{LATIN CAPITAL LETTER G}"
          u"\N{LATIN CAPITAL LETTER H}"
          u"\N{LATIN CAPITAL LETTER I}"
          u"\N{LATIN CAPITAL LETTER J}"
          u"\N{LATIN CAPITAL LETTER K}"
          u"\N{LATIN CAPITAL LETTER L}"
          u"\N{LATIN CAPITAL LETTER M}"
          u"\N{LATIN CAPITAL LETTER N}"
          u"\N{LATIN CAPITAL LETTER O}"
          u"\N{LATIN CAPITAL LETTER P}"
          u"\N{LATIN CAPITAL LETTER Q}"
          u"\N{LATIN CAPITAL LETTER R}"
          u"\N{LATIN CAPITAL LETTER S}"
          u"\N{LATIN CAPITAL LETTER T}"
          u"\N{LATIN CAPITAL LETTER U}"
          u"\N{LATIN CAPITAL LETTER V}"
          u"\N{LATIN CAPITAL LETTER W}"
          u"\N{LATIN CAPITAL LETTER X}"
          u"\N{LATIN CAPITAL LETTER Y}"
          u"\N{LATIN CAPITAL LETTER Z}"
          u"\N{LEFT SQUARE BRACKET}"
          u"\N{REVERSE SOLIDUS}"
          u"\N{RIGHT SQUARE BRACKET}"
          u"\N{LOW LINE}"
          u"\N{LATIN SMALL LETTER A}"
          u"\N{LATIN SMALL LETTER B}"
          u"\N{LATIN SMALL LETTER C}"
          u"\N{LATIN SMALL LETTER D}"
          u"\N{LATIN SMALL LETTER E}"
          u"\N{LATIN SMALL LETTER F}"
          u"\N{LATIN SMALL LETTER G}"
          u"\N{LATIN SMALL LETTER H}"
          u"\N{LATIN SMALL LETTER I}"
          u"\N{LATIN SMALL LETTER J}"
          u"\N{LATIN SMALL LETTER K}"
          u"\N{LATIN SMALL LETTER L}"
          u"\N{LATIN SMALL LETTER M}"
          u"\N{LATIN SMALL LETTER N}"
          u"\N{LATIN SMALL LETTER O}"
          u"\N{LATIN SMALL LETTER P}"
          u"\N{LATIN SMALL LETTER Q}"
          u"\N{LATIN SMALL LETTER R}"
          u"\N{LATIN SMALL LETTER S}"
          u"\N{LATIN SMALL LETTER T}"
          u"\N{LATIN SMALL LETTER U}"
          u"\N{LATIN SMALL LETTER V}"
          u"\N{LATIN SMALL LETTER W}"
          u"\N{LATIN SMALL LETTER X}"
          u"\N{LATIN SMALL LETTER Y}"
          u"\N{LATIN SMALL LETTER Z}"
          u"\N{VERTICAL LINE}"
          u"\N{TILDE}"):
    xlate[ord(c)] = c
    
def fix_unicode(s):
    try:
       return str(s.translate(xlate))
    except TypeError:
       return s
