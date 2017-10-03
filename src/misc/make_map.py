#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse

parser = argparse.ArgumentParser(description='Make a map')
parser.add_argument('input', type=str, help='Input', default="Json file")

def make_map(values, mini=None, maxi=None, title="", delim=None):
    if mini == None:
        mini = min(values.values())
    if maxi == None:
        maxi = max(values.values())

    dic = {
            'title': title,
            'hidden': [],
            'borders': "#000000",
            'groups': {},
            }

    colors = [ "#f0f9e8", "#bae4bc", "#7bccc4", "#43a2ca", "#0868ac" ]
    nb_colors = len(colors)

    bin_size = (float(maxi) - mini) / nb_colors

    if delim is None:
        delim = []
        for i in range(nb_colors + 1):
            delim.append(round(mini + i * bin_size, 2))

    for i in range(nb_colors):
        dic['groups'][colors[i]] = {
                'div': "#box{}".format(i),
                'label': "[{} - {}]".format(delim[i], delim[i + 1]),
                'paths': [],
                }

    for state, val in values.items():
        for i in range(nb_colors):
            if val <= delim[i + 1]:
                dic['groups'][colors[i]]['paths'].append(state)
                break

    return dic


if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.input, "r") as f:
        values = json.load(f)
    print(json.dumps(make_map(values), indent=2))

