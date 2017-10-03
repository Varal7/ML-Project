#-*- coding: utf-8 -*-
import re
import sys
import json
import math
import numpy as np
import operator
from pymongo import *
from evaluate import evaluate

def split_sentence(s):
    regex = []
    # Match a whole word:
    regex += [ur'[\w\u0080-\u07ff]+']
    # Match a single CJK character:
    regex += [ur'[\u4e00-\ufaff]']
    # Match one of anything else, except for spaces:
    regex += [ur'[^\s]']
    regex = "|".join(regex)
    r = re.compile(regex)
    return set(r.findall(s))

stats = {"N": 0, "label_cnt": {}, "word_cnt": {}, "word_label_cnt": {}}

client = MongoClient('localhost', 30000)
tw = client.twitter

cnt = 0

for obj in tw.tweet.find({'location.country': 'USA'}):
    cnt += 1
    if cnt % 5000000 == 0:
        print cnt
        evaluate(stats)
    if obj['user_id'] % 2 == 1:
        continue
    loc = obj['location']
    if 'us_state' not in loc or 'abbrev' not in loc['us_state'] or 'text' not in obj:
        continue
    label = loc['us_state']['abbrev']
    stats['N'] += 1
    if label not in stats['label_cnt']:
        stats['label_cnt'][label] = 0
    stats['label_cnt'][label] += 1
    text = obj['text']
    if 'entities' in obj:
        for x in obj['entities']['user_mentions']:
            text = text.replace('@' + x['screen_name'], '')
        for x in obj['entities']['hashtags']:
            text = text.replace('#' + x['text'], '')
        for x in obj['entities']['urls']:
            text = text.replace(x['url'], '')
    words = split_sentence(text)
    for word in words:
        if len(word) > 20:
            continue
        if word not in stats['word_cnt']:
            stats['word_cnt'][word] = 0
            stats['word_label_cnt'][word] = {}
        stats['word_cnt'][word] += 1
        if label not in stats['word_label_cnt'][word]:
            stats['word_label_cnt'][word][label] = 0
        stats['word_label_cnt'][word][label] += 1

output_f = file('stats.out','w')
json.dump(stats, output_f)
output_f.close()


# value = {}
# for word in stats['word_label_cnt']:
#     if stats['word_cnt'][word] < 100:
#         continue
#     for label in stats['word_label_cnt'][word]:
#         A = stats['word_label_cnt'][word][label]
#         B = stats['word_cnt'][word] - A
#         C = stats['label_cnt'][label] - A
#         D = stats['N'] - A - B - C
#         chi = float(np.square(A*D-C*B)) / ((A+C)*(B+D)*(A+B)*(C+D))
#         if label not in value:
#             value[label] = {}
#         value[label][word] = chi

# for label in ['CHN','TWN','HKG','JPN','KOR','USA','GBR','AUS']:
#     sorted_x = sorted(value[label].items(), key=operator.itemgetter(1), reverse=True)
#     print label,
#     for tup in sorted_x[:10]:
#         print tup[0].encode('utf-8'),
#     print


