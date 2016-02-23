## Script (Python) "busca_materias_normas_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pesquisa
##title=
##

request = container.REQUEST
response = request.RESPONSE
session = request.SESSION

if str(request['AUTHENTICATED_USER']) == 'Anonymous User':
    if session.get('listaPesq') and request['page'] != 1:
        lResults = session.get('listaPesq')
        return lResults

pseudoBusca = False

def pd(key, value, prefixo=True):
    result = ''
    if prefixo:
        result = key+'-'*100
        result += '\n'
        result += str(value)
        result += '\n'
    if same_type(value, 0):
        result += str(value)
    if same_type(value, ''):
        result += value
    elif same_type(value, []):
        for v in value:
            result += pd('', v, prefixo=False)
    elif same_type(value, {}):
        for k, v in value.items():
            result += k+': '+pd(k, v, prefixo=False)
    return result+'\n'

if 'debug' in request:
    print pd('pesquisa', pesquisa)

context.zsql.termo_busca_incluir_zsql(
        termo=pesquisa,
        remote_addr=request['HTTP_X_FORWARDED_FOR'],
        http_user_agent=request['HTTP_USER_AGENT'],
        user=request['AUTHENTICATED_USER'],
        query_string=request['QUERY_STRING'])


""" Separação de texto e números no campo de pesquisa """
pesqBase = context.pysc.stop_word_remove_pysc(pesquisa.strip())
if len(pesqBase) < 2:
    pesqBase = ''

termos = pesqBase.split(' ')

numeros = []  # pesquisa norma por numeros
palavras = []  # pesquisa norma por Termos
for termo in termos:
    if termo.lower() == 'and' or termo.lower() == 'or':
        continue
    try:
        # separa numeros
        num = int(termo)
        numeros.append(num)
    except:
        if termo:
            palavras.append(termo)

if 'debug' in request:
    print pd('termos', termos)
    print pd('numeros', numeros)
    print pd('palavras', palavras)

lNormas = None


expressao = ''
expr = []
expr_num = []
expr_geral = []
expr_html = []

norms_html = []
norms_geral = []
diarios_oficiais = []

lResults = []
item_results = {}

if 'debug' in request:
    print pd('user', request['AUTHENTICATED_USER'])
