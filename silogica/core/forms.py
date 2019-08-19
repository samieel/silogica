from django import forms
from .models import PREMISSAS, CLASSE, E_CLASSE

class get_silogismo(forms.ModelForm):

    class Meta:
        model = PREMISSAS
        fields = ('extensao1','termo1','termo2','extensao2','termo3','termo4','extensao3','termo5','termo6')

class get_c_classe(forms.ModelForm):

    class Meta:
        model = CLASSE
        fields = ('cla_prof',)


class get_e_classe(forms.ModelForm):

    class Meta:
        model = E_CLASSE
        fields = ('e_codigo',)