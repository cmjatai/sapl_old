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

prm_dof = {
    'sort_on':     'LastModified',
    'sort_order':  'descending',
    'ContentType': 'application/pdf'}

diarios_oficiais = context.sapl_documentos.\
    diario_oficial.Catalog(prm_dof)

flag_dof = range(674)


for it in diarios_oficiais:

    if it.num_norma in flag_dof:
        flag_dof.remove(it.num_norma)
    # flag_dof[it.num_norma] = 0


return flag_dof


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
