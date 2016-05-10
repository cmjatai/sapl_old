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
