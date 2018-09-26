# Wikipedia search engine
A wikipedia search engine which comprises of two parts :
- Indexing
- Searching

**Note: This has been run successfully on a wiki-dump of size 46GB. This repository currently contains the index files for a smaller 100MB dump and the search queries will be done on the smaller dump. The bigger index files were not uploaded due to their sheer size(~14GB).**

## Indexing
In this part we index the wiki-xml dump and store it in a text file. The index contains words along with their list of document IDs corresponding to the documents in which they appear along with their frequency in that document. The following steps are taken before indexing the corpus :
- Tokenizing the text
- Removing stopwords
- Stemming the words
- Indexing the stemmed words
The frequency is modelled in terms of fields (title, body, categories, links, references, etc.). The index is sorted incase of big files (an entire 46GB dump) using the **Single-Pass In-Memory Indexing algorithm**. \
The index is also broken down into 36 smaller indexes (0.txt for words starting with 0, similarly p.txt and so on). This helps improve the query time.\
To index an xml dump run the following:
> python3 index.py <xml-dump-filename> <index-filename>

## Searching
This section involves searching through the index to obtain relevant documents and display them along with the time taken to find them. Document ranking is also done to check relevance by using the **TF-IDF scores** for each document.\
The **cosine similarity** for each document with the query is then calculated and the top 10 results and their document IDs are chosen.\
To further reduce the number of computations, **champions lists** have also been implemented where only the top 20 documents with the highest TF-IDF scores are taken into account when performing cosine similarity.\
Once the document IDs are obtained, using a mapping file, we obtain the titles mapped to each respective ID and display them along with the time taken to process the query. \
**Note: All index files should be in the index folder.**
To run the search engine run the following:
> python3 search.py
