import json
import numpy as np
import operator

def evaluate(stats):
    value = {}
    for word in stats['word_label_cnt']:
        if stats['word_cnt'][word] < 5000:
            continue
        for label in stats['word_label_cnt'][word]:
            A = stats['word_label_cnt'][word][label]
            B = stats['word_cnt'][word] - A
            C = stats['label_cnt'][label] - A
            D = stats['N'] - A - B - C
            N = stats['N']
            #chi = float(np.square(A*D-C*B)) / ((A+C)*(B+D)*(A+B)*(C+D))
            chi = np.log(float(A*N) / ((A+C)*(A+B)))
            #chi = float(stats['word_label_cnt'][word][label]) / stats['word_cnt'][word]
            if label not in value:
                value[label] = {}
            value[label][word] = chi
    for label in value:
        sorted_x = sorted(value[label].items(), key=operator.itemgetter(1), reverse=True)
        print label
        for tup in sorted_x[:15]:
            print tup[0].encode('utf-8'), tup[1], stats['word_cnt'][tup[0]]
        print

if __name__ == "__main__":
    f = file('stats.out')
    stats = json.load(f)
    evaluate(stats)
