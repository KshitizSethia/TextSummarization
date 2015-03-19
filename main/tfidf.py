from article import article
import math
import cPickle
import re
import os
from collections import Counter

def calculate_global_frequency():
	data_dir ="./data/data_4"
	countertotal = Counter()

	for filename in os.listdir(data_dir):
		try:
			counterdoc = Counter()
			path = os.path.join(data_dir, filename)
			thisArticle = cPickle.load(open(path,"rb"))
			for para in thisArticle.paras:
				para = re.sub('[~!@$%^&*()_+-=<>?,./;:\'\"{}\[\]\\|\n]','',para)
				words = para.split(" ")
				bigrams = zip(words, words[1:])
				for word in words:
					counterdoc[word] = 1

			countertotal += counterdoc



		except Exception as exp:
			print "\terror: " + str(exp)

	#print countertotal

	cPickle.dump(countertotal,open("idf.dat","wb"))


def tf(term,text):
	if type(term) <> tuple:
		termf = 0.0
		total = 0.0
		term = term.lower()
		text = re.sub('[~!@$%^&*()_+-=<>?,./;:\'\"{}\[\]\\|\n]','',text)
		text = text.lower()
		words = text.split(" ")
		for word in words:
			total += 1.0
			if word == term:
				termf += 1.00
		return termf/total
	else:
		termf = 0.0
		total = 0.0
		term = (term[0].lower(), term[1].lower())
		text = re.sub('[~!@$%^&*()_+-=<>?,./;:\'\"{}\[\]\\|\n]','',text)
		text = text.lower()
		words = text.split(" ")
		bigrams = zip(words, words[1:])
		for word in bigrams:
			total += 1.0
			if word==term:
				termf += 1.0
		return termf/total


def tfidf(term, text, countertotal):
	data_dir ="./data/data_4"
	#countertotal = cPickle.load(open("idf.dat","rb"))
	num_of_docs = float(len(os.listdir(data_dir))) 
	countertotal[term] += 1
	if countertotal[term] == 0:
		print "countertotal ", countertotal[term], " term ", term
	return tf(term, text) * math.log(num_of_docs/countertotal[term])

