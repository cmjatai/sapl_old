## Script (Python) "busca_analise_atalho_para_mat_norm_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pesquisa
##title=
## 

request = container.REQUEST
RESPONSE =  request.RESPONSE

session = request.SESSION 

listaPesq = session.get('listaPesq')

if listaPesq == None: 
    return []   
   
nResults = []
mResults = []
iResults = {}

tipoDeNormas = context.zsql.tipo_norma_juridica_obter_zsql(ind_excluido=0)
tipoDeMaterias = context.zsql.tipo_materia_legislativa_obter_zsql(ind_excluido=0)

for item in tipoDeNormas: 
    iResults = {}
    iResults['codigo'] = item['tip_norma']
    iResults['sigla'] = item['sgl_tipo_norma']
    iResults['titulo'] = item['des_tipo_norma']
    iResults['count'] = 0 
    iResults['mtnm'] = 'nm' 
    iResults['tipo'] = 2
    nResults.append(iResults)
    
for item in tipoDeMaterias: 
    iResults = {}
    iResults['codigo'] = item['tip_materia']
    iResults['sigla'] = item['sgl_tipo_materia']
    iResults['titulo'] = item['des_tipo_materia']
    iResults['count'] = 0 
    iResults['mtnm'] = 'mt' 
    iResults['tipo'] = 1
    mResults.append(iResults)

for it in listaPesq:
    if it['tipo'] == 1: #Mat�ria Legislativa 
        for item in mResults:
            if it['item']['tip_materia'] == item['codigo']:
                 item['count'] = item['count'] + 1
                 break 
        
    elif it['tipo'] == 2:
        for item in nResults:
            if it['item']['tipo_norma'] == item['codigo']:
                 item['count'] = item['count'] + 1
                 break 
        pass

lResults = nResults + mResults

for item in lResults[:]:
    if item['count'] == 0:
         lResults.remove(item)   


 




















if len(lResults) == 1:
    lResults[0]['codigo'] = ''
return lResults
 
 
 
 
 