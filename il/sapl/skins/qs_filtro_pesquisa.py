## Script (Python) "busca_materias_normas_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

request = container.REQUEST
response = request.RESPONSE
session = request.SESSION

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


filtro = session.get('filtro')
if not filtro:
    filtro = qs_filtro()

if str(request['AUTHENTICATED_USER']) != 'dev':

    if str(request['AUTHENTICATED_USER']) == 'Anonymous User':
        if session.get('listaPesq') and filtro['p'] != 1:
            lResults = session.get('listaPesq')
            return lResults

    context.zsql.termo_busca_incluir_zsql(
            termo=' '.join(filtro['q']),
            remote_addr=request['HTTP_X_FORWARDED_FOR'],
            http_user_agent=request['HTTP_USER_AGENT'],
            user=request['AUTHENTICATED_USER'],
            query_string=str(filtro))

    numeros = []  # pesquisa norma por numeros
    palavras = []  # pesquisa norma por Termos
    for termo in filtro['q']:
        if termo.lower() == 'and' or termo.lower() == 'or':
            continue
        try:
            # separa numeros
            num = int(termo)
            numeros.append(num)
        except:
            if termo:
                palavras.append(termo)

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

    if filtro['v'] == 0 and (len(filtro['tc']) == 0 or 'tn' in filtro['tc'] or 'ta' in filtro['tc'] or 'td' in filtro['tc']):

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

        # analisa termos na pesquisa para pesquisas em arquivos não html
        for pl in palavras:
            if '"' not in pl:
                expr_geral.append(
                    '(%s* OR *%s* OR *%s)' % (
                        pl, pl, pl))
            else:
                expr_geral.append(pl)

        # analisa termos na pesquisa para pesquisas em arquivos html
        autOld = "ãâáàäêéèëîíìïõôóòöûúùüçÃÂÁÀÄÊÉÈËÎÍÌÏÕÔÓÒÖÛÚÙÜÇ"

        plHtml = []

        pnCount = 0
        for pl in palavras:
            plHtml.append(palavras[pnCount])
            for letra in autOld:
                plHtml[pnCount] = plHtml[pnCount].replace(letra, '')
            pnCount = pnCount + 1

        for pl in plHtml:
            if '"' not in pl:
                expr_html.append(
                    '(%s* OR *%s* OR *%s)' % (
                        pl, pl, pl))
            else:
                expr_html.append(pl)

        if not filtro['tc'] or 'tn' in filtro['tc'] or 'ta' in filtro['tc'] or filtro['tn']:
            """ Se a pesquisa incluir normas jurídicas
            - Se não existir filtro tc - tipo de conteúdo
            - Se existir filtro tc e tn estiver nele
            - Se houver ao menos uma seleção direta de tn - tipo de norma
            """

            tns = ([0, ] if 0 not in filtro['tn'] else []) + filtro['tn']

            if 'ta' in filtro['tc']:
                tns.append(27)

            for tn in tns:
                # get catalogo para html
                param_html = {
                    'sort_on':     'LastModified',
                    'sort_order':  'descending',
                    'ContentType': 'text/html'}

                if ((tn == 0 and len(tns) > 2 and 27 in tns) or (tn == 0 and len(tns) > 1 and 27 not in tns)):
                    continue

                if tn:
                    param_html['tipo_norma'] = tn


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

                # get catalogo para geral
                prm_geral = {
                    'sort_on':     'LastModified',
                    'sort_order':  'descending'}

                if tn:
                    prm_geral['tipo_norma'] = tn

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

                # join dos catálogos
                for it in norms_html:
                    if it.tipo_norma == 27 and len(filtro['tc']) and 'ta' not in filtro['tc']:
                        continue
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
                    if it.tipo_norma == 27 and len(filtro['tc']) and 'ta' not in filtro['tc']:
                        continue
                    item_results = {}
                    item_results['data'] = it.LastModified
                    item_results['codigo'] = it.num_norma
                    item_results['id'] = it.cod_norma
                    item_results['item'] = {}
                    item_results['item']['codNorma'] = it.cod_norma
                    item_results['item']['tipo_norma'] = it.tipo_norma
                    item_results['tipo'] = 2
                    lResults.append(item_results)

        if not filtro['tc'] or 'td' in filtro['tc']:
            # get catalogo para diarios_oficiais
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

            diarios_oficiais = context.sapl_documentos.\
                diario_oficial.Catalog(prm_dof)

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

    if filtro['v'] or (not filtro['tc'] or 'tm' in filtro['tc']):
        """  """
        for pl in palavras:
            pl.replace('"', '')


        tms = ([0, ] if 0 not in filtro['tm'] else []) + filtro['tm']
        tss = ([0, ] if 0 not in filtro['ts'] else []) + filtro['ts']

        for tm in tms:


            param = {
                'rd_ordem':        '4',
                'itens_privados':  request.itens_privados,
            }

            if not tm and len(tms) > 1:
                continue

            if tm:
                param['tip_id_basica'] = tm

            if filtro['v']:
                param['des_tipo_autor'] = 'Parlamentar'
                param['cod_autor'] = filtro['v']


            if palavras:
                param['des_assunto'] = ' '.join(palavras)

            if filtro['tr']:
                param['ind_tramitacao'] = filtro['tr'][0]

            if len(numeros) > 0:
                param['num_ident_basica'] = str(numeros[0])

            for ts in tss:

                if not ts and len(tss) > 1:
                    continue

                if ts:
                    param['cod_status'] = ts

                lMaterias = context.zsql.materia_pesquisar_zsql(param)

                point = 0
                pointPrivado = 0

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

                        if itMat.ind_publico == 0 and itMat.ind_tramitacao:
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



    if str(request['AUTHENTICATED_USER']) == 'Anonymous User':
        if filtro['p'] == 1:
            session.set('listaPesq', lResults)


    return lResults
