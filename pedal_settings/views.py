from io import BytesIO
import zipfile

import pandas
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils.translation import get_language
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from pedal_settings.forms import IndexForm, PrimeForm, AccidentsForm
from lib import core
from pedal_settings.templatetags.dispositions_extras import radial_format


# Create your views here.

COLUMNS = ['Notes (scalar)', 'Notes (radial)', 'PC Set', 'Prime Form', 'Forte class']
RADIAL = False


def get_language_url():
    # ugly javascript localization
    if get_language() == 'pt-br':
        return "http://cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese-Brasil.json"
    else:
        return "http://cdn.datatables.net/plug-ins/3cfcc339e89/i18n/English.json"


def error404(request):
    return render(request, "404.html")


def error500(request):
    return render(request, "500.html")


def home(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "dashboard.html")


def about(request):
    return render(request, "about.html")


def show_settings_by_index(request, pedal_index):
    df = core.load_csv()

    series = df.loc[int(pedal_index)]
    df = pandas.DataFrame([series])

    df = df[COLUMNS]

    args = {
        'title': 'Settings index {}'.format(pedal_index),
        'df': df,
        'language_url': get_language_url(),
        'radial': RADIAL,
    }
    return render(request, "show_settings.html", args)


def show_settings_by_prime(request, pedal_prime):
    df = core.load_csv()

    df = df[df['Prime Form'] == pedal_prime]

    df = df[COLUMNS]

    args = {
        'title': 'Settings with PC Prime Form {}'.format(pedal_prime),
        'settings': len(df),
        'df': df,
        'language_url': get_language_url(),
        'radial': RADIAL,
    }
    return render(request, "show_settings.html", args)


def show_settings_by_accidents(request, accidents):
    df = core.load_csv()

    df = df[df['Accidents'] == accidents]

    df = df[COLUMNS]

    args = {
        'title': 'Settings with PC Prime Form {}'.format(accidents),
        'settings': len(df),
        'df': df,
        'language_url': get_language_url(),
        'radial': RADIAL,
    }
    return render(request, "show_settings.html", args)


def show_all_settings(request):
    df = core.load_csv()

    df = df[COLUMNS]

    args = {
        'title': 'All settings',
        'settings': len(df),
        'df': df,
        'language_url': get_language_url(),
        'radial': RADIAL,
    }
    return render(request, 'show_settings.html', args)


def get_by_index(request):
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            ind = form.cleaned_data['settings_index']
            return HttpResponseRedirect(reverse('pedal_settings.views.show_settings_by_index', args={ind,}))

    else:
        form = IndexForm()
    return render(request, 'filter_index.html', {'form': form})


def get_by_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            prime = form.cleaned_data['settings_prime']
            return HttpResponseRedirect(reverse('pedal_settings.views.show_settings_by_prime', args={prime,}))

    else:
        form = PrimeForm()
    return render(request, 'filter_prime_form.html', {'form': form})


def get_by_accidents(request):
    if RADIAL:
        notes = list('dcbefga')
    else:
        notes = list('cdefgab')
    if request.method == 'POST':
        form = AccidentsForm(request.POST)
        if form.is_valid():
            accidents = tuple([int(form.cleaned_data[c]) for c in notes])
            df = core.load_csv()
            disposition = df[df['Accidents'] == str(accidents)]
            index = disposition.index.values[0]
            return HttpResponseRedirect(reverse('pedal_settings.views.show_settings_by_index', args={index,}))

    else:
        init_dic = {}
        for a in list('abcdefg'):
            init_dic[a] = 0
        form = AccidentsForm(init_dic)
    return render(request, 'filter_accidents.html', {'form': form})


def download_all_settings(request):
    df = core.load_csv()
    buff = BytesIO()

    df = df[COLUMNS]

    df.index = [radial_format(i) for i in df.index]
    df.index.name = 'Index'

    zip_archive = zipfile.ZipFile(buff, mode='w')
    zip_archive.writestr('pedal_settings.txt', df.to_string())
    zip_archive.close()

    response = HttpResponse(buff.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=pedal_settings.zip'
    return response


def show_statistics(request):
    df = core.load_csv()
    pf_series = df['Prime Form']

    type_series = pandas.Series(map(len, pf_series), index=pf_series.index)
    type_count_simple = type_series.value_counts(sort=True)
    type_count_normalized = type_series.value_counts(normalize=True, sort=True)
    type_count_df = pandas.DataFrame([type_count_simple, type_count_normalized]).T
    type_count_df.columns = [_('Amount'), _('Proportion')]
    type_count_df.index.name = _('Number of Pitch Classes')
    type_count_df = type_count_df.T

    count_items = type_count_df.T[_('Amount')].to_dict().items()
    chord_type_pie_data = list(map(lambda x: [str(x[0]), x[1]], count_items))
    chord_type_pie_data.insert(0, list(type_count_df.index))

    pf_histogram_data = pf_series.value_counts().to_dict().items()
    pf_histogram_data = list(map(list, pf_histogram_data))
    pf_histogram_data.insert(0, [_('Forte class'), _('Number of pedal settings')])

    # interval vector
    iv_string_list = [str(i) for i in range(1, 7)]
    iv_columns = COLUMNS[:]
    iv_columns.extend(iv_string_list)

    # global interval_vector
    iv_sum_series = df[iv_string_list].sum()
    iv_sum_distribution_series = (iv_sum_series - iv_sum_series.mean()) / iv_sum_series.std()
    iv_sum_distribution_series = iv_sum_distribution_series.to_dict().items()
    iv_sum_distribution_series = list(map(list, sorted(iv_sum_distribution_series)))
    iv_sum_distribution_series.insert(0, [_('Interval'), _('Amount')])

    args = {
        'type_table_data': type_count_df,
        'chord_type_pie_data': chord_type_pie_data,
        'pf_histogram_data': pf_histogram_data,
        'interval_vector_data': iv_sum_series,
        'interval_vector_line_data': iv_sum_distribution_series,
    }

    return render(request, 'statistics.html', args)
