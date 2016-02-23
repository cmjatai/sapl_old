## Script (Python) "get_geolocation_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cep
##title=
##

from Products.CMFCore.utils import getToolByName

st = getToolByName(context, 'portal_sapl')
if len(cep.split('-')) == 1:
    cep = cep[:5] + '-' + cep[5:]
localidade = context.sapl_documentos.props_sapl.cod_localidade
cidade = context.zsql.localidade_obter_zsql(cod_localidade=localidade)
if cidade:
    cidade = cidade[0].nom_localidade

geolocations = st.get_geolocations(cidade, cep)
if not geolocations:
    return ['','']
else:
    return geolocations
