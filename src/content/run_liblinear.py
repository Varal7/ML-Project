from sklearn.metrics import accuracy_score
from liblinearutil import *
import time
import numpy as np
import os
import sys
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-method', choices=['LR', 'SVM'], default='LR')
parser.add_argument('-thread', type=int, default=1)

args = parser.parse_args()

feature2id = {}
features = []
labels = []
label2id = {}
cnt = 0
for line in tqdm(f):
	if line[0] == '#':
		break
	a = line.strip().split('#')[0].split('\t')
	label = a[0][1:]
	if label not in labels:
		label2id[label] = len(labels)
		labels.append(label)
	for x in a[1:]:
		if ':' not in x:
			continue
		token = x.split(':')[0]
		if token not in feature2id:
			feature2id[token] = cnt
			features.append(token)
			cnt += 1
f.close()

print ''
print 'num_label', len(labels)


train_x = []
train_y = []
test_x = []
test_y = []
all_x = []
all_y = []

f = file(args.input)
line2label = ['']
xxx = 0
for line in tqdm(f):
	if line[0] == '#':
		break
	a = line.strip().split('#')[0].split('\t')
	type_ = a[0][0]
	if type_ == '*':
		type_ = '+'
	label = a[0][1:]
	if type_ == '+':
		line2label.append(label)
	else:
		line2label.append('?')
	featv = np.zeros(len(feature2id))
	for x in a[1:]:
		if ':' not in x:
			continue
		b = x.split(':')
		fid = feature2id[b[0]]
		val = float(b[1])
		featv[fid] = val
	featv = list(featv)
	label = label2id[label]
	if type_ == '+':
		train_x.append(featv)
		train_y.append(label)
	else:
		test_x.append(featv)
		test_y.append(label)
	all_x.append(featv)
	all_y.append(label)


print ''
print 'start training ...'
start = time.time()
if args.method == "LR":
	prob = problem(train_y, train_x)
	param = parameter('-s 0 -c 1 -n %d -q' % args.thread)
	clf = train(prob, param)
	save_model('liblinear_LR.model', clf)
else:
	prob = problem(train_y, train_x)
	param = parameter('-s 2 -c 1 -n %d -q' % args.thread)
	clf = train(prob, param)
	save_model('liblinear_SVM.model', clf)

end = time.time()
print 'Time:', end - start

C = clf.get_nr_class()
F = clf.get_nr_feature()

print 'start testing ...'
y, p_acc, p_vals = predict(test_y, test_x, clf)
print accuracy_score(test_y, y)

if args.method == 'LR':
	y, p_acc, p_vals = predict(all_y, all_x, clf, '-b 1 -q')
	y_proba = p_vals
else:
	y, p_acc, p_vals = predict(all_y, all_x, clf, '-b 0 -q')
	y_proba = p_vals


classes_ = clf.get_labels()

output = file('pred_%s.txt' % args.method, 'w')
for j in range(len(classes_)):
    output.write('%s ' % (labels[classes_[j]]))
output.write('\n')
for i in tqdm(xrange(len(y_proba))):
	for j in range(len(classes_)):
		output.write('%.3f ' % (y_proba[i][j]))
	if len(labels) != len(classes_):
		for x in labels:
			if x not in classes_:
				output.write('0 ' % x)
	output.write('\n')
output.close()


'''print classification_report(test_y, y)

print clf.classes_

[precision, recall, fscore, support] = precision_recall_fscore_support(test_y, y)
print precision, np.mean(precision)
print recall, np.mean(recall)
print fscore, np.mean(fscore)

'''
