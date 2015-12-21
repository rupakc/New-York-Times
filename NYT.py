# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:26:54 2015
Wrapper around the New York Times Article Search API
@author: Rupak Chakraborty
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
Defines a keyword class for containing all the given keywords of a given article
'''
class Keyword:
    
    rank = ""
    is_major = ""
    value = ""
    name = ""
'''
Defines the headline of a given article
'''
class Headline:
    
    main = ""
    kicker = ""
    print_headline = ""
    content_kicker = ""
'''
Defines the class for bylines i.e. list of reporters for the given article
'''
class Byline:
    
    original = ""
    personList = []
    
'''
Defines a person i.e. Reporter information of the article
'''
class Person:
    
    organization = ""
    role = ""
    rank = ""
    firstname = ""
    lastname = ""
'''
Defines the multimedia associated with an article mostly images in different formats
'''
class Multimedia:
    
    width = ""
    height = ""
    url = ""
    subtype = ""
    
'''
Main class to fetch the article information from New York Times API
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
    bylineList = []
    multimediaList = []
    PAGEPARAM = "&page="
    PAGE = 1;
    ISPAGINATION = False;
    BEGINDATEPARAM = "&begin_date="
    ENDDATEPARAM = "&end_date="
    BEGINDATE="-1"
    ENDDATE="-1"
    
    def __init__(self,apikey): 
        self.APIKEY = apikey 

    def setQuery(self,query):
        self.QUERY = query
        self.QUERY = query.replace(" ","%20") 
        
    def setBeginDate(self,begin_date):
        self.BEGINDATE = begin_date.strip() 
        
    def setEndDate(self,end_date):
        self.ENDDATE = end_date.strip()
    def setPagination(self,boolPaginate):
        self.ISPAGINATION = boolPaginate;
        
    def linkGen(self):
        
        link = self.APIENDPOINT + self.QUERYPARAM + self.QUERY + self.APIKEYPARAM + self.APIKEY
        
        if self.BEGINDATE != "-1":
            link = link + self.BEGINDATEPARAM + self.BEGINDATE
        if self.ENDDATE != "-1":
            link = link + self.ENDDATEPARAM + self.ENDDATE
        if self.ISPAGINATION:
            link = link + self.PAGEPARAM + str(self.PAGE)
            
        return link  
    
    def populateMultiMedia(self,multimediaArray): 
        
        mediaList = []
    
        for multimedia in multimediaArray: 
            
            media = Multimedia() 
            
            if "width" in multimedia: 
                media.width = multimedia["width"]
            if "height" in multimedia:
                media.height = multimedia["height"]
            if "url" in multimedia:
                media.url = multimedia["url"]
            if "subtype" in multimedia:
                media.subtype = multimedia["subtype"]
                
            mediaList.append(media)
        
        return mediaList
        
    def populateByLine(self,byline): 
        
        bye = Byline()  
        
        if "original" in byline:
            bye.original = byline["original"] 
        
        if "person" in byline:
            for per in byline["person"]: 
                
                subject = Person() 
                
                if "organization" in per:
                    subject.organization = per["organization"]
                if "role" in per:
                    subject.role = per["role"]
                if "firstname" in per:
                    subject.firstname = per["firstname"]
                if "rank" in per:
                    subject.rank = per["rank"]
                if "lastname" in per:
                    subject.lastname = per["lastname"]
                bye.personList.append(subject)
            
        return bye
        
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
            
            if len(documentList) == 0:
                return
                
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
                
                if "byline" in document and document["byline"] != None:
                    self.bylineList.append(self.populateByLine(document["byline"])) 
                    
                if "keywords" in document and document["keywords"] != None:
                    self.keywordList.append(self.populateKeywordList(document["keywords"]))
                
                if "headline" in document and document["headline"] != None:
                    self.headlineList.append(self.populateHeadline(document["headline"]))
                
                if "multimedia" in document and document["multimedia"] != None:
                    self.multimediaList.append(self.populateMultiMedia(document["multimedia"]))
                
                self.articleList.append(article)   
                
    def articleProcessingPipeline(self): 
        
        if self.ISPAGINATION:
            while self.PAGE <= 100:
                link = self.linkGen()
                print self.PAGE
                jsonResponse = self.getJSONResponse(link)
                self.PAGE = self.PAGE + 1
                if (jsonResponse != "failure"):
                    if "docs" in jsonResponse["response"]:
                        documentList = jsonResponse["response"]["docs"]
                        if len(documentList) > 0:
                            self.populateJSONFields(jsonResponse)
                        else:
                            break
        else:
            link = self.linkGen()
            jsonResponse = self.getJSONResponse(link)
            if (jsonResponse != "failure"):
                self.populateJSONFields(jsonResponse)
                
def main():
    test = NYArticle("5caa290b6f044865a614b3a22d653997%3A0%3A72414519")
    test.setQuery("india")
    test.setBeginDate("20110101")
    test.setEndDate("20110601")
    test.setPagination(True)
    print test.linkGen()
   
    test.articleProcessingPipeline()
    for art in test.articleList:
        print art.snippet
   
    
    
if __name__ == "__main__":
    main()