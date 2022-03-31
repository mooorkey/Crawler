import nltk
import requests
import re
import string
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

################################## Extract ##################################
def extract_text_from_html(url:str):
    soup = BeautifulSoup(requests.get(url).text, features = "lxml") #init soup
    texts = soup.find_all(text=True)                                #get all text
    visible_texts = filter(tag_visible, texts)                      #filtered out tags
    text = u" ".join(t.strip().lower() for t in visible_texts)
    return text

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
################################## Extract ##################################




################################## Transform ##################################
# Deleting Stop Words and Tokenize
def delete_stopwords(text:str):
    unwanted_words = set(stopwords.words('english')+word_tokenize(string.punctuation + '.' + '’' + '-' + '‘' + '``' + '.'))
    word_tokens = word_tokenize(text)

    deleted_stopwords_keywords = [word for word in word_tokens if not word.lower() in unwanted_words]
    deleted_stopwords_keywords = []
    
    for word in word_tokens:
        if word not in unwanted_words:
            deleted_stopwords_keywords.append(word)

    return deleted_stopwords_keywords

# Stemming
def stemming_keyword(keywords):
    ps = PorterStemmer()
    stemmed_keywords = [ps.stem(word) for word in keywords]
    return stemmed_keywords


def cleaned_keywords(url):
    texts = extract_text_from_html(url)
    no_stop_words = delete_stopwords(texts)
    cleaned = stemming_keyword(no_stop_words)
    return cleaned
################################## Transform ##################################





################################## Find Occurance ##################################
def find_occur(keywords:list[str], words:list[str]):
    fd = nltk.FreqDist(keywords)
    for word in words:
        print(f"{word} : {fd[word.lower()]}")
    
################################## Find Occurance ##################################



################################## Crawling ##################################
def crawl(url, path, max_depth, visited, data = [], depth = 0):
    if depth < max_depth:
        try:
            print(f"url : {url+path}")
            soup = BeautifulSoup(requests.get(url + path).text, features = "lxml")
            keywords = cleaned_keywords(url+path)
            data += keywords

            for link in soup.find_all("a"):
                href = link.get('href')
                print(href)
                if href == None:
                    continue

                if href not in visited:
                    visited.add(href)
                    if href.startswith("http"):
                        crawl(href, "", max_depth, visited, data, depth + 1)
                    else:
                        crawl(url, href, max_depth, visited, data, depth + 1)
        except:
            pass
    return data

def url_crawl(url, keywords, max_depth):
    data = crawl(url, "", max_depth, set([url]))   
    find_occur(data, keywords)
################################## Crawling ##################################




def main():
    print("Hello World!")

if __name__ == "__main__":
    urls = ["https://www.imdb.com/",
            "https://www.themoviedb.org/",
            "https://letterboxd.com/",
            "https://www.metacritic.com/",
            "https://www.rottentomatoes.com/",
            "http://www.criticker.com/",
            "https://www.boxofficemojo.com/"]
    url_crawl(urls[0], ["batman"], 3)

    
