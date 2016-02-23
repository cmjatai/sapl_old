## Script (Python) "presenca_sessao_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_parlamentar, cod_sessao_plen, endereco_ip='', endereco_mac='', cod_perfil='operador', login=False, recontagem=False
##title=
##

try:
    cod_parlamentar = cod_parlamentar.split()
except AttributeError:
    pass

if recontagem:
    ind_recontagem = 1
else:
    ind_recontagem = 0

# verifica se a votação esta aberta
cod_registro_pre = context.zsql.recomposicao_presencas_sessao_verificar_ultima_aberta_zsql(cod_sessao_plen = cod_sessao_plen)[0].cod_registro_pre
if cod_registro_pre:
    aberta = True
else:
    aberta = False

if aberta:
    lista_presenca=context.zsql.presenca_sessao_obter_zsql(cod_sessao_plen=cod_sessao_plen,ind_excluido=0)
    parlamentares=[]
    for parlamentar in lista_presenca:
        parlamentares.append(str(parlamentar.cod_parlamentar))

    lista_presenca_excl=context.zsql.presenca_sessao_obter_zsql(cod_sessao_plen=cod_sessao_plen,ind_excluido=1)
    parlamentares_excl=[]
    for parlamentar in lista_presenca_excl:
        parlamentares_excl.append(str(parlamentar.cod_parlamentar))

    for i in cod_parlamentar:
        if i not in parlamentares and i not in parlamentares_excl:
            context.zsql.presenca_sessao_incluir_zsql(
                cod_parlamentar=i,
                cod_sessao_plen=cod_sessao_plen,
                endereco_ip=endereco_ip,
                endereco_mac=endereco_mac,
                cod_perfil=cod_perfil,
                ind_recontagem=ind_recontagem
            )
        else:
            context.zsql.presenca_sessao_alterar_zsql(
                cod_parlamentar=i,
                cod_sessao_plen=cod_sessao_plen,
                endereco_ip=endereco_ip,
                endereco_mac=endereco_mac,
                cod_perfil=cod_perfil,
                ind_excluido=0,
                ind_recontagem=ind_recontagem
            )

    if not login:
        for i in parlamentares:
            if i not in cod_parlamentar:

                context.zsql.presenca_sessao_alterar_zsql(
                    cod_parlamentar=i,
                    cod_sessao_plen=cod_sessao_plen,
                    endereco_ip=endereco_ip,
                    endereco_mac=endereco_mac,
                    cod_perfil=cod_perfil,
                    ind_recontagem=ind_recontagem,
                    ind_excluido=1
                )

    return True

else:
    return False
