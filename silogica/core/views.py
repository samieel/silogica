from django.shortcuts import render, redirect
from .forms import get_silogismo, get_c_classe, get_e_classe, get_e_erro
from .models import PREMISSAS, REDUCAO, ERRO, CLASSE
from . import models

#erros
e_termos1 = 'Encontrado erro referente aos termos, termo 1 igual ao termo 2'
e_termos2 = 'Encontrado erro referente aos termos, termo 3 igual ao termo 4'
e_termos3 = 'Encontrado erro referente aos termos, numero de termos diferente de 3'
e_negativas = 'Encontrado erro, de duas negativas nada se conclui'
e_particulares = 'Encontrado erro, de duas particulares nada se conclui'
e_conclusao = 'Encontrado erro referente a conclusão'
e_medio = 'Encontrado erro referente ao termo medio, termo medio não indentificado'
e_modos = 'Encontrado erro ao definir o modo do silogismo'

def bg1(s):
    s.termo1 = s.termo1.lower()
    s.termo2 = s.termo2.lower()
    s.termo3 = s.termo3.lower()
    s.termo4 = s.termo4.lower()
    s.termo5 = s.termo5.lower()
    s.termo6 = s.termo6.lower()

def s_erro(s, e):
    s.save()
    er= ERRO()
    er.err_classe = s.classe
    er.err_sid = s.id
    er.err_erro = e
    er.save()

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

def reducao_error(r, s):
    r.save()
    red = REDUCAO()
    red.sid_silogismo = s.id
    red.sid_reducao = r.id
    red.save()

def classe(request):
    e_classe = get_e_classe(request.POST)
    c_classe = get_c_classe(request.POST)

    if e_classe.is_valid():
        cc = e_classe.save(commit=False)
        try:
            e = CLASSE.objects.get(cla_codigo=cc.e_codigo)
            classe = cc.e_codigo
            return redirect('/s/%s' % classe)
        except:
            erro = 'classe não existe'
            return render(request, 'ec_class.html', {'e_cla':e_classe, 'c_cla':c_classe, 'erro':erro})

    if c_classe.is_valid():
        cc = c_classe.save(commit=False)
        
        cc.save()
        classe = cc.cla_codigo
        return redirect('/new/%s' % classe)
    
    return render(request, 'ec_class.html', {'e_cla':e_classe, 'c_cla':c_classe})

def nclasse(request, classe):
    cod = classe
    return render(request, 'new_class.html', {'cod':cod})

def e_erro(request):
    e_erro = get_e_erro(request.POST)
    if e_erro.is_valid():
        cc = e_erro.save(commit=False)
        try:
            e = CLASSE.objects.get(cla_codigo=cc.e_codigo)
            if cc.e_prof == e.cla_prof:
                classe = cc.e_codigo
                return redirect('/erros/%s' % classe)
            else:
                erro = 'a classe informada não esta relacionada ao professor'
                return render(request, 'e_erro.html', {'e_erro':e_erro, 'erro':erro})               
        except:
            erro = 'classe não existe'
            return render(request, 'e_erro.html', {'e_erro':e_erro, 'erro':erro})


    return render(request, 'e_erro.html')

def index(request, classe):
    form = get_silogismo(request.POST)
    if form.is_valid():
        s = form.save(commit=False)
        s.classe = classe
        bg1(s)

        #auxiliares
        negativas = ['Nenhum', 'Algum não']
        particulares = ['Algum', 'Algum não']
        c_termos = [s.termo1, s.termo2, s.termo3, s.termo4]
        conclu = [s.termo5, s.termo6]

        #erro termos = na mesma premissa
        if s.termo1 == s.termo2:
            s_erro(s, e_termos1)
            return render(request, 'erro.html', {'erro': e_termos1})
        elif s.termo3 == s.termo4:
            s_erro(s, e_termos2)
            return render(request, 'erro.html', {'erro': e_termos2})

        #erro não tem 3 termos nas 2 premissas
        if c_termos.count(s.termo1) + c_termos.count(s.termo2) != 3:
            s_erro(s, e_termos3)
            return render(request, 'erro.html', {'erro': e_termos3})
        else:
            #erro duas negativas
            if negativas.count(s.extensao1) + negativas.count(s.extensao2) > 1:
                s_erro(s, e_negativas)
                return render(request, 'erro.html', {'erro': e_negativas})
            #erro duas particulares
            elif particulares.count(s.extensao1) + particulares.count(s.extensao2) > 1:
                s_erro(s, e_particulares)
                return render(request, 'erro.html', {'erro': e_particulares})
            else:
                # 1° figura
                if s.termo1 == s.termo4:
                    #erro conclusão
                    if s.termo2 != s.termo6 or s.termo3 != s.termo5:
                        s_erro(s, e_conclusao)
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
                        #erro modo 1fig
                        else:
                            s_erro(s, e_modos)
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo2 == s.termo4:
                    # 2° figura
                    #erro conclusão
                    if s.termo1 != s.termo6 or s.termo3 != s.termo5:
                        s_erro(s, e_conclusao)
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
                        #erro modo 2fig
                        else:
                            s_erro(s, e_modos)
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo1 == s.termo3:
                    # 3° figura
                    #erro conclusão
                    if s.termo2 != s.termo6 or s.termo4 != s.termo5:
                        s_erro(s, e_conclusao)
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
                        #erro modo 3fig
                        else:
                            s_erro(s, e_modos)
                            return render(request, 'erro.html', {'erro': e_modos})


                elif s.termo2 == s.termo3:
                    # 4° figura
                    #erro conclusão
                    if s.termo1 != s.termo6 or s.termo4 != s.termo5:
                        return render(request, 'erro.html', {'erro': e_conclusao})
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
                            #erro modo 4fig
                            s_erro(s, e_modos)
                            return render(request, 'erro.html', {'erro': e_modos})
                #erro sem termo medio
                else:
                    s_erro(s, e_medio)
                    return render(request, 'erro.html', {'erro': e_medio})

        key = s.id
        if r == 'Irredutivel':
            return redirect('/silogismo/%s' % key)
        else:
            return redirect('/reducao/%s' % key)
    return render(request, 'index.html', {'form': form})


