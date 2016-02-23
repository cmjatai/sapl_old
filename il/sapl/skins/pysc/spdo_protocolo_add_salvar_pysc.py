## Script (Python) "spdo_protocolo_add_salvar_pysc"
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
end_add_protocolo = end_spdo + '/@@ws-add-protocolo'

id_usuario_sapl = request['AUTHENTICATED_USER'].getId()
id_usuario_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_login_spdo
senha_spdo = context.zsql.spdo_users_obter_zsql(txt_login_sapl=id_usuario_sapl)[0].txt_senha_spdo

origens = form['lst_origem']
origens = [{'email': origens.split(';')[0], 'nome': origens.split(';')[1]}]

destinos = form['lst_destino']
destinos = [{'email': destinos.split(';')[0], 'nome': destinos.split(';')[1]}]

assunto = form['txt_assunto']
observacao = form['txa_txt_observacao']

data = form['txt_dat_documento']
data_emissao = data[6:] + '-' + data[3:5] + '-' + data[0:2]

situacao = form['lst_situacao']

tipodocumento = form['lst_tip_documento']

tipoprotocolo = form['lst_tip_protocolo']

files = form['files']

dados = {
    'origens': origens,
    'destinos': destinos,
    'assunto': assunto,
    'observacao': observacao,
    'numero_documento': '',
    'data_emissao': data_emissao,
    'situacao': situacao,
    'tipodocumento': tipodocumento,
    'tipoprotocolo': tipoprotocolo
}

anexos = []

for f in files:
    anexos.append({
        'src': f.name,
        'dst': '/tmp/' + f.filename
    })

anexos = st.get_anexos(*anexos)
dados = json.dumps(dados)
ret = st.call_ws(end_add_protocolo, id_usuario_spdo, senha_spdo, dados, anexos)
num_protocolo_spdo = ret.split()[1]
params = context.REQUEST.form
params['num_protocolo_spdo'] = num_protocolo_spdo
query = make_query(params)

url = context.cadastros.protocolo.protocolo_legislativo_salvar_proc.absolute_url() + '?' + query

return context.REQUEST.RESPONSE.redirect(url)
