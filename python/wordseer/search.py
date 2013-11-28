import wordseer.setup
from wordseer.util import decode_heuristically, punctuation

def getMatchingSentenceText(query):
    c = wordseer.setup.getCursor();
    c.execute("SELECT sentence, tagged from sentence WHERE MATCH sentence AGAINST(%s);",
        (query,))
    sentence = c.fetchone()
    while not sentence == None:
        result = decode_heuristically(sentence["sentence"])[0]
        sentence = c.fetchone()
        yield result
    c.close()        

def getMatchingSentencesIDs(query):
    c = wordseer.setup.getCursor();
    c.execute("SELECT id from sentence WHERE MATCH sentence AGAINST(%s);",
        (query,))
    sentence = c.fetchone()
    while not sentence == None:
        yield sentence["id"]
        sentence = c.fetchone()
    c.close()

def getMatchingSentences(query):
    c = wordseer.setup.getCursor();
    c.execute("SELECT * from sentence WHERE MATCH sentence AGAINST(%s);",
        (query,))
    sentence = c.fetchone()
    while not sentence == None:
        yield sentence
        sentence = c.fetchone()
    c.close()    

def getMatchingSentencesByLemma(query, limit=None):
    lemmas = getLemmas(query)
    sentence_ids = []
    for lemma in lemmas:
        sentence_ids.extend(getSentenceIDsByLemma(lemma, limit))
    return getSentencesByID(sentence_ids)

def getSentenceIDsByLemma(lemma, limit=None):
    sentence_ids = []
    c = wordseer.setup.getCursor()
    query = "SELECT sentence_id from sentence_xref_word where lemma = %s "
    if limit is not None:
        query += "LIMIT "+str(limit);
    c.execute(query, (lemma,))
    id_results = c.fetchall()
    c.close()
    for id_result in id_results:
        sentence_ids.append(id_result["sentence_id"])
    return sentence_ids

def getSentencesByID(sentence_ids):
    c = wordseer.setup.getCursor()
    c.execute("SELECT * from sentence WHERE id in %s;", (sentence_ids,))
    sentence = c.fetchone()
    while not sentence == None:
        yield sentence
        sentence = c.fetchone()
    c.close()
    
def getLemmas(query):
    lemmas = [];
    for word in query.split():
        text = word;
        for punctuation in wordseer.util.punctuation:
            if punctuation in word:
                text = text.split(punctuation)[0]
        c = wordseer.setup.getCursor()
        c.execute("SELECT lemma from word where word = %s;", (text,))
        lemma_results = c.fetchall()
        for lemma_result in lemma_results:
            if lemma_result["lemma"] not in lemmas:
                lemmas.append(lemma_result["lemma"])
        c.close()
    return lemmas
