## Script (Python) "pesquisa_inteligente_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pesquisa
##title=
##
request = container.REQUEST
RESPONSE = request.RESPONSE




def jsonToString(result):
    rStr = str(result).decode('unicode-escape').split("'")
    rStr = '"'.join(rStr)
    rStr = rStr.replace('False', '"False"')
    rStr = rStr.replace('True', '"True"')
    rStr = rStr.replace('<', '"<')
    rStr = rStr.replace('>', '>"')
    rStr = rStr.replace(': u"', ': "')
    return rStr

results = []
item_results = {}

termos = context.pysc.stop_word_remove_pysc(pesquisa.strip()).split(' ')
pesquisa_new = context.pysc.stop_word_remove_pysc(pesquisa.strip())

legislaturas = context.zsql.legislatura_obter_zsql(ind_excluido=0)
legAtual = 0
for item in legislaturas:
    if DateTime() >= item.dat_inicio and DateTime() <= item.dat_fim:
        legAtual = item.num_legislatura

sessoesLegislativas = context.zsql.sessao_legislativa_obter_zsql(
    num_legislatura = legAtual, ind_excluido=0)
sessLegAtual = 0
for item in sessoesLegislativas:
    if DateTime() >= item.dat_inicio and DateTime() <= item.dat_fim:
        sessLegAtual = item.cod_sessao_leg

parlamentares = []
composicao = context.zsql.composicao_mesa_obter_zsql(cod_sessao_leg=sessLegAtual, ind_excluido=0)


if 'debug' in request and request['debug'] == '0':
    return '-'+str(len(list(composicao)))  # jsonToString(results)




for item in composicao:
     bdParlamentar = context.zsql.parlamentar_obter_zsql(cod_parlamentar=item.cod_parlamentar, ind_excluido=0)
     bdCargo = context.zsql.cargo_mesa_obter_zsql(cod_cargo=item.cod_cargo, ind_excluido=0)
     p = {}
     p['codigo'] = bdParlamentar[0].cod_parlamentar
     p['nome'] = bdParlamentar[0].nom_parlamentar
     p['cargo'] = bdCargo[0].des_cargo
     p['ativo'] = len(termos)
     p['img_absolute_url'] = ''

     parlamentares.append(p)



lista_parlamentares = []
if 'cod_parlamentar' in request and request['cod_parlamentar'] != '':
    lista_parlamentares = context.zsql.parlamentar_obter_zsql(cod_parlamentar=request.cod_parlamentar, ind_excluido=0)
else:
    lista_parlamentares = context.zsql.parlamentar_obter_zsql(num_legislatura=legAtual, ind_excluido=0)

for item in lista_parlamentares:
    if item.nom_parlamentar.find('Todos') != -1:
        continue

    match = None
    for ip in parlamentares:
        if ip['codigo'] == item.cod_parlamentar:
           match = ip
           break

    if match != None:
        continue

    p = {}
    p['codigo'] =item.cod_parlamentar
    p['nome'] = item.nom_parlamentar

    p['cargo'] = 'Vereador'

    if item.sex_parlamentar == 'F':
        p['cargo'] = 'Vereadora'


    if legAtual != item.num_legislatura:
        p['cargo'] = (p['cargo'] + ' na '+str(item.num_legislatura)+'ª'.decode("utf-8")+' Legislatura').encode()
    p['legAtual'] = legAtual
    if item.ind_ativo == 0:
        p['ativo'] = 0
    else:
        p['ativo'] = len(termos)
    p['img_absolute_url'] = ''

    parlamentares.append(p)


listaFotos = context.sapl_documentos.parlamentar.fotos.objectValues()
for item in parlamentares[:]:

    for iFoto in listaFotos:
        if item['codigo']+'_'+context.sapl_documentos.parlamentar.fotos.nom_documento == iFoto.getId():
            item['img_absolute_url'] = iFoto.absolute_url()




for item in parlamentares[:]:
    if 'cod_parlamentar' in request and len(request.cod_parlamentar) > 0:
        if request.cod_parlamentar != item['codigo']:
           parlamentares.remove(item)


item_results['pesquisa_new'] = pesquisa_new
item_results['parlamentares'] = parlamentares
item_results['tipo_materias'] = []
results.append(item_results)

if len(parlamentares) == 1:

    listaProposicoes = context.zsql.parlamentar_obter_proposicao_zsql(cod_parlamentar=parlamentares[0]['codigo'], grp_ano='0', pri_autor='0')

    for item in listaProposicoes:

        tm = {}
        tm['tipo_materia'] = item.tip_materia
        tm['sgl_tipo_materia'] = item.sgl_tipo_materia
        tm['des_tipo_materia_plural'] = item.des_tipo_materia_plural
        tm['qtde_materia'] = int(item.qtde)
        tm['cod_parlamentar'] = parlamentares[0]['codigo']
        item_results['tipo_materias'].append(tm)





#return printed


return results











return jsonToString(results)

lista_results

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
