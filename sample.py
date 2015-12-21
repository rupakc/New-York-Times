# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 17:31:10 2015

@author: rupachak
"""

import NYT

article = NYT.NYArticle("5caa290b6f044865a614b3a22d653997%3A0%3A72414519")
article.setQuery("Obama")

article.articleProcessingPipeline()
for art in article.articleList:
    print art.snippet
   
