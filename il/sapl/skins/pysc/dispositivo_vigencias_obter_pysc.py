## Script (Python) "dispositivo_vigencias_obter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_norma
##title=
##  

request = container.REQUEST
RESPONSE =  request.RESPONSE


result = []

listaIniVigencias = context.zsql.dispositivo_vigencias_obter_zsql(cod_norma=cod_norma, ini_fim='i')
listaFimVigencias = context.zsql.dispositivo_vigencias_obter_zsql(cod_norma=cod_norma, ini_fim='f')

agora = DateTime()
dataInicial = agora
dataFinal = agora
if len(listaFimVigencias) == 0 or listaFimVigencias[len(listaFimVigencias)-1].data < agora:
    dataFinal = agora
else:
    dataFinal = listaFimVigencias[len(listaFimVigencias)-1].data
    
    
for item in listaIniVigencias:
    ir = {}
    ir['data_ini'] = item.data
    if item.cod_norma_publicada != 0:
        ir['cod_norma_publicada'] = item.cod_norma_publicada
    else:
        ir['cod_norma_publicada'] = cod_norma
     
    
    
    ir['data_fim'] = dataFinal
    
    if len(result) > 0:
        result[len(result)-1]['data_fim'] = item.data
    elif item.data >= agora:
        return result
    else:
        dataInicial = item.data
        
    result.append(ir)
    
    
    
if len(result) == 0:
    return result
    
if len(result) == 1:
    result[0]['css'] = 'flexauto' 
    return result


dias = (dataFinal - dataInicial) * 1.6


for ir in result:
    ir['css'] = 'flex'+str(int(((ir['data_fim'] - ir['data_ini']) / dias) * 100))
        
#result[len(result)-1]['pc'] = 'flexauto'    
    
    
    
    

    

 


return result