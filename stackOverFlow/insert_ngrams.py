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
"""
class Ngrams(Base):
    __tablename__ = 'ngrams'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,autoincrement=True, primary_key=True)
    questionid = Column(Integer)
    ngrams = Column(String(3500))
    
    def __init__(self,questionid,ngram):
        self.quesionid = questionid
        self.ngram = ngram
    def __repr__(self):
        return '<User %s,%s>' %(self.questionid,self.ngram)
    
class Phrases(Base):
    __tablename__ = 'phrases'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,autoincrement=True, primary_key=True)
    phrase = Column(String(3000))
    count = Column(Integer)
    questionids = Column(String(3000))
    
    def __init__(self,phrase,count,ids):
        self.phrase = phrase
        self.count = count
        self.questionids = ids
    def __repr__(self):
        return '<Phrase %r>' %self.phrase
"""
def newPhraseInfo(phrase):
    return {"count":0,
        "ids":set(),
        "phrase":phrase
        }

def insertdata():
	from models import Ngrams
	from models import Phrases
	allphrases = {}
	phrase_index= {}
	questions = Table('questions', metadata, autoload=True)
	con = engine.connect()
	r = engine.execute('select * from questions_temp')
	data = r.fetchall()
	for row in data:
	    answer = row[2]
	    ans = answer.split()
	    for i in range(len(ans)):
	        for j in range(i+1, len(ans)+1):
	            phrase = " ".join(ans[i:j])
	            #phrase = phrase.lower()
	            ng = Ngrams(row[0],phrase)
	            print ng.returnvalue()
	            print ng.questionid
	            print ng.ngrams
	            #db_session.add(ng)
	            #db_session.commit()
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
	            phrase_index[phrase]["ids"].add(row[0])

	for unique_phrases in phrase_index.keys():
		ph = Phrases(phrase_index[unique_phrases], phrase_index[unique_phrases]["count"],
			phrase_index[unique_phrases]["ids"])
		#print ph.count
    #db_session.add(ph)
    #db_session.commit() 
if __name__ == "__main__":
	insertdata()

