from lxml import etree
import re
import os
import sys
from parser import Parser
from tools import Tokenizer
from tools import StopWordStem
from tools import Indexer
from merge_sort import merge_sort_parallel
from sort import sort_file

class WikiIndexCreator():
	def __init__(self):
		self.parser = Parser()
		self.tokenizer = Tokenizer()
		self.sws = StopWordStem()
		self.indexer = Indexer()

	def write_index(self, index, id, arr):
		'''
		out = open('index', 'a+')
		for word in index:
			line = word + ":" + "d" + id + "-"
			if "t" in index[word]:
				line += "t" + str(index[word]["t"])
			if "b" in index[word]:
				line += "b" + str(index[word]["b"])
			out.write(line + "\n")

		out.close()
		'''
		for word in index:
			line = word + ":" + "d" + id + "-"
			if "t" in index[word]:
				line += "t" + str(index[word]["t"])
			if "b" in index[word]:
				line += "b" + str(index[word]["b"])
			if "c" in index[word]:
				line += "c" + str(index[word]["c"])
			if "i" in index[word]:
				line += "i" + str(index[word]["i"])
			if "l" in index[word]:
				line += "l" + str(index[word]["l"])
			arr.append(line + "\n")

		return arr

	def process(self, text):
		text = self.tokenizer.tokenize(text)
		text = self.sws.remove_and_stem(text)
		text = self.indexer.create_map(text)
		return text

	def build_params(self, element):
		id, title, body, cat, info, links = self.parser.parse_page(element)

		title = self.process(title)
		body = self.process(body)
		cat = self.process(cat)
		info = self.process(info)
		links = self.process(links)

		index = self.indexer.combine_maps(title, body, cat, info, links)
		return index, id

	def create(self, infilename, outfilename):
		context = etree.iterparse(infilename, events=('end',),
						tag='{http://www.mediawiki.org/xml/export-0.8/}page')

		arr = []

		for event, elem in context:
			index, id = self.build_params(elem)

			arr = self.write_index(index, id, arr)
			#self.write_index(index, id, arr)

			elem.clear()
			while elem.getprevious() is not None:
				del elem.getparent()[0]

		#sort_file("index", "10M")

		index = merge_sort_parallel(arr)
		out = open(outfilename, "w+")
		for line in index:
			out.write(line)
		out.close()


length = len(sys.argv)
if length < 3:
	print("Not enough arguments given. Please specify input and output files.")
else:
	indexer = WikiIndexCreator()
	indexer.create(sys.argv[1], sys.argv[2])
