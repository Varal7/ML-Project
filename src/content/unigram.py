import sys
import math
from operator import itemgetter
import random
import json
import re
import os
import numpy as np
from multiprocessing import Pool

f = file('../uids.txt')
uid2type = {}
uid2tag = {}
tags = []

for line in f:
    a = line.strip().split(' ')
    typ = a[0]
    uid = int(a[1])
    tag = a[2]
    uid2type[uid] = typ
    uid2tag[uid] = tag
    if tag not in tags:
        tags.append(tag)

f.close()


if os.path.isfile('word_tag_cnt.json'):
    f = file('word_tag_cnt.json')
    word_tag_cnt = json.load(f)
    f.close()
else:
    print 'Start Training ...'

    word_tag_cnt = {}
    f = file('../tweet_content.txt')

    cnt = 1
    for line in f:
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
            sys.stdout.flush()
        a = line.strip().split(' ', 1)
        uid = int(a[0])
        if uid2type[uid] != '+':
            continue
        tag = uid2tag[uid]
        if len(a) == 1:
            print 'NO WORD:', uid
            continue
        words = a[1].split(' ')
        for word in words:
            if word not in word_tag_cnt:
                word_tag_cnt[word] = {}
            if tag not in word_tag_cnt[word]:
                word_tag_cnt[word][tag] = 0
            word_tag_cnt[word][tag] += 1

    f.close()

    f = file('word_tag_cnt.json', 'w')
    json.dump(word_tag_cnt, f)
    f.close()

tag_cnt = {}
word_cnt = {}
word_total = 0

for word in word_tag_cnt:
    for tag, cnt in word_tag_cnt[word].items():
        if word not in word_cnt:
            word_cnt[word] = 0
        if tag not in tag_cnt:
            tag_cnt[tag] = 0
        word_cnt[word] += cnt
        tag_cnt[tag] += cnt
        word_total += cnt

print 'Word Total:', word_total
sys.stdout.flush()

word_number = len(word_cnt)
tag_number = len(tag_cnt)

IG = {}
IV = {}
IGR = {}

H = 0
for tag, cnt in tag_cnt.items():
    p = float(cnt) / float(word_total)
    H += - p * math.log(p, 2)

eps = 1e-9

for word in word_cnt:
    if word_cnt[word] < 100:
        continue
    s1 = 0
    for tag in tag_cnt:
        if tag not in word_tag_cnt[word]:
            word_tag_cnt[word][tag] = 0
        p = (word_tag_cnt[word][tag] + eps) / (word_cnt[word] + eps * tag_number)
        s1 += p * math.log(p, 2)
    s2 = 0
    for tag in tag_cnt:
        p = float(tag_cnt[tag] - word_tag_cnt[word][tag]) / float(word_total - word_cnt[word])
        s2 += p * math.log(p, 2)
    p1 = float(word_cnt[word]) / float(word_total)
    p2 = 1 - p1
    IG[word] = H + p1 * s1 + p2 * s2
    IV[word] = - p1 * math.log(p1, 2) - p2 * math.log(p2, 2)
    IGR[word] = IG[word] / IV[word]

print 'Word number:', len(IGR)

print 'Start Testing ...'
sys.stdout.flush()

IGR_list = IGR.items()
IGR_list = sorted(IGR_list, key=itemgetter(1), reverse=True)

print("voc size")
print(len(IGR_list))

for word, igr in IGR_list[:20]:
    print '\t', word.encode('utf-8'), igr, word_cnt[word]

def predict(ratio, output=False):

    IGR_threshold = IGR_list[int((len(IGR_list) - 1) * ratio)][1]

    f = file('../tweet_content.txt')
    tag_number = len(tags)

    if output:
        output_f = file('pred_content.txt', 'w')
        output_f.write(' '.join(tags) + '\n')

    valid_hit = 0
    valid_miss = 0
    test_hit = 0
    test_miss = 0

    for line in f:
        a = line.strip().split(' ')
        uid = int(a[0])
        if not output and uid2type[uid] == '+':
            continue
        words = a[1:]
        prob = [0] * tag_number
        for word in words:
            if word not in IGR or IGR[word] < IGR_threshold:
                continue
            for tag_ix in range(tag_number):
                tag = tags[tag_ix]
                prob[tag_ix] += float(word_tag_cnt[word][tag]) / float(word_cnt[word])
        z = sum(prob)
        if z != 0:
            for ix in range(tag_number):
                prob[ix] /= z
        tagix = 0
        for ix in range(tag_number):
            if prob[ix] > prob[tagix]:
                tagix = ix
        if uid2type[uid] == '*':
            if uid2tag[uid] == tags[tagix]:
                valid_hit += 1
            else:
                valid_miss += 1
        if uid2type[uid] == '?':
            if uid2tag[uid] == tags[tagix]:
                test_hit += 1
            else:
                test_miss += 1
        if output:
            for ix in range(tag_number):
                output_f.write('%.5f ' % prob[ix])
            output_f.write('\n')

    valid_acc = float(valid_hit) / float(valid_hit + valid_miss)
    test_acc = float(test_hit) / float(test_hit + test_miss)

    print 'ratio:', ratio, 'valid_acc:', valid_acc, 'test_acc:', test_acc
    sys.stdout.flush()

    f.close()
    if output:
        output_f.close()

    return valid_acc


pool = Pool(processes=8) 

ratios = list(np.arange(0.02, 0.3, 0.01))
results = pool.map(predict, ratios)

best_acc = 0
best_ratio = 0

for i in range(len(ratios)):
    ratio = ratios[i]
    valid_acc = results[i]
    if valid_acc > best_acc:
        best_acc = valid_acc
        best_ratio = ratio

print 'Final Test'
predict(best_ratio, False)

