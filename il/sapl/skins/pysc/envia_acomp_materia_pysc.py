## Script (Python) "confirma_acomp_materia_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_materia
##title=
request=context.REQUEST
response=request.RESPONSE
session= request.SESSION

try:
   mailhost=getattr(context, context.superValues('Mail Host')[0].id)
except:
   raise AttributeError, "cant find a Mail Host object"

data_registro=DateTime().strftime('%d/%m/%Y')

if hasattr(context.sapl_documentos.props_sapl,'logo_casa.gif'):
  imagem = context.sapl_documentos.props_sapl['logo_casa.gif'].absolute_url()
else:
  imagem = context.imagens.absolute_url() + "/brasao_transp.gif"

casa={}
aux=context.sapl_documentos.props_sapl.propertyItems()
for item in aux:
  casa[item[0]] = item[1]
email_casa = casa['end_email_casa']
casa_legislativa = casa['nom_casa']

for materia in context.zsql.materia_obter_zsql(cod_materia=cod_materia):
 ementa = materia.txt_ementa
 projeto = materia.sgl_tipo_materia+" "+materia.des_tipo_materia+" "+str(materia.num_ident_basica)+"/"+str(materia.ano_ident_basica)
 autores=[]
 for autoria in context.zsql.autoria_obter_zsql(cod_materia = materia.cod_materia):
  dic_autor = {}
  for autor in context.zsql.autor_obter_zsql(cod_autor = autoria.cod_autor):
   dic_autor['nom_autor']= " "
   if autor.des_tipo_autor=='Parlamentar':
    for parlamentar in context.zsql.parlamentar_obter_zsql(cod_parlamentar=autor.cod_parlamentar):
     dic_autor['nom_autor']=parlamentar.nom_completo
   elif autor.des_tipo_autor=='Comissao':
    for comissao in context.zsql.comissao_obter_zsql(cod_comissao=autor.cod_comissao):
     dic_autor['nom_autor']=comissao.nom_comissao
   else:
    dic_autor['nom_autor']=autor.nom_autor
   autores.append(dic_autor)
 for tramitacao in context.zsql.tramitacao_obter_zsql(cod_materia=cod_materia, ind_ult_tramitacao=1):
   data = tramitacao.dat_tramitacao
   status = tramitacao.des_status
   texto_acao = tramitacao.txt_tramitacao

remetente = email_casa

destinatarios=[]
for destinatario in context.zsql.acomp_materia_obter_inscritos_zsql(cod_materia=cod_materia):
  dic={}
  dic['end_email']=destinatario.end_email
  dic['txt_hash']=destinatario.txt_hash
  destinatarios.append(dic)

for dic in destinatarios:
     mMsg = "To: " + dic['end_email'] + "\n"
     mMsg = mMsg + "From: " + remetente + "\n"
     mMsg = mMsg + "Mime-Version: 1.0\n"
     mMsg = mMsg + "Content-Type: text/html; charset=UTF-8\n\n"
     mMsg = mMsg + "<html><head></head><body bgcolor='#ffffff'>"
     mMsg = mMsg + "<p align='center'><img src="+imagem+" width='81' height='77'></p>"
     mMsg = mMsg + "<h2 align='center'><b>"+ str(casa_legislativa) +"</b><br />"
     mMsg = mMsg + " Sistema de Apoio ao Processo Legislativo</h2>"
     mMsg = mMsg + "<p>A seguinte mat&eacute;ria de seu interesse sofreu tramita&ccedil;&atilde;o registrada em "+data_registro+" :</p>"
     mMsg = mMsg + "<h4> <a href='"+context.consultas.absolute_url()+"/materia/materia_mostrar_proc?cod_materia="+cod_materia+"'><b>"+ projeto +"</b></a> <br />"
     mMsg = mMsg + " "+ ementa +" <br /> "
     mMsg = mMsg + " <b>Autoria:</b> "
     for autor in autores:
         mMsg = mMsg + autor['nom_autor'] +"<br /> "
     mMsg = mMsg + "</h4>" 
     mMsg = mMsg + "<p></p>"
     mMsg = mMsg + "<p><b>Data da a&ccedil;&atilde;o</b>: "+data+" <br />"
     mMsg = mMsg + "<b>Status</b>: "+status+"<br />"
     mMsg = mMsg + "<b>Texto da a&ccedil;&atilde;o</b>: "+texto_acao+"</p>"
     mMsg = mMsg + " <hr> "
     mMsg = mMsg + " <p> <a href='"+context.consultas.absolute_url()+"/materia/acompanhamento/acomp_materia_excluir_proc?txt_hash="+ dic['txt_hash'] +"'>Clique aqui para excluir seu e-mail da lista de envio</a><p>"
     mMsg = mMsg + "<p>Esta &eacute; uma mensagem autom&aacute;tica. Por favor, n&atilde;o a responda.</p>"
     mMsg = mMsg + "</body></html>"

     mSubj = "[SAPL] "+ projeto +" - Acompanhamento de Materia Legislativa"

     mailhost.send(mMsg, subject=mSubj, encode='base64')