else:
















    if str(request['AUTHENTICATED_USER']) == 'Anonymous User':
        if session.get('listaPesq') and filtro['p'] != 1:
            lResults = session.get('listaPesq')
            return lResults

    context.zsql.termo_busca_incluir_zsql(
            termo=' '.join(filtro['q']),
            remote_addr=request['HTTP_X_FORWARDED_FOR'],
            http_user_agent=request['HTTP_USER_AGENT'],
            user=request['AUTHENTICATED_USER'],
            query_string=str(filtro))

    numeros = []  # pesquisa norma por numeros
    palavras = []  # pesquisa norma por Termos
    for termo in filtro['q']:
        if termo.lower() == 'and' or termo.lower() == 'or':
            continue
        try:
            # separa numeros
            num = int(termo)
            numeros.append(num)
        except:
            if termo:
                palavras.append(termo)

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

    flagAno = False

    filtroVazio = not filtro['v'] and not filtro['tc'] and not filtro['q']

    if filtro['v'] == 0 and (len(filtro['tc']) == 0 or 'tn' in filtro['tc'] or 'ta' in filtro['tc'] or 'td' in filtro['tc']):

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

        # analisa termos na pesquisa para pesquisas em arquivos não html
        for pl in palavras:
            if '"' not in pl:
                expr_geral.append(
                    '(%s* OR *%s* OR *%s)' % (
                        pl, pl, pl))
            else:
                expr_geral.append(pl)

        # analisa termos na pesquisa para pesquisas em arquivos html
        autOld = "ãâáàäêéèëîíìïõôóòöûúùüçÃÂÁÀÄÊÉÈËÎÍÌÏÕÔÓÒÖÛÚÙÜÇ"

        plHtml = []

        pnCount = 0
        for pl in palavras:
            plHtml.append(palavras[pnCount])
            for letra in autOld:
                plHtml[pnCount] = plHtml[pnCount].replace(letra, '')
            pnCount = pnCount + 1

        for pl in plHtml:
            if '"' not in pl:
                expr_html.append(
                    '(%s* OR *%s* OR *%s)' % (
                        pl, pl, pl))
            else:
                expr_html.append(pl)

        if not filtro['tc'] or 'tn' in filtro['tc'] or 'ta' in filtro['tc'] or filtro['tn']:
            """ Se a pesquisa incluir normas jurídicas
            - Se não existir filtro tc - tipo de conteúdo
            - Se existir filtro tc e tn estiver nele
            - Se houver ao menos uma seleção direta de tn - tipo de norma
            """

            tns = ([0, ] if 0 not in filtro['tn'] else []) + filtro['tn']

            if 'ta' in filtro['tc']:
                tns.append(27)

            for tn in tns:
                # get catalogo para html
                param_html = {
                    'sort_on':     'LastModified',
                    'sort_order':  'descending',
                    'ContentType': 'text/html'}

                if not tn and len(tns) > 1:
                    continue

                if tn:
                    param_html['tipo_norma'] = tn


                if expr_num and expr_html:
                    param_html['PrincipiaSearchSource'] = \
                            '%(expr_num)s AND %(expr_html)s' % {
                            'expr_num': ' AND '.join(expr_num),
                            'expr_html': ' AND '.join(expr_html)}
                elif expr_num and not expr_html:
                    param_html['PrincipiaSearchSource'] = ' AND '.join(expr_num)
                elif expr_html and not expr_num:
                    param_html['PrincipiaSearchSource'] = ' AND '.join(expr_html)

                if filtroVazio:
                    param_html['sort_limit'] = 10
                    norms_html = context.sapl_documentos.norma_juridica.Catalog(param_html)
                else:
                    norms_html = context.sapl_documentos.norma_juridica.Catalog(param_html)

                # get catalogo para geral
                prm_geral = {
                    'sort_on':     'LastModified',
                    'sort_order':  'descending'}

                if tn:
                    prm_geral['tipo_norma'] = tn

                if expr_num and expr_geral:
                    prm_geral['PrincipiaSearchSource'] = \
                            '%(expr_num)s AND %(expr_geral)s' % {
                            'expr_num': ' AND '.join(expr_num),
                            'expr_geral': ' AND '.join(expr_geral)}
                elif expr_num and not expr_geral:
                    prm_geral['PrincipiaSearchSource'] = ' AND '.join(expr_num)
                elif expr_geral and not expr_num:
                    prm_geral['PrincipiaSearchSource'] = ' AND '.join(expr_geral)

                if filtroVazio:
                    prm_geral['sort_limit'] = 10
                    norms_geral = context.sapl_documentos.norma_juridica.Catalog(prm_geral)
                else:
                    norms_geral = context.sapl_documentos.norma_juridica.Catalog(prm_geral)

                # join dos catálogos
                for it in norms_html:
                    item_results = {}
                    item_results['data'] = it.LastModified
                    item_results['codigo'] = it.num_norma
                    item_results['id'] = it.cod_norma
                    item_results['item'] = {}
                    item_results['ano_norma'] = it.ano_norma
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
                    item_results['ano_norma'] = it.ano_norma
                    item_results['item']['codNorma'] = it.cod_norma
                    item_results['item']['tipo_norma'] = it.tipo_norma
                    item_results['tipo'] = 2
                    lResults.append(item_results)

        if not filtro['tc'] or 'td' in filtro['tc']:
            # get catalogo para diarios_oficiais
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

            if filtroVazio:
                prm_dof['sort_limit'] = 10
                diarios_oficiais = context.sapl_documentos.\
                    diario_oficial.Catalog(prm_dof)
            else:
                diarios_oficiais = context.sapl_documentos.\
                    diario_oficial.Catalog(prm_dof)

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

    if filtro['v'] or (not filtro['tc'] or 'tm' in filtro['tc']):
        """  """
        for pl in palavras:
            pl.replace('"', '')


        tms = ([0, ] if 0 not in filtro['tm'] else []) + filtro['tm']
        tss = ([0, ] if 0 not in filtro['ts'] else []) + filtro['ts']

        if not numeros:
            numeros.insert(0, 0)

        for i in (1, 2, 3):
            for num in numeros:
                """
                primeira iteração - pesquisa com o número do documento
                    aceita se numero não for zero
                segunda iteração - pesquisa com o número no texto do documento

                terceira iteração - pesquisa com número no ano do documento
                    faz apenas se num for entre 1950 e 2030
                """

                if i != 2 and not num:
                    continue

                if i == 3 and (num < 1950 or num > 2030):
                    continue

                for tm in tms:
                    param = {
                        'rd_ordem':        '4',
                        'itens_privados':  request.itens_privados,
                    }

                    if not tm and len(tms) > 1:
                        continue

                    if tm:
                        param['tip_id_basica'] = tm

                    if filtro['v']:
                        param['des_tipo_autor'] = 'Parlamentar'
                        param['cod_autor'] = filtro['v']

                    if filtro['tr']:
                        param['ind_tramitacao'] = filtro['tr'][0]

                    if i == 1:
                        param['num_ident_basica'] = str(num)
                    elif i == 3:
                        param['ano_ident_basica'] = str(num)
                    elif i == 2:
                        if palavras and not num and len(numeros) > 1:
                            param['des_assunto'] = '%s %s' % (
                                ' '.join(palavras),
                                ' '.join([str(item) for item in numeros[1:]]))
                        elif palavras:
                            param['des_assunto'] = ' '.join(palavras)


                    for ts in tss:

                        if not ts and len(tss) > 1:
                            continue

                        if ts:
                            param['cod_status'] = ts

                        if filtroVazio:
                            lMaterias = context.zsql.materia_pesquisar_zsql_limited(param)
                        else:
                            lMaterias = context.zsql.materia_pesquisar_zsql(param)

                        point = 0
                        pointPrivado = 0

                        count = 0
                        if lMaterias:
                            for itMat in lMaterias:
                                count += 1
                                if count == 10:
                                    break
                                item_results = {}
                                item_results['data'] = itMat.dat_apresentacao.millis() / 1000
                                item_results['codigo'] = itMat['num_ident_basica']
                                item_results['id'] = itMat['cod_materia']
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

    lResults = {
        ('%s-%s' % (v['tipo'], v['id'])): v for v in lResults}.values()

    lResults = map(lambda x: (x['data'], x), lResults)
    lResults.sort()
    lResults = [v for k, v in lResults]

    lResults.reverse()




    session.set('listaPesq', lResults)


    return lResults
