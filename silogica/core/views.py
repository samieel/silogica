from django.shortcuts import render, redirect
from .forms import get_silogismo
from .models import PREMISSAS
from . import models

# Create your views here.


def index(request):
    form = get_silogismo(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        key = post.id
        return redirect('silogismo/%s' % key)
    return render(request, 'testform.html', {'form': form})