#!/usr/bin/env python

import itertools
import pandas
import os
import socket
import subprocess
import argparse


# prime form
def add_last(s):
    return s + [s[0]]


def diff(a, b):
    return (a - b) % 12


def rotate(s, ind):
    return s[ind:] + s[:ind]


def intervals(s):
    return [diff(b, a) for a, b in zip(s, s[1:])]


def renumerate(s):
    r = [0]
    for i in s:
        r.append((r[-1] + i) % 12)
    return r


def invert(s):
    return [(12 - i) % 12 for i in s]


def get_prime_form(s):
    seq = sorted(list(set(s)))
    d = {}
    for i in range(len(seq)):
        r = rotate(seq, i)
        ordinal = r
        inverted = invert(r)

        for current_s in [ordinal, inverted]:
            intervals_seq = intervals(current_s)
            ret_intervals_seq = intervals_seq[:]
            ret_intervals_seq.reverse()

            for current_i_seq in [intervals_seq, ret_intervals_seq]:
                distance = sum(current_i_seq)
                if distance not in d:
                    d[distance] = []
                d[distance].append(current_i_seq)

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
        prime = get_prime_form(list(set(pcset)))
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


# FIXME: adapt to pandas and improve
# make figs
def make_lily_code(int_tup):
    dic = {
        'b': 'v',
        'n': '-',
        '#': '^',
        }

    pre = '\paper {\n\ttagline= ##f\n}\n\markup \harp-pedal #'
    left = ''.join(map(str, [int_tup[1], int_tup[0], int_tup[6]]))
    right = ''.join(map(str, int_tup[2:-1]))
    post = '"{}|{}"'.format(left, right)
    return pre + post


def run_lilypond(int_tup, n):
    lily = '/Applications/LilyPond.app/Contents/Resources/bin/lilypond'
    conv = '/usr/local/bin/convert'
    static = 'static'
    filename = os.path.join(static, 'tmp.ly')
    in_png = 'tmp.png'

    out = os.path.join(static, 'img', str(n) + '.png')
    with open(filename, 'w') as f:
        f.write(make_lily_code(int_tup))

    subprocess.call([lily, '--png', filename])
    subprocess.call([conv, '-trim', in_png, out])

    for f in filename, in_png:
        os.remove(f)


def make_figs(df):
    series = df['Accidents']
    for i, tup in series.to_dict().items():
        print('Processing {} ...'.format(i))
        run_lilypond(tup, i)


def arguments():
    parser = argparse.ArgumentParser(description='Create auxiliary files for Harp app.')
    parser.add_argument("-i", "--make_images", help="Create Lilypond images",
                        action="store_true")
    parser.add_argument("-s", "--save_csv", help="Save csv file with data",
                        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    if args.make_images:
        df = make_table()
        make_figs(df)
    if args.save_csv:
        make_table().to_csv(os.path.join('csv', 'harp.csv'))
