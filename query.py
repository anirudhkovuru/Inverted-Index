import re
from tools import Tokenizer
from tools import StopWordStem
from parse import Parser
from collections import Counter
import math as m
import operator

tokenizer = Tokenizer()
sws = StopWordStem()
parser = Parser()

titlePattern = re.compile("t:(.+?)(?=[tclrib][:]|$)", re.M)
categoryPattern = re.compile("c:(.+?)(?=[tclrib][:]|$)", re.M)
infoboxPattern = re.compile("i:(.+?)(?=[tclrib][:]|$)", re.M)
referencePattern = re.compile("r:(.+?)(?=[tclrib][:]|$)", re.M)
linkPattern = re.compile("l:(.+?)(?=[tclrib][:]|$)", re.M)
bodyPattern = re.compile("b:(.+?)(?=[tclrib][:]|$)", re.M)

N = 17640866


class QueryParser:
    def __init__(self, query):
        self.q = query

    def parse_query(self, pattern):
        try:
            text = re.findall(pattern, self.q)
            text = " ".join(text)
            text = parser.clean(text)
            text = self.linguistic_tech(text)
        except:
            text = {}
        return text

    def linguistic_tech(self, text):
        text = parser.clean(text)
        text = tokenizer.tokenize(text)
        text = sws.remove_and_stem(text)
        text = Counter(text)
        for k, v in text.items():
            text[k] = m.log10(1 + v)
        return text

    def process_query(self):
        if ":" in self.q:
            title = self.parse_query(titlePattern)
            category = self.parse_query(categoryPattern)
            infobox = self.parse_query(infoboxPattern)
            reference = self.parse_query(referencePattern)
            link = self.parse_query(linkPattern)
            body = self.parse_query(bodyPattern)
            self.q = dict()
            self.q["t"] = title
            self.q["c"] = category
            self.q["i"] = infobox
            self.q["r"] = reference
            self.q["l"] = link
            self.q["b"] = body
            return False
        else:
            self.q = self.linguistic_tech(self.q)
            return True


def cos_rank(q, doc_list, idf):
    top_docs = {}
    for doc, doc_vec in doc_list.items():
        dot = 0
        for k in q:
            if k in doc_vec:
                dot += q[k] * idf[k] * doc_vec[k]

        magnitude_q = 0
        for k in q:
            magnitude_q += (q[k] * idf[k]) ** 2
        magnitude_q = m.sqrt(magnitude_q)

        magnitude_d = 0
        for k in doc_vec:
            magnitude_d += doc_vec[k] ** 2
        magnitude_d = m.sqrt(magnitude_d)

        top_docs[doc] = dot / (magnitude_q * magnitude_d)
    top_docs = dict(sorted(top_docs.items(), key=operator.itemgetter(1), reverse=True)[:10])
    return top_docs


def search(query):
    terms = QueryParser(query)
    if terms.process_query():
        doc_list = {}
        idf = {}
        for t in terms.q:
            with open("./46gb/levels/" + t[0] + ".txt", "r") as f:
                for line in f:
                    temp = line.rstrip().split(":")
                    word = temp[0].split("-")[0]

                    if t == word:
                        doc_freq = int(temp[0].split("-")[1])
                        idf[t] = m.log10(N / doc_freq)
                        posting_list = temp[1].split("|")
                        for i in range(len(posting_list)):
                            temp = posting_list[i]
                            if not temp.split("-")[0]:
                                posting_list[i] = [-int(temp.split("-")[1]), temp.split("-")[2]]
                            else:
                                posting_list[i] = [int(temp.split("-")[0]), temp.split("-")[1]]

                        # [DOC_ID, FIELD_PARTS]

                        for i in range(len(posting_list)):
                            freq = re.split(r"[a-z]", posting_list[i][1])
                            freq.remove("")
                            tf = 0
                            for j in freq:
                                tf += int(j)
                            posting_list[i][1] = m.log10(1 + tf) * idf[t]

                        champions_list = dict(sorted(top_docs.items(), key=operator.itemgetter(1), reverse=True)[:10])

                        # [DOC_ID, FREQ]

                        for i in range(1, len(posting_list)):
                            posting_list[i][0] = posting_list[i][0] + posting_list[i-1][0]

                            if posting_list[i][0] not in doc_list:
                                doc_list[posting_list[i][0]] = {}
                            doc_list[posting_list[i][0]][t] = posting_list[i][1]
                        break
            f.close()

        top_docs = cos_rank(terms.q, doc_list, idf)

    return top_docs
