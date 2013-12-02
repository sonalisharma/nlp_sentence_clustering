import nltk
from nltk.corpus import stopwords
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
wnl=WNL()

def removestopwords(query):
	wordlist =  [ word for word in query.split() if word not in stopwords.words('english') ]
	return " ".join(wordlist)

def lemmatize(query):
	wordlist =  [wnl.lemmatize(word) for word in query.split()]
	return " ".join(wordlist)

def fetchphrases(query):
	query_nostopwords = removestopwords(query)
	query_lemmatized = lemmatize(query_nostopwords)
	for word in query_lemmatized.split():
		db_query = "select * from LemmaTemp where lemma={}".format(word)
		con = engine.execute(db_query)
		data = con.fetchall()








