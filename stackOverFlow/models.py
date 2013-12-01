from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

Base = declarative_base()
class Ngrams(Base):
    __tablename__ = 'ngrams'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,autoincrement=True, primary_key=True)
    questionid = Column(Integer)
    ngrams = Column(String(3500))
    
    def __init__(self,questionid,ngrams):
        self.questionid = questionid
        self.ngrams = ngrams
    def __repr__(self):
        return '<User %s,%s>' %(self.questionid,self.ngrams)
    def returnvalue(self):
        return self.questionid
    
class Phrases(Base):
    __tablename__ = 'phrases'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,autoincrement=True, primary_key=True)
    phrase = Column(String(4000))
    count = Column(Integer)
    questionids = Column(String(20))
    
    def __init__(self,phrase,count,ids):
        self.phrase = phrase
        self.count = count
        self.questionids = ids
    def __repr__(self):
        return '<Phrase %s,%d,%s>' %(self.phrase, self.count,self.questionids)
    
class LemmaTemp(Base):
    __tablename__ = 'LEMMA_TEMP'
    id=Column(Integer,primary_key=True,autoincrement=True)
    lemma=Column(String(25))
    original=Column(String(30))
    wordid=Column(Integer)
    #wordid=Column(Integer,ForeignKey('ngram.wordid'))

    def __init__(self,lemma,orig,wordid):
        self.lemma=lemma
        self.original=orig
        self.wordid=wordid

    def __repr__(self):
        return '<Lemma %r>' %self.lemma