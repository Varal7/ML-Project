import numpy as np
import json

f = file('stats.out')
stats = json.load(f)

value = {}

for word in stats['word_label_cnt']:
    if stats['word_cnt'][word] < 500:
        continue
    value[word] = {}
    for label in stats['word_label_cnt'][word]:
        A = stats['word_label_cnt'][word][label]
        B = stats['word_cnt'][word] - A
        C = stats['label_cnt'][label] - A
        D = stats['N'] - A - B - C
        N = stats['N']
        #chi = float(np.square(A*D-C*B)) / ((A+C)*(B+D)*(A+B)*(C+D))
        chi = np.log(float(A*N) / ((A+C)*(A+B)))
        #chi = float(stats['word_label_cnt'][word][label]) / stats['word_cnt'][word]
        value[word][label] = chi


out = file('value.out', 'w')
json.dump(value, out)
