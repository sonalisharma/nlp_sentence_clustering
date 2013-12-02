import nltk
from nltk.corpus import stopwords
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
import insert_tables as it
from collections import Counter

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
	phraseids = []
	for word in query_lemmatized.split():
		print "**************"
		print word
		print "**************"
		#query_lemma = "select * from LEMMA_TEMP where lemma='{}'".format(word)
		#print query_lemma
		#con = it.engine.execute(query_lemma)
		#rows = con.fetchall() # 13|look|looks|187   14|look|looking|189
		#ngram_ids = [ str(data[3]) for data in rows ]
		#print ngram_ids
		query_ngram = "select id from ngrams where lower(ngrams.lemmangrams) like lower('%{}%')".format(word)
		print query_ngram
		con = it.engine.execute(query_ngram)
		rows_phrase = con.fetchall()
		if rows_phrase:
			print "------------"
			print rows_phrase
			print "------------"
			ngramids = list(set([str(i[0]) for i in rows_phrase]))
		print "@@@@@@@@@@@@@@@@@@@"
		print ngramids
		print "@@@@@@@@@@@@@@@@@@@"
		phraseids.extend(ngramids)
		phraseids = list(set(phraseids))
	categorize(phraseids)

def categorize(phraseids):
	#print phraseids
	query = "select lemmangrams from ngrams where id in ({})".format(",".join(phraseids))
	con = it.engine.execute(query)
	rows_phrase = con.fetchall()
	#print rows_phrase
	n = [data[0] for data in rows_phrase]
	d = Counter(n)
	return d.most_common(20)

if __name__=='__main__':
	fetchphrases("gold magi")


















