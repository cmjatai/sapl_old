## Script (Python) "sessao_plenaria_materiais_crc32"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
 
from zlib import crc32
import math 

request = context.REQUEST
pysc = context.pysc
zsql = context.zsql


#result = str(int(math.random()*1000000))
#return str(result)


#dat_sessao = pysc.data_proxima_pysc(lista_de_datas=[r['dat_inicio_sessao'] for r in context.zsql.data_sessao_plenaria_obter_zsql(ind_excluido = 0)])
dat_sessao = zsql.ultima_sessao_plenaria_obter_zsql()[0].dat_inicio_sessao
 
cod_sessao_plen = '0' 

result = ''


if not 'cod_sessao_plen' in request:
   cod_sessao_plen = zsql.sessao_plenaria_obter_zsql( ind_excluido = 0)[-1]['cod_sessao_plen']
else:
   cod_sessao_plen = request['cod_sessao_plen']

 
result += cod_sessao_plen

for matexp in zsql.expediente_materia_obter_zsql(cod_sessao_plen = cod_sessao_plen, ind_excluido=0):
    for mevot in zsql.votacao_expediente_materia_obter_zsql(cod_ordem = matexp.cod_ordem, ind_excluido=0):
        materia = zsql.materia_obter_zsql(cod_materia=mevot.cod_materia, ind_excluido=0)[-1]
        
        result += str(mevot.num_ordem)
        result += str(materia.cod_materia)
        result += str(materia.sgl_tipo_materia)
        result += str(materia.des_tipo_materia)
        result += str(materia.num_ident_basica)
        result += str(materia.ano_ident_basica)
        result += str(materia.num_protocolo)
        result += str(mevot.tip_resultado_votacao)
        result += str(materia.dat_apresentacao)
        
        
        if hasattr(context.sapl_documentos.materia,materia.cod_materia+'_texto_integral'):
            result += getattr(context.sapl_documentos.materia, materia.cod_materia+'_texto_integral').getContentType()
        
        for turno in zsql.tramitacao_turno_obter_zsql(cod_materia=materia.cod_materia, dat_inicio_sessao=dat_sessao):
            result += turno.sgl_turno
        
        for autoria in zsql.autoria_obter_zsql(cod_materia=materia.cod_materia, ind_primeiro_autor=1):
            for autor in zsql.autor_obter_zsql(cod_autor=autoria.cod_autor):
        
                try:
                    if autor.cod_parlamentar:
                        result += str(zsql.parlamentar_obter_zsql(cod_parlamentar=autor['cod_parlamentar'])[-1]['nom_parlamentar'])
                    if autor.cod_comissao: 
                        result += str(zsql.comissao_obter_zsql(cod_comissao=autor['cod_comissao'])[-1]['nom_comissao'])  
                
                    if autor.cod_parlamentar or autor.cod_comissao:
                        result += str(autor.nom_autor)
                except:
                   pass
        
        result += materia.txt_ementa
        
        if mevot.tip_resultado_votacao:
            for vot in zsql.tipo_resultado_votacao_obter_zsql(tip_resultado_votacao=mevot['tip_resultado_votacao'], ind_excluido=0):
                result += str(mevot.cod_votacao)
                result += str(mevot.tip_votacao)
                result += str(vot.nom_resultado)
                result += str(mevot.votacao_observacao)
                result += str(mevot.num_votos_sim)
                result += str(mevot.num_votos_nao)
                result += str(mevot.num_abstencao)
                result += str(mevot.dat_ordem) 
        try: 
            if matexp.txt_tramitacao:
                result += matexp.txt_tramitacao
        except:
            pass
            

for ordemdia in zsql.ordem_dia_obter_zsql(cod_sessao_plen = cod_sessao_plen, ind_excluido=0):
    for odvot in zsql.votacao_ordem_dia_obter_zsql(cod_ordem = ordemdia['cod_ordem'], ind_excluido=0):
        materia = zsql.materia_obter_zsql(cod_materia=odvot.cod_materia, ind_excluido=0)[-1]
        
        result += str(odvot.num_ordem)         
        result += str(materia.cod_materia)
        result += str(materia.sgl_tipo_materia)
        result += str(materia.des_tipo_materia)
        result += str(materia.num_ident_basica) 
        result += str(materia.ano_ident_basica)
        result += str(materia.num_protocolo)
        result += str(odvot.tip_resultado_votacao)
        result += str(materia.dat_apresentacao)
        
        if hasattr(context.sapl_documentos.materia,materia.cod_materia+'_texto_integral'):
            result += getattr(context.sapl_documentos.materia, materia.cod_materia+'_texto_integral').getContentType()
        
        for numeracao in zsql.numeracao_obter_zsql(cod_materia=materia.cod_materia):
            result += str(numeracao.num_materia)
            result += str(numeracao.ano_materia)
        
        for turno in zsql.tramitacao_turno_obter_zsql(cod_materia=materia.cod_materia, dat_inicio_sessao=dat_sessao):
            result += turno.sgl_turno
        
        for autoria in zsql.autoria_obter_zsql(cod_materia=materia.cod_materia, ind_primeiro_autor=1):
            for autor in zsql.autor_obter_zsql(cod_autor=autoria.cod_autor):
        
                try:
                    if autor.cod_parlamentar:
                        result += str(zsql.parlamentar_obter_zsql(cod_parlamentar=autor['cod_parlamentar'])[-1]['nom_parlamentar'])
                    if autor.cod_comissao: 
                        result += str(zsql.comissao_obter_zsql(cod_comissao=autor['cod_comissao'])[-1]['nom_comissao'])  
        
                    if autor.cod_parlamentar or autor.cod_comissao:
                        result += str(autor.nom_autor)
                except:
                    pass
        
        result += materia.txt_ementa
        
        if odvot.tip_resultado_votacao:
            for vot in zsql.tipo_resultado_votacao_obter_zsql(tip_resultado_votacao=odvot.tip_resultado_votacao, ind_excluido=0):
              
                result += str(odvot.cod_votacao)
                result += str(odvot.tip_votacao)
                result += str(vot.nom_resultado)
                result += str(odvot.votacao_observacao)
                result += str(odvot.num_votos_sim)
                result += str(odvot.num_votos_nao)
                result += str(odvot.num_abstencao)
                result += str(odvot.dat_ordem) 
        
        
        try: 
            if ordemdia.txt_tramitacao:
                result += ordemdia.txt_tramitacao
        except:
            pass
     
            
result = str(int(math.fabs(int(crc32(result)))))
return str(result)