if str(request['AUTHENTICATED_USER']):
    if 'cod_parlamentar' in request and len(request.cod_parlamentar) != 0:
        """ Se a pesquisa citar um parlamentar, obrigatoriamente
        não é feita pesquisa em normas"""
        pass
    else:
        for num in numeros:
            value = str(num)
            if num >= 1000:
                expr_num.append(
                    '(%s* OR %s* OR *%s* OR *%s* OR *%s OR *%s)' % (
                        value,
                        '{:,}'.format(num).replace(',', '.'),
                        value,
                        '{:,}'.format(num).replace(',', '.'),
                        value,
                        '{:,}'.format(num).replace(',', '.'),
                        ))
            elif num > 0:
                expr_num.append('*'+value+'* ')
        if 'debug' in request:
            print pd('expr_num', expr_num)

        # analisa termos na pesquisa para pesquisas em arquivos não html
        for pl in palavras:
            expr_geral.append(
                '(%s* OR *%s* OR *%s)' % (
                    pl, pl, pl))
        if 'debug' in request:
            print pd('expr_geral', expr_geral)

        # analisa termos na pesquisa para pesquisas em arquivos html
        autOld = "ãâáàäêéèëîíìïõôóòöûúùüçÃÂÁÀÄÊÉÈËÎÍÌÏÕÔÓÒÖÛÚÙÜÇ"
        if 'debug' in request:
            print pd('autOld', autOld)

        plHtml = []

        pnCount = 0
        for pl in palavras:
            plHtml.append(palavras[pnCount])
            for letra in autOld:
                plHtml[pnCount] = plHtml[pnCount].replace(letra, '')
            pnCount = pnCount + 1

        if 'debug' in request:
            print pd('plHtml', plHtml)

        for pl in plHtml:
            expr_html.append(
                '(%s* OR *%s* OR *%s)' % (
                    pl, pl, pl))

        if 'debug' in request:
            print pd('expr_html', expr_html)

        if 'mtnm' not in request or request.mtnm == '' or request.mtnm == 'nm':
            """ Se a pesquisa incluir normas jurídicas """

            # get catalogo para html
            param_html = {
                'sort_on':     'LastModified',
                'sort_order':  'descending',
                'ContentType': 'text/html'}

            if 'nm_tip_norma' in request and len(request.nm_tip_norma) > 0:
                param_html['tipo_norma'] = int(request.nm_tip_norma)

            if expr_num and expr_html:
                param_html['PrincipiaSearchSource'] = \
                        '%(expr_num)s AND %(expr_html)s' % {
                        'expr_num': ' AND '.join(expr_num),
                        'expr_html': ' AND '.join(expr_html)}
            elif expr_num and not expr_html:
                param_html['PrincipiaSearchSource'] = ' AND '.join(expr_num)
            elif expr_html and not expr_num:
                param_html['PrincipiaSearchSource'] = ' AND '.join(expr_html)
            norms_html = context.sapl_documentos.norma_juridica.Catalog(param_html)
            if 'debug' in request:
                print pd('norms_html', len(norms_html))

            # get catalogo para geral
            prm_geral = {
                'sort_on':     'LastModified',
                'sort_order':  'descending'}
            if 'nm_tip_norma' in request and len(request.nm_tip_norma) > 0:
                prm_geral['tipo_norma'] = int(request.nm_tip_norma)

            if expr_num and expr_geral:
                prm_geral['PrincipiaSearchSource'] = \
                        '%(expr_num)s AND %(expr_geral)s' % {
                        'expr_num': ' AND '.join(expr_num),
                        'expr_geral': ' AND '.join(expr_geral)}
            elif expr_num and not expr_geral:
                prm_geral['PrincipiaSearchSource'] = ' AND '.join(expr_num)
            elif expr_geral and not expr_num:
                prm_geral['PrincipiaSearchSource'] = ' AND '.join(expr_geral)
            norms_geral = context.sapl_documentos.norma_juridica.Catalog(prm_geral)
            if 'debug' in request:
                print pd('norms_geral', len(norms_geral))

            # join dos catálogos
            for it in norms_html:
                item_results = {}
                item_results['data'] = it.LastModified
                item_results['codigo'] = it.num_norma
                item_results['id'] = it.cod_norma
                item_results['item'] = {}
                item_results['item']['codNorma'] = it.cod_norma
                item_results['item']['tipo_norma'] = it.tipo_norma
                item_results['tipo'] = 2
                lResults.append(item_results)

            for it in norms_geral:
                item_results = {}
                item_results['data'] = it.LastModified
                item_results['codigo'] = it.num_norma
                item_results['id'] = it.cod_norma
                item_results['item'] = {}
                item_results['item']['codNorma'] = it.cod_norma
                item_results['item']['tipo_norma'] = it.tipo_norma
                item_results['tipo'] = 2
                lResults.append(item_results)

        if 'mtnm' not in request or request.mtnm == '' or request.mtnm == 'dof':
            # get catalogo para diarios_oficiais
            if 'ntnm' not in request or 'ntnm' in request and request.ntnm == '':
                prm_dof = {
                    'sort_on':     'LastModified',
                    'sort_order':  'descending',
                    'ContentType': 'application/pdf'}

                if expr_num and expr_geral:
                    prm_dof['PrincipiaSearchSource'] = \
                            '%(expr_num)s AND %(expr_geral)s' % {
                            'expr_num': ' AND '.join(expr_num),
                            'expr_geral': ' AND '.join(expr_geral)}
                elif expr_num and not expr_geral:
                    prm_dof['PrincipiaSearchSource'] = ' AND '.join(expr_num)
                elif expr_geral and not expr_num:
                    prm_dof['PrincipiaSearchSource'] = ' AND '.join(expr_geral)


                if 'debug' in request:
                    print pd('prm_dof', prm_dof)

                diarios_oficiais = context.sapl_documentos.\
                    diario_oficial.Catalog(prm_dof)
                if 'debug' in request:
                    print pd('diarios_oficiais', len(diarios_oficiais))

            for it in diarios_oficiais:
                item_results = {}
                item_results['data'] = it.LastModified
                item_results['codigo'] = it.num_norma
                item_results['id'] = it.cod_norma
                item_results['ano_norma'] = it.ano_norma
                item_results['txt_epigrafe'] = it.txt_epigrafe.decode('iso-8859-15')
                item_results['item'] = {}
                item_results['item']['codNorma'] = it.cod_norma
                item_results['item']['tipo_norma'] = it.tipo_norma
                item_results['tipo'] = 3
                lResults.append(item_results)

        lResults = {
            ('%s-%s' % (v['tipo'], v['id'])): v for v in lResults}.values()

        lResults = map(lambda x: (x['data'], x), lResults)
        lResults.sort()
        lResults = [v for k, v in lResults]

        lResults.reverse()

        if 'debug' in request:
            print pd('lResults', len(lResults))

    if 'mtnm' not in request or request.mtnm == '' or request.mtnm == 'mt':
        """  """

        param = {
            'tip_id_basica':  request.tip_materia,
            'des_assunto':     ' '.join(palavras),
            'cod_autor':       request.cod_parlamentar,
            'des_tipo_autor':  request.lst_tip_autor,
            'rd_ordem':        '4',
            'itens_privados':  request.itens_privados}

        if len(request.mt_tramitando) > 0:
            param['ind_tramitacao'] = request.mt_tramitando

        if len(request.mt_status) > 0:
            param['cod_status'] = request.mt_status

        if len(numeros) > 0:
            param['num_ident_basica'] = str(numeros[0])

        lMaterias = context.zsql.materia_pesquisar_zsql(param)

        point = 0
        pointPrivado = 0

        if 'debug' in request:
            print pd('lMaterias', len(lMaterias))

        if lMaterias:
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

                if point < len(lResults):
                    while lResults[point]['data'] >= item_results['data']:
                        point = point + 1
                        if point >= len(lResults):
                            break
                    if point < len(lResults):
                        lResults.insert(point, item_results)
                    else:
                        lResults.append(item_results)
                else:
                    lResults.append(item_results)

    point = 0
    pointInsert = 0
    if len(numeros) > 0:
        while True:
            if point >= len(lResults):
                break
            if lResults[point]['codigo'] == numeros[0]:
                item_results = lResults[point]
                lResults.pop(point)
                lResults.insert(pointInsert, item_results)
                pointInsert = pointInsert + 1
            point = point + 1

    if 'debug' in request:
        print pd('lResults', len(lResults))
        return printed


    session.set('listaPesq', lResults)


    if 'debug' in request:
        return printed

    return lResults







