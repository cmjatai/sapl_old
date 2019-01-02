## Script (Python) "get_diario_oficial"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=num_norma, num_lei
##title=
##
request = container.REQUEST
response = request.RESPONSE
session = request.SESSION

try:
    params = {
        'num_norma': int(num_norma)}
    diario = container.sapl_documentos.diario_oficial.Catalog(params)[0]

    diario_com_lei = []
    if num_lei:
        num_lei = '{:,}'.format(num_lei).replace(',', '.')
        params['PrincipiaSearchSource'] = '"lei nº 999" OR "lei n.º 999" OR "lei n.° 999" OR "lei n° 999" OR "Lei Complementar n° 999" OR "Lei Complementar n.° 999" OR "Lei Complementar nº 999" OR "Lei Complementar n.º 999"'

        params['PrincipiaSearchSource'] = params['PrincipiaSearchSource'].replace('999', num_lei)

        diario_com_lei = container.sapl_documentos.diario_oficial.Catalog(params)

    return {
        'titulo': 'Diário Oficial Eletrônico do Município de Jataí - GO'
        ' - nº %s/%s' % (diario['num_norma'], diario['ano_norma']),
        'codigo': diario['cod_norma'],
        'numero': diario['num_norma'],
        'ano': diario['ano_norma'],
        'data': context.ZopeTime(int(diario['LastModified'])).strftime('%d/%m/%Y'),
        'lei_no_diario': len(diario_com_lei or []) != 0
    }
except:
    return {}














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
