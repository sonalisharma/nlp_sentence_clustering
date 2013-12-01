from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


SQLALCHEMY_DATBASE_URI='sqlite:///tutorial.db'
engine = create_engine(SQLALCHEMY_DATBASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

Base.metadata.create_all(bind=engine)

def newPhraseInfo(phrase):
    return {"count":0,
        "ids":set(),
        "phrase":phrase
        }

def insertdata():
	import models
	from models import Ngrams
	from models import Phrases
	allphrases = {}
	phrase_index= {}
	questions = Table('questions', metadata, autoload=True)
	r = engine.execute('select * from questions_temp')
	data = r.fetchall()
	for row in data:
	    answer = row[2]
	    ans = answer.split()
	    for i in range(len(ans)):
	        for j in range(i+1, len(ans)+1):
	            phrase = " ".join(ans[i:j])
	            #print phrase
	            #phrase = phrase.lower()
	            
	            ng=Ngrams(row[0],phrase)
	            #print ng
	            db_session.add(ng)
	            db_session.commit()
	            #print phrase
	            #print "----------"
	            phrase = phrase.lower()
	            if phrase not in allphrases:
	                allphrases[phrase] = [phrase.lower()]
	                phrase_index[phrase] = newPhraseInfo(phrase)
	            #if phrase =="the blue":
	                #print "Yes"
	                #print phrase_index[phrase]
	                #print "======================"
	            #phrase_index[phrase] = newPhraseInfo(phrase)
	            phrase_index[phrase]["count"] += 1
	            phrase_index[phrase]["ids"].add(str(row[0]))
	#print phrase_index.keys()
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
if __name__ == "__main__":
	insertdata()

