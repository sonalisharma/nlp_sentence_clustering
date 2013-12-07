import nltk
from nltk.corpus import stopwords
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
import insert_tables as it
from collections import Counter
from sqlalchemy.sql.expression import text as sql

wnl = WNL()
# SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'
#
# engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_size=100, pool_recycle=7200)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                              autoflush=False,
#                                              bind=engine))
# Base.query = db_session.query_property()


def removestopwords(query):
    wordlist = [word for word in query.split() if word not in stopwords.words('english')]
    return " ".join(wordlist)


def lemmatize(query):
    wordlist = [wnl.lemmatize(word) for word in query.split()]
    return " ".join(wordlist)


def fetchphrases(query):
    query_nostopwords = removestopwords(query)
    print query_nostopwords
    query_lemmatized = lemmatize(query_nostopwords) #look like
    print query_lemmatized
    phraseids = []
    ngramids = []
    for word in query_lemmatized.split():
        #query = "SELECT id FROM ngrams WHERE lower(lemmangrams) LIKE lower(\'\%"+str(word)+"\%\')"
        from models import Ngrams
        rows_phrase = it.db_session.query(Ngrams).filter(Ngrams.lemmangrams.like('%%%s%%' % ('python',)))
        if rows_phrase:
            ngramids = [str(i.id) for i in rows_phrase]
            phraseids.extend(ngramids)
    phraseids = list(set(phraseids))
    return categorize(phraseids)

"""
        for ngram_row in rows_phrase:
            ngram_row.id

        query = sql.text("SELECT id FROM ngrams WHERE lower(lemmangrams) like lower('%%')")
        query = "SELECT id FROM ngrams WHERE lower(lemmangrams) like lower('%%%s%%')"
        params = (word,)
        # print params
        print query
        # query = "select id from ngrams where lower(lemmangrams) like lower('%{}%')".format(str(word))
        #print query
        # r = engine.execute(query)
        # query_ngram = "select id from ngrams where lower(lemmangrams) like lower('%{}%')".format(str(word))
        con = it.engine.execute(query, params)
        rows_phrase = con.fetchall()
        temp_list = [str(i[0]) for i in rows_phrase]
        #print "First statement inside first method"
        #print temp_list
        #s = set(temp_list)

        if rows_phrase:
            ngramids = list(set([str(i[0]) for i in rows_phrase]))
        phraseids.extend(ngramids)
        phraseids = list(set(phraseids))
        print "Inside first method"
        print phraseids
    return categorize(phraseids)
"""

def categorize(phraseids):
    #print "Inside second method"
    #print phraseids
    query = "select lemmangrams from ngrams where id in ({})".format(",".join(phraseids))
    #print query
    con = it.engine.execute(query)
    rows_phrase = con.fetchall()
    #print rows_phrase
    #print rows_phrase
    n = [data[0] for data in rows_phrase]
    d = Counter(n)
    print d.most_common(20)
    return d.most_common(20)


if __name__ == '__main__':
    fetchphrases("python")


















