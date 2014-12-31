from io import BytesIO
import zipfile
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from dispositions.forms import NumberForm, PrimeForm, AccidentsForm

import possibilities

# Create your views here.


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
    return render(request, "show_dispositions.html", args)


def show_combination_by_prime(request, pedal_prime):
    df = possibilities.load_csv()

    df = df[df['Prime Form'] == pedal_prime]

    del df['Accidents']

    args = {
        'title': 'Combinations with PC Prime Form {}'.format(pedal_prime),
        'dispositions': len(df),
        'df': df,
    }
    return render(request, "show_dispositions.html", args)


def show_combination_by_accidents(request, accidents):
    df = possibilities.load_csv()

    df = df[df['Accidents'] == accidents]

    del df['Accidents']

    args = {
        'title': 'Combinations with PC Prime Form {}'.format(accidents),
        'dispositions': len(df),
        'df': df,
    }
    return render(request, "show_dispositions.html", args)


def show_all_dispositions(request):

    df = possibilities.load_csv()

    del df['Accidents']

    args = {
        'title': 'All dispositions',
        'dispositions': len(df),
        'df': df,
        }
    return render(request, 'show_dispositions.html', args)


def get_number(request):
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/number/' + form.cleaned_data['disposition_number'])

    else:
        form = NumberForm()
    return render(request, 'filter_number.html', {'form': form})


def get_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/prime/' + form.cleaned_data['disposition_prime'])

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

def download_all_dispositions(request):
    df = possibilities.load_csv()
    buff = BytesIO()

    del df['Code']
    del df['Accidents']

    zip_archive = zipfile.ZipFile(buff, mode='w')
    zip_archive.writestr('harp_dispositions.txt', df.to_string())
    zip_archive.close()

    response = HttpResponse(buff.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=harp_dispositions.zip'
    return response