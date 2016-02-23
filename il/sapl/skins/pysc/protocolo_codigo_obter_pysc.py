## Script (Python) "protocolo_codigo_obter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ano=""
##title=
##


cod_protocolo = None

# Busca o último número
if len(ano) > 0:
    try:
        cod_protocolo=context.zsql.protocolo_codigo_obter_zsql(ano=ano)[0].cod_protocolo
    except:
        pass
else:
    try:
        cod_protocolo=context.zsql.protocolo_codigo_obter_zsql()[0].cod_protocolo
    except:
        pass

# retorna próximo código de protocolo
return cod_protocolo + 1