else:
    if len(request.cod_parlamentar) != 0:
        """ Se a pesquisa citar um parlamentar, obrigatoriamente
        não é feita pesquisa em normas"""
        pass
    elif request.mtnm == '' or request.mtnm == 'nm':
        """ Se a pesquisa incluir normas jurídicas """

        for num in numeros:
            value = str(num)
            if num >= 1000:
                expr.append('(*%s OR *%s*)' % (
                    value,
                    '{:,}'.format(num).replace(',', '.')
                    ))
            elif num > 0:
                expr.append('*'+value+'* ')










        expressao = ' AND '.join(expr)



        if len(pesqBase) > 0:
            #analisa numeros na pesquisa
            it = iter(numeros)
            num = 0
            try:
                num = it.next()
            except StopIteration:
                pass
            while True:
                value = str(num)
                if num >= 1000:
                    expressao = expressao + '( *'+value+'* OR *'+value[:-3]+'.'+value[-3:]+'* ) '
                elif num >= 1:
                    expressao = expressao + '*'+value+'* '

                try:
                    num = it.next()
                    expressao = expressao + 'AND '
                except StopIteration:
                    break


            pnConverte = []

            #analisa termos na pesquisa
            pnCount = 0
            for nt in palavras:

                pnConverte.append(palavras[pnCount])
                autOld ="ãâáàäêéèëîíìïõôóòöûúùüçÃÂÁÀÄÊÉÈËÎÍÌÏÕÔÓÒÖÛÚÙÜÇ".decode("utf-8")
                for letra in autOld:
                    pnConverte[pnCount] = pnConverte[pnCount].replace(letra, '')

                pnCount = pnCount + 1

            it = iter(pnConverte)
            value = ''
            try:
                value = it.next()
            except StopIteration:
                pass

            if len(value) > 0 and len(expressao) > 0:
                expressao = expressao + 'AND '

            while len(value) > 0:

                expressao += '( *'+value+'* OR '
                expressao += value+'* OR '
                expressao += value+' ) '

                try:
                    value = it.next()
                    expressao = expressao + 'AND '
                except StopIteration:
                    break

            expressao = expressao.strip()


        if 'debug' in request:
            print pd('expressao2', expressao)

        if request['AUTHENTICATED_USER'].has_role(['Operador']) == 1:
            param ={'sort_on':     'LastModified',
                    'sort_order':  'descending',
                    'ContentType': 'text/html'}
        else:
            param ={'sort_on':     'LastModified',
                    'sort_order':  'descending',
                    'ContentType': 'text/html'}

        if len(expressao) > 0:
            param['PrincipiaSearchSource'] = expressao

        if len(request.nm_tip_norma) > 0:
            param['tipo_norma'] = int(request.nm_tip_norma)

        if 'debug' in request and request['debug'] == '1':
            return 'debug: "' + str(param) + '"\n\nconfirmação do conteúdo de PrincipiaSearchSource: "'+param['PrincipiaSearchSource']+'"'


        lNormas = context.sapl_documentos.norma_juridica.Catalog( param )

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
                'des_assunto':     ' '.join(palavras),
                'cod_autor':       request.cod_parlamentar,
                'des_tipo_autor':  request.lst_tip_autor,
                'rd_ordem':        '4',
                'itens_privados':  request.itens_privados}

        if len(request.mt_tramitando) > 0:
            param['ind_tramitacao'] = request.mt_tramitando

        if len(request.mt_status) > 0:
            param['cod_status'] = request.mt_status

        if len(numeros) > 0:
            param['num_ident_basica'] = str(numeros[0])

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
    if len(numeros) > 0:
        while True:
            if point >= len(lResults):
                break
            if lResults[point]['codigo'] == numeros[0]:
                item_results = lResults[point]
                lResults.pop(point)
                lResults.insert(pointInsert, item_results)
                pointInsert = pointInsert + 1
            point = point + 1

    session.set('listaPesq', lResults)


    if 'debug' in request:
        return printed

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
