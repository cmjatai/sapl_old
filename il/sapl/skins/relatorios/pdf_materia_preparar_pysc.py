import os

request=context.REQUEST
#print request
#return printed
response=request.RESPONSE
session= request.SESSION

data=DateTime().strftime('%d/%m/%Y')

#Abaixo é gerada a string para o rodapé da página
casa={}
aux=context.sapl_documentos.props_sapl.propertyItems()
for item in aux:
    casa[item[0]]=item[1]
localidade=context.zsql.localidade_obter_zsql(cod_localidade=casa["cod_localidade"])
if len(casa["num_cep"])==8:
    cep=casa["num_cep"][:4]+"-"+casa["num_cep"][5:]
else:
    cep=""

linha1=casa["end_casa"]
if cep!="":
    if casa["end_casa"]!="" and casa["end_casa"]!=None:
        linha1 = linha1 + " - "
    linha1 = linha1 + "CEP "+cep
if localidade[0].nom_localidade!="" and localidade[0].nom_localidade!=None:
    linha1 = linha1 + " - "+localidade[0].nom_localidade+" "+localidade[0].sgl_uf
if casa["num_tel"]!="" and casa["num_tel"]!=None:
    linha1 = linha1 + " Tel.: "+ casa["num_tel"]

linha2=casa["end_web_casa"]
if casa["end_email_casa"]!="" and casa["end_email_casa"]!=None:
    if casa["end_web_casa"]!="" and casa["end_web_casa"]!=None:
        linha2 = linha2 + " - "
    linha2 =  linha2 + "E-mail: "+casa["end_email_casa"]

data_emissao=DateTime().strftime("%d/%m/%Y")
rodape=[linha1,linha2,data_emissao]

#Por fim, gera-se as entradas para o cabeçalho
estados=context.zsql.localidade_obter_zsql(tip_localidade="u")
for uf in estados:
    if localidade[0].sgl_uf==uf.sgl_uf:
        nom_estado=uf.nom_localidade
        break
cabecalho={}
cabecalho["nom_casa"]=casa["nom_casa"]
cabecalho["nom_estado"]="Estado de "+nom_estado

# tenta buscar o logotipo da casa LOGO_CASA
if hasattr(context.sapl_documentos.props_sapl,'logo_casa.gif'):
    imagem = context.sapl_documentos.props_sapl['logo_casa.gif'].absolute_url()
else:
    imagem = context.imagens.absolute_url() + "/brasao_transp.gif"

#Por fim, utiliza o PythonScript para pesquisar as matérias e gerar os dados

materias=[]
REQUEST=context.REQUEST
# ------------------------------------ total matérias : informar quando o autor foi indicado no parâmetro da consulta ---------
cabecalho["total_materias"]=""
if len(REQUEST['hdn_cod_autor'])>0:
    if 'total_materias' in REQUEST: 
        total=REQUEST['total_materias']
        cabecalho["total_materias"]=str(total)
# -----------------------------------------------------------------------------------------------------------------------------

