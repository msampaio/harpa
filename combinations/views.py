from django.shortcuts import render
from django.http import HttpResponseRedirect
from combinations.forms import NumberForm, PrimeForm, AccidentsForm

import possibilities

# Create your views here.

def select_filter(name, item, arguments, template='music_data__%s'):
    if item != "all":
        arguments[template % name] = item

def home(request):
    return render(request, "index.html")


def show_combination_by_number(request, pedal_number):
    df = possibilities.load_csv()

    df = df[df['Code'] == int(pedal_number)]

    del df['Accidents']

    args = {
        'title': 'Combination number {}'.format(pedal_number),
        'df': df,
    }
    return render(request, "show_combinations.html", args)


def show_combination_by_prime(request, pedal_prime):
    df = possibilities.load_csv()

    df = df[df['Prime Form'] == pedal_prime]

    del df['Accidents']

    args = {
        'title': 'Combinations with PC Prime Form {}'.format(pedal_prime),
        'combinations': len(df),
        'df': df,
    }
    return render(request, "show_combinations.html", args)


def show_combination_by_accidents(request, accidents):
    df = possibilities.load_csv()

    df = df[df['Accidents'] == accidents]

    del df['Accidents']

    args = {
        'title': 'Combinations with PC Prime Form {}'.format(accidents),
        'combinations': len(df),
        'df': df,
    }
    return render(request, "show_combinations.html", args)


def show_complete_list(request):

    df = possibilities.load_csv()

    del df['Accidents']

    args = {
        'title': 'All combinations',
        'combinations': len(df),
        'df': df,
        }
    return render(request, 'show_combinations.html', args)


def get_number(request):
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/number/' + form.cleaned_data['combination_number'])

    else:
        form = NumberForm()
    return render(request, 'filter_number.html', {'form': form})


def get_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/prime/' + form.cleaned_data['combination_prime'])

    else:
        form = PrimeForm()
    return render(request, 'filter_prime_form.html', {'form': form})


def get_accidents(request):
    if request.method == 'POST':
        form = AccidentsForm(request.POST)
        if form.is_valid():
            accidents = tuple([int(form.cleaned_data[c]) for c in list('cdefgab')])
            df = possibilities.load_csv()
            code = str(df[df['Accidents'] == str(accidents)].iloc[0]['Code'])
            print(code, str(accidents))
            return HttpResponseRedirect('/number/' + code)

    else:
        form = AccidentsForm()
    return render(request, 'filter_accidents.html', {'form': form})