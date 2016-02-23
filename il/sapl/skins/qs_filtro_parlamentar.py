## Script (Python) "qs_filtro_parlamentar"

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

r = []
item_results = {}


filtro = session.get('filtro')
if not filtro:
    filtro = qs_filtro()

legislaturas = context.zsql.legislatura_obter_zsql(ind_excluido=0)
legAtual = 0
for item in legislaturas:
    if DateTime() >= item.dat_inicio and DateTime() <= item.dat_fim:
        legAtual = item.num_legislatura

sessoesLegislativas = context.zsql.sessao_legislativa_obter_zsql(
    num_legislatura=legAtual, ind_excluido=0)
sessLegAtual = 0
for item in sessoesLegislativas:
    if DateTime() >= item.dat_inicio and DateTime() <= item.dat_fim:
        sessLegAtual = item.cod_sessao_leg


composicao = context.zsql.composicao_mesa_obter_zsql(
    cod_sessao_leg=sessLegAtual, ind_excluido=0)


parlamentares = []
pAntigos = []

if filtro['v'] != 0:
    lista_parlamentares = context.zsql.parlamentar_obter_zsql(
        cod_parlamentar=filtro['v'])

    if len(lista_parlamentares) > 0:
        p = {}
        p['codigo'] = lista_parlamentares[0].cod_parlamentar
        p['nome'] = lista_parlamentares[0].nom_parlamentar

        p['cargo'] = 'Vereador' if lista_parlamentares[0].sex_parlamentar != 'F' else 'Vereadora'
        p['cargo'] = (p['cargo'] + ' na '+str(
            lista_parlamentares[0].num_legislatura)+'ª'.decode("utf-8")+' Legislatura').encode()

        p['num_legislatura'] = lista_parlamentares[0].num_legislatura
        p['legAtual'] = legAtual
        p['ativo'] = 1 if lista_parlamentares[0].ind_ativo == 1 else 0
        p['img_absolute_url'] = ''
        parlamentares.append(p)

if not parlamentares:
    for item in composicao:

        bdParlamentar = context.zsql.parlamentar_obter_zsql(
            cod_parlamentar=item.cod_parlamentar, ind_excluido=0)
        bdCargo = context.zsql.cargo_mesa_obter_zsql(
            cod_cargo=item.cod_cargo, ind_excluido=0)
        p = {}
        p['codigo'] = bdParlamentar[0].cod_parlamentar
        p['nome'] = bdParlamentar[0].nom_parlamentar
        p['cargo'] = bdCargo[0].des_cargo
        p['ativo'] = 1
        p['img_absolute_url'] = ''
        parlamentares.append(p)
else:
    for item in composicao:
        if item.cod_parlamentar == parlamentares[0]['codigo']:
            bdCargo = context.zsql.cargo_mesa_obter_zsql(
                cod_cargo=item.cod_cargo, ind_excluido=0)
            p['cargo'] = bdCargo[0].des_cargo


if filtro['v'] == 0:
    lista_parlamentares = context.zsql.parlamentar_obter_zsql(
        num_legislatura=legAtual, ind_excluido=0)
    for item in lista_parlamentares:

        if item.ind_ativo == 0:
            continue

        match = False
        for ip in parlamentares:
            if ip['codigo'] == item.cod_parlamentar:
                match = True
                break

        if match:
            continue

        p = {}
        p['codigo'] = item.cod_parlamentar
        p['nome'] = item.nom_parlamentar

        p['cargo'] = 'Vereador'

        if item.sex_parlamentar == 'F':
            p['cargo'] = 'Vereadora'

        if legAtual != item.num_legislatura:
            p['cargo'] = (p['cargo'] + ' na '+str(item.num_legislatura)+'ª'.decode("utf-8")+' Legislatura').encode()
        p['legAtual'] = legAtual
        p['ativo'] = 1 if item.ind_ativo == 1 else 0
        p['img_absolute_url'] = ''

        parlamentares.append(p)


    if len(filtro['q']) > 0:
        lista_parlamentares = context.zsql.parlamentar_obter_zsql(ind_excluido=0)

        for item in lista_parlamentares:
            match = True
            for q in filtro['q']:
                q = q.replace('"', '').lower()
                if q not in item.nom_parlamentar.lower() and q not in item.nom_completo.lower():
                    match = False
                if not match:
                    break
            if not match:
                continue

            for ip in parlamentares:
                if ip['codigo'] == item.cod_parlamentar:
                    match = False
                    break
            if not match:
                continue

            for ip in pAntigos:
                if ip['codigo'] == item.cod_parlamentar:
                    match = False
                    break
            if not match:
                continue

            p = {}
            p['codigo'] = item.cod_parlamentar
            p['nome'] = item.nom_parlamentar

            p['cargo'] = 'Vereador' if item.sex_parlamentar != 'F' else 'Vereadora'
            p['cargo'] = (p['cargo'] + ' na '+str(
                item.num_legislatura)+'ª'.decode("utf-8")+' Legislatura').encode()

            p['num_legislatura'] = item.num_legislatura
            p['legAtual'] = legAtual
            p['ativo'] = 1 if item.ind_ativo == 1 else 0
            p['img_absolute_url'] = ''

            pAntigos.append(p)

        pAntigos = {v['codigo']: v for v in pAntigos}.values()

        pAntigos = map(lambda x: (x['num_legislatura'], x), pAntigos)
        pAntigos.sort()
        pAntigos = [v for k, v in pAntigos]

        pAntigos.reverse()

listaFotos = context.sapl_documentos.parlamentar.fotos.objectValues()

for item in parlamentares[:]:
    for iFoto in listaFotos:
        if item['codigo']+'_'+context.sapl_documentos.parlamentar.fotos.nom_documento == iFoto.getId():
            item['img_absolute_url'] = iFoto.absolute_url()

for item in pAntigos[:]:
    for iFoto in listaFotos:
        if item['codigo']+'_'+context.sapl_documentos.parlamentar.fotos.nom_documento == iFoto.getId():
            item['img_absolute_url'] = iFoto.absolute_url()

item_results['parlamentares'] = parlamentares
item_results['p_antigos'] = pAntigos
item_results['tipo_materias'] = []
r.append(item_results)

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

    tm = item_results['tipo_materias']

    tm = {v['tipo_materia']: v for v in tm}.values()
    tm = map(lambda x: (x['qtde_materia'], x), tm)
    tm.sort()
    tm = [v for k, v in tm]
    tm.reverse()

    item_results['tipo_materias'] = tm

return r
