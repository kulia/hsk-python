def get_words(test_num=1):
	'''
	Download the words for the hsk exam from hskshk.com

	:param test_num: level of hsk exam. test_num=1 for HSK1, test_num=2 for HSK2 etc.
	:return: pandas dataframe with all words in frequent order
	'''
	url = 'http://data.hskhsk.com/lists/HSK%20Official%20With%20Definitions%202012%20L{}%20freqorder.txt'
	url = url.format(test_num)

	import pandas as pd

	names = ['sim', 'trad', 'pyn', 'pyt', 'en']

	df = pd.read_csv(url, sep='\t', names=names)

	return df


def say(word):
	'''
	Use macOS built in voice to speak :code:`word`.

	:param word: string
	'''
	from os import system
	system('say -v Ting-Ting {}'.format(word))

def counter(reset=False):
	'''
	Increment counter by one every time it is called.

	:return: number of time function is called
	'''
	if reset:
		counter.num = -1

	try:
		counter.num += 1
	except AttributeError:
		counter.num = 0
	return counter.num