from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from nltk.stem import WordNetLemmatizer as WNL
from models import LemmaTemp,Base

wnl=WNL()
SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_size=100, pool_recycle=7200)
# engine = create_engine(SQLALCHEMY_DATBASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
Base.query = db_session.query_property()

def lemmatize(query):
    wordlist =  [wnl.lemmatize(word).lower() for word in query]
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
    return {"count":0,
        "ids":set(),
        "phrase":phrase
        }

def insert_db():
    from models import Ngrams
    ngrams=Ngrams.query.all()
    entries=[]
    for ngram in ngrams:
        phrase=str(ngram.ngrams)
        if len(phrase.split())==1:
            entries.append((ngram.id,phrase))
    #entries=[('dogs',1),('cats',2),('jumping',3),('happened',4),('best',5),('worst',6)]
    print entries[:10]
    wnl=WNL()
    for e in entries:
        original=e[1]
        lemma=wnl.lemmatize(original)
        wordid=e[0]
        l=LemmaTemp(lemma,original,wordid)
        db_session.add(l)
        db_session.commit()

def insertdata():
    import models   
    from models import Ngrams
    from models import Phrases
    allphrases = {}
    phrase_index= {}
    r = engine.execute('select * from questions where id < 100000')
    data = r.fetchall()
    for row in data:
        answer = row[4]
        ans = answer.split()
        for i in range(len(ans)):
            for j in range(i+1, len(ans)+1):
                phrase = " ".join(ans[i:j])
                # Getting only 4 grams instead of all ngrams
                if len(phrase.split()) < 4:
                    print row[0]
                    # print phrase
                    lemmaphrase = lemmatize(ans[i:j])
                    ng = Ngrams(row[0],phrase, lemmaphrase)
                    #print "------------"
                    #print ng.lemmangrams
                    #print "------------"
                    db_session.add(ng)
                    phrase = phrase.lower()
                    if phrase not in allphrases:
                        allphrases[phrase] = [phrase.lower()]
                        phrase_index[phrase] = newPhraseInfo(phrase)
                    phrase_index[phrase]["count"] += 1
                    phrase_index[phrase]["ids"].add(str(row[0]))
    db_session.commit()
    i = 0
    """
    for unique_phrases in phrase_index.keys():
        l = list(phrase_index[unique_phrases]["ids"])
        phraseids = '*'.join(l)
        #print i
        i+=1
        ph = Phrases(phrase_index[str(unique_phrases)]["phrase"], phrase_index[unique_phrases]["count"], phraseids)
        #print ph
        db_session.add(ph)
        db_session.commit() 
    """

if __name__=='__main__':
    init_db()
    Base.metadata.bind=engine
    insertdata()
    #insert_db()

