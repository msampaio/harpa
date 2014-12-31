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

def get_max_ind(s):
    r = add_last(s)
    inv = intervals(r)
    m = max(inv)
    return (inv.index(m) + 1) % len(s)

def renumerate(s):
    r = [0]
    for i in s:
        r.append((r[-1] + i) % 12)
    return r

def renumerate2(s):
    r = [0]
    for i in s:
        r.append(r[-1] + i)
    return r

# FIXME: 027B


def get_prime_form(s):
    s1 = sorted(list(set(s)))
    ind = get_max_ind(s1)
    r1 = rotate(s1, ind)
    r2 = list(r1)
    r2.reverse()
    inv1 = intervals(r1, False)
    inv2 = intervals(r2, True)
    prime_inv = sorted([inv1, inv2])[0]
    return renumerate(prime_inv)


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
