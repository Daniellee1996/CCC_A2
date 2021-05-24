#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from textblob import TextBlob
import textblob.exceptions
from tweet_processor import tweet_processor


class SentiScoreCalculator:

    def __init__(self, _json = None):
        self.processor = tweet_processor()
        if _json != None:
            self.lang_code = self.processor.get_lang_code(_json)
            self.text = self.processor.get_full_text(_json)
        if self.lang_code != 'en':
            self.text = self.to_english(self.text)

    
    def to_english(self, text = None):
        if text == None:
            text = self.text
        try:
            blob = TextBlob(text)
            return str(blob.translate(to = 'en'))
        except:
            return text
        
    
    def classify(self, text = None):
        if text == None:
            text = self.text
        try:
            blob = TextBlob(text)
            pol = blob.sentiment.polarity
            if pol > 0:
                return 'positive'
            elif pol == 0:
                return 'neutral'
            else:
                return 'negative'
        except:
            return 'neutral'

    def get_polarity(self, text = None):
        if text == None:
            text = self.text
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except:
            return 0.0

    def get_subjectivity(self, text = None):
        if text == None:
            text = self.text
        try:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
        except:
            return 0.0
    
if __name__ == "__main__":
    #print(classify('i am happy'))
    #print(classify('i am sad'))
    #p = tweet_processor()
    #c = SentiScoreCalculator()
    with open('stream_sample.txt','r') as lines:       
        for line in lines:
            c = SentiScoreCalculator(line)
            print(c.classify())

                

                
