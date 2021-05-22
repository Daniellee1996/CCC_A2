#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
class tweet_processor:
    def __init__(self):
        pass

    def check_type(self, json_obj):
        if type(json_obj) != dict:
            return json.loads(json_obj)
        else:
            return json_obj

    def get_full_text(self, json_obj):
        data = self.check_type(json_obj)
        if data.get('full_text'):
            return data['full_text']
        # if data['text']:
        #     if data['text'].startswith('RT @'):
        #         if 'extended_tweet' in data['retweeted_status']:
        #             return(data['retweeted_status']['extended_tweet']['full_text'])
        #         else:
        #             return(data['retweeted_status']['text'])
        #     else:
        #         if not 'extended_tweet' in data:
        #             return(data['text'])
        #         else:    
        #             return(data['extended_tweet']['full_text'])
        if data['extended_tweet']['full_text']:
            return data['extended_tweet']['full_text']
        if data['text']:
            return data['text']
        return ''
                    
    def get_hastags(self, json_obj):
        data = json.loads(json_obj)
        return data['doc']['entities']['hashtags']

    def get_lang_code(self, json_obj):
        data = self.check_type(json_obj)
        return data['lang']

    def get_location(self, json_obj):
        data = json.loads(json_obj)
        if data['user']['location']:
            return data['user']['location']
        return None
    
    def drop_duplicates(self, file):
        ids = set()

        with open(file,'r') as lines:     
            with open('output.json', 'w') as f:  
                for line in lines:
                    data = json.loads(line)
                    if data['id_str'] not in ids:                  
                        ids.add(data['id_str'])
                        json.dump(data, f)
                        f.write('\n')
        print('duplicates removed')

    def get_city(self, loc):
        """
        check if this is an AU city
        """
        abbrv_states = ['vic', 'qls', 'nsw', 'tas', 'act', 'nt', 'sa', 'wa', 'au']
        states = ['victoria', 'queensland', 'new south wales', 'tasmania', 'western australia', 
        'northern territory', 'australian capital territory', 'south australia', 'australia']
        
        try:
            if loc != None and loc != '':
                lst = loc.split(', ')
                if (len(lst)) >= 2:
                    if lst[1].lower() in abbrv_states or lst[1].lower() in states:
                        return lst[0].lower()
        except ValueError:
            print('error found')
        return None



