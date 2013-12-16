# Initial loading of data into tables
# =====================================
# This code is used to populate the ngrams table in the database
# We read all answers from the questions table, tokenize them,
# lemmatize and store unigram, bgrams amd trigrams in ngrams table.
# The table also stores question id.
#
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from nltk.stem import WordNetLemmatizer as WNL
from models import LemmaTemp,Base

wnl=WNL()
# Initializing database
SQLALCHEMY_DATABASE_URI = 'sqlite:///tutorial.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

def lemmatize(query):
    """
    Lemmatizing the input text
    """
    wordlist = [wnl.lemmatize(word).lower() for word in query]
    return " ".join(wordlist)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.bind=engine
    Base.metadata.create_all(bind=engine)
    #print Base.metadata.tables.keys()
    #print Base.metadata.reflect(engine)


def newPhraseInfo(phrase):
    """
    This method is used to store the number of Phrases
    the set of associated question ids and the phrase itself in the formm
    of dictionary. 
    """
    return {"count":0,
        "ids":set(),
        "phrase":phrase
        }

def insertdata():
    """
    Method is used to insert data into ngrams table.
    Input:
    Data read from questions table. Format -
    questionid | questiontext | answer id | answer text | answer w/o stopword 

    Output:
    Data inserted in ngrams table
    Format -
    ngrams id | question id | ngram | lemmatized ngram

    e.g.
    1|4|explicit|explicit
    2|4|explicit cast|explicit cast
    3|4|explicit cast double|explicit cast double
    4|4|cast|cast
    5|4|cast double|cast double
    6|4|cast double isnt|cast double isnt

    """
    import models   
    from models import Ngrams
    from models import Phrases
    allphrases = {}
    phrase_index= {}
    # Reading 100000 questions for this project. Original data was 7GB 
    # and very large to process.
    r = engine.execute('select * from questions where id < 100000')
    data = r.fetchall()
    for row in data:
        answer = row[4]
        # Tokenizing answer
        ans = answer.split()
        for i in range(len(ans)):
            # Running inner loop to generate trigrams
            for j in range(i+1, len(ans)+1):
                phrase = " ".join(ans[i:j])
                # Getting only 3 grams instead of all ngrams
                if len(phrase.split()) < 4:
                    print row[0]
                    lemmaphrase = lemmatize(ans[i:j])
                    ng = Ngrams(row[0],phrase, lemmaphrase)
                    db_session.add(ng)
                    phrase = phrase.lower()
                    if phrase not in allphrases:
                        allphrases[phrase] = [phrase.lower()]
                        phrase_index[phrase] = newPhraseInfo(phrase)
                    phrase_index[phrase]["count"] += 1
                    phrase_index[phrase]["ids"].add(str(row[0]))
    db_session.commit()

if __name__=='__main__':
    init_db()
    Base.metadata.bind=engine
    insertdata()

