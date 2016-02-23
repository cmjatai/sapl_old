## Script (Python) "votacao_salvar_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_parlamentar, cod_ordem, cod_materia, tip_resultado_votacao, ind_votacao_iniciada=1, expediente=0, txt_observacao="", vot_parlamentar=""
##title=
##

from Products.CMFCore.utils import getToolByName

membership_tool = getToolByName(context, 'portal_membership')
member = membership_tool.getAuthenticatedMember()
login = member.getUserName()

dic = {}
votos_sim = []
votos_nao = []
votos_abstencao = []
votos_nao_votou = []
#cod_vot=None
if vot_parlamentar is not None and vot_parlamentar != '[]':
    for voto in vot_parlamentar:
        if voto=='Sim':
            votos_sim.append(voto)

    for voto in vot_parlamentar:
        if voto=='Não':
            votos_nao.append(voto)

    for voto in vot_parlamentar:
        if voto=='Abstenção':
            votos_abstencao.append(voto)

    for voto in vot_parlamentar:
        if voto=='Não Votou':
            votos_nao_votou.append(voto)

#for n in range(len(cod_parlamentar)):
#    dic[cod_parlamentar[n]]=vot_parlamentar[n]
    dic = dict(zip(cod_parlamentar, vot_parlamentar))
else:
    vot_parlamentar = []

#votacao=context.zsql.votacao_obter_zsql(cod_votacao=cod_votacao,cod_ordem=cod_ordem,cod_materia=cod_materia,ind_excluido=0)
votacao=context.zsql.votacao_obter_zsql(cod_ordem=cod_ordem,cod_materia=cod_materia, ind_excluido=0)
materia=context.zsql.materia_obter_zsql(cod_materia=cod_materia, ind_excluido=0)[0]

try:
    tip_resultado = context.zsql.tipo_resultado_votacao_obter_zsql(tip_resultado_votacao=tip_resultado_votacao)[0].nom_resultado
    ind_excluido = 0
except IndexError:
    tip_resultado = '-1'
    ind_excluido = 1
try:
    cod_sessao_plen = context.zsql.ordem_dia_obter_zsql(cod_ordem=cod_ordem)[0].cod_sessao_plen
except IndexError:
    cod_sessao_plen = context.zsql.expediente_materia_obter_zsql(cod_ordem=cod_ordem)[0].cod_sessao_plen

if not expediente:
    presenca = context.zsql.presenca_ordem_dia_obter_zsql(cod_sessao_plen=cod_sessao_plen, ind_excluido=0)
else:
    presenca = context.zsql.presenca_sessao_obter_zsql(cod_sessao_plen=cod_sessao_plen, ind_excluido=0)

if votos_nao_votou:
    nao_votou = len(votos_nao_votou)
else:
    nao_votou = len(presenca) - len(vot_parlamentar)

#for v in votacao:
#    cod_vot=v.cod_votacao
try:
    cod_votacao = votacao[0].cod_votacao
except IndexError:
    cod_votacao = None
if cod_votacao is None:
    context.zsql.votacao_incluir_zsql(
        num_votos_sim=len(votos_sim),
        num_votos_nao=len(votos_nao),
        num_abstencao=len(votos_abstencao),
        num_nao_votou=nao_votou,
        txt_observacao=txt_observacao,
        cod_ordem=cod_ordem,
        cod_materia=cod_materia,
        tip_resultado_votacao=tip_resultado_votacao
    )

    context.pysc.sessao_plenaria_log_pysc(
        cod_sessao_plen = cod_sessao_plen,
        txt_acao = 'inclusão de votação',
        txt_mensagem = 'Votação da matéria ' + materia.sgl_tipo_materia + ' - ' + materia.des_tipo_materia + ' ' +
                       str(materia.num_ident_basica) + '/' + str(materia.ano_ident_basica) +
                       ' incluída na sessão plenária. Resultado: ' + str(len(votos_sim)) + ' votos sim, ' +
                       str(len(votos_nao)) + ' votos não e ' + str(len(votos_abstencao)) + ' votos de abstenção. Tipo do resultado: ' + tip_resultado
    )

else:
    context.zsql.votacao_atualizar_zsql(
        cod_votacao=cod_votacao,
        num_votos_sim=len(votos_sim),
        num_votos_nao=len(votos_nao),
        num_abstencao=len(votos_abstencao),
        num_nao_votou=nao_votou,
        txt_observacao=txt_observacao,
        cod_ordem=cod_ordem,
        cod_materia=cod_materia,
        tip_resultado_votacao=tip_resultado_votacao
    )

    context.pysc.sessao_plenaria_log_pysc(
        cod_sessao_plen = cod_sessao_plen,
        txt_acao = 'atualização de votação',
        txt_mensagem = 'Votação da matéria ' + materia.sgl_tipo_materia + ' - ' + materia.des_tipo_materia + ' ' +
                       str(materia.num_ident_basica) + '/' + str(materia.ano_ident_basica) +
                       ' atualizada na sessão plenária. Resultado: ' + str(len(votos_sim)) + ' votos sim, ' +
                       str(len(votos_nao)) + ' votos não e ' + str(len(votos_abstencao)) + ' votos de abstenção. Tipo do resultado: ' + tip_resultado
    )

parlamentares=[]
if cod_votacao is not None:
    votacao_parlamentares=context.zsql.votacao_parlamentar_obter_zsql(
        cod_votacao=cod_votacao,
        ind_excluido=0
    )
    if not votacao_parlamentares:
        votacao_parlamentares=context.zsql.votacao_parlamentar_obter_zsql(
        cod_votacao=cod_votacao,
        ind_excluido=1
    )
    for parlamentar in votacao_parlamentares:
        parlamentares.append(str(parlamentar.cod_parlamentar))
else:
    votacao_incluida=context.zsql.votacao_incluida_obter_zsql()
    cod_votacao = votacao_incluida[0].cod_votacao
    #for v in votacao_incluida:
    #    cod_votacao=v.cod_votacao

if vot_parlamentar is not None and vot_parlamentar != '[]':
    for p in cod_parlamentar:
        if p not in parlamentares:
            context.zsql.votacao_parlamentar_incluir_zsql(
                cod_votacao=cod_votacao,
                cod_parlamentar=p,
                txt_login=login,
                vot_parlamentar=dic.get(p)
            )
        else:
            try:
                orig_login = context.zsql.votacao_parlamentar_obter_zsql(cod_votacao=cod_votacao,
                                                                         ind_excluido=0,
                                                                         cod_parlamentar=p)[0].txt_login
            except IndexError:
                orig_login = context.zsql.votacao_parlamentar_obter_zsql(cod_votacao=cod_votacao,
                                                                         ind_excluido=1,
                                                                         cod_parlamentar=p)[0].txt_login
            context.zsql.votacao_parlamentar_atualizar_zsql(
                cod_votacao=cod_votacao,
                cod_parlamentar=p,
                vot_parlamentar=dic.get(p),
                txt_login=orig_login,
                ind_excluido=ind_excluido
            )

if ind_votacao_iniciada == 0 and not expediente:
    context.zsql.votacao_iniciar_zsql(
        cod_ordem=cod_ordem,
        ind_votacao_iniciada=ind_votacao_iniciada
    )

if ind_votacao_iniciada == 0 and expediente:
    context.zsql.votacao_expediente_iniciar_zsql(
        cod_ordem=cod_ordem,
        ind_votacao_iniciada= ind_votacao_iniciada
    )

return 1
