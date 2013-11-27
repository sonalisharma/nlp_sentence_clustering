import sys
import re

def decode_heuristically(string, enc = None, denc = sys.getdefaultencoding()):
    """
    Try to interpret 'string' using several possible encodings.
    @input : string, encode type.
    @output: a list [decoded_string, flag_decoded, encoding]
    """
    if isinstance(string, unicode): return string, 0, "utf-8"
    try:
        new_string = unicode(string, "ascii")
        return string, 0, "ascii"
    except UnicodeError:
        encodings = ["utf-8","iso-8859-1","cp1252","iso-8859-15"]

        if denc != "ascii": encodings.insert(0, denc)

        if enc: encodings.insert(0, enc)

        for enc in encodings:
            if (enc in ("iso-8859-15", "iso-8859-1") and
                re.search(r"[\x80-\x9f]", string) is not None):
                continue

            if (enc in ("iso-8859-1", "cp1252") and
                re.search(r"[\xa4\xa6\xa8\xb4\xb8\xbc-\xbe]", string)\
                is not None):
                continue

            try:
                new_string = unicode(string, enc)
            except UnicodeError:
                pass
            else:
                if new_string.encode(enc) == string:
                    return new_string, 0, enc

        # If unable to decode,doing force decoding i.e.neglecting those chars.
        output = [(unicode(string, enc, "ignore"), enc) for enc in encodings]
        output = [(len(new_string[0]), new_string) for new_string in output]
        output.sort()
        new_string, enc = output[-1][1]
        return new_string, 1, enc

prepositions = """about away across against along around at behind beside besides by 
despite down during for from in inside into near of off on onto over through to
toward with within whence until without upon hither thither unto""".split()

pronouns = """i its it you thou thee we he they me us her them him my mine her 
hers his our thy thine ours their theirs myself itself mimself ourselves herself themselves anything
something everything nothing anyone someone everyone ones such""".split()

determiners = """the a an some any this these each that no every all half both twice
one two first second other another next last many few much little more less most least
several no own""".split()

conjunctions = """and or but so after before when since as while because although
if though what who where whose which how than nor not""".split()

modal_verbs = """can canst might may would wouldst will willst 
should shall must could""".split()

primary_verbs = """is be been being went go do doth have hath was were had""".split()

adverbs = """again very here there today tomorrow now then always never sometimes usually
often therefore however besides moreover though otherwise else instead anyway
incidentally meanwhile""".split()

punctuation = """. ! @ # $ % ^ & * ( ) _ - + = ` ~ { } [ ] | \\ : ; " ' < > ? , . 
/ """.split()

contractions = """ 's 'nt 'll o s""".split()

STOP_WORDS = [];
#STOP_WORDS = extend(pronouns)
STOP_WORDS.extend(prepositions)
STOP_WORDS.extend(determiners)
STOP_WORDS.extend(conjunctions)
STOP_WORDS.extend(modal_verbs)
STOP_WORDS.extend(primary_verbs)
#STOP_WORDS.extend(adverbs)
STOP_WORDS.extend(punctuation)
STOP_WORDS.extend(contractions)
