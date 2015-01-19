#!/usr/bin/env python

import music21
import pandas
import itertools
import os
import midi
import subprocess
import argparse


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


def special_interval(s):
    z = s[:]
    if z[0] == 11:
        z[0] = -1
    if z[-1] == 0:
        z[-1] = 12
    return [(right - left) for left, right in zip(z, z[1:])]


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


def add_int(a, b):
    return (a + b) % 12


def make_dataframe():
    base = [0, 2, 4, 5, 7, 9, 11]
    notes = list('CDEFGAB')
    accidents = [-1, 0, 1]
    p = itertools.product(accidents, repeat=7)
    r = []
    index_counter = 1

    for seq in p:
        music21_notes = []
        harp_notes = []
        pcset = [(acc + pc) % 12 for acc, pc in zip(seq, base)]

        for note, accident in zip(notes, seq):
            music21_notes.append(note + ['-', '', '#'][accident + 1])
            harp_notes.append(note + list('bn#')[accident + 1])

        chord = music21.chord.Chord(music21_notes)
        prime = chord.primeForm
        forte = chord.forteClassTnI
        interval_vector = chord.intervalVector
        row = [index_counter, ' '.join(harp_notes), pretty_print(pcset), pretty_print(prime), forte, seq]
        for iv in interval_vector:
            row.append(iv)
        r.append(row)
        index_counter += 1

    columns = ['Index', 'Notes', 'PC Set', 'Prime Form', 'Forte class', 'Accidents']
    for i in range(1, 7):
        columns.append(str(i))

    df = pandas.DataFrame(r, columns=columns)
    df.index = list(range(1, len(df) + 1))
    return df


def save_to_csv(filename='harp.csv'):
    make_dataframe().to_csv(os.path.join('csv', filename))


# midi
def make_midi(pc_set=[0,2,4,5,7,9,11], filename='example'):
    def aux(track, current_tick, current_note):
        track.append(midi.NoteOnEvent(tick=current_tick, velocity=127, pitch=current_note))
        track.append(midi.NoteOffEvent(tick=current_tick, pitch=current_note))

    intervals_seq = special_interval(pc_set)
    ret_intevals_seq = intervals_seq[:]
    ret_intevals_seq.reverse()

    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)
    span = 1
    current_note = midi.C_4
    current_tick = 100
    tempo = midi.SetTempoEvent()
    tempo.set_bpm(600)
    events = [
        midi.ProgramNameEvent(tick=0, text='1\x00', data=[49, 0]),
        midi.ProgramChangeEvent(tick=0, channel=0, data=[46]),
        tempo
    ]

    for event in events:
        track.append(event)

    while current_note < midi.A_6:
        for i in intervals_seq:
            aux(track, current_tick, current_note)
            current_note += i

    while current_note > midi.Bb_3:
        for j in ret_intevals_seq:
            aux(track, current_tick, current_note)
            current_note -= j

    current_tick += span * 1000
    eot = midi.EndOfTrackEvent(tick=current_tick)
    track.append(eot)
    midi.write_midifile(filename + '.mid', pattern)


def save_midi_files(df):
    series = df['PC Set']
    i = 1
    for pcset in series:
        print('saving {}'.format(i))
        make_midi(parse_pcset(pcset), os.path.join('static', 'midi', str(i)))
        i += 1


# images
def make_lily_code(int_tup):
    def aux(ind):
        return ['^', '-', 'v'][ind + 1]

    pre = '\paper {\n\ttagline= ##f\n}\n\markup \harp-pedal #'
    left_tup = (int_tup[1], int_tup[0], int_tup[6])
    right_tup = int_tup[2:-1]
    left = ''.join(map(aux, left_tup))
    right = ''.join(map(aux, right_tup))
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
    parser.add_argument("-m", "--save_midi", help="Save midi files",
                        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    if args.make_images:
        df = make_dataframe()
        make_figs(df)
    if args.save_csv:
        make_dataframe().to_csv(os.path.join('csv', 'harp.csv'))
    if args.save_midi:
        df = make_dataframe()
        save_midi_files(df)
