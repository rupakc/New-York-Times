# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 00:05:28 2015

@author: rupachak
"""

import pymongo
import NYT
from pymongo import MongoClient
import jsonpickle
import json

class MongoBase: 
    
    client = MongoClient()
    db = ""
    collection = "" 
    
    def __init__(self,dbName,collectionName): 
        
        self.client = MongoClient()
        self.db = self.client[dbName]
        self.collection = self.db[collectionName] 
        
    def jsonSerializeArticle(self,article): 
        
        jsondata = {}
        jsondata["Articles"] = article.articleList
        jsondata["Bylines"] = article.bylineList
        jsondata["Headlines"] = article.headlineList
        jsondata["Multimedia"] = article.multimediaList
        jsondata["Keywords"] = article.keywordList
        jsondata["Query"] = article.QUERY
        jsondata["Channel"] = "NYT"   
        
        pickledjson = jsonpickle.encode(jsondata)
        jsondict = json.loads(pickledjson)
        
        return jsondict

    def insertInDBPipeline(self,article):
        
        jsondata = self.jsonSerializeArticle(article)
        print jsondata
        self.collection.insert(jsondata)

def main():
    article = NYT.NYArticle("5caa290b6f044865a614b3a22d653997%3A0%3A72414519")
    article.setQuery("obama")
    article.articleProcessingPipeline()
    mongo = MongoBase("Central","Test")
    mongo.insertInDBPipeline(article)

if __name__ == "__main__":
    main()
