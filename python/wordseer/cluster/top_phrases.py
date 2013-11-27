import wordseer.setup
import wordseer.search
import wordseer.util

def calculateTopPhrases(query):
    """
    Calculates and returns the most frequent n-grams in the sentences
    that contain the query.

    TODO: This algorithm isn't very efficiently implemented. There are way
    too many SQL queries.
    """

    ## First get the sentences that match the query, matching all word forms
    sentences = wordseer.search.getMatchingSentencesByLemma(query);

    phrase_index = {}
    surface_phrase_index = {}
    ranked_sentence_ids = [] # Sentence IDs ordered by the order of search results.

    """
    Sentence information keyed by sentence-ID from the DB
     'sentence' - the full text of the sentence
     'phrase_ids' -  IDs of all the phrases in it
     'rank' - the order of this sentence in the search results

    """
    sentence_index = {}
    variants = {}

    for sentence in sentences:
        id = sentence["id"]
        ranked_sentence_ids.append(id)

        sentence_index[id] = sentence
        sentence_index[id]["phrase_ids"] = []
        sentence_index[id]["rank"] = len(ranked_sentence_ids)

        ## Given the sentence ID, look up all the words & lemmas in this sentence
        ## ordered by their position in the sentence.
        c = wordseer.setup.getCursor()
        sql = """SELECT lemma as lemma, surface from sentence_xref_word
            where sentence_id = %s
            ORDER BY position ASC;
            """
        c.execute(sql, (id,))
        tokens = c.fetchall();

        # the list of lemmas in the sentence
        lemmas = [w["lemma"].lower() for w in tokens]

        # the 'surface' words in its original capitalization
        surfaces = [w["surface"] for w in tokens]

        """
        Calculate all the n-grams (i.e. phrases) in this sentence as follows:
        Go through the sentence word by word. For each word, get all the
        sub-sentences starting at that word.
        Every time a new phrase is encountered, give it a unique ID.
        If a phrase already has an ID, increment its count, so that we end up
        with a count of how many times that phrase occurs in these search
        results.
        """
        for i in range(len(lemmas)):
            # Get all the sub-phrases containing this word
            for j in range(i+1, len(lemmas)+1):
                phrase = " ".join(lemmas[i:j])
                surface_phrase = " ".join(surfaces[i:j])

                # Record the surface form of the phrase as a variant
                if phrase not in variants:
                    variants[phrase] = [phrase]
                if surface_phrase not in variants:
                    variants[surface_phrase] = [surface_phrase];
                if surface_phrase not in variants[phrase]:
                    variants[phrase].append(surface_phrase)
                if phrase not in variants[surface_phrase]:
                    variants[surface_phrase].append(phrase)

                ## Remove stop words if this phrase has them and record that too
                has_stop_words = hasStopWords(lemmas[i:j])
                if not allStopWords(lemmas[i:j]):
                    if (not phrase_index.has_key(phrase)):
                        phrase_index[phrase] = newPhraseInfo(phrase,
                            has_stop_words, True)
                    if (not surface_phrase_index.has_key(surface_phrase)):
                        surface_phrase_index[surface_phrase] = newPhraseInfo(
                            surface_phrase, has_stop_words, False)
                    phrase_index[phrase]["count"] += 1
                    surface_phrase_index[surface_phrase]["count"] += 1
                    phrase_index[phrase]["ids"].add(id)
                    surface_phrase_index[surface_phrase]["ids"].add(id)
        c.close()

    phrases = removeSubsumedPhrases(phrase_index);
    surface_phrases = removeSubsumedPhrases(surface_phrase_index)
    phrase_id_index = {}
    ranked_phrase_ids = assignIDs(phrases, "lemma_", phrase_id_index, phrase_index,
        sentence_index)
    ranked_surface_phrase_ids = assignIDs(surface_phrases, "surface_", phrase_id_index,
        surface_phrase_index, sentence_index)
    ranked_phrase_ids.extend(ranked_surface_phrase_ids)
    return ranked_phrase_ids, phrase_id_index, ranked_sentence_ids, sentence_index, variants


def newPhraseInfo(phrase, has_stop_words, is_lemmatized):
    return {"count":0,
        "ids":set(),
        "phrase":phrase,
        "has_stop_words":has_stop_words,
        "is_lemmatized":is_lemmatized}

def allStopWords(words):
    """ Returns true if all the words in the given list are stop words.
    """
    for word in words:
        if not word.lower() in  wordseer.util.STOP_WORDS:
            return False
    return True

def hasStopWords(words):
    """ Returns true if this list of words contains a stop word."""
    for word in words:
        if word.lower() in wordseer.util.STOP_WORDS:
            return True
    return False

def removeSubsumedPhrases(phrase_index):
    """
    Removes shorter phrases if there are longer phrases that have the same words
    and occur in all the same sentences.
    i.e. if 'the blue' and 'the blue sky' occur in all the same sentences,
    it removes 'the blue' and only keeps the longer 'the blue sky'.

    However, if there is also 'the blue boat', it'll keep 'the blue'.
    """
    unique_phrases = set()
    disallowed = set()
    by_length = sorted(phrase_index.keys(), key=len)
    by_length.reverse()
    for phrase in by_length:
        if phrase_index[phrase]["count"] > 1 and not phrase in disallowed:
            unique_phrases.add(phrase)
            phrase_ids = phrase_index[phrase]["ids"]
            constituents = phrase.split()
            for i in range(len(constituents)):
                for j in range(i+1, len(constituents)+1):
                    sub_phrase = " ".join(constituents[i:j])
                    if phrase_index.has_key(sub_phrase):
                        sub_ids = phrase_index[sub_phrase]["ids"]
                        if phrase_ids.issuperset(sub_ids) and canSubsume(constituents, constituents[i:j]):
                            disallowed.add(sub_phrase)
                            if phrase not in sub_phrase:
                                if sub_phrase in unique_phrases:
                                    unique_phrases.remove(sub_phrase)
                        else:
                            unique_phrases.add(sub_phrase)

    def get_count(key):
        return len(phrase_index[key]["ids"])
    phrases = sorted(unique_phrases, key=get_count)
    phrases.reverse()
    for phrase in phrase_index.keys():
        if phrase not in unique_phrases:
            del(phrase_index[phrase])
        else:
            phrase_index[phrase]["ids"] = list(phrase_index[phrase]["ids"])
    return phrases

def canSubsume(phrase, sub_phrase):
    phrase_has_stops = hasStopWords(phrase)
    sub_has_stops = hasStopWords(sub_phrase)
    if phrase_has_stops:
        return sub_has_stops
    else:
        return True

def assignIDs(phrases, prefix, phrase_id_index, phrase_index, sentence_index):
    ranked_phrase_ids = []
    for i, phrase in enumerate(phrases):
        id = prefix + str(i)
        ranked_phrase_ids.append(id);
        phrase_index[phrase]["phrase_id"] = id
        phrase_id_index[id] = phrase_index[phrase];
        sentence_ids = phrase_index[phrase]["ids"]
        for sentence_id in sentence_ids:
            sentence_index[sentence_id]["phrase_ids"].append(id)
    return ranked_phrase_ids
