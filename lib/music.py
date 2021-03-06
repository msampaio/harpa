#!/usr/bin/env python

import music21
import pandas
import itertools
import os
import pcsets
# usar music21 midi
# http://web.mit.edu/music21/doc/moduleReference/moduleMidi.html
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


def base_n(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0" ) or ( base_n(num // b, b).lstrip("0") + numerals[num % b])


def convert_radial_scalar(seq, to_scalar=False):
    if to_scalar:
        ord = [1, 0, 3, 4, 5, 6, 2]
    else:
        ord = [1, 0, 6, 2, 3, 4, 5]
    return [seq[i] for i in ord]


def make_dataframe(radial=False):
    radial_order = [2, 0, 11, 4, 5, 7, 9]
    radial_notes = list('DCBEFGA')
    scalar_order = sorted(radial_order)
    scalar_notes = list('CDEFGAB')

    if radial:
        notes_order = radial_order
        main_notes = radial_notes
        main_title = "Notes (radial)"
        secondary_title = "Notes (scalar)"
    else:
        notes_order = scalar_order
        main_notes = scalar_notes
        main_title = "Notes (scalar)"
        secondary_title = "Notes (radial)"

    repeat = 7
    accidents = [0, 1, 2]
    accidents_size = len(accidents)
    harp_settings = itertools.product(accidents, repeat=repeat)

    settings_index_counter = 0
    settings_index_list = []

    rows = []

    for hs in harp_settings:
        settings_index = base_n(settings_index_counter, accidents_size)
        settings_index_list.append(int(settings_index))

        pitches = []
        music21_notes = []
        main_display = []

        for pitch, main_note, accident in zip(notes_order, main_notes, hs):
            pitches.append(((pitch - 1) + accident) % 12)
            music21_notes.append(main_note + ['-', '', '#'][accident])
            main_display.append(main_note + ['b', 'n', '#'][accident])

        secondary_display = convert_radial_scalar(main_display, radial)

        chord = music21.chord.Chord(music21_notes)
        prime = chord.primeForm
        if tuple(prime) in pcsets.transition.keys():
            forte, prime = pcsets.transition[tuple(prime)]
            prime = list(prime)
        else:
            forte = chord.forteClassTnI
        interval_vector = chord.intervalVector

        row = [' '.join(main_display), ' '.join(secondary_display), pretty_print(pitches), pretty_print(prime), forte, hs]
        for iv in interval_vector:
            row.append(iv)
        rows.append(row)

        settings_index_counter += 1

    columns = [main_title, secondary_title, 'PC Set', 'Prime Form', 'Forte class', 'Accidents']
    for i in range(1, 7):
        columns.append(str(i))

    df = pandas.DataFrame(rows, columns=columns)
    df.index = settings_index_list
    df.index.name = 'Index'

    return df


def save_to_csv(filename='harp.csv'):
    make_dataframe().to_csv(os.path.join('csv', filename))


# midi
def make_midi(pc_set=[0,2,3,4,5,7,9,11], filename='example'):
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


def _save_one_midi_file(ind, pcset):
    # receive pcset in radial order
    print('saving {}'.format(ind))
    parsed = parse_pcset(pcset)
    ordered = [parsed[int(i)] for i in list(str(1034562))]
    make_midi(ordered, os.path.join('static', 'midi', str(ind)))


def save_midi_files(df):
    series = df['PC Set']
    for i, pcset in series.iteritems():
        _save_one_midi_file(i, pcset)


# images
def make_lily_code(int_tup):
    # receive int_tup in radial order
    def aux(ind):
        return ['^', '-', 'v'][ind]

    pre = '\paper {\n\ttagline= ##f\n}\n\markup \harp-pedal #'

    left_tup = int_tup[:3]
    right_tup = int_tup[3:]

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
