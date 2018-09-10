from query import search
from time import time as t

if __name__ == "__main__":
    print("Enter query to search and type '.' to end the loop")
    while True:
        start = t()
        string = input("Enter your query : ")
        if string == ".":
            break
        doc_list = search(string)
        if not doc_list:
            print("No results found")
        for k in doc_list:
            print(k, doc_list[k])
        print("Time taken:", t() - start)
