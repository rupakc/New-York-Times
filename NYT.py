# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:26:54 2015
Wrapper around the New York Times Article Search API
@author: Rupak Chakraborty
TODO - Add multimedia support byline support and pagination and time interval of query
"""

import urllib2
import json
import socket

'''
Defines an article class which contains the necessary fields of a given article
'''
class Article:
    
    web_url = ""
    Id = ""
    source = ""
    snippet = ""
    abstract = ""
    print_page = ""
    document_type = ""
    lead_paragraph = ""
    pub_date = ""
    section_name = ""
    subsection_name = ""
    slideshow_credits = ""
    type_of_material = ""
    word_count = ""
    news_desk = ""

'''
'''

class Keyword:
    
    rank = ""
    is_major = ""
    value = ""
    name = ""
'''
'''
  
class Headline:
    
    main = ""
    kicker = ""
    print_headline = ""
    content_kicker = ""
'''
'''

class NYArticle: 
    
    APIKEY = "5caa290b6f044865a614b3a22d653997%3A0%3A72414519"
    APIKEYPARAM = "&api-key="
    QUERY = "obama"
    QUERYPARAM = "q="
    APIENDPOINT = "http://api.nytimes.com/svc/search/v2/articlesearch.json?"
    articleList = []
    keywordList = []
    headlineList = [] 
    
    def __init__(self,apikey): 
        self.APIKEY = apikey 

    def setQuery(self,query):
        self.QUERY = query 
        
    def linkGen(self):
        link = self.APIENDPOINT + self.QUERYPARAM + self.QUERY + self.APIKEYPARAM + self.APIKEY
        return link 
        
    def getJSONResponse(self,link):
        jsonResponse = ""
        response = urllib2.urlopen(link,timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
        
        if response.getcode() != 200:
            jsonResponse = "failure"
            return jsonResponse
        
        data = response.read()
        jsonResponse = json.loads(data) 
        
        return jsonResponse
        
    def populateHeadline(self,headline):
        
        head = Headline()
        if "main" in headline:
            head.main = headline["main"]
        if "kicker" in headline:
            head.kicker = headline["kicker"]
        if "content_kicker" in headline:
            head.content_kicker = headline["content_kicker"]
        if "print_headline" in headline:
            head.print_headline = headline["print_headline"] 
            
        return head;
            
    def populateKeywordList(self,keywords):
        
        keywordArray = []
        for keyword in keywords:
            
            key = Keyword()
            
            if "rank" in keyword:
                key.rank = keyword["rank"]
            if "is_major" in keyword:
                key.is_major = keyword["is_major"]
            if "value" in keyword:
                key.value = keyword["value"]
            if "name" in keyword["name"]:
                key.name = keyword["name"] 
                
            keywordArray.append(key)
            
        return keywordArray
        
    def populateJSONFields(self,jsonData):
        
        if "docs" in jsonData["response"]:
            
            documentList = jsonData["response"]["docs"] 
            
            for document in documentList: 
                
                article = Article()
                article.web_url = document["web_url"]
                article.source = document["source"]
                article.snippet = document["snippet"]
                article.abstract = document["abstract"]
                article.document_type = document["document_type"]
                article.print_page = document["print_page"]
                article.lead_paragraph = document["lead_paragraph"]
                article.Id = document["_id"]
                article.section_name = document["section_name"]
                article.subsection_name = document["subsection_name"]
                article.news_desk = document["news_desk"]
                article.type_of_material = document["type_of_material"]
                article.word_count = document["word_count"]
                article.slideshow_credits = document["slideshow_credits"]
                
                if "keywords" in document:
                    self.keywordList.append(self.populateKeywordList(document["keywords"]))
                
                if "headline" in document:
                    self.headlineList.append(self.populateHeadline(document["headline"]))
                
                self.articleList.append(article)   
                
    def articleProcessingPipeline(self): 
        
        link = self.linkGen()
        jsonResponse = self.getJSONResponse(link)
        
        if (jsonResponse != "failure"):
            self.populateJSONFields(jsonResponse)
                
def main():
    test = NYArticle("5caa290b6f044865a614b3a22d653997%3A0%3A72414519")
    test.setQuery("obama")
    test.articleProcessingPipeline()
    for art in test.articleList:
        print art.snippet
    
if __name__ == "__main__":
    main()