from parser import Parser
from tools import Tokenizer
from tools import StopWordStem
from tools import Indexer
from lxml import etree
import re

class WikiIndexCreator():
	def __init__(self):
		self.parser = Parser()
		self.tokenizer = Tokenizer()
		self.sws = StopWordStem()
		self.indexer = Indexer()

	def write_index(self, index, id):
		out = open('out.txt', 'a+')
		for word in index:
			line = word + " : " + "d" + id + " -"
			if "t" in index[word]:
				line += " t" + str(index[word]["t"])
			if "b" in index[word]:
				line += " b" + str(index[word]["b"])
			out.write(line + "\n")

		out.close()

	def create(self, filename):
		context = etree.iterparse(filename, events=('end',),
						tag='{http://www.mediawiki.org/xml/export-0.8/}page')

		for event, elem in context:
			id, title, body = self.parser.parse_page(elem)

			title = self.tokenizer.tokenize(title)
			body = self.tokenizer.tokenize(body)

			title = self.sws.remove_and_stem(title)
			body = self.sws.remove_and_stem(body)

			title = self.indexer.create_map(title)
			body = self.indexer.create_map(body)
			index = self.indexer.combine_maps(title, body)

			self.write_index(index, id)

			#print(index)
			#print("\n\n\n\n\n\n")

			#print(text)

			elem.clear()
			while elem.getprevious() is not None:
				del elem.getparent()[0]

indexer = WikiIndexCreator()
indexer.create('wiki-search-small.xml')
