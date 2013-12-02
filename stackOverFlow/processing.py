import nltk
from nltk.corpus import stopwords
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
import insert_tables as it

wnl=WNL()

def removestopwords(query):
	wordlist =  [ word for word in query.split() if word not in stopwords.words('english') ]
	return " ".join(wordlist)

def lemmatize(query):
	wordlist =  [wnl.lemmatize(word) for word in query.split()]
	return " ".join(wordlist)

def fetchphrases(query): #looks like
	query_nostopwords = removestopwords(query)
	query_lemmatized = lemmatize(query_nostopwords) #look like
	for word in query_lemmatized.split():
		#query_lemma = "select * from LEMMA_TEMP where lemma='{}'".format(word)
		#print query_lemma
		#con = it.engine.execute(query_lemma)
		#rows = con.fetchall() # 13|look|looks|187   14|look|looking|189
		#ngram_ids = [ str(data[3]) for data in rows ]
		#print ngram_ids
		query_ngram = "select id from ngrams where ngrams.lemmangrams like '%{}%'".format(word)
		con = it.engine.execute(query_ngram)
		rows_phrase = con.fetchall()
		print rows_phrase[0]
		print type(rows_phrase) 
		ngramids = list(set([i[0] for i in rows_phrase]))
		categorize(ngramids)

def categorize(phraselist):
	print phraselist
	print "I am inside categorize"

if __name__=='__main__':
	fetchphrases("looks blue")


















