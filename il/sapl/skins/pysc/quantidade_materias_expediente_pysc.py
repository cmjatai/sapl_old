## Script (Python) "quantidade_materiais_expediente_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_sessao_plen
##title=
##

materias_ordem = context.zsql.expediente_materia_obter_zsql(cod_sessao_plen = cod_sessao_plen)
return len(materias_ordem)
