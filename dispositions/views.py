from io import BytesIO
import zipfile
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from dispositions.forms import IndexForm, PrimeForm, AccidentsForm
from django.utils.translation import get_language
import core

# Create your views here.


def home(request):
    return render(request, "index.html")


def show_combination_by_index(request, pedal_index):
    df = core.load_csv()

    df = df[df['Code'] == int(pedal_index)]

    del df['Accidents']

    args = {
        'title': 'Settings index {}'.format(pedal_index),
        'df': df,
    }
    return render(request, "show_settings.html", args)


def show_combination_by_prime(request, pedal_prime):
    df = core.load_csv()

    df = df[df['Prime Form'] == pedal_prime]

    del df['Accidents']

    args = {
        'title': 'Settings with PC Prime Form {}'.format(pedal_prime),
        'settings': len(df),
        'df': df,
    }
    return render(request, "show_settings.html", args)


def show_combination_by_accidents(request, accidents):
    df = core.load_csv()

    df = df[df['Accidents'] == accidents]

    del df['Accidents']

    args = {
        'title': 'Settings with PC Prime Form {}'.format(accidents),
        'settings': len(df),
        'df': df,
    }
    return render(request, "show_settings.html", args)


def show_all_settings(request):

    df = core.load_csv()

    del df['Accidents']

    # ugly javascript localization
    if get_language() == 'pt-br':
        language_url = "http://cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese-Brasil.json"
    else:
        language_url = "http://cdn.datatables.net/plug-ins/3cfcc339e89/i18n/English.json"

    args = {
        'title': 'All settings',
        'settings': len(df),
        'df': df,
        'language_url': language_url,
        }
    return render(request, 'show_settings.html', args)


def get_by_index(request):
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/index/' + form.cleaned_data['settings_index'])

    else:
        form = IndexForm()
    return render(request, 'filter_index.html', {'form': form})


def get_by_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/prime/' + form.cleaned_data['settings_prime'])

    else:
        form = PrimeForm()
    return render(request, 'filter_prime_form.html', {'form': form})


def get_by_accidents(request):
    if request.method == 'POST':
        form = AccidentsForm(request.POST)
        if form.is_valid():
            accidents = tuple([int(form.cleaned_data[c]) for c in list('cdefgab')])
            df = core.load_csv()
            code = str(df[df['Accidents'] == str(accidents)].iloc[0]['Code'])
            print(code, str(accidents))
            return HttpResponseRedirect('/index/' + code)

    else:
        init_dic = {}
        for a in list('abcdefg'):
            init_dic[a] = 0
        form = AccidentsForm(init_dic)
    return render(request, 'filter_accidents.html', {'form': form})


def download_all_settings(request):
    df = core.load_csv()
    buff = BytesIO()

    del df['Code']
    del df['Accidents']

    zip_archive = zipfile.ZipFile(buff, mode='w')
    zip_archive.writestr('harp_settings.txt', df.to_string())
    zip_archive.close()

    response = HttpResponse(buff.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=harp_settings.zip'
    return response