def exibir_silogismo(request, key):
    sin = PREMISSAS.objects.get(id=key)
    return render(request, 'silogismo.html', {'s':sin})

def reducao(request, key):
    s = PREMISSAS.objects.get(id=key)

    form = get_silogismo(request.POST)

    if form.is_valid():
        r = form.save(commit=False)
        r.classe = s.classe
        bg1(r)
        if s.modo == 'Cesare':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo3 and r.termo4 == s.termo4 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                print('mds')
                r.termo1 = s.termo2
                r.termo2 = s.termo1 
                r.termo3 = s.termo3
                r.termo4 = s.termo4 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        
        elif s.modo == 'Camestres':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo3
                r.termo2 = s.termo4 
                r.termo3 = s.termo1
                r.termo4 = s.termo2 
                r.termo5 = s.termo6 
                r.termo6 = s.termo5
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Festino':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo3 and r.termo4 == s.termo4 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo2
                r.termo2 = s.termo1 
                r.termo3 = s.termo3
                r.termo4 = s.termo4 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Darapti':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo1
                r.termo2 = s.termo2 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Felapton':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo1
                r.termo2 = s.termo2 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Disamis':
            if s.termo1 == r.termo4 and s.termo2 == r.termo3 and s.termo3 == r.termo1 and s.termo4 == r.termo2 and s.termo5 == r.termo6 and s.termo6 == r.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo3
                r.termo2 = s.termo4 
                r.termo3 = s.termo2
                r.termo4 = s.termo1 
                r.termo5 = s.termo6 
                r.termo6 = s.termo5
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Datisi':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo1
                r.termo2 = s.termo2 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Ferison':
            if r.termo1 == s.termo1 and r.termo2 == s.termo2 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo1
                r.termo2 = s.termo2 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Bamalip':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Todo' and r.extensao3 == 'Todo':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo3
                r.termo2 = s.termo4 
                r.termo3 = s.termo1
                r.termo4 = s.termo2 
                r.termo5 = s.termo6 
                r.termo6 = s.termo5
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Fesapo':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo2
                r.termo2 = s.termo1 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Fresison':
            if r.termo1 == s.termo2 and r.termo2 == s.termo1 and r.termo3 == s.termo4 and r.termo4 == s.termo3 and r.termo5 == s.termo5 and r.termo6 == s.termo6:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum não':   
                    r.extensao3 = 'Algum'
                    r.n3 = 'não'
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo2
                r.termo2 = s.termo1 
                r.termo3 = s.termo4
                r.termo4 = s.termo3 
                r.termo5 = s.termo5 
                r.termo6 = s.termo6
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Calemes':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Nenhum' and r.extensao2 == 'Todo' and r.extensao3 == 'Nenhum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo3
                r.termo2 = s.termo4 
                r.termo3 = s.termo1
                r.termo4 = s.termo2 
                r.termo5 = s.termo6 
                r.termo6 = s.termo5
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
        elif s.modo == 'Dimatis':
            if r.termo1 == s.termo3 and r.termo2 == s.termo4 and r.termo3 == s.termo1 and r.termo4 == s.termo2 and r.termo5 == s.termo6 and r.termo6 == s.termo5:
                if r.extensao1 == 'Todo' and r.extensao2 == 'Algum' and r.extensao3 == 'Algum':   
                    reducao_ok(r, s)
                    return render(request, 'reducao_ok.html', {'s':s, 'r':r})
            else:
                r.termo1 = s.termo3
                r.termo2 = s.termo4 
                r.termo3 = s.termo1
                r.termo4 = s.termo2 
                r.termo5 = s.termo6
                r.termo6 = s.termo5
                reducao_error(r, s)
                return render(request, 'reducao_error.html', {'s':s, 'form':form, 'r':r})
    return render(request, 'reducao.html', {'s':s, 'form':form})

def contato(request):
    return render(request, 'contato.html')

def avalia(request):
    return render(request, 'avalia.html')

def erros(request, classe):
    ers = ERRO.objects.filter(err_classe=classe)
    return render(request, 'c_erros.html', {'e':ers})