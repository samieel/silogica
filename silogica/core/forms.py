from django import forms
from .models import PREMISSAS

class get_silogismo(forms.ModelForm):

    class Meta:
        model = PREMISSAS
        fields = ('modo','reducao','extensao1','termo1','termo2','extensao2','termo3','termo4','extensao3','termo5','termo6')