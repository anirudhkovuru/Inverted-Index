from lxml import etree
import re

redirectPattern = re.compile("#"+"#REDIRECT"+"\\s*\\[\\[(.*?)\\]\\]")
stubPattern = re.compile("\\-"+"stub"+"\\}\\}")
disambiguationPattern = re.compile("\\{\\{"+"disambig"+"\\}\\}")

stylesPattern = re.compile("\\{\\|.*?\\|\\}$")
infoboxCleanUpPattern = re.compile("\\{\\{infobox.*?\\}\\}")
curlyCleanUpPattern0 = re.compile("^\\{\\{.*?\\}\\}$")
curlyCleanUpPattern1 = re.compile("\\{\\{.*?\\}\\}")
tagsPattern = re.compile("<.*>")
commentsCleanUpPattern = re.compile("<!--.*?-->")
linkPattern = re.compile("\[http.*]")
numberPattern = re.compile("[ ]+[0-9]+[ ]+")
quotePattern = re.compile("[']")
specCharsPattern = re.compile("[^A-Za-z0-9 ]")

class Parser():
	def __init__(self):
		pass

	def clean(self, text):
		text = re.sub(stylesPattern, "", text)
		text = re.sub(infoboxCleanUpPattern, "", text)
		text = re.sub(curlyCleanUpPattern0, "", text)
		text = re.sub(curlyCleanUpPattern1, "", text)
		text = re.sub(tagsPattern, "", text)
		text = re.sub(commentsCleanUpPattern, "", text)
		text = re.sub(linkPattern, "", text)
		text = re.sub(quotePattern, "", text)
		text = re.sub(specCharsPattern, " ", text)
		text = re.sub(numberPattern, "", text)
		return text

	def parse_id(self, element):
		idElem = element.xpath('.//x:id',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
		return idElem[0].text

	def parse_title(self, element):
		titleElem = element.xpath('.//x:redirect',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
		if not titleElem:
			titleElem = element.xpath('.//x:title',
	 					namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
			return self.clean(titleElem[0].text)
		else:
			return self.clean(titleElem[0].get('title'))

	def parse_text(self, element):
		textElem = element.xpath('.//x:text',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
		text = self.clean(textElem[0].text)
		return text

	def parse_page(self, element):
		id = self.parse_id(element)
		title = self.parse_title(element)
		text = self.parse_text(element)
		return id, title, text
