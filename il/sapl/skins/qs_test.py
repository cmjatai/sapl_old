## Script (Python) "qs_test"
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



normas = context.zsql.norma_juridica_obter_zsql()

print len(normas)
for norma in list(normas)[:51]:
    #context.zsql.norma_juridica_atualizar_zsql()

    num_diario = None
    try:
        num_diario = int(norma.des_veiculo_publicacao)
    except:
        continue

    params = {'num_norma': int(num_diario)}
    diario = container.sapl_documentos.diario_oficial.Catalog(params)

    data_diario = context.ZopeTime(int(diario[0]['LastModified'])).strftime('%d/%m/%Y')


    print norma.cod_norma, norma.dat_publicacao, data_diario, norma.dat_publicacao == data_diario


    """context.zsql.norma_juridica_atualizar_zsql(
        cod_norma=int(norma.cod_norma),
        tip_norma=norma.tip_norma_sel,
        num_norma=norma.num_norma,
        ano_norma=norma.ano_norma,
        dat_publicacao=context.pysc.data_converter_pysc(data=context.ZopeTime(int(diario[0]['LastModified'])).strftime('%d/%m/%Y'))

        tip_esfera_federacao   = norma.tip_esfera_federacao,
        cod_materia            = norma.cod_materia,
        dat_norma              = pysc.data_converter_pysc(data=norma.dat_norma),
        des_veiculo_publicacao = norma.des_veiculo_publicacao,
        num_pag_inicio_publ    = norma.num_pag_inicio_publ,
        num_pag_fim_publ       = norma.num_pag_fim_publ,
        txt_ementa             = norma.txt_ementa,
        txt_indexacao          = norma.txt_indexacao,
        txt_observacao         = norma.txt_observacao,
        ind_complemento        = norma.ind_complemento,
        cod_assunto            = norma.cod_assunto,
        cod_situacao           = norma.cod_situacao
        )"""


    #print norma.num_norma,  norma.dat_norma, norma.dat_publicacao, context.ZopeTime(int(diario['LastModified'])).strftime('%d/%m/%Y')
    #print '"%s"' % norma.des_veiculo_publicacao


return printed


users = context.acl_users.getUserNames()
print users
return printed



data = DateTime()
print data.minute()
return printed




lMaterias = context.zsql.materia_pesquisar_zsql(ano_ident_basica=2016)

data = DateTime()
for itMat in lMaterias:
    print data, itMat.dat_apresentacao, (data - itMat.dat_apresentacao)


return printed














objetos = context.sapl.sapl_documentos.norma_juridica.objectValues()
count = 1
for o in objetos:
    obj_id = str(o.id)
    if 'Catalog' in obj_id:
        continue

    if o.content_type in ['application/pdf', 'text/html']:
        continue

    print count, o.id, o.content_type
    #o.manage_changeProperties(content_type='application/pdf')
    #o.manage_permission("View", [], 1)
    count += 1


return printed
