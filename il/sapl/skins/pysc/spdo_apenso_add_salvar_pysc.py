## Script (Python) "spdo_protocolo_add_salvar_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=materia_principal, materias, add=1
##title=
##

import simplejson as json
from Products.CMFCore.utils import getToolByName
from ZTUtils import make_query

request = context.REQUEST
form = request.form

st = getToolByName(context, 'portal_sapl')
end_spdo = context.sapl_documentos.props_sapl.end_spdo
end_add_apenso = end_spdo + '/@@ws-add-apenso'

id_usuario_sapl = request['AUTHENTICATED_USER'].getId()
id_usuario_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_login_spdo
senha_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_senha_spdo

protocolo = context.zsql.materia_obter_zsql(cod_materia=materia_principal)[0].num_protocolo_spdo

apensos = []
if isinstance(materias, str):
    materias = [materias]
for materia in materias:
    apenso = context.zsql.materia_obter_zsql(cod_materia=materia)[0].num_protocolo_spdo
    apensos.append(apenso)

dados = {
    'protocolo': protocolo,
    'apensos': apensos,
    'add': add
}

dados = json.dumps(dados)
ret = st.call_ws_nofile(end_add_apenso, id_usuario_spdo, senha_spdo, dados)

if ret == 'null':
    return True
else:
    return False
