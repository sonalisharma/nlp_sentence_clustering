import nltk
from nltk.corpus import stopwords
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
import insert_tables as it
from collections import Counter
import traceback

wnl=WNL()
ctr=0
limit=0

def removestopwords(query):
	wordlist =  [ word for word in query.split() if word not in stopwords.words('english') ]
	return " ".join(wordlist)

def lemmatize(query):
	wordlist =  [wnl.lemmatize(word) for word in query.split()]
	return " ".join(wordlist)

def removeurl(wordlist):
	newlist=[]
	for w in wordlist:
		if(str(w).startswith("http") is False):
			newlist.append(w)	
	return newlist

def searchphrases(query): 
	query_nostopwords = removestopwords(query)
	query_lemmatized = lemmatize(query_nostopwords) #look like
	phraseids = []
	ngramids=[]
	words=query_lemmatized.split()
	query_ngram = "select id from ngrams where lower(lemmangrams) like lower('%{}%')".format(words[0])
	for word in words[1:]:
		query_ngram=query_ngram+" and lower(lemmangrams) like lower('%{}%')".format(word)
	con = it.engine.execute(query_ngram)
	rows_phrase = con.fetchall()
	if rows_phrase:
		ngramids = list(set([str(i[0]) for i in rows_phrase]))
	phraseids.extend(ngramids)
	phraseids = list(set(phraseids))
	results=categorize(phraseids)
	return results

def categorize(phraseids):
	query = "select lemmangrams from ngrams where id in ({})".format(",".join(phraseids))
	con = it.engine.execute(query)
	rows_phrase = con.fetchall()
	n = [data[0] for data in rows_phrase]
	d = Counter(n)
	return d.most_common(100)

def fetchphrases(query):
	results=searchphrases(query)
	print results
	parents={}
	children={}
	categories=[]
	unigrams={}
	bigrams={}
	trigrams={}
	grand={}
	for cat in results:
		categories.append(cat[0])
	for cat in results:
		try:
			phrase=str(cat[0]).split()
			if(len(phrase)==1):
				categories.remove(cat[0])
				unigrams[phrase[0]]=cat[1]
			elif(len(phrase)==2):
				phrase=" ".join(phrase)
				categories.remove(cat[0])
				bigrams[phrase]=cat[1]
			elif(len(phrase)==3):
				phrase=" ".join(phrase)
				categories.remove(cat[0])
				trigrams[phrase]=cat[1]
			else:
				print "Rest in categories"
		except:
			print "Exception in ",phrase
			print traceback.format_exc()
	if(unigrams is not None):
		parents=unigrams
		if(bigrams is not None):
			for unigram in unigrams.keys():
				for bigram,freq in bigrams.items():
					if(unigram in bigram):
						children[unigram]=(bigram,freq)
			if(trigrams is not None):
				for bigram in bigrams.keys():
					for trigram,freq in trigrams.items():
						if(bigram in trigram):
							grand[bigram]=(trigram,freq)
		elif(trigrams is not None):
			for unigram in unigrams.keys():
				for trigram,freq in trigrams.items():
					if(unigram in trigram):
						children[unigram]=(trigram,freq)
	elif(bigrams is not None):
		parents=bigrams
		if(trigrams is not None):
				for bigram in bigrams.keys():
					for trigram,freq in trigrams.items():
						if(bigram in trigram):
							children[bigram]=(trigram,freq)
	elif(trigrams is not None):
		parents=trigrams
	else:
		parents={}
	print "Parents",parents
	print "Children",children
	print "Grand",grand
	return parents,children,grand

if __name__=='__main__':
	fetchphrases('memory')














