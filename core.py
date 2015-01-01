#!/usr/bin/env python

import itertools
import pandas
import os
import socket


# prime form
def add_last(s):
    return s + [s[0]]

def diff(a, b):
    return (a - b) % 12

def rotate(s, ind):
    return s[ind:] + s[:ind]


def intervals(s, reverse=False):
    if reverse:
        return [diff(a, b) for a, b in zip(s, s[1:])]
    else:
        return [diff(b, a) for a, b in zip(s, s[1:])]


def renumerate(s):
    r = [0]
    for i in s:
        r.append((r[-1] + i) % 12)
    return r


def get_prime_form(s):
    def aux(intervals_seq, dic):
        distance = sum(intervals_seq)
        if distance not in dic:
            dic[distance] = []
        dic[distance].append(intervals_seq)

    seq = sorted(list(set(s)))
    d = {}
    for i in range(len(seq)):
        r = rotate(seq, i)
        aux(intervals(r, False), d)
        aux(intervals(r, True), d)

    lowest_distance = sorted(d.keys())[0]
    more_compact = sorted(d[lowest_distance])[0]
    return renumerate(more_compact)


def pretty_print(s):
    r = []
    for i in s:
        if i == 10:
            i = 'A'
        elif i == 11:
            i = 'B'
        else:
            i = str(i)
        r.append(i)
    return ''.join(r)


def get_print_prime_form(s):
    return pretty_print(get_prime_form(s))


def parse_pcset(s):
    r = []
    for c in list(s):
        if c.upper() == 'A':
            c = 10
        elif c.upper() == 'B':
            c = 11
        else:
            c = int(c)
        r.append(c)
    return r


# pedals
def add_int(a, b):
    return (a + b) % 12


def add_str(a, b):
    return a + list('bn#')[b + 1]


def make_table():
    base = [0, 2, 4, 5, 7, 9, 11]
    notes = list('CDEFGAB')
    accidents = [-1, 0, 1]
    p = itertools.product(accidents, repeat=7)
    r = []
    n = 1
    for seq in p:
        pcset = [add_int(a, b) for a, b in zip(seq, base)]
        pcset = list(set(pcset))
        prime = get_prime_form(pcset)
        ns = [add_str(a, b) for a, b in zip(notes, seq)]
        r.append([n, ' '.join(ns), pretty_print(pcset), pretty_print(prime), seq])
        n += 1
    df = pandas.DataFrame(r, columns=['Code', 'Notes', 'PC Set', 'Prime Form', 'Accidents'])
    df.index = list(range(1, len(df) + 1))
    return df


def save_to_csv(filename='harp.csv'):
    make_table().to_csv(os.path.join('csv', filename))


def load_csv(filename='harp.csv'):
    hostname = socket.gethostname()
    if "webfaction.com" in hostname:
        f = os.path.join('/home/genos/webapps/harp/harp', 'csv', filename)

    else:
        f = os.path.join('csv', filename)
    return pandas.DataFrame.from_csv(f)
