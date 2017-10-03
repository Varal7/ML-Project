import json
import sys
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from math import radians, cos, sin, asin, sqrt
import random
import threading

NUM_THREAD = 1
for x in sys.argv:
    if x.isdigit():
        NUM_THREAD = int(x)

def distance(coordu, coordv):
    lon1, lat1, lon2, lat2 = map(radians, [coordu[1], coordu[0], coordv[1], coordv[0]])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    mile = 3959 * c
    return mile

def prob(coordu, coordv):
    return 0.0019 * np.power(distance(coordu, coordv) + 0.196, -1.05)

def calc_lam(thread_num, thread_id, coords, coord_list, output):
    for u in range(len(coord_list)):
        if u % thread_num != thread_id:
            continue
        coordu = coord_list[u]
        res = 0
        for coordv in coords:
            if coordv != None:
                res += np.log(1 - prob(coordu, coordv))
        output[coordu] = res
    print(output)

def calc_update(thread_num, thread_id, train_y, coords, graph, lam, output):
    N = len(train_y)
    for u in range(N):
        if u % thread_num != thread_id:
            continue
        if train_y[u] != '?':
            continue

        # Skip examples that are now connected to the graph
        if u not in graph:
            continue
        #tmp = {}
        coord_proba = []
        used_coord_list = []

        for candi in graph[u]:
            # Coords of test examples are unknown
            if coords[candi] == None:
                continue
            coordu = coords[candi]

            if coordu in used_coord_list:
                continue
            else:
                used_coord_list.append(coordu)

            proba = lam[coordu]
            # if coordu in lam:
            #     proba = lam[coordu]
            # else:
            #     proba = 0
            # lb = coord2loc[coordu]
            # if lb not in tmp:
            #     tmp[lb] = 0
            # tmp[lb] += 1

            # Traverse through all neighbors of u
            for v in graph[u]:
                # Skip if the neighbour is a test example
                if coords[v] == None:
                    continue
                coordv = coords[v]
                proba += np.log(prob(coordu, coordv)) - np.log(1 - prob(coordu, coordv))

            coord_proba.append((coordu, proba))
            # if proba > max_proba or max_proba == 1:
            #     max_proba = proba
            #     max_coord = coordu

        coord_proba = sorted(coord_proba, key=lambda x: x[1])

        coord_proba = coord_proba[::-1]

        if len(coord_proba) > 0:
            output[u] = coord_proba

def findme(train_y, test_y, graph, coords, coord2loc, labels):
    N = len(train_y)

    coord_set = set()
    for coord in coords:
        if coord != None:
            coord_set.add(coord)
    coord_list = list(coord_set)
    test_coord_all = {}

    for itera in range(5):
        print 'Iter', itera
        sys.stdout.flush()

        lam = {}

        lam_thread = [{}] * NUM_THREAD
        ts = []
        for thread_id in range(NUM_THREAD):
            t = threading.Thread(target=calc_lam, args=(NUM_THREAD, thread_id, coords, coord_list, lam_thread[thread_id]))
            ts.append(t)
            t.start()
        for t in ts:
            t.join()
        for thread_id in range(NUM_THREAD):
            for (k,v) in lam_thread[thread_id].items():
                lam[k] = v

        # print 'precompute finished'

        update_thread = [{}] * NUM_THREAD
        ts = []
        for thread_id in range(NUM_THREAD):
            t = threading.Thread(target=calc_update, args=(NUM_THREAD, thread_id, train_y, coords, graph, lam, update_thread[thread_id]))
            ts.append(t)
            t.start()
        for t in ts:
            t.join()
        
        for thread_id in range(NUM_THREAD):
            for (k, v) in update_thread[thread_id].items():
                coords[k] = v[0][0] + tuple()
                test_coord_all[k] = [t+tuple() for t in v]
        y = []
        idx = 0
        true_y = []
        pred_y = []
        for u in range(N):
            if train_y[u] == '?':
                if coords[u] != None:
                    y.append(coord2loc[coords[u]])
                    true_y.append(test_y[idx])
                    pred_y.append(coord2loc[coords[u]])
                else:
                    y.append('CA') # majority baseline
                idx += 1
        print accuracy_score(y_true=test_y, y_pred=y)
        print(len(y))
        print accuracy_score(y_true=true_y, y_pred=pred_y)
        print(len(pred_y))
        print confusion_matrix(y_true=true_y, y_pred=pred_y)
        sys.stdout.flush()

    f = file('pred_find.txt', 'w')
    for i, l in enumerate(labels):
        if i != len(labels)-1:
            f.write(l + " ")
        else:
            f.write(l + "\n")
    unknown = 0

    majority = [7118, 4787, 27255, 2266, 9677, 7459, 4285, 5795, 18533, 8588,
            15479, 6983, 7474, 3133, 895, 6731, 6200, 3082, 12281, 2296, 2938,
            608, 331, 643, 1960, 2875, 1856, 1627, 2784, 234, 3479, 1040, 1967,
            3879, 1408, 2369, 1149, 1617, 297, 706, 2131, 165, 653, 1180, 593,
            246, 676, 144, 87, 328, 160]


    for u in range(N):
        if coords[u] == None:
            unknown += 1
            for v in majority:
                f.write('{} '.format(v))
            f.write('\n')
        else:
            if train_y[u] != '?':
                label = coord2loc[coords[u]]
                for x in labels:
                    if x == label:
                        f.write('%s 1 ' % x)
                    else:
                        f.write('%s 0 ' % x)
                f.write('\n')
            else:
                # if u not in test_coord_all:
                #     print(u)
                #     print(u in coords)
                for i, v in enumerate(test_coord_all[u]):
                    test_coord_all[u][i] = (coord2loc[v[0]], v[1])
                prob_dict = dict(test_coord_all[u])

                for x in labels:
                    if x in prob_dict:
                        f.write('{} '.format(prob_dict[x]))
                    else:
                        f.write('-1e+100 ')
                f.write('\n')
    f.close()
    print unknown
    # f = file('pred_find.txt', 'w')
    # unknown = 0
    # for u in range(N):
    #     if coords[u] == None:
    #         unknown += 1
    #         label = '' #random.choice(labels)
    #     else:
    #         label = coord2loc[coords[u]]
    #     for x in labels:
    #         if x == label:
    #             f.write('%s 1 ' % x)
    #         else:
    #             f.write('%s 0 ' % x)
    #     f.write('\n')
    # f.close()
    # print unknown

    return coords



