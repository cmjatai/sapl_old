## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions

from Products.CMFCore.utils import getToolByName
import time

REQUEST = context.REQUEST
membership_tool = getToolByName(context, 'portal_membership')
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')

    return state.set(status='failure')

member = membership_tool.getAuthenticatedMember()
username = member.getUserName()

endereco_ip = REQUEST.form.get('endereco_ip', None)
endereco_mac = REQUEST.form.get('endereco_mac', None)

tempo_expira = time.time() + 5 * 3600 # expira o cookie em cinco horas
expira = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(tempo_expira))

# grava cookie com os dados do ip e do mac
REQUEST.RESPONSE.setCookie('endereco_ip', endereco_ip, path='/')
REQUEST.RESPONSE.setCookie('endereco_mac', endereco_mac, path='/')

# verifica se existe alguma sessao iniciada
sessao = context.zsql.sessao_plenaria_obter_zsql(ind_iniciada = 1)

#verifica se o login pertence a algum parlamentar
parlamentar = context.zsql.parlamentar_obter_zsql(txt_login=username)

# verifica se se existe recomposicao de presencas
if sessao:
    cod_registro_sessao_pre = context.zsql.recomposicao_presencas_sessao_verificar_ultima_aberta_zsql(cod_sessao_plen = sessao[0].cod_sessao_plen)[0].cod_registro_pre
    if cod_registro_sessao_pre:
        sessao_aberta = True
    else:
        sessao_aberta = False
else:
    sessao_aberta = False

# verifica se existe recomposicao de presencas
if sessao:
    cod_registro_ordem_pre = context.zsql.recomposicao_presencas_ordem_verificar_ultima_aberta_zsql(cod_sessao_plen = sessao[0].cod_sessao_plen)[0].cod_registro_pre
    if cod_registro_ordem_pre:
        ordem_aberta = True
    else:
        ordem_aberta = False
else:
    ordem_aberta = False

if len(sessao) > 0 and len(parlamentar) > 0 and 'Parlamentar' in member.getRoles():
    if context.pysc.rede_sapl_pysc():
        cod_sessao = sessao[0].cod_sessao_plen
        dat_sessao = context.pysc.data_converter_pysc(data=sessao[0].dat_inicio_sessao)
        cod_parlamentar = parlamentar[0].cod_parlamentar
        if sessao_aberta:
            context.pysc.presenca_sessao_pysc(
                cod_parlamentar,
                cod_sessao,
                endereco_ip,
                endereco_mac,
                cod_perfil='parlamentar',
                login=True
            )
            context.zsql.sessao_plenaria_log_incluir_zsql(
                txt_login = username,
                txt_ip = endereco_ip,
                txt_mac = endereco_mac,
                txt_acao = 'registro de presença sessão',
                txt_mensagem = 'O usuário ' + username + ' registrou presença no expediente da sessão plenária usando o equipamento com o IP ' + endereco_ip,
            )
            state.set(status='expediente_iniciado')
        if ordem_aberta:
            context.pysc.presenca_ordem_dia_pysc(
                cod_sessao,
                cod_parlamentar,
                dat_sessao,
                endereco_ip,
                endereco_mac,
                cod_perfil='parlamentar',
                login=True
            )
            context.zsql.sessao_plenaria_log_incluir_zsql(
                txt_login = username,
                txt_ip = endereco_ip,
                txt_mac = endereco_mac,
                txt_acao = 'registro de presença ordem',
                txt_mensagem = 'O usuário ' + username + ' registrou presença na ordem do dia usando o equipamento com o IP ' + endereco_ip,
            )
            state.set(status='ordem_dia_iniciada')
    else:
        context.zsql.sessao_plenaria_log_incluir_zsql(
            txt_login = username,
            txt_ip = endereco_ip,
            txt_mac = endereco_mac,
            txt_acao = 'registro de presena',
            txt_mensagem = 'O usuário ' + username + ' não conseguiu registrar presença no sistema usando o equipamento com o IP ' + endereco_ip + ' por estar fora da rede.',
        )
        state.set(status='fora_rede')

elif len(parlamentar) == 0:
    context.zsql.sessao_plenaria_log_incluir_zsql(
        txt_login = username,
        txt_ip = endereco_ip,
        txt_mac = endereco_mac,
        txt_acao = 'login no sapl',
        txt_mensagem = 'O usuário ' + username + ' efetuou login no sistema usando o equipamento com o IP ' + endereco_ip,
    )
    state.set(status='nao_parlamentar')

elif len(sessao) == 0:
    context.zsql.sessao_plenaria_log_incluir_zsql(
        txt_login = username,
        txt_ip = endereco_ip,
        txt_mac = endereco_mac,
        txt_acao = 'registro de presença',
        txt_mensagem = 'O usuário ' + username + ' não conseguiu registrar presença no sistema usando o equipamento com o IP ' + endereco_ip + ' pois não existe sessão iniciada.',
    )
    state.set(status='sessao_nao_iniciada')

elif aberta is False:
    context.zsql.sessao_plenaria_log_incluir_zsql(
        txt_login = username,
        txt_ip = endereco_ip,
        txt_mac = endereco_mac,
        txt_acao = 'registro de presença',
        txt_mensagem = 'O usuário ' + username + ' não conseguiu registrar presença no sistema usando o equipamento com o IP ' + endereco_ip + ' pois não existe votação aberta.',
    )
    state.set(status='votacao_fechada')

return state
