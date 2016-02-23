## Script (Python) "busca_materias_normas_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pesquisa
##title=
## 

from Products.AdvancedQuery import And, Or, Eq, Ge, In

request = container.REQUEST
RESPONSE =  request.RESPONSE

session = request.SESSION 

    
#if session.get('listaPesq') != None and request['page'] != 1: 
#    lResults = session.get('listaPesq') 
#    return lResults    
  
  
lResults = []
item_results = {}

#pesquisa = pesquisa.decode('utf-8')

if 'debug' in request and request['debug'] == '0':
    return 'debug: "'+pesquisa+'"' 
 
lNormas = None
npn = ''  #nova pesquisa em normas

pnNums = [] #pesquisa norma por numeros
pnTermos = [] #pesquisa norma por Termos


""" Separação de texto e números no campo de pesquisa"""
pesqBase = context.pysc.stop_word_remove_pysc(pesquisa.strip())

if len(pesqBase) < 2:
    pesqBase = ''

pn = pesqBase.split(' ') #pesquisa em normas
it = iter(pn)
value = ''
try:
    value = it.next() 
except StopIteration:
    pass   
    
while len(value) > 0:

    if value.lower() == 'and' or value.lower() == 'or':
        pass
    elif len(value) > 0:
        try:
            #separa numeros
            num = int(value)
            pnNums.append(num)
        except:
            pnTermos.append(value)

    try:
        value = it.next() 
    except StopIteration:
        break   
 
if len(request.cod_parlamentar) != 0:    
    """ Se a pesquisa citar um parlamentar, obrigatoriamente não é feita pesquisa em normas"""
    pass

elif request.mtnm == '' or request.mtnm == 'nm': 
    """ Se a pesquisa incluir normas jurídicas """
    
    if len(pesqBase) > 0:          
        
        #analisa numeros na pesquisa               
        it = iter(pnNums)
        num = 0
        try:
            num = it.next() 
        except StopIteration:
            pass   
        while True:
            value = str(num)
            if num >= 1000:
                npn = npn + "( '%"+value+"%' OR '%"+value[:-3]+"."+value[-3:]+"%' ) "
            elif num >= 1:
                npn = npn + "'%"+value+"%' "
                
            try:
                num = it.next()       
                npn = npn + 'AND '
            except StopIteration:
                break   
                                   
        
        
        #analisa termos na pesquisa            
        it = iter(pnTermos)
        value = ''
        try:
            value = it.next() 
        except StopIteration:
            pass   
            
        if len(value) > 0 and len(npn) > 0:
            npn = npn + 'AND '
            
        while len(value) > 0:
                
            #npn += "( *"+value+"* OR "
            #npn += value+"* OR "
            #npn += value+" ) "
            
            npn += " "+ value+" "
            
            try:
                value = it.next()    
                npn = npn + 'AND '
            except StopIteration:
                break      
                     
        npn = npn.strip()
     
    
    param ={'sort_on':     'LastModified',
            'sort_order':  'descending',
            'ContentType': 'text/html'}
    
    if len(npn) > 0:
        param['PrincipiaSearchSource'] = npn
   
    if len(request.nm_tip_norma) > 0:
        param['tipo_norma'] = int(request.nm_tip_norma)  
        
    if 'debug' in request and request['debug'] == '1':
        return 'debug: "' + str(param) + '"\n\nconfirmação do conteúdo de PrincipiaSearchSource: "'+param['PrincipiaSearchSource']+'"'
        
    query = Eq('PrincipiaSearchSource', npn)
    
     
    lNormas = context.sapl_documentos.norma_juridica.Catalog.evalAdvancedQuery( query  )
                   # thesaurus=('txng.thesaurus.de', 'txng.thesaurus.de-special')
    if 'debug' in request and request['debug'] == '5':
        return len(lNormas)
        
    if lNormas != None:
        for itNorma in lNormas:
             item_results = {}
             item_results['data'] = itNorma.LastModified
             item_results['codigo'] = itNorma.num_norma 
             item_results['item'] = {} 
             item_results['item']['codNorma'] = itNorma.cod_norma 
             item_results['item']['tipo_norma'] = itNorma.tipo_norma
             item_results['tipo'] = 2 
        
             lResults.append(item_results)  
     
