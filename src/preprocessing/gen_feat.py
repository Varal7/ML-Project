# coding: utf-8
from pymongo import *
import json
import re
import numpy as np
import time
import sys

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
    return r.findall(s)

client = MongoClient('localhost', 30000)
tw = client.twitter

f = file('../content_usa/value.out')
value = json.load(f)

labels = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

task_id = int(sys.argv[1])
out_file = file('features_%d.txt' % task_id, 'w')

cnt = 0
cursor = tw.user.find(no_cursor_timeout=True)
for uobj in cursor:
    if 'label_us' not in uobj or uobj['id'] % 10 != task_id:
        continue
    uid = uobj['id']
    ulabel = uobj['label_us']
    
    out_line = str(uid) + '\t' + ulabel
    
    timezone = ''
    if uobj['time_zone'] != None:
        timezone = uobj['time_zone'].replace(' ', '')
    out_line = out_line + '\ttz_%s:1' % timezone

    ulang = ''
    if uobj['lang'] != None:
        ulang = uobj['lang']
    out_line = out_line + '\tul_%s:1' % ulang

    v = {}
    for label in labels:
        v[label] = []
    ok = False
    start = time.time()
    tweet_cnt = 0
    for obj in tw.tweet.find({'user_id':uid}).batch_size(2048):
        if 'us_state' not in obj['location']:
            continue
        ok = True
        if obj['location']['us_state']['abbrev'] != ulabel:
            ok = False
            break
        tweet_cnt += 1
        text = obj['text']
        for x in obj['entities']['user_mentions']:
            text = text.replace('@' + x['screen_name'], '')
        for x in obj['entities']['hashtags']:
            text = text.replace('#' + x['text'], '')
        for x in obj['entities']['urls']:
            text = text.replace(x['url'], '')
        words = split_sentence(text)
        for word in words:
            if word not in value:
                continue
            for label in labels:
                if label not in value[word]:
                    continue
                v[label].append(value[word][label])
    end = time.time()
    if ok == False:
        continue

    out_line = out_line + '\ttw_cnt:%d' % tweet_cnt

    for label in labels:
        if len(v[label]) == 0:
            continue
        out_line = out_line + '\tc_%s_max:%.3f' % (label, max(v[label]))
        out_line = out_line + '\tc_%s_avg:%.3f' % (label, np.mean(v[label]))
    out_line += '\n'

    cnt += 1
    out_file.write(out_line)

print task_id, 'done!', cnt
cursor.close()
out_file.close()

#for (u, v) in edges:
    #if u not in uid2line or v not in uid2line:
    #   continue
    #fgm_f.write('#edge %d %d mention\n' % (uid2line[u], uid2line[v]))
