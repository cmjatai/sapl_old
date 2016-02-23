## Script (Python) "qs_filtro"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

import re
from sets import Set as set

request = container.REQUEST
response = request.RESPONSE
session = request.SESSION


def filtroLimpo():

    filtro = {}
    filtro['tc'] = []  # tipo de conteudo a ser filtrado values = tm, tn, td
    filtro['tm'] = []  # se tc = 'tm' > materia - então tm guarda ids de tipos de matéria
    filtro['ts'] = []  # se tc = 'tm' > materia - então ts guarda ids de status
    filtro['tn'] = []  # se tc = 'tn' > norma - então tn guarda ids de tipos de norma
    filtro['tr'] = []  # se tc = 'tm' > materia - tr - tramitando - [] para tanto faz, [0, ] para nao e [1,] para sim
    filtro['q'] = []   # expressão de pesquisa
    filtro['qs-user'] = ''   # expressão de pesquisa
    filtro['v'] = 0    # v - vereador
    filtro['p'] = 1    # p - pagina
    filtro['s'] = 10   # s - step
    filtro['a'] = []   # a - ano
    filtro['n'] = []   # n - número do documento
    return filtro


# session.set('filtro', filtroLimpo())

filtro = session.get('filtro')

p = None

if filtro:
    d = '' if 'd' not in request else request.d
    # d - variavel de remoção do filtro
    # d espera o padrão 'aa-bb' onde aa é chave do filtro e bb qual o valor a ser removido
    # ou d, espera x para limpar filtro

    if d:
        if d == '-':
            filtro = filtroLimpo()
        else:
            d = d.split('-')
            if len(d) == 2:
                try:
                    if d[1] == 'ta':
                        if 'ta' in filtro['tc']:
                            filtro['tc'].remove('ta')
                    elif d[1] == 'td':
                        if 'td' in filtro['tc']:
                            filtro['tc'].remove('td')
                    elif d[0] == 'tn':
                        if int(d[1]) in filtro['tn']:
                            filtro['tn'].remove(int(d[1]))
                        # if len(filtro['tn']) == 0 and 'tn' in filtro['tc']:
                        #    filtro['tc'].remove('tn')
                    elif d[0] == 'tc' and d[1] == 'tm':
                        filtro['tm'] = []
                        filtro['tr'] = []
                        filtro['ts'] = []
                        if 'tm' in filtro['tc']:
                            filtro['tc'].remove('tm')
                    elif d[0] == 'tc' and d[1] == 'tn':
                        filtro['tn'] = []
                        if 'tn' in filtro['tc']:
                            filtro['tc'].remove('tn')
                    elif d[0] == 'tm':
                        if int(d[1]) in filtro['tm']:
                            filtro['tm'].remove(int(d[1]))
                        # if len(filtro['tm']) == 0 and 'tm' in filtro['tc']:
                        #    filtro['tc'].remove('tm')
                    elif d[0] == 'v':
                        filtro['v'] = 0
                    else:
                        filtro[d[0]].remove(int(d[1]))
                    p = 1
                except:
                    pass


else:
    filtro = filtroLimpo()

if 'tc' in request and len(request.tc) > 0:
    if request.tc not in filtro['tc']:
        filtro['tc'].append(request.tc)
        filtro['v'] = 0
        p = 1

for key in ['tm', 'ts', 'tr', 'tn', 'a']:
    if key in request and len(request[key]) > 0:
        try:
            value = int(request[key])
            if value not in filtro[key]:
                filtro[key].append(value)
                p = 1
            if key == 'tr':
                filtro['tr'] = [filtro['tr'][-1], ]
        except:
            pass

if filtro['tn'] and 'tn' not in filtro['tc']:
    filtro['tc'].append('tn')

if filtro['tm'] and 'tm' not in filtro['tc']:
    filtro['tc'].append('tm')

if filtro['ts'] and 'tm' not in filtro['tc']:
    filtro['tc'].append('tm')

if filtro['tr'] and 'tm' not in filtro['tc']:
    filtro['tc'].append('tm')

if 'v' in request and len(request.v) > 0:
    try:
        filtro['v'] = int(request.v)
        filtro['tc'] = ['tm', ]
    except:
        filtro['v'] = 0

if filtro['v'] != 0:
    filtro['tc'] = ['tm', ]

if 's' in request and len(request.s) > 0:
    try:
        filtro['s'] = int(request.s)
    except:
        filtro['s'] = 10
    p = 1

if 'q' in request:
    q = context.pysc.stop_word_remove_pysc(request.q).replace("'", '"')
    q = list(set(filter(None, re.split('("(?:[^"]|"")*")| ', q))))
    rng = range(len(q))
    rng.reverse()
    for i in rng:
        if len(q[i]) < 3:
            try:
                n = int(q[i])
            except:
                q.pop(i)
        if len(q) == 0:
            break
    if q != filtro['q']:
        filtro['q'] = q
        filtro['qs-user'] = request.q
        filtro['p'] = 1
else:
    if 'p' in request and len(request.p) > 0:
        try:
            filtro['p'] = int(request.p)
        except:
            filtro['p'] = 1
if 'p' not in request and p:
    filtro['p'] = p
    #elif 'p' not in request and not p:
    #    filtro['q'] = []
    #    filtro['qs-user'] = ''
    #    filtro['p'] = 1


if 'c' in request and len(request.c) > 0:
    try:
        if int(request.c) > 0:
            filtro['p'] = int(request.c)
        filtro['c'] = int(request.c)
    except:
        filtro['c'] = 1

if 'n' in request and len(request.n) > 0:
    try:
        filtro['n'] = int(request.n)
    except:
        filtro['n'] = 0

session.set('filtro', filtro)

return filtro
