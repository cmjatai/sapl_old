## Script (Python) "spdo_pesquisar_protocolo_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

import simplejson as json
from Products.CMFCore.utils import getToolByName
from ZTUtils import make_query

request = context.REQUEST
form = request.form

st = getToolByName(context, 'portal_sapl')
end_spdo = context.sapl_documentos.props_sapl.end_spdo
end_search_protocolo = end_spdo + '/@@ws-search-protocolo'

dados = {}

origem = form.get('txt_origem', None)
destino = form.get('txt_destino', None)
assunto = form.get('txt_assunto', None)
situacao = form.get('lst_situacao', None)
tipodocumento = form.get('lst_tip_documento', None)
tipoprotocolo = form.get('lst_tip_protocolo', None)
inativo = form.get('txt_inativo', None)
area = form.get('lst_area', None)

if origem:
    dados['origem'] = unicode(origem)

if destino:
    dados['destino'] = unicode(destino)

if assunto:
    dados['assunto'] = unicode(assunto)

if situacao:
    dados['situacao'] = unicode(situacao)

if tipodocumento:
    dados['tipodocumento'] = unicode(tipodocumento)

if tipoprotocolo:
    dados['tipoprotocolo'] = unicode(tipoprotocolo)

if inativo:
    dados['inativo'] = unicode(inativo)

if area:
    dados['area'] = unicode(area)

dados = json.dumps(dados)

ret = st.call_ws_search(end_search_protocolo, dados)

# nao finalizado

# return context.REQUEST.RESPONSE.redirect(url)