if __name__ == '__main__':
    f = file(sys.argv[1])
    labels = []
    all_y = []
    train_y = []
    test_y = []
    graph = {}

    lbl_cnts = {}

    for line in f:
        if line[0] != '#':
            a = line.split('\t', 2)
            label = a[0][1:]
            if label not in labels:
                labels.append(label)
                lbl_cnts[label] = 0
            type_ = a[0][0]
            all_y.append(label) # sequenced by according to the data
            if type_ == '+' or type_ == '*':
                train_y.append(label)
                lbl_cnts[label] += 1
            if type_ == '?':
                train_y.append('?')
                test_y.append(label)
        else:
            a = line.split(' ')
            u = int(a[1]) ## node specified by the data
            v = int(a[2]) ## node specified by the data
            if u not in graph:
                graph[u] = set()
            graph[u].add(v)
            if v not in graph:
                graph[v] = set()
            graph[v].add(u)

    f.close()

    labels = ['NC', 'LA', 'CA', 'MS', 'GA', 'IL', 'TN', 'MD', 'NY', 'OH', 'TX',
            'MI', 'PA', 'SC', 'UT', 'NJ', 'VA', 'AL', 'FL', 'WI', 'AZ', 'RI',
            'NH', 'NE', 'KY', 'WA', 'CO', 'AR', 'MO', 'SD', 'IN', 'KS', 'NV',
            'MA', 'OR', 'CT', 'IA', 'OK', 'ID', 'WV', 'MN', 'VT', 'HI', 'DC',
            'NM', 'AK', 'DE', 'ND', 'WY', 'ME', 'MT']

    # tmp = []
    # for lbl in labels:
    #     tmp.append(lbl_cnts[lbl])
    # print(tmp)
    # exit(0)

    f = file(sys.argv[2])
    gt_coords = []
    coords = []
    # ------------------------------------------------------------------------
    # coords and train_y, test_y are shared
    # ------------------------------------------------------------------------
    coord2loc = {}
    cnt = 0
    for line in f:
        a = line.split(' ')
        la = float(a[0])
        lo = float(a[1])
        gt_coords.append((la,lo)) # sequenced according to the data
        if train_y[cnt] == '?':
            coords.append(None)
        else:
            coords.append((la,lo))
            coord2loc[(la,lo)] = train_y[cnt]
        cnt += 1

    # labels = ['NC', 'LA', 'CA', 'MS', 'GA', 'IL', 'TN', 'MD', 'NY', 'OH', 'TX',
    #         'MI', 'PA', 'SC', 'UT', 'NJ', 'VA', 'AL', 'FL', 'WI', 'AZ', 'RI',
    #         'NH', 'NE', 'KY', 'WA', 'CO', 'AR', 'MO', 'SD', 'IN', 'KS', 'NV',
    #         'MA', 'OR', 'CT', 'IA', 'OK', 'ID', 'WV', 'MN', 'VT', 'HI', 'DC',
    #         'NM', 'AK', 'DE', 'ND', 'WY', 'ME', 'MT']
    coords = findme(train_y, test_y, graph, coords, coord2loc, labels)
