## Script (Python)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_sessao_plen,cod_expediente,txt_expediente
##title=
##

dic={}

# verifica se existe apenas um expediente e caso não exista ele faz um laço para construir um dicionário
if len(cod_expediente) > 1:
    for n in range(len(cod_expediente)):
        dic[cod_expediente[n]]=txt_expediente[n]

else:
    dic[cod_expediente]=txt_expediente
    
for cod in cod_expediente:
    expedientes=context.zsql.expediente_obter_zsql(cod_sessao_plen=cod_sessao_plen,ind_excluido=0)
expediente=[]
nomes_expediente={}
for e in expedientes:
    expediente.append(str(e.cod_expediente))
    nom_expediente = context.zsql.tipo_expediente_obter_zsql(cod_expediente = e.cod_expediente)[0].nom_expediente
    nomes_expediente[str(e.cod_expediente)] = nom_expediente

for e in cod_expediente:
    if e not in expediente:
        context.zsql.expediente_incluir_zsql(
            cod_sessao_plen=cod_sessao_plen,
            cod_expediente=e,
            txt_expediente=dic.get(e)
        )

        nome_expediente = context.zsql.tipo_expediente_obter_zsql(cod_expediente = e, ind_excluido = 0)[0].nom_expediente
        context.pysc.sessao_plenaria_log_pysc(
            cod_sessao_plen = cod_sessao_plen,
            txt_acao = 'inclusão de expediente',
            txt_mensagem = 'O expediente ' + nome_expediente + ' foi incluído na sessão plenária.'
        )

    else:
        context.zsql.expediente_alterar_zsql(
            cod_sessao_plen=cod_sessao_plen,
            cod_expediente=e,
            txt_expediente=dic.get(e),
            ind_excluido=0
        )
        context.pysc.sessao_plenaria_log_pysc(
            cod_sessao_plen = cod_sessao_plen,
            txt_acao = 'atualização de expediente',
            txt_mensagem = 'O expediente ' + nomes_expediente[e] + ' foi atualizado na sessão plenária.'
        )

return 1
