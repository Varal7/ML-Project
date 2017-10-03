import sys
import operator
import json
import argparse
import numpy as np
from math import radians, cos, sin, asin, sqrt
from collections import Counter

parser = argparse.ArgumentParser(description='Error analysis')
parser.add_argument('--pred', type=str, help='Prediction file', default="pred_TCMH.txt")
parser.add_argument('--uids', type=str, help='Gold values', default="uids.txt")
parser.add_argument('--coords', type=str, help='state.json file', default="baseline/state.json")
parser.add_argument('--state', type=str, help='State to test', default="CA")
args = parser.parse_args()


def distance(coordu, coordv):
    lon1, lat1, lon2, lat2 = map(radians, [coordu[1], coordu[0], coordv[1], coordv[0]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# Load coords
with open(args.coords, 'r') as f:
    coords = json.load(f)

label = []
ltype = []

# Load real states
with open(args.uids, 'r') as f:
    for line in f:
	a = line.strip().split(' ')
	label.append(a[2])
	ltype.append(a[0])

label_set = set(label)
M = len(label_set)




# Load predictions
model_name = args.pred.split('.')[0].split('_')[1]
with open(args.pred, 'r') as f:
    line = f.readline()
    tags = line.strip().split(' ')

    cnt = 0
    test = 0

    TP = 0
    FP = 0
    FN = 0

    states_fp = Counter()
    states_fn = Counter()

    dist_error_fp = []
    dist_error_fn = []

    for line in f:
        lb = label[cnt]
        typ = ltype[cnt]
        cnt += 1
        if typ != '?':
            continue
        a = line.split(' ')
	b = {}
	for i in range(M):
		b[tags[i]] = float(a[i])
	c = sorted(b.items(), key=operator.itemgetter(1), reverse=True)
	test += 1
	pred_lb = c[0][0]

        if args.state not in [lb, pred_lb]:
            continue

        if lb == pred_lb:
            TP += 1
        elif lb == args.state:
            FN += 1
        else:
            FP += 1

        if pred_lb == args.state:
            dist_error_fp.append(distance(coords[lb], coords[pred_lb]))
            states_fp[lb] += 1

        if lb == args.state:
            dist_error_fn.append(distance(coords[pred_lb], coords[lb]))
            states_fn[pred_lb] += 1

if TP == 0:
    prec = 0
    rec = 0
else:
    prec = float(TP) / float(TP + FP)
    rec = float(TP) / float(TP + FN)
if prec + rec == 0:
    F1 = 0
else:
    F1 = 2 * prec * rec / (prec + rec)

print 'TP: %d, FP: %d, FN: %d, F1: %f' % (TP, FP, FN, F1)

states_fn = sorted(states_fn.items(), key=lambda x: x[1], reverse=True)
states_fp = sorted(states_fp.items(), key=lambda x: x[1], reverse=True)

def csv(states):
    char = '\t'
    result = char.join([state[0] for state in states])
    result += '\n'
    result += char.join([str(state[1]) for state in states])
    return result

print 'Prediction is %s' % args.state
print csv(states_fp)
print 'Mean error distance: %.2f' % (np.mean(np.array(dist_error_fp)))
print ''

print 'True label is %s' % args.state
print csv(states_fn)
print 'Mean error distance: %.2f' % (np.mean(np.array(dist_error_fn)))
print ''
