## Script (Python)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_norma
##title=
##

request = container.REQUEST
response = request.RESPONSE


if str(request['AUTHENTICATED_USER']) != 'leandro':
    raise Exception("Acesso não Autorizado")

codigo=int(cod_norma)
try:
    context.zsql.norma_check_zsql(cod_norma=codigo)
    norma = context.zsql.norma_juridica_obter_zsql(cod_norma=codigo)[0]
    if norma["cod_materia"]:
        context.zsql.materia_check_zsql(cod_materia=norma["cod_materia"])
except Exception as e:
    return str(e)
return "ok"
