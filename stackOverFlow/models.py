from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Ngrams(Base):
    __tablename__ = 'ngrams'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,autoincrement=True, primary_key=True)
    questionid = Column(Integer)
    ngrams = Column(String(3500))
    lemmangrams = Column(String(3500))
    
    def __init__(self,questionid,ngrams,lemmangrams):
        self.questionid = questionid
        self.ngrams = ngrams
        self.lemmangrams = lemmangrams
    def __repr__(self):
        return '<Ngrams %s,%s>' %(self.id,self.ngrams)
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


class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    ques_text = Column(String(3500))
    answer_id = Column(Integer)
    answer_text = Column(String(3500))
    answer_wo_stop_words = Column(String(3500))

    def __init__(self, ques_id, ques_text, answer_id):
        self.id = ques_id
        self.ques_text = ques_text
        self.answer_id = answer_id

    def __repr__(self):
        return '<Question %s,%s>' % (self.ques_text, self.answer_text)

    def return_value(self):
        return self.ques_text


class Answers(Base):
    __tablename__ = 'answers'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    answer_text = Column(String(3500))
    answer_wo_stop_words = Column(String(3500))

    def __init__(self, ans_id, ans_text):
        self.id = ans_id
        self.answer_text = ans_text

    def __repr__(self):
        return '<Answer %s,%s>' % (self.id, self.answer_text)

    def return_value(self):
        return self.answer_text
