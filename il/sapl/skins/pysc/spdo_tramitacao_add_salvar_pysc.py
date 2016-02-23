## Script (Python) "spdo_tramitacao_add_salvar_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_materia,cod_unid_tram_dest,txt_tramitacao
##title=
##

import simplejson as json
from Products.CMFCore.utils import getToolByName

request = context.REQUEST
form = request.form

st = getToolByName(context, 'portal_sapl')
end_spdo = context.sapl_documentos.props_sapl.end_spdo
end_add_protocolo = end_spdo + '/@@ws-tramite'

id_usuario_sapl = request['AUTHENTICATED_USER'].getId()
id_usuario_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_login_spdo
senha_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_senha_spdo

protocolo = context.zsql.materia_obter_zsql(cod_materia=cod_materia)[0].num_protocolo_spdo
area = context.zsql.unidade_tramitacao_obter_zsql(cod_unid_tramitacao=cod_unid_tram_dest)[0].txt_unid_spdo

dados = {
    'area': area,
    'despacho': txt_tramitacao,
    'protocolo': protocolo
}

dados = json.dumps(dados)
ret = st.call_ws_nofile(end_add_protocolo, id_usuario_spdo, senha_spdo, dados)
return True
