import wordseer.setup
from wordseer.util import decode_heuristically

def getSentenceText(sentence_id):
    """Returns the text of the given sentence ID. If no such sentence ID exists,
    returns None"""
    c = wordseer.setup.getCursor()
    c.execute("SELECT sentence from sentence where sentence_id = %s",
        (sentence_id,))
    sentence = c.fetchone()
    if sentence is not None:
        return sentence["sentence"]
    else:
        return None