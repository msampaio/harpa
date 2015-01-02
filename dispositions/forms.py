from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_number(value):
    if value not in map(str, range(1, 2188)):
        raise ValidationError(_(u'%s is not a number between 1 and 2187') % value)


def validate_prime(seq):
    allowed = list(map(str, range(10)))
    for s in ('a', 'b'):
        allowed.append(s)
        allowed.append(s.upper())

    if not all((v in allowed) for v in seq):
        raise ValidationError(_(u'%s is not in prime form format') % seq)


class IndexForm(forms.Form):
    settings_index = forms.CharField(label=_('Settings index'),
                                         max_length=4,
                                         help_text=_('Insert an index number between 1 and 2187'),
                                         validators=[validate_number])

class PrimeForm(forms.Form):
    settings_prime = forms.CharField(label=_('Settings Prime Form'),
                                        min_length=4,
                                        max_length=12,
                                        help_text=_('Insert a pcset prime form such as 02468A'),
                                        validators=[validate_prime])

class AccidentsForm(forms.Form):
    choices = ((-1, 'b'), (0, 'n'), (1, '#'))
    c = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    d = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    e = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    f = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    g = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    a = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
    b = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-inline'}), choices=choices)
