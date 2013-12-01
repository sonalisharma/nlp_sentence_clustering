from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
#from create_lemma import Base
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()


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