if request.mtnm == '' or request.mtnm == 'mt': 
    """  """

    param = {'tip_id_basica':  request.tip_materia,
            'des_assunto':     ' '.join(pnTermos),
            'cod_autor':       request.cod_parlamentar,
            'des_tipo_autor':  request.lst_tip_autor,
            'rd_ordem':        '4',
            'itens_privados':  request.itens_privados}
            
    if len(request.mt_tramitando) > 0:
        param['ind_tramitacao'] = request.mt_tramitando
            
    if len(request.mt_status) > 0:
        param['cod_status'] = request.mt_status
        
    if len(pnNums) > 0:
        param['num_ident_basica'] = str(pnNums[0])
             
    if 'debug' in request and request['debug'] == '2':
        return param
    #num_ident_basica="" ano_ident_basica="" num_protocolo="" 

    lMaterias = context.zsql.materia_pesquisar_zsql(param)

    if 'debug' in request and request['debug'] == '3':
        return lMaterias
    #return len(lMaterias) 

    point = 0 
    pointPrivado = 0 
    
    if lMaterias != None:
        for itMat in lMaterias:
             item_results = {}
             item_results['data'] = itMat.dat_apresentacao.millis() / 1000
             item_results['codigo'] = itMat['num_ident_basica']
             item_results['tipo'] = 1 
             item_results['item'] = {}
             item_results['item']['ind_publico'] = itMat['ind_publico']
             item_results['item']['cod_materia'] = itMat['cod_materia']
             item_results['item']['des_tipo_materia'] = itMat['des_tipo_materia']
             item_results['item']['num_ident_basica'] = itMat['num_ident_basica']
             item_results['item']['ano_ident_basica'] = itMat['ano_ident_basica']
             item_results['item']['txt_ementa'] = itMat['txt_ementa']
             item_results['item']['dat_apresentacao'] = itMat['dat_apresentacao'] 
             item_results['item']['sgl_tipo_materia'] = itMat['sgl_tipo_materia']
             item_results['item']['tip_materia'] = itMat['tip_materia'] 
             
             if itMat.ind_publico == 0:
                 lResults.insert(pointPrivado, item_results)
                 pointPrivado = pointPrivado + 1
                 point = point + 1
                 continue
                 
             
             if 'debug' in request and request['debug'] == '4':
                return item_results
            
            
             if point < len(lResults):
                 while lResults[point]['data'] >= item_results['data']:
                     point = point + 1
                     if point >= len(lResults):
                        break;
                 if point < len(lResults):
                     lResults.insert(point, item_results)
                 else:         
                     lResults.append(item_results)
             else:         
                 lResults.append(item_results) 

                 
point = 0     
pointInsert = 0
if len(pnNums) > 0:
    while True:
        if point >= len(lResults):
            break
        if lResults[point]['codigo'] == pnNums[0]:
            item_results = lResults[point]
            lResults.pop(point)
            lResults.insert(pointInsert, item_results)
            pointInsert = pointInsert + 1 
        point = point + 1 
           
session.set('listaPesq', lResults)


return lResults
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
lista_results = []

#ATENCAO: Parametro norma_or_materia: 1-materia legislativa, 2-norma juridica

#Verifica se a palavra informada para pesquisa possui somente espacos
if txt_texto.isspace() == False:

	lista_catalog = []
	lista_DB = []
	
	#Teste para saber se pesquisara norma ou materia
	if norma_or_materia == 1:

		#Chama o Catalog do Zope para realizar a busca textual no ZODB
		lista_catalog = context.sapl.sapl_documentos.materia.Catalog(PrincipiaSearchSource=txt_texto)

		#Utiliza este script para realizar a busca no DB de todos os registros do tipo de materia
		lista_DB = context.zsql.materia_obter_zsql(tip_id_basica=lst_tipo)
	
	else:
		#Chama o Catalog do Zope para realizar a busca textual no ZODB
		lista_catalog = context.sapl.sapl_documentos.norma_juridica.Catalog(PrincipiaSearchSource=txt_texto)

		#Utiliza este script para realizar a busca no DB de todos os registros do tipo de materia
		lista_DB = context.zsql.norma_juridica_obter_zsql(tip_norma=lst_tipo)

	#Verifica se lista_catalog e lista_DB estao vazia
	if ((lista_catalog != None) and (lista_DB != None)):

		#Percorre a lista obtida do Banco de Dados
		for elem_DB in lista_DB:

			#Percorre a lista obtida do zcatalog
			for elem_catalog in lista_catalog:

                #cria o id para comparar com os registros obtidos do zcatalog
				id_pesq = str(elem_DB[0]) + '_texto_integral' 
				
				#Verifica se existe o registro com o id obtido do zcatalog
				if id_pesq == elem_catalog.id:
					lista_result.append(elem_DB)


return lista_result
