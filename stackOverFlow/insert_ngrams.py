from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from nltk.stem import WordNetLemmatizer as WNL
from models import LemmaTemp,Base

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    print Base.metadata.tables.keys()
    print Base.metadata.reflect(engine)


def newPhraseInfo(phrase):
    return {"count":0,
        "ids":set(),
        "phrase":phrase
        }

def insert_db():
    entries=[('dogs',1),('cats',2),('jumping',3),('happened',4),('best',5),('worst',6)]
    wnl=WNL()
    for e in entries:
        original=e[0]
        lemma=wnl.lemmatize(original)
        wordid=e[1]
        l=LemmaTemp(lemma,original,wordid)
        db_session.add(l)
	db_session.commit()

def insertdata():
	import models
	
	from models import Ngrams
	from models import Phrases
	allphrases = {}
	phrase_index= {}
	questions = Table('questions', Base.metadata, autoload=True)
	r = engine.execute('select * from questions_temp')
	data = r.fetchall()
	for row in data:
	    answer = row[2]
	    ans = answer.split()
	    for i in range(len(ans)):
	        for j in range(i+1, len(ans)+1):
	            phrase = " ".join(ans[i:j])
	            ng=Ngrams(row[0],phrase)
	            db_session.add(ng)
	            db_session.commit()
	            phrase = phrase.lower()
	            if phrase not in allphrases:
	                allphrases[phrase] = [phrase.lower()]
	                phrase_index[phrase] = newPhraseInfo(phrase)
	            phrase_index[phrase]["count"] += 1
	            phrase_index[phrase]["ids"].add(str(row[0]))
	i = 0
	for unique_phrases in phrase_index.keys():
		l = list(phrase_index[unique_phrases]["ids"])
		phraseids = '*'.join(l)
		print i
		i+=1
		ph = Phrases(phrase_index[str(unique_phrases)]["phrase"], phrase_index[unique_phrases]["count"], phraseids)
		print ph
    	db_session.add(ph)
    	db_session.commit() 

if __name__=='__main__':
    SQLALCHEMY_DATBASE_URI='sqlite:///Database/tutorial.db'
    engine = create_engine(SQLALCHEMY_DATBASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    init_db()
    insert_db()
    insertdata()

