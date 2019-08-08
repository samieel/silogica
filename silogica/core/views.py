from django.shortcuts import render, redirect
from .forms import get_silogismo
from .models import PREMISSAS, REDUCAO
from . import models

#erros
e_termos = 'Encontrado erro referente aos termos'
e_negativas = 'Encontrado erro, de duas negativas nada se conclui'
e_particulares = 'Encontrado erro, de duas particulares nada se conclui'
e_conclusao = 'Encontrado erro referente a conclusão'
e_modos = 'Encontrado erro ao definir o modo do silogismo'

def grava(x, r, s):
    s.modo = x
    s.reducao = r
    s.save()

def reducao_ok(r, s):
    r.save()
    print(r.id)
    red = REDUCAO()
    red.sid_silogismo = s.id
    red.sid_reducao = r.id
    red.save()

def index(request):
    form = get_silogismo(request.POST)

    if form.is_valid():
        s = form.save(commit=False)

        #auxiliares
        negativas = ['Nenhum', 'Algum não']
        particulares = ['Algum', 'Algum não']
        c_termos = [s.termo1, s.termo2, s.termo3, s.termo4]
        conclu = [s.termo5, s.termo6]

        #erro termos = na mesma premissa
        if s.termo1 == s.termo2 or s.termo3 == s.termo4:
            return render(request, 'erro.html', {'erro': e_termos})

        #erro não tem 3 termos nas 2 premissas
        if c_termos.count(s.termo1) + c_termos.count(s.termo2) != 3:
            return render(request, 'erro.html', {'erro': e_termos})
        else:
            #erro duas negativas
            if negativas.count(s.extensao1) + negativas.count(s.extensao2) > 1:
                return render(request, 'erro.html', {'erro': e_negativas})
            #erro duas particulares
            elif particulares.count(s.extensao1) + particulares.count(s.extensao2) > 1:
                return render(request, 'erro.html', {'erro': e_particulares})
            else:
                # 1° figura
                if s.termo1 == s.termo4:
                    if s.termo2 != s.termo6 or s.termo3 != s.termo5:
                        return render(request, 'erro.html', {'erro': e_conclusao})
                    else:
                        if s.extensao1 == 'Todo' and s.extensao2 == 'Todo' and s.extensao3 == 'Todo':
                            # BARBARA
                            x = 'Barbara'
                            r = 'Irredutivel'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Todo' and s.extensao3 == 'Nenhum':
                            # CELARENT
                            x = 'Celarent'
                            r = 'Irredutivel'
                            grava(x, r, s)
                        elif s.extensao1 == 'Todo' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum':
                            # DARII
                            x = 'Darii'
                            r = 'Irredutivel'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum não':
                            # FERIO
                            x = 'Ferio'
                            r = 'Irredutivel'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            
                            grava(x, r, s)
                        else:
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo2 == s.termo4:
                    # 2° figura
                    if s.termo1 != s.termo6 or s.termo3 != s.termo5:
                        return render(request, 'erro.html', {'erro': e_conclusao})
                    else:
                        if s.extensao1 == 'Nenhum' and s.extensao2 == 'Todo' and s.extensao3 == 'Nenhum':
                            # CESARE
                            x = 'Cesare'
                            r = 'Celarent'
                            grava(x, r, s)
                        elif s.extensao1 == 'Todo' and s.extensao2 == 'Nenhum' and s.extensao3 == 'Nenhum':
                            # CAMESTRES
                            x = 'Camestres'
                            r = 'Celarent'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum não':
                            # FESTINO
                            x = 'Festino'
                            r = 'Ferio'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Todo' and s.extensao2 == 'Algum não' and s.extensao3 == 'Algum não':
                            # BAROCO
                            x = 'Baroco'
                            r = 'Irredutivel'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            s.extensao2 = 'Algum'
                            s.n2 = 'não'
                            grava(x, r, s)
                        else:
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo1 == s.termo3:
                    # 3° figura
                    if s.termo2 != s.termo6 or s.termo4 != s.termo5:
                        return render(request, 'erro.html', {'erro': e_conclusao})
                    else:
                        if s.extensao1 == 'Todo' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum':
                            # DARAPTI
                            x = 'Darapti'
                            r = 'Darii'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum não':
                            # FELAPTON
                            x = 'Felapton'
                            r = 'Ferio'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum não':
                            # FERISON
                            x = 'Ferison'
                            r = 'Ferio'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Algum' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum':
                            # DISAMIS
                            x = 'Disamis'
                            r = 'Darii'
                            grava(x, r, s)
                        elif s.extensao1 == 'Algum não' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum não':
                            # BOCARDO ajeitar
                            x = 'Bocardo'
                            r = 'Irredutivel'
                            s.extensao1 = 'Algum'
                            s.n1 = 'não'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Todo' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum':
                            # DATISI
                            x = 'Datisi'
                            r = 'Darii'
                            grava(x, r, s)
                        else:
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo2 == s.termo3:
                    # 4° figura
                    if s.termo1 != s.termo6 or s.termo4 != s.termo5:
                        return render(request, 'errp.html', {'erro': e_conclusao})
                    else:
                        if s.extensao1 == 'Todo' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum':
                            # BAMALIP
                            x = 'Bamalip'
                            r = 'Barbara'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum não':
                            # FESAPO
                            x = 'Fesapo'
                            r = 'Ferio'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Nenhum' and s.extensao2 == 'Algum' and s.extensao3 == 'Algum não':
                            # FRESISON
                            x = 'Fresison'
                            r = 'Ferio'
                            s.extensao3 = 'Algum'
                            s.n3 = 'não'
                            grava(x, r, s)
                        elif s.extensao1 == 'Todo' and s.extensao2 == 'Nenhum' and s.extensao3 == 'Nenhum':
                            # CALEMES
                            x = 'Calemes'
                            r = 'Celarent'
                            grava(x, r, s)
                        elif s.extensao1 == 'Algum' and s.extensao2 == 'Todo' and s.extensao3 == 'Algum':
                            # DIMATIS
                            x = 'Dimatis'
                            r = 'Darii'
                            grava(x, r, s)
                        else:
                            return render(request, 'erro.html', {'erro': e_modos})
                else:
                    return render(request, 'erro.html', {'erro': e_modos})

        key = s.id
        if r == 'Irredutivel':
            return redirect('silogismo/%s' % key)
        else:
            return redirect('reducao/%s' % key)
    return render(request, 'index.html', {'form': form})


def exibir_silogismo(request, key):
    sin = PREMISSAS.objects.get(id=key)
    return render(request, 'silogismo.html', {'s':sin})

def reducao(request, key):
    s = PREMISSAS.objects.get(id=key)

    form = get_silogismo(request.POST)

    if form.is_valid():
        r = form.save(commit=False)
        if s.modo == 'Cesare':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo3 and r.termo4 == s.termo4 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Camestres':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Festino':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo3 and r.termo4 == s.termo4 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Darapti':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Felapton':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Disamis':
            if s.termo1 == r.termo4 and s.termo2 == r.termo3 and s.termo3 == r.termo1 and s.termo4 == r.termo2 and s.termo5 == r.termo6 and s.termo6 == r.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Datisi':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Ferison':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Bamalip':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Todo' and r.extensao3 == 'Todo':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Fesapo':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Fresison':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Calemes':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
        elif s.modo == 'Dimatis':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
    return render(request, 'reducao.html', {'s':s, 'form':form})

def contato(request):
    return render(request, 'embreve.html')

def sobre(request):
    return render(request, 'embreve.html')