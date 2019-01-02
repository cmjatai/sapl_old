## Script (Python) "protocolo_conta_requerimentos_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= ano_base, mes_base
##title=
##
import simplejson as json

def subtract_date(date, year=0, month=0):
    year, month = divmod(year*12 + month, 12)
    if date.month() <= month:
        year = date.year() - year - 1
        month = date.month() - month + 12
    else:
        year = date.year() - year
        month = date.month() - month
    return DateTime(str(year)+'/'+str(month)+'/'+str(date.day()))

request = container.REQUEST
RESPONSE = request.RESPONSE

lResults = []
iResults = {}

dataAtual = DateTime()
dia1MesAtual =  DateTime(str(dataAtual.year())+'/'+str(dataAtual.month())+'/01')
d1 = dia1MesAtual
try:
    d1 = DateTime(ano_base+'/'+mes_base+'/01')
except:
    d1 = dia1MesAtual
df = d1 + 35
df = DateTime(str(df.year())+'/'+str(df.month())+'/01') - 1
d2 = DateTime(str(df.year())+'/'+str(df.month())+'/16')


lReqTramitando = []
if d1 == dia1MesAtual:
    param = {'tip_id_basica':  3, 'ind_tramitacao':  '1'}
    lReqTramitando = context.zsql.materia_pesquisar_zsql(param)

sessoes = context.zsql.sessao_plenaria_listar_dia_zsql(ano_sessao=d1.year(), mes_sessao=d1.month())

lAprovados = []

dataAprovados = {}
for d in sessoes:
    od = context.zsql.votacao_ordem_dia_obter_zsql(dat_ordem='%s/%s/%s'%(d1.year(),d1.month(),d.dia_sessao ))
    for o in od:
        if o.tip_id_basica == 3 and o.tip_resultado_votacao == 1:
            mat = context.zsql.materia_obter_zsql(cod_materia=o.cod_materia)
            if len(mat):
                lAprovados.append(mat[0])
                dataAprovados[str(o.cod_materia)] = DateTime('%s/%s/%s' % (d1.year(), d1.month(), d.dia_sessao))

lMaterias = []
for mat in lReqTramitando:
    lMaterias.append(mat)

for mat in lAprovados:
    lMaterias.append(mat)

ja_inclusos = {}

count = 1
autores = {}
for mat in lMaterias:
    autorias = context.zsql.autoria_obter_zsql(cod_materia=mat['cod_materia'])

    if len(autorias) < 5:
        #print "V "+str(count)+" - "+str(mat['cod_materia'])+' - '+str(mat['dat_apresentacao'])+' - '+ str( mat['dat_apresentacao'] >= d2) + ' - ' + str([a.cod_autor for a in autorias])

        count = count + 1

        for autoria in autorias:
            for autor in context.zsql.autor_obter_zsql(cod_autor=autoria['cod_autor']):
                if autor['des_tipo_autor'] == 'Parlamentar':
                    for parl in context.zsql.parlamentar_obter_zsql(cod_parlamentar=autor['cod_parlamentar']):

                        codigo = str(parl['nom_parlamentar'])

                        cod_materia = str(mat.cod_materia)

                        if codigo not in ja_inclusos:
                            ja_inclusos[codigo] = []

                        if cod_materia in ja_inclusos[codigo]:
                            continue

                        ja_inclusos[codigo].append(cod_materia)

                        if codigo in autores:
                            if cod_materia in dataAprovados:
                                if dataAprovados[cod_materia] >= d2:
                                    autores[codigo]['segQ'].append((mat['num_ident_basica'], cod_materia, True))
                                else:
                                    autores[codigo]['primQ'].append((mat['num_ident_basica'], cod_materia, True))
                            else:
                                if dataAtual >= d2:
                                    autores[codigo]['segQ'].append((mat['num_ident_basica'], cod_materia, False))
                                else:
                                    autores[codigo]['primQ'].append((mat['num_ident_basica'], cod_materia, False))
                        else:
                            item = {}
                            item['nome'] = codigo


                            item['primQ'] = []
                            item['segQ'] = []

                            if cod_materia in dataAprovados:
                                if dataAprovados[cod_materia] >= d2:
                                    item['segQ'] = [(mat['num_ident_basica'], cod_materia, True), ]
                                else:
                                    item['primQ'] = [(mat['num_ident_basica'], cod_materia, True), ]
                            else:
                                if dataAtual >= d2:
                                    item['segQ'] = [(mat['num_ident_basica'], cod_materia, False), ]
                                else:
                                    item['primQ'] = [(mat['num_ident_basica'], cod_materia, False), ]
                            autores[codigo] = item


#return printed



lResults = []
for k,v in autores.items():
    iResults = (k, v)
    v['primQ'].sort()
    v['segQ'].sort()

    ta1q = 0
    tt1q = 0 #total tramitando na primeira quinzena
    ta2q = 0
    tt2q = 0
    v['ta1q'] = 0 #total aprovado na primeira quinzena
    v['tt1q'] = 0 #total aprovado na primeira quinzena
    v['ta2q'] = 0 #total aprovado na primeira quinzena
    v['tt2q'] = 0 #total aprovado na primeira quinzena
    for item in v['primQ']:
        if item[2]:
            v['ta1q'] = v['ta1q'] + 1
        else:
            v['tt1q'] = v['tt1q'] + 1

    for item in v['segQ']:
        if item[2]:
            v['ta2q'] = v['ta2q'] + 1
        else:
            v['tt2q'] = v['tt2q'] + 1

    lResults.append(iResults)

return lResults
