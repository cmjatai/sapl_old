## Script (Python) "protocolo_conta_requerimentos_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= ano_base, mes_base
##title=
##
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
RESPONSE =  request.RESPONSE

lResults = []
iResults = {}


dataAtual = DateTime()
dia1MesAtual =  DateTime(str(dataAtual.year())+'/'+str(dataAtual.month())+'/01')
diaIniUser = dia1MesAtual
try:
   diaIniUser = DateTime(ano_base+'/'+mes_base+'/01')
except:
   diaIniUser = dia1MesAtual


lReqTramitando = []
if diaIniUser == dia1MesAtual:
   param = {'tip_id_basica':  3, 'ind_tramitacao':  '1'}
   lReqTramitando = context.zsql.materia_pesquisar_zsql(param)

diaFimUser = diaIniUser + 35
diaFimUser = DateTime(str(diaFimUser.year())+'/'+str(diaFimUser.month())+'/01') - 1
dia2Quiz =  DateTime(str(diaFimUser.year())+'/'+str(diaFimUser.month())+'/16')


param = {'tip_id_basica':  3, 'cod_status': '55' , 'dat_ini_tramitacao': diaIniUser , 'dat_fim_tramitacao': diaFimUser }
lReqEncaminhados = context.zsql.materia_pesquisar_zsql(param)

lMaterias = []
for mat in lReqTramitando:
    lMaterias.append(mat)


for mat in lReqEncaminhados:
    lMaterias.append(mat)



count = 1
autores = {}
for mat in lMaterias:
    autorias = context.zsql.autoria_obter_zsql(cod_materia=mat['cod_materia'])


    if len(autorias) < 5:
        #try:
        #    print "T "+str(count)+" - "+str(mat['cod_materia'])+' - '+str(mat['dat_tramitacao'])+' - '+ str( mat['dat_tramitacao'] >= dia2Quiz)
        #except:
        #    print "V "+str(count)+" - "+str(mat['cod_materia'])+' - '+str(mat['dat_apresentacao'])+' - '+ str( mat['dat_apresentacao'] >= dia2Quiz)

        #count = count + 1

        for autoria in autorias:
            for autor in context.zsql.autor_obter_zsql(cod_autor=autoria['cod_autor']):
                if autor['des_tipo_autor'] == 'Parlamentar':
                    for parl in context.zsql.parlamentar_obter_zsql(cod_parlamentar=autor['cod_parlamentar']):

                        if 'debug' in request and request['debug'] == '0':
                            print str(mat['num_ident_basica']) + ' - ' + str(parl['nom_parlamentar'])

                        codigo = str(parl['nom_parlamentar'])
                        #print codigo
                        if codigo in autores:
                            try:
                                if mat['dat_tramitacao'] >= dia2Quiz:
                                    autores[codigo]['segQ'] = autores[codigo]['segQ'] + 1
                                else:
                                    autores[codigo]['primQ'] = autores[codigo]['primQ'] + 1
                            except:
                                if mat['dat_apresentacao'] >= dia2Quiz or dataAtual >= dia2Quiz:
                                    autores[codigo]['segQ'] = autores[codigo]['segQ'] + 1
                                else:
                                    autores[codigo]['primQ'] = autores[codigo]['primQ'] + 1
                        else:
                            item = {}
                            item['nome'] = parl['nom_parlamentar']

                            item['primQ'] = 0
                            item['segQ'] = 0
                            try:
                                if mat['dat_tramitacao'] >= dia2Quiz:
                                    item['segQ'] = 1
                                else:
                                    item['primQ'] = 1
                            except:
                                if mat['dat_apresentacao'] >= dia2Quiz or dataAtual >= dia2Quiz:
                                    item['segQ'] = 1
                                else:
                                    item['primQ'] = 1
                            autores[codigo] = item



#return printed
lResults = []
for k,v in autores.items():
    iResults = (k, v)
    lResults.append(iResults)

if 'debug' in request and request['debug'] == '0':
    return printed

return lResults
