import nltk
from nltk.corpus import stopwords
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer as WNL
from models import Base
import insert_tables as it
from collections import Counter
import traceback
import operator
from collections import OrderedDict
from sqlalchemy.sql.expression import text as sql

wnl = WNL()

ctr=0
limit=0


def removestopwords(query):
    wordlist = [word for word in query.split() if word not in stopwords.words('english')]
    return " ".join(wordlist)


def lemmatize(query):
    wordlist = [wnl.lemmatize(word) for word in query.split()]
    return " ".join(wordlist)


def removeurl(wordlist):
	newlist=[]
	for w in wordlist:
		phrases=str(w[0]).split()
		for phrase in phrases:
			if(phrase.startswith('http') is True):
				phrase=""
		newlist.append((phrases,w[1]))	
	return newlist

def searchphrases(query): 
	query_nostopwords = removestopwords(query)
	query_lemmatized = lemmatize(query_nostopwords) #look like
	phraseids = []
	ngramids=[]
	words=query_lemmatized.split()
	query_ngram = "select id from ngrams where lower(lemmangrams) like lower('%{}%')".format(words[0])
	for word in words[1:]:
		query_ngram=query_ngram+" or lower(lemmangrams) like lower('%{}%')".format(word)
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
	categories=d.most_common(5)
	tag_categories(categories)
	return categories

def fetchphrases(query):
	results=searchphrases(query)
	#results=removeurl(results)
	print "Results",results
	parents=OrderedDict()
	children=OrderedDict()
	grand=OrderedDict()
	categories=[]
	unigrams={}
	bigrams={}
	trigrams={}
	dups=[]
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
	if(len(unigrams)!=0):
		parents=unigrams
		if(len(bigrams)!=0):
			for unigram in unigrams.keys():
				for bigram,freq in bigrams.items():
					if(unigram in bigram):
						dups.append(bigram)
						try:
							children[unigram].append((bigram,freq))
						except:
							children[unigram]=[(bigram,freq)]

					else:
						parents[bigram]=freq
			if(len(trigrams)!=0):
				for bigram in bigrams.keys():
					for trigram,freq in trigrams.items():
						if(bigram in trigram):
							dups.append(trigram)
							try:
								grand[bigram].append((trigram,freq))
							except:
								grand[bigram]=(trigram,freq)
						else:
							try:
								children[bigram].append((trigram,freq))
							except:
								children[bigram]=(trigram,freq)
		elif(len(trigrams)!=0):
			for unigram in unigrams.keys():
				for trigram,freq in trigrams.items():
					if(unigram in trigram):
						dups.append(trigram)
						try:
							children[unigram].append((trigram,freq))
						except:
							children[unigram]=(trigram,freq)
						del trigrams[trigram]
					else:
						parents[trigram]=freq
	elif(len(bigrams)!=0):
		parents=bigrams
		if(len(trigrams)!=0):
				for bigram in bigrams.keys():
					for trigram,freq in trigrams.items():
						if(bigram in trigram):
							dups.append(trigram)
							try:
								children[bigram].append((trigram,freq))
							except:
								children[bigram]=(trigram,freq)
							del trigrams[trigram]
						else:
							parents[trigram]=freq
	elif(len(trigrams)!=0):
		parents=trigrams
	else:
		parents={}

	for d in dups:
		try:
			del parents[d]
		except:
			continue

	for key,values in children.items():
		sorted_child=sorted(values,key=lambda x:x[1],reverse=True)
		children[key]=sorted_child

	for key,values in grand.items():
		sorted_gchild=sorted(values,key=lambda x:x[1],reverse=True)
		grand[key]=sorted_gchild

	print "Parents",parents
	print "Children",children
	print "Grand",grand
	return parents,children,grand


def tag_categories(results):
	categories=[str(r[0]) for r in results]
	sorted_tags=[]
	tags=[]
	for cat in categories:
		text=nltk.word_tokenize(cat)
		tags.append(nltk.pos_tag(text))
	print "Categories and POS Tagging"
	print tags
	for tag in tags:
		print tag

if __name__=='__main__':
	fetchphrases('big data')