for materia in context.zsql.materia_pesquisar_zsql(tip_id_basica=REQUEST['lst_tip_materia'], num_ident_basica=REQUEST['txt_numero'],
    ano_ident_basica=REQUEST['txt_ano'], ind_tramitacao=REQUEST['rad_tramitando'],
    des_assunto=REQUEST['txt_assunto'], nom_relator=REQUEST['txt_relator'],
    cod_status=REQUEST['lst_status'], des_tipo_autor=REQUEST['lst_tip_autor'],
    dat_apresentacao=REQUEST['dt_apres'], dat_apresentacao2=REQUEST['dt_apres2'],
    dat_publicacao=REQUEST['dt_public'], dat_publicacao2=REQUEST['dt_public2'],
    cod_partido=REQUEST['lst_cod_partido'],cod_autor=REQUEST['hdn_cod_autor'],
    rd_ordem=REQUEST['rd_ordenacao']):

    dic={}

    dic['titulo']=materia.sgl_tipo_materia+" "+materia.des_tipo_materia+" "+str(materia.num_ident_basica)+"/"+str(materia.ano_ident_basica)
    dic['txt_ementa']=materia.txt_ementa

    lst_autoria_exp_mat=[]
    a="2"
    n="NC"
    nc=n
    t="não definido"
    for autoria in context.zsql.autoria_obter_zsql(cod_materia=materia.cod_materia):
        # if len(autoria) > 0: # se existe autor
        # autoria = autoria[0]
        a="2"
        if autoria.ind_primeiro_autor=="1":
            a="1"
        for autor in context.zsql.autor_obter_zsql(cod_autor=autoria.cod_autor):
            # if len(autor) > 0:
            #     autor = autor[0]
            try:
                if autor.des_tipo_autor == "Parlamentar":
                    parlamentar = context.zsql.parlamentar_obter_zsql(cod_parlamentar=autor.cod_parlamentar)[0]
                    # dic_expediente_materia["nom_autor"] = parlamentar.nom_parlamentar
                    n=parlamentar.nom_parlamentar
                    nc=parlamentar.nom_completo
                    t="Parlamentar"
                elif autor.des_tipo_autor == "Comissao":
                    comissao = context.zsql.comissao_obter_zsql(cod_comissao=autor.cod_comissao)[0]
                    # dic_expediente_materia["nom_autor"] = comissao.nom_comissao
                    n=comissao.sgl_comissao
                    nc=comissao.nom_comissao
                    t="Comissão"
                elif autor.nom_autor != "":
                    # dic_expediente_materia["nom_autor"] = autor.nom_autor
                    n=autor.nom_autor
                    nc=n
                    t=autor.des_tipo_autor
                else:
                    # dic_expediente_materia["nom_autor"] = autor.des_tipo_autor
                    n=autor.des_tipo_autor
                    nc=n
                    t=autor.des_tipo_autor
            except:
                # dic_expediente_materia["nom_autor"] = "NC-em"
                n="NC-em"
                nc=n
                t="não definido"
            lst_autoria_exp_mat.append({a+n:[a,n,nc,t]})

    lst_autoria_exp_mat.sort()

    if len(lst_autoria_exp_mat)>0:
        dic['autoria_materia']=lst_autoria_exp_mat
    else:
        lst_autoria_exp_mat.append({a+n:[a,n,nc,t]})
        dic['autoria_materia']=lst_autoria_exp_mat

    des_status = ''
    txt_tramitacao=''

    dic['localizacao_atual']=" "
    for tramitacao in context.zsql.tramitacao_obter_zsql(cod_materia=materia.cod_materia,ind_ult_tramitacao=1):
        if tramitacao.cod_unid_tram_dest:
            cod_unid_tram = tramitacao.cod_unid_tram_dest
        else:
            cod_unid_tram = tramitacao.cod_unid_tram_local

        for unidade_tramitacao in context.zsql.unidade_tramitacao_obter_zsql(cod_unid_tramitacao = cod_unid_tram):
            if unidade_tramitacao.cod_orgao:
                dic['localizacao_atual']=unidade_tramitacao.nom_orgao
            else:
                dic['localizacao_atual']=unidade_tramitacao.nom_comissao

        des_status=tramitacao.des_status
        txt_tramitacao=tramitacao.txt_tramitacao

    dic['des_situacao']=des_status
    dic['ultima_acao']=txt_tramitacao


    dic['norma_vinculada']=" "
    for norma_vinculada in context.zsql.materia_buscar_norma_juridica_zsql(cod_materia=materia.cod_materia):
        dic['norma_vinculada']=norma_vinculada.des_norma+" "+str(norma_vinculada.num_norma)+"/"+str(norma_vinculada.ano_norma)

    materias.append(dic)

filtro={} # Dicionário que conterá os dados do filtro

# Atribuições diretas do REQUEST
filtro['numero']=REQUEST.txt_numero
filtro['ano']=REQUEST.txt_ano
filtro['autor']=REQUEST.hdn_txt_autor
filtro['tipo_autor']=REQUEST.lst_tip_autor
filtro['relator']=REQUEST.txt_relator
filtro['assunto']=REQUEST.txt_assunto

# Atribuição do restante dos dados que precisam de processamento
if REQUEST.hdn_txt_autor=='  ': # Corrige bug do Netscape
    filtro['autor']=''

filtro['tipo_materia']=''
if REQUEST.lst_tip_materia!='':
    for tipo_materia in context.zsql.tipo_materia_legislativa_obter_zsql(ind_excluido=0, tip_materia=REQUEST.lst_tip_materia):
        filtro['tipo_materia']= tipo_materia.sgl_tipo_materia + ' - ' + tipo_materia.des_tipo_materia

filtro['partido']=''
if REQUEST.lst_cod_partido!='':
    for partido in context.zsql.partido_obter_zsql(ind_excluido=0,cod_partido=REQUEST.lst_cod_partido):
        filtro['partido']=partido.sgl_partido + ' - ' + partido.nom_partido

filtro['tramitando']=''
if REQUEST.rad_tramitando=='1':
    filtro['tramitacao']='Sim'
elif REQUEST['rad_tramitando']=='0':
    filtro['tramitacao']='Não'

filtro['situacao_atual']=''
if REQUEST.lst_status!='':
    for status in context.zsql.status_tramitacao_obter_zsql(ind_excluido=0,cod_status=REQUEST.lst_status):
        filtro['situacao_atual']=status.sgl_status + ' - ' + status.des_status

sessao=session.id
caminho = context.pdf_materia_gerar(sessao,imagem,data,materias,cabecalho,rodape,filtro)
if caminho=='aviso':
    return response.redirect('mensagem_emitir_proc')
else:
    response.redirect(caminho)
